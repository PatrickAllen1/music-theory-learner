#!/usr/bin/env python3
"""
recommend_phrase_evidence.py

Recommend phrase-writing evidence for a song brief by combining ALS note clips,
composition-heavy transcript spans, and composition techniques.
"""

from __future__ import annotations

import argparse
import json
from argparse import Namespace
from pathlib import Path

try:
    from design_full_song_blueprint import build_report as build_full_song_blueprint_report
    from phrase_evidence import (
        DEFAULT_ANALYSIS_DIR,
        DEFAULT_TRANSCRIPTS_DIR,
        build_phrase_library,
        recommend_for_blueprint,
    )
    from technique_bank import DEFAULT_BANK_PATH, load_bank
except ModuleNotFoundError:
    from .design_full_song_blueprint import build_report as build_full_song_blueprint_report
    from .phrase_evidence import (
        DEFAULT_ANALYSIS_DIR,
        DEFAULT_TRANSCRIPTS_DIR,
        build_phrase_library,
        recommend_for_blueprint,
    )
    from .technique_bank import DEFAULT_BANK_PATH, load_bank


DEFAULT_CATALOG_DIR = Path("als/catalog/profiles")
DEFAULT_SERUM_BRIEFS_PATH = Path("als/serum-track-briefs.json")
DEFAULT_SONG_BRIEFS_PATH = Path("als/song-blueprint-briefs.json")
DEFAULT_TEMPLATES_PATH = Path("als/song-production-templates.json")


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Recommend composition phrase evidence for a song brief.")
    parser.add_argument("--brief", required=True, help="Song brief id from the manifest.")
    parser.add_argument("--song-briefs", default=str(DEFAULT_SONG_BRIEFS_PATH), help="Song-level brief manifest JSON.")
    parser.add_argument("--templates", default=str(DEFAULT_TEMPLATES_PATH), help="Song production templates JSON.")
    parser.add_argument("--catalog-dir", default=str(DEFAULT_CATALOG_DIR), help="Directory of generated *-profiles.json files.")
    parser.add_argument("--serum-briefs", default=str(DEFAULT_SERUM_BRIEFS_PATH), help="Serum brief manifest JSON.")
    parser.add_argument("--analysis-dir", default=str(DEFAULT_ANALYSIS_DIR), help="ALS analysis JSON directory.")
    parser.add_argument("--transcripts-dir", default=str(DEFAULT_TRANSCRIPTS_DIR), help="Transcript spans directory.")
    parser.add_argument("--technique-bank", default=str(DEFAULT_BANK_PATH), help="Technique bank JSON path.")
    parser.add_argument("--prefer-rendered", action="store_true", help="Prefer rendered profiles where available.")
    parser.add_argument("--limit-per-part", type=int, default=5, help="Max candidates to inspect per part. Default: 5")
    parser.add_argument("--mutation-limit", type=int, default=6, help="Max mutation suggestions per part. Default: 6")
    parser.add_argument("--max-swaps", type=int, default=2, help="Maximum refinement swaps to apply. Default: 2")
    parser.add_argument("--limit", type=int, default=10, help="Max evidence rows to return. Default: 10")
    parser.add_argument("--format", choices=["json", "text"], default="text", help="Output format.")
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
    bank = load_bank(Path(args.technique_bank))
    library = build_phrase_library(
        bank,
        analysis_dir=Path(args.analysis_dir),
        transcripts_dir=Path(args.transcripts_dir),
    )
    return recommend_for_blueprint(blueprint, library, args.limit)


def render_text(report: dict) -> str:
    lines = []
    lines.append("# Phrase Evidence")
    lines.append("")
    lines.append(f"- brief: `{report['brief_id']}`")
    lines.append(f"- results: {report['result_count']}")
    if report.get("emotional_target"):
        lines.append(f"- emotional target: {', '.join(report['emotional_target'])}")
    lines.append("")
    for row in report["recommendations"]:
        lines.append(f"- `{row['title']}` [{row['kind']}/{row['role']}] score={row['score']} source={row['source']}")
        if row["matched_keywords"]:
            lines.append(f"  matched: {', '.join(row['matched_keywords'])}")
        if row["emotion_hints"]:
            lines.append(f"  emotion: {', '.join(row['emotion_hints'])}")
        lines.append(f"  {row['summary']}")
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
