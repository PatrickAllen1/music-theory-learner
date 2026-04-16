#!/usr/bin/env python3
"""
compare_full_song_blueprints.py

Compare two generated full-song blueprints so arrangement, processing, and
readiness differences are visible before lesson authoring starts.
"""

from __future__ import annotations

import argparse
import json
from argparse import Namespace
from pathlib import Path

try:
    from design_full_song_blueprint import build_report as build_full_song_report
except ModuleNotFoundError:
    from .design_full_song_blueprint import build_report as build_full_song_report


DEFAULT_CATALOG_DIR = Path("als/catalog/profiles")
DEFAULT_SERUM_BRIEFS_PATH = Path("als/serum-track-briefs.json")
DEFAULT_SONG_BRIEFS_PATH = Path("als/song-blueprint-briefs.json")
DEFAULT_TEMPLATES_PATH = Path("als/song-production-templates.json")


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Compare two full-song blueprints.")
    parser.add_argument("--left-brief", required=True, help="Left song brief id.")
    parser.add_argument("--right-brief", required=True, help="Right song brief id.")
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


def _namespace(args: argparse.Namespace, brief_id: str) -> Namespace:
    return Namespace(
        brief=brief_id,
        song_briefs=args.song_briefs,
        templates=args.templates,
        catalog_dir=args.catalog_dir,
        serum_briefs=args.serum_briefs,
        prefer_rendered=args.prefer_rendered,
        limit_per_part=args.limit_per_part,
        mutation_limit=args.mutation_limit,
        max_swaps=args.max_swaps,
        format="json",
    )


def build_report(args: argparse.Namespace) -> dict:
    left = build_full_song_report(_namespace(args, args.left_brief))
    right = build_full_song_report(_namespace(args, args.right_brief))
    left_layers = {row["part_id"]: row for row in left["synth_layers"]}
    right_layers = {row["part_id"]: row for row in right["synth_layers"]}
    shared_parts = sorted(set(left_layers) & set(right_layers))

    return {
        "left_brief": left["brief_id"],
        "right_brief": right["brief_id"],
        "tempo_delta": right["bpm"] - left["bpm"],
        "left_key": left["key"],
        "right_key": right["key"],
        "left_readiness": left["readiness"]["label"],
        "right_readiness": right["readiness"]["label"],
        "left_total_bars": left["readiness"]["total_bars"],
        "right_total_bars": right["readiness"]["total_bars"],
        "arrangement_diff": {
            "left": [f"{row['section_id']}:{row['start_bar']}-{row['end_bar']}" for row in left["arrangement"]],
            "right": [f"{row['section_id']}:{row['start_bar']}-{row['end_bar']}" for row in right["arrangement"]],
        },
        "sample_lane_counts": {
            "left_required": sum(1 for row in left["sample_lanes"] if row["required"]),
            "right_required": sum(1 for row in right["sample_lanes"] if row["required"]),
        },
        "shared_synth_parts": [
            {
                "part_id": part_id,
                "left_profile_id": left_layers[part_id]["profile_id"],
                "right_profile_id": right_layers[part_id]["profile_id"],
                "same_selection": left_layers[part_id]["profile_id"] == right_layers[part_id]["profile_id"],
            }
            for part_id in shared_parts
        ],
        "left_issues": left["readiness"]["issues"],
        "right_issues": right["readiness"]["issues"],
    }


def render_text(report: dict) -> str:
    lines = []
    lines.append("# Full Song Blueprint Comparison")
    lines.append("")
    lines.append(f"- left: `{report['left_brief']}`")
    lines.append(f"- right: `{report['right_brief']}`")
    lines.append(f"- tempo delta: {report['tempo_delta']}")
    lines.append(f"- key: {report['left_key']} -> {report['right_key']}")
    lines.append(f"- readiness: {report['left_readiness']} -> {report['right_readiness']}")
    lines.append(
        f"- total bars: {report['left_total_bars']} -> {report['right_total_bars']}"
    )
    lines.append("")
    lines.append("## Arrangement")
    lines.append(f"- left: {' | '.join(report['arrangement_diff']['left'])}")
    lines.append(f"- right: {' | '.join(report['arrangement_diff']['right'])}")
    lines.append("")
    lines.append("## Required Sample Lanes")
    lines.append(
        f"- left vs right: {report['sample_lane_counts']['left_required']} vs "
        f"{report['sample_lane_counts']['right_required']}"
    )
    lines.append("")
    lines.append("## Shared Synth Parts")
    for row in report["shared_synth_parts"]:
        lines.append(
            f"- `{row['part_id']}` :: {row['left_profile_id']} <> {row['right_profile_id']} "
            f"[same={row['same_selection']}]"
        )
    if report["left_issues"] or report["right_issues"]:
        lines.append("")
        lines.append("## Readiness Issues")
        if report["left_issues"]:
            lines.append(f"- left: {' | '.join(report['left_issues'])}")
        if report["right_issues"]:
            lines.append(f"- right: {' | '.join(report['right_issues'])}")
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
