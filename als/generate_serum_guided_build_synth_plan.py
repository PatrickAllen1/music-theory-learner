#!/usr/bin/env python3
"""
generate_serum_guided_build_synth_plan.py

Turn a refined Serum brief into a synth-authoring scaffold that can be dropped
into guided-build writing: per-part load/tweak/listen steps, render-validation
flags, and replacement lanes from the real Garage preset banks.

Examples:
    python3 als/generate_serum_guided_build_synth_plan.py --brief ukg-2step-dark-stab
    python3 als/generate_serum_guided_build_synth_plan.py --brief ukg-4x4-pluck-driver --format json
"""

from __future__ import annotations

import argparse
import json
from argparse import Namespace
from pathlib import Path

try:
    from generate_serum_lesson_notes import build_report as build_lesson_notes_report
    from report_serum_brief_bank_candidates import build_report as build_brief_bank_report
    from report_serum_lesson_author_queue import build_report as build_author_queue_report
    from report_serum_render_backlog import build_report as build_render_backlog_report
    from suggest_serum_blueprint_mutations import build_report as build_mutation_plan_report
except ModuleNotFoundError:
    from .generate_serum_lesson_notes import build_report as build_lesson_notes_report
    from .report_serum_brief_bank_candidates import build_report as build_brief_bank_report
    from .report_serum_lesson_author_queue import build_report as build_author_queue_report
    from .report_serum_render_backlog import build_report as build_render_backlog_report
    from .suggest_serum_blueprint_mutations import build_report as build_mutation_plan_report


DEFAULT_CATALOG_DIR = Path("als/catalog/profiles")
DEFAULT_BRIEFS_PATH = Path("als/serum-track-briefs.json")

ROLE_JOB_MAP = {
    "bass": "anchor the groove with a stable, mono-safe low-end center",
    "sub": "anchor the very bottom without masking the kick",
    "reese": "add width and movement around the bass without taking over the sub range",
    "pad": "hold the harmonic bed behind the drums and hook",
    "lead": "carry the main melodic focus in the upper mids",
    "pluck": "add a bright rhythmic hook that reads quickly",
    "stab": "punctuate the groove with short harmonic or melodic accents",
    "fx": "support transitions and ear candy without distracting from the groove",
}


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate a synth-authoring scaffold for one Serum brief.")
    parser.add_argument("--brief", required=True, help="Brief id from the manifest.")
    parser.add_argument("--catalog-dir", default=str(DEFAULT_CATALOG_DIR), help="Directory of generated *-profiles.json files.")
    parser.add_argument("--briefs", default=str(DEFAULT_BRIEFS_PATH), help="Track brief manifest JSON.")
    parser.add_argument("--prefer-rendered", action="store_true", help="Prefer rendered profiles where available.")
    parser.add_argument("--limit-per-part", type=int, default=5, help="Max candidates to inspect per part. Default: 5")
    parser.add_argument("--mutation-limit", type=int, default=6, help="Max mutation suggestions per part. Default: 6")
    parser.add_argument("--max-swaps", type=int, default=2, help="Maximum refinement swaps to apply. Default: 2")
    parser.add_argument("--bank-dir", action="append", default=[], help="Preset bank directory to scan. Pass multiple times.")
    parser.add_argument("--bank-top-per-part", type=int, default=3, help="Maximum bank alternatives per part. Default: 3")
    parser.add_argument("--render-limit", type=int, default=6, help="Maximum brief render blockers to inspect. Default: 6")
    parser.add_argument("--format", choices=["json", "text"], default="text", help="Output format.")
    return parser


def _lesson_namespace(args: argparse.Namespace) -> Namespace:
    return Namespace(
        catalog_dir=args.catalog_dir,
        briefs=args.briefs,
        brief=args.brief,
        prefer_rendered=args.prefer_rendered,
        limit_per_part=args.limit_per_part,
        mutation_limit=args.mutation_limit,
        refine=True,
        max_swaps=args.max_swaps,
        format="json",
    )


def _mutation_namespace(args: argparse.Namespace) -> Namespace:
    return Namespace(
        catalog_dir=args.catalog_dir,
        briefs=args.briefs,
        brief=args.brief,
        prefer_rendered=args.prefer_rendered,
        limit_per_part=args.limit_per_part,
        mutation_limit=args.mutation_limit,
        alternative_limit=max(args.limit_per_part, 5),
        max_swaps=args.max_swaps,
        refine=True,
        suggestion_limit=8,
        format="json",
    )


def _shared_namespace(args: argparse.Namespace) -> Namespace:
    return Namespace(
        catalog_dir=args.catalog_dir,
        briefs=args.briefs,
        prefer_rendered=args.prefer_rendered,
        limit_per_part=args.limit_per_part,
        mutation_limit=args.mutation_limit,
        max_swaps=args.max_swaps,
        format="json",
    )


def _bank_namespace(args: argparse.Namespace) -> Namespace:
    return Namespace(
        brief=args.brief,
        catalog_dir=args.catalog_dir,
        briefs=args.briefs,
        prefer_rendered=args.prefer_rendered,
        limit_per_part=args.limit_per_part,
        mutation_limit=args.mutation_limit,
        max_swaps=args.max_swaps,
        bank_dir=args.bank_dir,
        top_per_part=args.bank_top_per_part,
        include_stable=False,
        format="json",
    )


def _brief_render_blockers(backlog: dict, brief_id: str, limit: int) -> list[dict]:
    rows = []
    for row in backlog["backlog"]:
        links = [item for item in row["briefs"] if item["brief_id"] == brief_id]
        if not links:
            continue
        rows.append({
            "profile_id": row["profile_id"],
            "track": row.get("track"),
            "analysis_slug": row.get("analysis_slug"),
            "priority": row["priority"],
            "score": row["score"],
            "reasons": row["reasons"],
            "brief_links": links,
        })
    rows.sort(key=lambda row: (-row["score"], row["profile_id"]))
    return rows[:limit]


def _job_in_track(role: str) -> str:
    return ROLE_JOB_MAP.get(role, "support the groove in its assigned role")


def _part_step_sequence(part: dict, lesson_part: dict, mutation_part: dict, render_rows: list[dict], bank_part: dict | None) -> list[dict]:
    selection = lesson_part.get("profile_id")
    if lesson_part["status"] != "selected" or not selection:
        return [{
            "step_type": "resolve_selection",
            "title": f"Replace the unresolved `{part['part_id']}` sound",
            "details": ["No starting profile is selected yet; use the bank alternatives to choose a viable base sound."],
        }]

    steps = [
        {
            "step_type": "load_base_preset",
            "title": f"Load `{lesson_part['track']}` as the `{part['part_id']}` sound",
            "details": [
                lesson_part["summary"],
                f"In the arrangement, this part should {_job_in_track(part['role'])}.",
            ],
        }
    ]

    suggestions = mutation_part.get("suggestions") or []
    if suggestions:
        details = [
            f"`{row['path']}` {row['action']} {row['current_value']} -> {row['suggested_value']} [{row['goal']}]"
            for row in suggestions[:4]
        ]
        steps.append({
            "step_type": "apply_mutations",
            "title": f"Apply the first targeted Serum edits for `{part['part_id']}`",
            "details": details,
        })

    if lesson_part.get("listen_for"):
        steps.append({
            "step_type": "listen_check",
            "title": f"Listen-check `{part['part_id']}` in context",
            "details": lesson_part["listen_for"],
        })

    if render_rows:
        steps.append({
            "step_type": "render_validate",
            "title": f"Render-validate `{part['part_id']}` before finalizing the lesson",
            "details": [
                f"`{row['profile_id']}` is still a `{row['priority']}` render blocker for this brief."
                for row in render_rows
            ],
        })

    if bank_part and bank_part.get("candidates"):
        details = [
            f"`{row['track']}` from `{row.get('bank') or '-'}` [score={row['score']}]"
            for row in bank_part["candidates"][:3]
        ]
        steps.append({
            "step_type": "audition_alternatives",
            "title": f"Keep replacement options ready for `{part['part_id']}`",
            "details": details,
        })

    return steps


def build_report(args: argparse.Namespace) -> dict:
    lesson_notes = build_lesson_notes_report(_lesson_namespace(args))
    mutation_plan = build_mutation_plan_report(_mutation_namespace(args))
    author_queue = build_author_queue_report(_shared_namespace(args))
    render_backlog = build_render_backlog_report(_shared_namespace(args))
    bank_candidates = build_brief_bank_report(_bank_namespace(args))

    author_row = next(row for row in author_queue["queue"] if row["brief_id"] == args.brief)
    render_rows = _brief_render_blockers(render_backlog, args.brief, args.render_limit)
    lesson_by_part = {row["part_id"]: row for row in lesson_notes["parts"]}
    mutation_by_part = {row["part_id"]: row for row in mutation_plan["parts"]}
    bank_by_part = {row["part_id"]: row for row in bank_candidates["parts"]}

    synth_sections = []
    for part in mutation_plan["parts"]:
        lesson_part = lesson_by_part[part["part_id"]]
        matching_render_rows = [
            row for row in render_rows
            if any(link["part_id"] == part["part_id"] for link in row["brief_links"])
        ]
        bank_part = bank_by_part.get(part["part_id"])
        flags = []
        if part["status"] != "selected":
            flags.append("unresolved")
        if part.get("constraint_mode") and part["constraint_mode"] != "full":
            flags.append("fallback_selected")
        if not (part.get("suggestions") or []):
            flags.append("no_actionable_mutations")
        if matching_render_rows:
            flags.append("needs_render_validation")
        if bank_part and bank_part.get("candidates"):
            flags.append("replacement_lane_open")

        synth_sections.append({
            "part_id": part["part_id"],
            "role": part["role"],
            "job_in_track": _job_in_track(part["role"]),
            "flags": flags,
            "current_profile_id": lesson_part.get("profile_id"),
            "current_track": lesson_part.get("track"),
            "constraint_mode": part.get("constraint_mode"),
            "why_this_sound": lesson_part.get("why_this_sound") or [],
            "listen_for": lesson_part.get("listen_for") or [],
            "starting_tweaks": lesson_part.get("starting_tweaks") or [],
            "render_blockers": matching_render_rows,
            "bank_alternatives": (bank_part or {}).get("candidates") or [],
            "step_sequence": _part_step_sequence(part, lesson_part, part, matching_render_rows, bank_part),
        })

    cross_part_checks = []
    for row in lesson_notes["pairwise_analysis"]:
        if row["conflicts"] or row["complements"]:
            cross_part_checks.append({
                "left_part_id": row["left_part_id"],
                "right_part_id": row["right_part_id"],
                "conflicts": row["conflicts"],
                "complements": row["complements"],
            })

    return {
        "brief_id": lesson_notes["brief_id"],
        "description": lesson_notes["description"],
        "refined": lesson_notes["refined"],
        "readiness": author_row["readiness"],
        "author_score": author_row["author_score"],
        "next_actions": author_row["next_actions"],
        "selected_profile_ids": lesson_notes["selected_profile_ids"],
        "synth_sections": synth_sections,
        "cross_part_checks": cross_part_checks,
    }


def render_text(report: dict) -> str:
    lines = []
    lines.append("# Serum Guided-Build Synth Plan")
    lines.append("")
    lines.append(f"- brief: `{report['brief_id']}`")
    lines.append(f"- readiness: `{report['readiness']}`")
    lines.append(f"- author score: {report['author_score']}")
    lines.append(f"- refined: {'yes' if report['refined'] else 'no'}")
    lines.append("")
    lines.append("## Global Next Actions")
    for row in report["next_actions"]:
        lines.append(f"- {row}")
    lines.append("")
    for section in report["synth_sections"]:
        lines.append(f"## {section['part_id']} ({section['role']})")
        lines.append(f"- job in track: {section['job_in_track']}")
        lines.append(f"- current sound: `{section['current_profile_id'] or '-'}` ({section['current_track'] or '-'})")
        lines.append(f"- constraint mode: {section['constraint_mode'] or '-'}")
        if section["flags"]:
            lines.append(f"- flags: {', '.join(section['flags'])}")
        for row in section["why_this_sound"]:
            lines.append(f"- why: {row}")
        for row in section["step_sequence"]:
            lines.append(f"- step: {row['title']}")
            for detail in row["details"]:
                lines.append(f"  detail: {detail}")
        lines.append("")
    if report["cross_part_checks"]:
        lines.append("## Cross-Part Checks")
        for row in report["cross_part_checks"]:
            lines.append(f"- `{row['left_part_id']}` vs `{row['right_part_id']}`")
            for note in row["conflicts"]:
                lines.append(f"  conflict: {note}")
            for note in row["complements"]:
                lines.append(f"  complement: {note}")
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
