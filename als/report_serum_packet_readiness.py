#!/usr/bin/env python3
"""
report_serum_packet_readiness.py

Report how ready each Serum brief is for lesson-packet export by comparing the
raw blueprint, refined blueprint, and resulting mutation-plan coverage.

Examples:
    python3 als/report_serum_packet_readiness.py
    python3 als/report_serum_packet_readiness.py --prefer-rendered --format json
"""

from __future__ import annotations

import argparse
import json
from argparse import Namespace
from pathlib import Path

try:
    from design_serum_track_blueprint import build_report as build_blueprint_report
    from refine_serum_track_blueprint import build_report as build_refined_blueprint_report
    from suggest_serum_blueprint_mutations import build_report as build_mutation_plan_report
except ModuleNotFoundError:
    from .design_serum_track_blueprint import build_report as build_blueprint_report
    from .refine_serum_track_blueprint import build_report as build_refined_blueprint_report
    from .suggest_serum_blueprint_mutations import build_report as build_mutation_plan_report


DEFAULT_CATALOG_DIR = Path("als/catalog/profiles")
DEFAULT_BRIEFS_PATH = Path("als/serum-track-briefs.json")


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Report readiness of Serum lesson packets per brief.")
    parser.add_argument("--catalog-dir", default=str(DEFAULT_CATALOG_DIR), help="Directory of generated *-profiles.json files.")
    parser.add_argument("--briefs", default=str(DEFAULT_BRIEFS_PATH), help="Track brief manifest JSON.")
    parser.add_argument("--prefer-rendered", action="store_true", help="Prefer rendered profiles where available.")
    parser.add_argument("--limit-per-part", type=int, default=5, help="Max candidates to inspect per part. Default: 5")
    parser.add_argument("--mutation-limit", type=int, default=6, help="Max mutation suggestions per part. Default: 6")
    parser.add_argument("--max-swaps", type=int, default=2, help="Maximum refinement swaps to apply. Default: 2")
    parser.add_argument("--format", choices=["json", "text"], default="text", help="Output format.")
    return parser


def _brief_ids(path: Path) -> list[str]:
    payload = json.loads(path.read_text())
    return sorted((payload.get("briefs") or {}).keys())


def _base_namespace(args: argparse.Namespace, brief_id: str) -> Namespace:
    return Namespace(
        catalog_dir=args.catalog_dir,
        briefs=args.briefs,
        brief=brief_id,
        prefer_rendered=args.prefer_rendered,
        limit_per_part=args.limit_per_part,
        mutation_limit=args.mutation_limit,
        format="json",
    )


def _refine_namespace(args: argparse.Namespace, brief_id: str) -> Namespace:
    return Namespace(
        **vars(_base_namespace(args, brief_id)),
        alternative_limit=max(args.limit_per_part, 5),
        max_swaps=args.max_swaps,
    )


def _mutation_namespace(args: argparse.Namespace, brief_id: str) -> Namespace:
    return Namespace(
        **vars(_refine_namespace(args, brief_id)),
        refine=True,
        suggestion_limit=8,
    )


def _readiness_label(unresolved_count: int, conflict_count: int, fallback_count: int, missing_mutation_count: int) -> str:
    if unresolved_count:
        return "blocked"
    if conflict_count == 0 and fallback_count == 0 and missing_mutation_count == 0:
        return "strong"
    if conflict_count <= 1 and fallback_count <= 1:
        return "usable"
    return "needs_work"


def _next_actions(unresolved_count: int, conflict_count: int, fallback_count: int, missing_mutation_count: int) -> list[str]:
    actions = []
    if unresolved_count:
        actions.append("expand the catalog or relax the brief because some parts are unresolved")
    if fallback_count:
        actions.append("review fallback-heavy parts and consider alternate presets or broader role coverage")
    if conflict_count:
        actions.append("apply the mutation plan or inspect further swaps to reduce remaining conflicts")
    if missing_mutation_count:
        actions.append("inspect parts with no actionable parameter moves and decide whether the base preset is already final or needs a stronger alternate")
    if not actions:
        actions.append("render the selected stack in Ableton/Serum to move from param-driven confidence to audio-verified confidence")
    return actions


def build_report(args: argparse.Namespace) -> dict:
    briefs = []
    counts = {"strong": 0, "usable": 0, "needs_work": 0, "blocked": 0}

    for brief_id in _brief_ids(Path(args.briefs)):
        raw = build_blueprint_report(_base_namespace(args, brief_id))
        refined = build_refined_blueprint_report(_refine_namespace(args, brief_id))
        mutations = build_mutation_plan_report(_mutation_namespace(args, brief_id))

        unresolved_count = sum(1 for part in refined["parts"] if not part.get("selection"))
        fallback_count = sum(1 for part in refined["parts"] if part.get("constraint_mode") != "full")
        missing_mutation_parts = [
            part["part_id"]
            for part in mutations["parts"]
            if part["status"] == "selected" and not part["suggestions"]
        ]
        readiness = _readiness_label(
            unresolved_count,
            refined["final"]["pairwise_conflict_count"],
            fallback_count,
            len(missing_mutation_parts),
        )
        counts[readiness] += 1

        briefs.append({
            "brief_id": brief_id,
            "description": refined["description"],
            "readiness": readiness,
            "raw_pairwise_conflicts": raw["pairwise_analysis"] and sum(len(row["conflicts"]) for row in raw["pairwise_analysis"]) or 0,
            "refined_pairwise_conflicts": refined["final"]["pairwise_conflict_count"],
            "swap_count": len(refined["refinement_swaps"]),
            "fallback_count": fallback_count,
            "unresolved_count": unresolved_count,
            "parts_with_mutations": sum(1 for part in mutations["parts"] if part["status"] == "selected" and part["suggestions"]),
            "parts_without_mutations": missing_mutation_parts,
            "remaining_conflict_notes": refined["conflict_notes"],
            "next_actions": _next_actions(
                unresolved_count,
                refined["final"]["pairwise_conflict_count"],
                fallback_count,
                len(missing_mutation_parts),
            ),
        })

    return {
        "brief_count": len(briefs),
        "prefer_rendered": args.prefer_rendered,
        "readiness_counts": counts,
        "briefs": briefs,
    }


def render_text(report: dict) -> str:
    lines = []
    lines.append("# Serum Packet Readiness")
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
            f"raw_conflicts={row['raw_pairwise_conflicts']}; refined_conflicts={row['refined_pairwise_conflicts']}; "
            f"swaps={row['swap_count']}; fallbacks={row['fallback_count']}; unresolved={row['unresolved_count']}"
        )
        if row["parts_without_mutations"]:
            lines.append(f"  parts without mutations: {', '.join(row['parts_without_mutations'])}")
        if row["remaining_conflict_notes"]:
            lines.append(f"  remaining conflicts: {' | '.join(row['remaining_conflict_notes'])}")
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
