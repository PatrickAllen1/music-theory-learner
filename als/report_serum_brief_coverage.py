#!/usr/bin/env python3
"""
report_serum_brief_coverage.py

Analyze all configured Serum track briefs, summarize how well the current
catalog satisfies them, and rank the highest-value render targets.

Examples:
    python3 als/report_serum_brief_coverage.py
    python3 als/report_serum_brief_coverage.py --prefer-rendered --format json
"""

from __future__ import annotations

import argparse
import json
from argparse import Namespace
from pathlib import Path

try:
    from design_serum_track_blueprint import build_report as build_blueprint_report
except ModuleNotFoundError:
    from .design_serum_track_blueprint import build_report as build_blueprint_report


DEFAULT_CATALOG_DIR = Path("als/catalog/profiles")
DEFAULT_BRIEFS_PATH = Path("als/serum-track-briefs.json")


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Report Serum brief coverage and render priorities.")
    parser.add_argument("--catalog-dir", default=str(DEFAULT_CATALOG_DIR), help="Directory of generated *-profiles.json files.")
    parser.add_argument("--briefs", default=str(DEFAULT_BRIEFS_PATH), help="Track brief manifest JSON.")
    parser.add_argument("--prefer-rendered", action="store_true", help="Prefer rendered profiles where available.")
    parser.add_argument("--limit-per-part", type=int, default=5, help="Max candidates to inspect per blueprint part. Default: 5")
    parser.add_argument("--mutation-limit", type=int, default=6, help="Max mutation suggestions per part. Default: 6")
    parser.add_argument("--format", choices=["json", "text"], default="text", help="Output format.")
    return parser


def _brief_ids(path: Path) -> list[str]:
    payload = json.loads(path.read_text())
    return sorted((payload.get("briefs") or {}).keys())


def _namespace(args: argparse.Namespace, brief_id: str) -> Namespace:
    return Namespace(
        catalog_dir=args.catalog_dir,
        briefs=args.briefs,
        brief=brief_id,
        prefer_rendered=args.prefer_rendered,
        limit_per_part=args.limit_per_part,
        mutation_limit=args.mutation_limit,
        format="json",
    )


def build_report(args: argparse.Namespace) -> dict:
    brief_reports = []
    selected_profile_counts: dict[str, int] = {}
    selected_profile_meta: dict[str, dict] = {}
    fallback_counts: dict[str, int] = {}
    unresolved_parts = []

    for brief_id in _brief_ids(Path(args.briefs)):
        blueprint = build_blueprint_report(_namespace(args, brief_id))
        resolved_count = 0
        rendered_selected = 0
        for part in blueprint["parts"]:
            selection = part.get("selection")
            if selection:
                resolved_count += 1
                profile_id = selection["profile_id"]
                selected_profile_counts[profile_id] = selected_profile_counts.get(profile_id, 0) + 1
                selected_profile_meta.setdefault(profile_id, {
                    "profile_id": profile_id,
                    "track": selection.get("track"),
                    "analysis_slug": selection.get("analysis_slug"),
                    "audio_status": selection.get("audio_status"),
                })
                if selection.get("audio_status") == "rendered":
                    rendered_selected += 1
            else:
                unresolved_parts.append({
                    "brief_id": brief_id,
                    "part_id": part["part_id"],
                    "role": part["role"],
                    "target_tone": part.get("target_tone", []),
                    "target_mix": part.get("target_mix", []),
                })
            fallback_counts[part["constraint_mode"]] = fallback_counts.get(part["constraint_mode"], 0) + 1

        brief_reports.append({
            "brief_id": brief_id,
            "description": blueprint["description"],
            "part_count": len(blueprint["parts"]),
            "resolved_count": resolved_count,
            "rendered_selected_count": rendered_selected,
            "conflict_count": len(blueprint["conflict_notes"]),
            "pairwise_conflict_count": sum(1 for row in blueprint["pairwise_analysis"] if row["conflicts"]),
            "selected_profile_ids": blueprint["selected_profile_ids"],
            "part_constraints": [
                {
                    "part_id": part["part_id"],
                    "role": part["role"],
                    "constraint_mode": part["constraint_mode"],
                    "selected_profile_id": part["selection"]["profile_id"] if part.get("selection") else None,
                    "audio_status": part["selection"].get("audio_status") if part.get("selection") else None,
                }
                for part in blueprint["parts"]
            ],
        })

    render_priorities = []
    for profile_id, count in sorted(selected_profile_counts.items(), key=lambda item: (-item[1], item[0])):
        meta = selected_profile_meta[profile_id]
        render_priorities.append({
            "profile_id": profile_id,
            "selection_count": count,
            "track": meta["track"],
            "analysis_slug": meta["analysis_slug"],
            "audio_status": meta["audio_status"],
            "render_priority": "high" if meta["audio_status"] != "rendered" and count >= 2 else ("medium" if meta["audio_status"] != "rendered" else "done"),
        })

    return {
        "brief_count": len(brief_reports),
        "prefer_rendered": args.prefer_rendered,
        "briefs": brief_reports,
        "fallback_counts": dict(sorted(fallback_counts.items())),
        "unresolved_parts": unresolved_parts,
        "render_priorities": render_priorities,
    }


def render_text(report: dict) -> str:
    lines = []
    lines.append("# Serum Brief Coverage")
    lines.append("")
    lines.append(f"- briefs: {report['brief_count']}")
    lines.append(f"- prefer rendered: {'yes' if report['prefer_rendered'] else 'no'}")
    lines.append("")
    lines.append("## Fallback Counts")
    for mode, count in report["fallback_counts"].items():
        lines.append(f"- `{mode}`: {count}")
    lines.append("")
    lines.append("## Briefs")
    for brief in report["briefs"]:
        lines.append(
            f"- `{brief['brief_id']}` :: resolved {brief['resolved_count']}/{brief['part_count']}; "
            f"rendered selections {brief['rendered_selected_count']}; "
            f"conflicts {brief['conflict_count']}; pairwise conflicts {brief['pairwise_conflict_count']}"
        )
    lines.append("")
    if report["unresolved_parts"]:
        lines.append("## Unresolved Parts")
        for row in report["unresolved_parts"]:
            lines.append(
                f"- `{row['brief_id']}` / `{row['part_id']}` ({row['role']}) "
                f"[tone: {', '.join(row['target_tone']) or '-'}; mix: {', '.join(row['target_mix']) or '-'}]"
            )
        lines.append("")
    lines.append("## Render Priorities")
    for row in report["render_priorities"]:
        lines.append(
            f"- `{row['profile_id']}` :: count={row['selection_count']}; "
            f"audio={row['audio_status']}; priority={row['render_priority']}"
        )
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
