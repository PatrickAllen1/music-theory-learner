#!/usr/bin/env python3
"""
report_serum_render_backlog.py

Rank which non-rendered Serum profiles should be rendered next based on packet
readiness, fallback pressure, conflict participation, and mutation coverage.

Examples:
    python3 als/report_serum_render_backlog.py
    python3 als/report_serum_render_backlog.py --format json
"""

from __future__ import annotations

import argparse
import json
from argparse import Namespace
from pathlib import Path

try:
    from refine_serum_track_blueprint import build_report as build_refined_blueprint_report
    from report_serum_packet_readiness import build_report as build_packet_readiness_report
    from suggest_serum_blueprint_mutations import build_report as build_mutation_plan_report
except ModuleNotFoundError:
    from .refine_serum_track_blueprint import build_report as build_refined_blueprint_report
    from .report_serum_packet_readiness import build_report as build_packet_readiness_report
    from .suggest_serum_blueprint_mutations import build_report as build_mutation_plan_report


DEFAULT_CATALOG_DIR = Path("als/catalog/profiles")
DEFAULT_BRIEFS_PATH = Path("als/serum-track-briefs.json")
READINESS_WEIGHT = {"blocked": 6, "needs_work": 4, "usable": 2, "strong": 0}


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Rank non-rendered Serum profiles for the next render pass.")
    parser.add_argument("--catalog-dir", default=str(DEFAULT_CATALOG_DIR), help="Directory of generated *-profiles.json files.")
    parser.add_argument("--briefs", default=str(DEFAULT_BRIEFS_PATH), help="Track brief manifest JSON.")
    parser.add_argument("--prefer-rendered", action="store_true", help="Prefer rendered profiles where available during blueprint building.")
    parser.add_argument("--limit-per-part", type=int, default=5, help="Max candidates to inspect per part. Default: 5")
    parser.add_argument("--mutation-limit", type=int, default=6, help="Max mutation suggestions per part. Default: 6")
    parser.add_argument("--max-swaps", type=int, default=2, help="Maximum refinement swaps to apply. Default: 2")
    parser.add_argument("--format", choices=["json", "text"], default="text", help="Output format.")
    return parser


def _refine_namespace(args: argparse.Namespace, brief_id: str) -> Namespace:
    return Namespace(
        catalog_dir=args.catalog_dir,
        briefs=args.briefs,
        brief=brief_id,
        prefer_rendered=args.prefer_rendered,
        limit_per_part=args.limit_per_part,
        mutation_limit=args.mutation_limit,
        alternative_limit=max(args.limit_per_part, 5),
        max_swaps=args.max_swaps,
        format="json",
    )


def _mutation_namespace(args: argparse.Namespace, brief_id: str) -> Namespace:
    return Namespace(
        **vars(_refine_namespace(args, brief_id)),
        refine=True,
        suggestion_limit=8,
    )


def _readiness_namespace(args: argparse.Namespace) -> Namespace:
    return Namespace(
        catalog_dir=args.catalog_dir,
        briefs=args.briefs,
        prefer_rendered=args.prefer_rendered,
        limit_per_part=args.limit_per_part,
        mutation_limit=args.mutation_limit,
        max_swaps=args.max_swaps,
        format="json",
    )


def _conflict_counts(refined: dict) -> dict[str, int]:
    counts: dict[str, int] = {}
    for issue in refined["final"]["issues"]:
        counts[issue["part_id"]] = issue["pairwise_conflicts"]
    return counts


def _mutation_map(mutation_plan: dict) -> dict[str, dict]:
    return {part["part_id"]: part for part in mutation_plan["parts"]}


def build_report(args: argparse.Namespace) -> dict:
    readiness = build_packet_readiness_report(_readiness_namespace(args))
    readiness_by_brief = {row["brief_id"]: row for row in readiness["briefs"]}

    backlog: dict[str, dict] = {}
    for brief_id, readiness_row in readiness_by_brief.items():
        refined = build_refined_blueprint_report(_refine_namespace(args, brief_id))
        mutation_plan = build_mutation_plan_report(_mutation_namespace(args, brief_id))
        mutation_by_part = _mutation_map(mutation_plan)
        part_conflicts = _conflict_counts(refined)

        for part in refined["parts"]:
            selection = part.get("selection")
            if not selection or selection.get("audio_status") == "rendered":
                continue

            profile_id = selection["profile_id"]
            mutation_part = mutation_by_part.get(part["part_id"], {})
            score = 1
            reasons = []

            readiness_bonus = READINESS_WEIGHT.get(readiness_row["readiness"], 0)
            score += readiness_bonus
            if readiness_bonus:
                reasons.append(f"brief readiness is {readiness_row['readiness']}")

            if part.get("constraint_mode") != "full":
                score += 3
                reasons.append(f"selected under {part['constraint_mode']} fallback")

            conflict_count = part_conflicts.get(part["part_id"], 0)
            if conflict_count:
                score += conflict_count * 2
                reasons.append(f"involved in {conflict_count} remaining pairwise conflicts")

            suggestion_count = len(mutation_part.get("suggestions") or [])
            if suggestion_count == 0:
                score += 2
                reasons.append("has no actionable mutation suggestions yet")
            elif suggestion_count <= 2:
                score += 1
                reasons.append("has only a small mutation surface")

            if any(row["part_id"] == part["part_id"] for row in refined.get("refinement_swaps") or []):
                score += 1
                reasons.append("was swapped in during refinement")

            entry = backlog.setdefault(profile_id, {
                "profile_id": profile_id,
                "track": selection.get("track"),
                "analysis_slug": selection.get("analysis_slug"),
                "audio_status": selection.get("audio_status"),
                "selection_count": 0,
                "score": 0,
                "briefs": [],
                "reasons": set(),
                "priority": "low",
            })
            entry["selection_count"] += 1
            entry["score"] += score
            entry["briefs"].append({
                "brief_id": brief_id,
                "part_id": part["part_id"],
                "role": part["role"],
                "constraint_mode": part.get("constraint_mode"),
                "conflict_count": conflict_count,
                "mutation_suggestion_count": suggestion_count,
                "readiness": readiness_row["readiness"],
                "score_contribution": score,
            })
            entry["reasons"].update(reasons)

    rows = []
    for row in backlog.values():
        if row["selection_count"] >= 2:
            row["score"] += 2
            row["reasons"].add("selected in multiple briefs")
        row["priority"] = "high" if row["score"] >= 8 else ("medium" if row["score"] >= 4 else "low")
        row["reasons"] = sorted(row["reasons"])
        row["briefs"].sort(key=lambda item: (-item["score_contribution"], item["brief_id"], item["part_id"]))
        rows.append(row)

    rows.sort(key=lambda item: (-item["score"], item["profile_id"]))
    return {
        "profile_count": len(rows),
        "prefer_rendered": args.prefer_rendered,
        "backlog": rows,
    }


def render_text(report: dict) -> str:
    lines = []
    lines.append("# Serum Render Backlog")
    lines.append("")
    lines.append(f"- profiles: {report['profile_count']}")
    lines.append(f"- prefer rendered: {'yes' if report['prefer_rendered'] else 'no'}")
    lines.append("")
    for row in report["backlog"]:
        lines.append(
            f"- `{row['profile_id']}` :: score={row['score']}; priority={row['priority']}; "
            f"count={row['selection_count']}; audio={row['audio_status']}"
        )
        if row["reasons"]:
            lines.append(f"  reasons: {' | '.join(row['reasons'])}")
        if row["briefs"]:
            brief_summary = " | ".join(
                f"{item['brief_id']}:{item['part_id']}({item['constraint_mode']}, conflicts={item['conflict_count']}, mutations={item['mutation_suggestion_count']})"
                for item in row["briefs"][:4]
            )
            lines.append(f"  briefs: {brief_summary}")
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
