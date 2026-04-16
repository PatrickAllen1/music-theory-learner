#!/usr/bin/env python3
"""
report_serum_lesson_author_queue.py

Rank Serum briefs by how close they are to being strong lesson-authoring
candidates, taking readiness, remaining conflicts, fallbacks, and render
dependencies into account.

Examples:
    python3 als/report_serum_lesson_author_queue.py
    python3 als/report_serum_lesson_author_queue.py --format json
"""

from __future__ import annotations

import argparse
import json
from argparse import Namespace

try:
    from report_serum_packet_readiness import build_report as build_packet_readiness_report
    from report_serum_render_backlog import build_report as build_render_backlog_report
except ModuleNotFoundError:
    from .report_serum_packet_readiness import build_report as build_packet_readiness_report
    from .report_serum_render_backlog import build_report as build_render_backlog_report


READINESS_BASE = {"strong": 12, "usable": 8, "needs_work": 4, "blocked": 0}


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Rank Serum briefs by lesson-authoring readiness.")
    parser.add_argument("--catalog-dir", default="als/catalog/profiles", help="Directory of generated *-profiles.json files.")
    parser.add_argument("--briefs", default="als/serum-track-briefs.json", help="Track brief manifest JSON.")
    parser.add_argument("--prefer-rendered", action="store_true", help="Prefer rendered profiles where available.")
    parser.add_argument("--limit-per-part", type=int, default=5, help="Max candidates to inspect per part. Default: 5")
    parser.add_argument("--mutation-limit", type=int, default=6, help="Max mutation suggestions per part. Default: 6")
    parser.add_argument("--max-swaps", type=int, default=2, help="Maximum refinement swaps to apply. Default: 2")
    parser.add_argument("--format", choices=["json", "text"], default="text", help="Output format.")
    return parser


def _namespace(args: argparse.Namespace) -> Namespace:
    return Namespace(
        catalog_dir=args.catalog_dir,
        briefs=args.briefs,
        prefer_rendered=args.prefer_rendered,
        limit_per_part=args.limit_per_part,
        mutation_limit=args.mutation_limit,
        max_swaps=args.max_swaps,
        format="json",
    )


def build_report(args: argparse.Namespace) -> dict:
    readiness = build_packet_readiness_report(_namespace(args))
    backlog = build_render_backlog_report(_namespace(args))

    render_by_brief: dict[str, list[dict]] = {}
    for row in backlog["backlog"]:
        for brief in row["briefs"]:
            render_by_brief.setdefault(brief["brief_id"], []).append({
                "profile_id": row["profile_id"],
                "priority": row["priority"],
                "score": row["score"],
                "part_id": brief["part_id"],
                "constraint_mode": brief["constraint_mode"],
                "conflict_count": brief["conflict_count"],
                "mutation_suggestion_count": brief["mutation_suggestion_count"],
            })

    rows = []
    for brief in readiness["briefs"]:
        render_blockers = sorted(render_by_brief.get(brief["brief_id"], []), key=lambda row: (-row["score"], row["profile_id"]))
        high_render_count = sum(1 for row in render_blockers if row["priority"] == "high")
        score = READINESS_BASE.get(brief["readiness"], 0)
        score -= brief["refined_pairwise_conflicts"] * 2
        score -= brief["fallback_count"] * 2
        score -= brief["unresolved_count"] * 4
        score -= len(brief["parts_without_mutations"])
        score -= high_render_count

        next_actions = list(brief["next_actions"])
        if high_render_count:
            next_actions.append("render the top high-priority profiles tied to this brief before authoring the lesson")

        rows.append({
            "brief_id": brief["brief_id"],
            "description": brief["description"],
            "readiness": brief["readiness"],
            "author_score": score,
            "refined_pairwise_conflicts": brief["refined_pairwise_conflicts"],
            "fallback_count": brief["fallback_count"],
            "parts_without_mutations": brief["parts_without_mutations"],
            "high_priority_render_count": high_render_count,
            "render_blockers": render_blockers[:5],
            "next_actions": next_actions,
        })

    rows.sort(key=lambda row: (-row["author_score"], row["brief_id"]))
    return {
        "brief_count": len(rows),
        "prefer_rendered": args.prefer_rendered,
        "queue": rows,
    }


def render_text(report: dict) -> str:
    lines = []
    lines.append("# Serum Lesson Author Queue")
    lines.append("")
    lines.append(f"- briefs: {report['brief_count']}")
    lines.append(f"- prefer rendered: {'yes' if report['prefer_rendered'] else 'no'}")
    lines.append("")
    for row in report["queue"]:
        lines.append(
            f"- `{row['brief_id']}` :: author_score={row['author_score']}; readiness={row['readiness']}; "
            f"conflicts={row['refined_pairwise_conflicts']}; fallbacks={row['fallback_count']}; "
            f"high_render_blockers={row['high_priority_render_count']}"
        )
        if row["parts_without_mutations"]:
            lines.append(f"  parts without mutations: {', '.join(row['parts_without_mutations'])}")
        if row["render_blockers"]:
            blockers = " | ".join(
                f"{item['profile_id']}->{item['part_id']}({item['priority']})"
                for item in row["render_blockers"]
            )
            lines.append(f"  render blockers: {blockers}")
        if row["next_actions"]:
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
