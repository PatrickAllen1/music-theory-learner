#!/usr/bin/env python3
"""
prepare_serum_preset_capture_session.py

Create a manual preset-capture queue from the current gap-driven preset
shortlist so future bank captures can target the highest-value missing sounds.

Examples:
    python3 als/prepare_serum_preset_capture_session.py --out-dir als/preset-capture-session
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    from report_serum_preset_capture_candidates import build_report as build_capture_report
except ModuleNotFoundError:
    from .report_serum_preset_capture_candidates import build_report as build_capture_report


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Prepare a preset-capture session from the current gap shortlist.")
    parser.add_argument("--out-dir", required=True, help="Output directory for the capture session bundle.")
    parser.add_argument("--catalog-dir", default="als/catalog/profiles", help="Directory of generated *-profiles.json files.")
    parser.add_argument("--briefs", default="als/serum-track-briefs.json", help="Track brief manifest JSON.")
    parser.add_argument("--prefer-rendered", action="store_true", help="Prefer rendered profiles where available when computing gaps.")
    parser.add_argument("--limit-per-part", type=int, default=5, help="Max candidates to inspect per part. Default: 5")
    parser.add_argument("--mutation-limit", type=int, default=6, help="Max mutation suggestions per part. Default: 6")
    parser.add_argument("--max-swaps", type=int, default=2, help="Maximum refinement swaps to apply. Default: 2")
    parser.add_argument("--bank-dir", action="append", default=[], help="Preset bank directory to scan. Pass multiple times.")
    parser.add_argument("--top-per-gap", type=int, default=5, help="Maximum preset candidates per gap. Default: 5")
    parser.add_argument("--overall-limit", type=int, default=12, help="Maximum unique presets in the overall shortlist. Default: 12")
    parser.add_argument("--force", action="store_true", help="Overwrite existing metadata files.")
    return parser


def _write_text(path: Path, content: str, force: bool) -> None:
    if path.exists() and not force:
        raise FileExistsError(f"{path} already exists; rerun with --force to overwrite")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def _tsv(report: dict) -> str:
    header = [
        "preset_path",
        "track",
        "bank",
        "role",
        "tone_tags",
        "gap_labels",
        "score_total",
    ]
    lines = ["\t".join(header)]
    for row in report["overall_shortlist"]:
        lines.append("\t".join([
            row["path"],
            row["track"],
            row.get("bank") or "",
            row["role"],
            ",".join(row["tone_tags"]),
            " | ".join(row["gap_labels"]),
            str(row["score_total"]),
        ]))
    return "\n".join(lines) + "\n"


def _readme(out_dir: Path, report: dict) -> str:
    lines = []
    lines.append("# Serum Preset Capture Session")
    lines.append("")
    lines.append(f"- presets in shortlist: {len(report['overall_shortlist'])}")
    lines.append(f"- gaps covered: {report['gap_count']}")
    lines.append("")
    lines.append("## Workflow")
    lines.append("1. Open `overall_shortlist.tsv` and work from the top row down.")
    lines.append("2. Load each listed preset in Serum 2 from the exact `preset_path`.")
    lines.append("3. Capture or render the preset using whatever session workflow we use next.")
    lines.append("4. Keep notes on which gap labels each preset is meant to help cover.")
    lines.append("")
    lines.append("## Files")
    lines.append("- `overall_shortlist.tsv`: top unique presets to capture first")
    lines.append("- `capture_candidates.json`: full structured candidate report by gap")
    lines.append("- `session_config.json`: generation parameters for this queue")
    lines.append("")
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = make_parser()
    args = parser.parse_args()
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    report = build_capture_report(args)
    _write_text(out_dir / "README.md", _readme(out_dir, report), args.force)
    _write_text(out_dir / "overall_shortlist.tsv", _tsv(report), args.force)
    _write_text(out_dir / "capture_candidates.json", json.dumps(report, indent=2) + "\n", args.force)
    _write_text(out_dir / "session_config.json", json.dumps({
        "catalog_dir": args.catalog_dir,
        "briefs": args.briefs,
        "prefer_rendered": args.prefer_rendered,
        "limit_per_part": args.limit_per_part,
        "mutation_limit": args.mutation_limit,
        "max_swaps": args.max_swaps,
        "bank_dirs": args.bank_dir,
        "top_per_gap": args.top_per_gap,
        "overall_limit": args.overall_limit,
    }, indent=2) + "\n", args.force)

    print(json.dumps({
        "ok": True,
        "out_dir": str(out_dir),
        "shortlist_count": len(report["overall_shortlist"]),
        "gap_count": report["gap_count"],
        "files": [
            "README.md",
            "overall_shortlist.tsv",
            "capture_candidates.json",
            "session_config.json",
        ],
    }, indent=2))


if __name__ == "__main__":
    main()
