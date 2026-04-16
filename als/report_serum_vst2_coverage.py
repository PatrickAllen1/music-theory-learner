#!/usr/bin/env python3
"""
report_serum_vst2_coverage.py
Report how much of the named Serum VST2 host control surface is already covered
by the current standalone FXP parser.

Examples:
    python3 als/report_serum_vst2_coverage.py
    python3 als/report_serum_vst2_coverage.py --summary-only
    python3 als/report_serum_vst2_coverage.py --category fx
"""

import argparse
import json
import sys

from parse_serum import SERUM_VST2_PLUGIN_BINARY_PATH, build_serum_vst2_host_coverage_report


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Report Serum VST2 host-catalog coverage by the current FXP parser.")
    parser.add_argument(
        "--binary",
        default=str(SERUM_VST2_PLUGIN_BINARY_PATH),
        help="Path to the Serum VST2 plugin binary",
    )
    parser.add_argument(
        "--summary-only",
        action="store_true",
        help="Only print top-level totals and category summaries",
    )
    parser.add_argument(
        "--category",
        help="Only include entries from one category (e.g. fx, matrix, envelope, osc_a)",
    )
    parser.add_argument(
        "--module",
        help="Only include entries from one module (e.g. fx_delay, fx_distortion, global_voicing)",
    )
    parser.add_argument(
        "--limit-uncovered",
        type=int,
        default=12,
        help="When using --summary-only, include up to N uncovered labels per category",
    )
    return parser


def _trim_summary(report: dict, limit_uncovered: int) -> dict:
    categories = {}
    for name, summary in report["categories"].items():
        categories[name] = {
            "total": summary["total"],
            "covered": summary["covered"],
            "uncovered": summary["uncovered"],
            "covered_pct": summary["covered_pct"],
            "covered_labels": summary["covered_labels"],
            "uncovered_labels": summary["uncovered_labels"][:limit_uncovered],
        }

    modules = {}
    for name, summary in report.get("modules", {}).items():
        modules[name] = {
            "manual_section": summary["manual_section"],
            "total": summary["total"],
            "covered": summary["covered"],
            "uncovered": summary["uncovered"],
            "covered_pct": summary["covered_pct"],
            "covered_labels": summary["covered_labels"],
            "uncovered_labels": summary["uncovered_labels"][:limit_uncovered],
        }

    return {
        "binary_path": report["binary_path"],
        "catalog_entry_count": report["catalog_entry_count"],
        "covered_entry_count": report["covered_entry_count"],
        "uncovered_entry_count": report["uncovered_entry_count"],
        "covered_pct": report["covered_pct"],
        "coverage_sources": report["coverage_sources"],
        "categories": categories,
        "modules": modules,
    }


def main():
    parser = make_parser()
    args = parser.parse_args()

    try:
        report = build_serum_vst2_host_coverage_report(binary_path=args.binary)
    except Exception as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        sys.exit(1)

    if args.category:
        category = args.category.strip()
        filtered_entries = [entry for entry in report["entries"] if entry["category"] == category]
        report = {
            **report,
            "entries": filtered_entries,
            "categories": {category: report["categories"].get(category, {
                "total": 0,
                "covered": 0,
                "uncovered": 0,
                "covered_pct": 0.0,
                "covered_labels": [],
                "uncovered_labels": [],
            })},
            "modules": {
                name: summary
                for name, summary in report.get("modules", {}).items()
                if any(entry["module"] == name for entry in filtered_entries)
            },
        }

    if args.module:
        module = args.module.strip()
        filtered_entries = [entry for entry in report["entries"] if entry["module"] == module]
        report = {
            **report,
            "entries": filtered_entries,
            "modules": {module: report.get("modules", {}).get(module, {
                "manual_section": "",
                "total": 0,
                "covered": 0,
                "uncovered": 0,
                "covered_pct": 0.0,
                "covered_labels": [],
                "uncovered_labels": [],
            })},
            "categories": {
                name: summary
                for name, summary in report["categories"].items()
                if any(entry["category"] == name for entry in filtered_entries)
            },
        }

    if args.summary_only:
        report = _trim_summary(report, args.limit_uncovered)

    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
