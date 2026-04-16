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

try:
    from parse_serum import SERUM_VST2_PLUGIN_BINARY_PATH, build_serum_vst2_host_coverage_report
    from rank_serum_vst2_module_candidates import rank_target_candidates
except ModuleNotFoundError:
    from .parse_serum import SERUM_VST2_PLUGIN_BINARY_PATH, build_serum_vst2_host_coverage_report
    from .rank_serum_vst2_module_candidates import rank_target_candidates


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
    parser.add_argument(
        "--include-module-candidates",
        action="store_true",
        help="Augment module summaries with best current candidate windows from the corpus ranker",
    )
    parser.add_argument(
        "--candidate-bank",
        choices=["garage", "speed_garage", "all"],
        default="all",
        help="Which preset bank(s) to use for --include-module-candidates",
    )
    parser.add_argument(
        "--candidate-top",
        type=int,
        default=2,
        help="How many candidate windows to retain per module when using --include-module-candidates",
    )
    parser.add_argument(
        "--exclude-range",
        action="append",
        default=[],
        help="Exclude candidate windows overlapping a slot range like 154-163. May be passed multiple times.",
    )
    return parser


def _build_candidate_window_summary(module: str, bank: str, top: int, exclude_ranges: list[str]) -> dict:
    try:
        ranked = rank_target_candidates(
            target=module,
            target_type="module",
            bank=bank,
            slots=180,
            threshold=0.01,
            top=top,
            window_size=0,
            exclude_ranges=[tuple(int(part) for part in item.split("-", 1)) for item in exclude_ranges],
        )
    except Exception as exc:
        return {"error": str(exc)}

    return {
        "bank": ranked["bank"],
        "candidate_window_size": ranked["candidate_window_size"],
        "top_windows": [
            {
                "range": f"{window['start_index']}-{window['end_index']}",
                "score": window["score"],
                "kind_match_score": window["kind_match_score"],
            }
            for window in ranked.get("top_windows", [])
        ],
        "top_cluster_ranges": [
            f"{cluster['start_index']}-{cluster['end_index']}"
            for cluster in ranked.get("clusters", [])[:top]
        ],
    }


def _trim_summary(report: dict, limit_uncovered: int, include_module_candidates: bool, candidate_bank: str, candidate_top: int, exclude_ranges: list[str]) -> dict:
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
        module_summary = {
            "manual_section": summary["manual_section"],
            "total": summary["total"],
            "covered": summary["covered"],
            "uncovered": summary["uncovered"],
            "covered_pct": summary["covered_pct"],
            "covered_labels": summary["covered_labels"],
            "uncovered_labels": summary["uncovered_labels"][:limit_uncovered],
        }
        if include_module_candidates and summary["uncovered"] > 0:
            module_summary["candidate_windows"] = _build_candidate_window_summary(
                module=name,
                bank=candidate_bank,
                top=candidate_top,
                exclude_ranges=exclude_ranges,
            )
        modules[name] = module_summary

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
        report = _trim_summary(
            report,
            args.limit_uncovered,
            args.include_module_candidates,
            args.candidate_bank,
            args.candidate_top,
            args.exclude_range,
        )

    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
