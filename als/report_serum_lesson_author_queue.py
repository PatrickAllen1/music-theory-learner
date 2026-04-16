#!/usr/bin/env python3
"""
report_serum_lesson_author_queue.py

Rank Serum briefs by how close they are to being strong lesson-authoring
candidates, taking full-song readiness, compiled-lesson quality, and render
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
    from report_serum_render_backlog import build_report as build_render_backlog_report
except ModuleNotFoundError:
    from .report_serum_render_backlog import build_report as build_render_backlog_report


READINESS_BASE = {"strong": 12, "usable": 8, "needs_work": 4, "blocked": 0}


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Rank Serum briefs by lesson-authoring readiness.")
    parser.add_argument("--brief", help="Optional single brief id to inspect.")
    parser.add_argument("--catalog-dir", default="als/catalog/profiles", help="Directory of generated *-profiles.json files.")
    parser.add_argument("--briefs", default="als/serum-track-briefs.json", help="Underlying Serum brief manifest JSON.")
    parser.add_argument("--song-briefs", default="als/song-blueprint-briefs.json", help="Song-level brief manifest JSON.")
    parser.add_argument("--templates", default="als/song-production-templates.json", help="Song production templates JSON.")
    parser.add_argument("--prefer-rendered", action="store_true", help="Prefer rendered profiles where available.")
    parser.add_argument("--limit-per-part", type=int, default=5, help="Max candidates to inspect per part. Default: 5")
    parser.add_argument("--mutation-limit", type=int, default=6, help="Max mutation suggestions per part. Default: 6")
    parser.add_argument("--max-swaps", type=int, default=2, help="Maximum refinement swaps to apply. Default: 2")
    parser.add_argument("--format", choices=["json", "text"], default="text", help="Output format.")
    return parser


def _namespace(args: argparse.Namespace) -> Namespace:
    return Namespace(
        catalog_dir=args.catalog_dir,
        brief=getattr(args, "brief", None),
        briefs=getattr(args, "briefs", "als/serum-track-briefs.json"),
        serum_briefs=getattr(args, "serum_briefs", getattr(args, "briefs", "als/serum-track-briefs.json")),
        song_briefs=getattr(args, "song_briefs", "als/song-blueprint-briefs.json"),
        templates=getattr(args, "templates", "als/song-production-templates.json"),
        prefer_rendered=args.prefer_rendered,
        limit_per_part=args.limit_per_part,
        mutation_limit=args.mutation_limit,
        max_swaps=args.max_swaps,
        format="json",
    )


def build_report(args: argparse.Namespace) -> dict:
    try:
        from report_full_song_blueprint_readiness import build_report as build_full_song_readiness_report
    except ModuleNotFoundError:
        from .report_full_song_blueprint_readiness import build_report as build_full_song_readiness_report

    readiness = build_full_song_readiness_report(_namespace(args))
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
        score += READINESS_BASE.get(brief["blueprint_readiness"], 0)
        score += READINESS_BASE.get(brief["lesson_readiness"], 0)
        score -= brief["synth_conflicts"] * 2
        score -= brief["fallback_synth_parts"] * 2
        score -= brief["unresolved_synth_parts"] * 4
        score -= len(brief["vague_step_ids"])
        score -= brief["missing_processing_chains"] * 3
        score -= high_render_count

        next_actions = list(brief["next_actions"])
        if high_render_count:
            next_actions.append("render the top high-priority profiles tied to this brief before authoring the lesson")

        rows.append({
            "brief_id": brief["brief_id"],
            "description": brief["description"],
            "readiness": brief["readiness"],
            "blueprint_readiness": brief["blueprint_readiness"],
            "lesson_readiness": brief["lesson_readiness"],
            "author_score": score,
            "synth_conflicts": brief["synth_conflicts"],
            "fallback_synth_parts": brief["fallback_synth_parts"],
            "unresolved_synth_parts": brief["unresolved_synth_parts"],
            "missing_processing_chains": brief["missing_processing_chains"],
            "vague_step_ids": brief["vague_step_ids"],
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
            f"blueprint={row['blueprint_readiness']}; lesson={row['lesson_readiness']}; "
            f"conflicts={row['synth_conflicts']}; fallbacks={row['fallback_synth_parts']}; "
            f"high_render_blockers={row['high_priority_render_count']}"
        )
        if row["vague_step_ids"]:
            lines.append(f"  vague steps: {', '.join(str(i) for i in row['vague_step_ids'])}")
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
