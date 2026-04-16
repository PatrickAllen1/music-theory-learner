#!/usr/bin/env python3
"""
recommend_production_techniques.py

Recommend production techniques from docs/techniques/bank.json for a full-song
brief so transcript-derived knowledge can influence track creation.

Examples:
    python3 als/recommend_production_techniques.py --brief ukg-2step-dark-stab
    python3 als/recommend_production_techniques.py --brief ukg-4x4-pluck-driver --limit 5 --format json
"""

from __future__ import annotations

import argparse
import json
from argparse import Namespace
from pathlib import Path

try:
    from design_full_song_blueprint import build_report as build_full_song_blueprint_report
    from technique_bank import DEFAULT_BANK_PATH, load_bank, recommend_for_blueprint
except ModuleNotFoundError:
    from .design_full_song_blueprint import build_report as build_full_song_blueprint_report
    from .technique_bank import DEFAULT_BANK_PATH, load_bank, recommend_for_blueprint

DEFAULT_CATALOG_DIR = Path("als/catalog/profiles")
DEFAULT_SERUM_BRIEFS_PATH = Path("als/serum-track-briefs.json")
DEFAULT_SONG_BRIEFS_PATH = Path("als/song-blueprint-briefs.json")
DEFAULT_TEMPLATES_PATH = Path("als/song-production-templates.json")


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Recommend production techniques for a full-song brief.")
    parser.add_argument("--brief", required=True, help="Song brief id from the manifest.")
    parser.add_argument("--bank", default=str(DEFAULT_BANK_PATH), help="Technique bank JSON path.")
    parser.add_argument("--song-briefs", default=str(DEFAULT_SONG_BRIEFS_PATH), help="Song-level brief manifest JSON.")
    parser.add_argument("--templates", default=str(DEFAULT_TEMPLATES_PATH), help="Song production templates JSON.")
    parser.add_argument("--catalog-dir", default=str(DEFAULT_CATALOG_DIR), help="Directory of generated *-profiles.json files.")
    parser.add_argument("--serum-briefs", default=str(DEFAULT_SERUM_BRIEFS_PATH), help="Serum brief manifest JSON.")
    parser.add_argument("--prefer-rendered", action="store_true", help="Prefer rendered profiles where available.")
    parser.add_argument("--limit-per-part", type=int, default=5, help="Max candidates to inspect per part. Default: 5")
    parser.add_argument("--mutation-limit", type=int, default=6, help="Max mutation suggestions per part. Default: 6")
    parser.add_argument("--max-swaps", type=int, default=2, help="Maximum refinement swaps to apply. Default: 2")
    parser.add_argument("--limit", type=int, default=8, help="Maximum recommendations to return. Default: 8")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="Output format.")
    return parser


def _namespace(args: argparse.Namespace) -> Namespace:
    return Namespace(
        brief=args.brief,
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
    blueprint = build_full_song_blueprint_report(_namespace(args))
    return recommend_for_blueprint(blueprint, load_bank(Path(args.bank)), args.limit)


def render_text(report: dict) -> str:
    lines = []
    lines.append("# Production Technique Recommendations")
    lines.append("")
    lines.append(f"- brief: `{report['brief_id']}`")
    lines.append(f"- results: {report['result_count']}")
    lines.append("")
    for row in report["recommendations"]:
        lines.append(f"- `{row['id']}` :: {row['name']} [{row['source']}] score={row['score']}")
        if row["matched_keywords"]:
            lines.append(f"  matched keywords: {', '.join(row['matched_keywords'])}")
        lines.append(f"  does: {row['what_it_does']}")
        lines.append(f"  when: {row['when_to_use']}")
        lines.append(f"  works with: {' | '.join(row['works_well_with'])}")
        lines.append(f"  clashes with: {' | '.join(row['likely_clashes_with'])}")
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
