#!/usr/bin/env python3
"""
report_full_song_blueprint_readiness.py

Report how ready each song brief is for real guided-build authoring by combining
full-song blueprint quality and compiled-lesson validation.

Examples:
    python3 als/report_full_song_blueprint_readiness.py
    python3 als/report_full_song_blueprint_readiness.py --format json
"""

from __future__ import annotations

import argparse
import json
from argparse import Namespace
from pathlib import Path

try:
    from compile_guided_build_lesson import build_report as build_compiled_lesson_report
    from design_full_song_blueprint import build_report as build_full_song_blueprint_report
    from validate_guided_build_lesson import build_report as build_lesson_validation_report
except ModuleNotFoundError:
    from .compile_guided_build_lesson import build_report as build_compiled_lesson_report
    from .design_full_song_blueprint import build_report as build_full_song_blueprint_report
    from .validate_guided_build_lesson import build_report as build_lesson_validation_report


DEFAULT_CATALOG_DIR = Path("als/catalog/profiles")
DEFAULT_SERUM_BRIEFS_PATH = Path("als/serum-track-briefs.json")
DEFAULT_SONG_BRIEFS_PATH = Path("als/song-blueprint-briefs.json")
DEFAULT_TEMPLATES_PATH = Path("als/song-production-templates.json")
READINESS_RANK = {"blocked": 0, "needs_work": 1, "usable": 2, "strong": 3}


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Report readiness of full-song blueprints and compiled lesson drafts.")
    parser.add_argument("--brief", help="Optional single song brief id to inspect.")
    parser.add_argument("--song-briefs", default=str(DEFAULT_SONG_BRIEFS_PATH), help="Song-level brief manifest JSON.")
    parser.add_argument("--templates", default=str(DEFAULT_TEMPLATES_PATH), help="Song production templates JSON.")
    parser.add_argument("--catalog-dir", default=str(DEFAULT_CATALOG_DIR), help="Directory of generated *-profiles.json files.")
    parser.add_argument("--serum-briefs", default=str(DEFAULT_SERUM_BRIEFS_PATH), help="Serum brief manifest JSON.")
    parser.add_argument("--prefer-rendered", action="store_true", help="Prefer rendered profiles where available.")
    parser.add_argument("--limit-per-part", type=int, default=5, help="Max candidates to inspect per part. Default: 5")
    parser.add_argument("--mutation-limit", type=int, default=6, help="Max mutation suggestions per part. Default: 6")
    parser.add_argument("--max-swaps", type=int, default=2, help="Maximum refinement swaps to apply. Default: 2")
    parser.add_argument("--format", choices=["json", "text"], default="text", help="Output format.")
    return parser


def _song_brief_ids(path: Path, only_brief: str | None = None) -> list[str]:
    payload = json.loads(path.read_text())
    brief_ids = sorted((payload.get("briefs") or {}).keys())
    if only_brief is not None:
        if only_brief not in brief_ids:
            raise KeyError(f"song brief not found: {only_brief}")
        return [only_brief]
    return brief_ids


def _namespace(args: argparse.Namespace, brief_id: str) -> Namespace:
    return Namespace(
        brief=brief_id,
        song_briefs=getattr(args, "song_briefs", str(DEFAULT_SONG_BRIEFS_PATH)),
        templates=getattr(args, "templates", str(DEFAULT_TEMPLATES_PATH)),
        catalog_dir=args.catalog_dir,
        serum_briefs=getattr(args, "serum_briefs", getattr(args, "briefs", str(DEFAULT_SERUM_BRIEFS_PATH))),
        prefer_rendered=args.prefer_rendered,
        limit_per_part=args.limit_per_part,
        mutation_limit=args.mutation_limit,
        max_swaps=args.max_swaps,
        format="json",
        lesson_only=False,
        lesson_json=None,
    )


def _overall_readiness(blueprint_label: str, lesson_label: str) -> str:
    if blueprint_label == "blocked" or lesson_label == "blocked":
        return "blocked"
    if blueprint_label == "strong" and lesson_label == "strong":
        return "strong"
    if blueprint_label in {"strong", "usable"} and lesson_label == "needs_work":
        return "usable"
    if blueprint_label == "usable" and lesson_label == "strong":
        return "usable"
    return "needs_work"


def _next_actions(blueprint: dict, lesson: dict) -> list[str]:
    actions = []
    readiness = blueprint["readiness"]
    technique_interactions = blueprint["production_techniques"]["interaction_analysis"]
    commitments = technique_interactions["decision_commitments"]
    if readiness["unresolved_synth_parts"]:
        actions.append("resolve the missing synth parts before treating the song as lesson-ready")
    if readiness["fallback_synth_parts"]:
        actions.append("replace or strengthen fallback-heavy synth selections")
    if readiness["pairwise_conflicts"]:
        actions.append("reduce the remaining synth conflicts before final authoring")
    if readiness["missing_processing_chains"]:
        actions.append("assign processing chains to every required lane")
    if technique_interactions["watchout_count"]:
        actions.append("honor the production commitments and apply the listed mitigation moves where techniques intentionally collide")
    if commitments["required_pairing_count"]:
        actions.append("treat the required technique pairings as part of the arrangement and mix plan, not optional flavor")
    if lesson["vague_step_ids"]:
        actions.append("tighten the remaining draft-style lesson wording")
    if lesson["readiness"] != "strong":
        actions.append("render and verify the chosen sounds in audio before finalizing the lesson")
    if not actions:
        actions.append("turn this brief into a real lesson JSON and start hand-tuning the musical details")
    return actions


def build_report(args: argparse.Namespace) -> dict:
    counts = {"strong": 0, "usable": 0, "needs_work": 0, "blocked": 0}
    briefs = []
    for brief_id in _song_brief_ids(Path(args.song_briefs), getattr(args, "brief", None)):
        namespace = _namespace(args, brief_id)
        compiler = build_compiled_lesson_report(namespace)
        blueprint = compiler["blueprint"]
        lesson = build_lesson_validation_report(Namespace(compiled_report=compiler))
        readiness = _overall_readiness(blueprint["readiness"]["label"], lesson["readiness"])
        counts[readiness] += 1

        briefs.append({
            "brief_id": brief_id,
            "description": blueprint["description"],
            "readiness": readiness,
            "blueprint_readiness": blueprint["readiness"]["label"],
            "lesson_readiness": lesson["readiness"],
            "total_bars": blueprint["readiness"]["total_bars"],
            "required_sample_slots": blueprint["readiness"]["required_sample_slots"],
            "reserved_space_count": len(blueprint["reserved_spaces"]),
            "synth_conflicts": blueprint["readiness"]["pairwise_conflicts"],
            "fallback_synth_parts": blueprint["readiness"]["fallback_synth_parts"],
            "unresolved_synth_parts": blueprint["readiness"]["unresolved_synth_parts"],
            "missing_processing_chains": blueprint["readiness"]["missing_processing_chains"],
            "step_count": lesson["step_count"],
            "vague_step_ids": lesson["vague_step_ids"],
            "compiler_warning_count": len(compiler["compiler_warnings"]),
            "technique_reinforcements": blueprint["production_techniques"]["interaction_analysis"]["reinforcement_count"],
            "technique_watchouts": blueprint["production_techniques"]["interaction_analysis"]["watchout_count"],
            "technique_required_pairings": blueprint["production_techniques"]["interaction_analysis"]["decision_commitments"]["required_pairing_count"],
            "technique_mandatory_constraints": blueprint["production_techniques"]["interaction_analysis"]["decision_commitments"]["mandatory_constraint_count"],
            "blueprint_issues": blueprint["readiness"]["issues"],
            "lesson_warnings": lesson["warnings"],
            "next_actions": _next_actions(blueprint, lesson),
        })

    briefs.sort(
        key=lambda row: (
            -READINESS_RANK[row["readiness"]],
            row["synth_conflicts"],
            row["fallback_synth_parts"],
            len(row["vague_step_ids"]),
            row["brief_id"],
        )
    )
    return {
        "brief_count": len(briefs),
        "prefer_rendered": args.prefer_rendered,
        "readiness_counts": counts,
        "briefs": briefs,
    }


def render_text(report: dict) -> str:
    lines = []
    lines.append("# Full Song Blueprint Readiness")
    lines.append("")
    lines.append(f"- briefs: {report['brief_count']}")
    lines.append(f"- prefer rendered: {'yes' if report['prefer_rendered'] else 'no'}")
    lines.append("")
    lines.append("## Readiness Counts")
    for key, value in report["readiness_counts"].items():
        lines.append(f"- `{key}`: {value}")
    lines.append("")
    lines.append("## Briefs")
    for row in report["briefs"]:
        lines.append(
            f"- `{row['brief_id']}` :: readiness={row['readiness']}; "
            f"blueprint={row['blueprint_readiness']}; lesson={row['lesson_readiness']}; "
            f"bars={row['total_bars']}; synth_conflicts={row['synth_conflicts']}; "
            f"fallbacks={row['fallback_synth_parts']}; vague_steps={len(row['vague_step_ids'])}; "
            f"technique_watchouts={row['technique_watchouts']}; "
            f"required_pairings={row['technique_required_pairings']}"
        )
        if row["blueprint_issues"]:
            lines.append(f"  blueprint issues: {' | '.join(row['blueprint_issues'])}")
        if row["lesson_warnings"]:
            lines.append(f"  lesson warnings: {' | '.join(row['lesson_warnings'])}")
        lines.append(f"  next: {' | '.join(row['next_actions'])}")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = make_parser()
    args = parser.parse_args()
    report = build_report(args)
    if args.format == "json":
        print(json.dumps(report, indent=2))
        return
    print(render_text(report), end="")


if __name__ == "__main__":
    main()
