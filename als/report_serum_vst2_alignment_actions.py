#!/usr/bin/env python3
"""
report_serum_vst2_alignment_actions.py

Generate prioritized parser-alignment actions from a postdiff workpack.

Examples:
    python3 als/report_serum_vst2_alignment_actions.py --mapping-json /tmp/serum-postdiff/mapping.json --mapping-coverage-json /tmp/serum-postdiff/mapping_coverage.json --gaps-json /tmp/serum-postdiff/gaps.json
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate prioritized Serum VST2 parser-alignment actions.")
    parser.add_argument("--mapping-json", required=True, help="Path to mapping.json.")
    parser.add_argument("--mapping-coverage-json", required=True, help="Path to mapping_coverage.json.")
    parser.add_argument("--gaps-json", required=True, help="Path to gaps.json.")
    parser.add_argument("--summary-only", action="store_true", help="Only print counts and ordered actions.")
    return parser


def build_alignment_actions(mapping: dict, coverage: dict, gaps: dict) -> dict:
    work_items = {row["implementation_target"]: row for row in mapping.get("parser_work_items", [])}
    gap_index = defaultdict(list)
    for item in gaps.get("unresolved", []):
        for module in item.get("matched_modules", []):
            gap_index[module].append(item)

    actions = []
    for row in coverage.get("alignment_queue", []):
        target_row = None
        for work_item in work_items.values():
            if row["module"] in work_item.get("modules", []):
                target_row = work_item
                break
        actions.append({
            "module": row["module"],
            "manual_section": row["manual_section"],
            "priority_score": row["evidenced_uncovered_count"] * 100 - row["dark_uncovered_count"],
            "evidenced_uncovered_count": row["evidenced_uncovered_count"],
            "dark_uncovered_count": row["dark_uncovered_count"],
            "implementation_target": (target_row or {}).get("implementation_target", "als/parse_serum.py"),
            "probe_ids": row["probe_ids"],
            "clusters": row["clusters"],
            "windows": row["windows"],
            "labels": row.get("evidenced_uncovered_labels", []),
            "supporting_gap_items": gap_index.get(row["module"], []),
        })

    actions.sort(key=lambda item: (-item["priority_score"], item["implementation_target"], item["module"]))

    targets = defaultdict(lambda: {"modules": [], "probe_ids": set()})
    for action in actions:
        row = targets[action["implementation_target"]]
        row["modules"].append(action["module"])
        row["probe_ids"].update(action["probe_ids"])

    return {
        "action_count": len(actions),
        "implementation_targets": [
            {
                "implementation_target": target,
                "module_count": len(row["modules"]),
                "modules": row["modules"],
                "probe_ids": sorted(row["probe_ids"]),
            }
            for target, row in sorted(targets.items())
        ],
        "actions": actions,
    }


def main() -> None:
    parser = make_parser()
    args = parser.parse_args()
    mapping = json.loads(Path(args.mapping_json).read_text())
    coverage = json.loads(Path(args.mapping_coverage_json).read_text())
    gaps = json.loads(Path(args.gaps_json).read_text())
    report = build_alignment_actions(mapping, coverage, gaps)
    if args.summary_only:
        report = {
            "action_count": report["action_count"],
            "implementation_targets": report["implementation_targets"],
            "actions": [
                {
                    "module": item["module"],
                    "implementation_target": item["implementation_target"],
                    "priority_score": item["priority_score"],
                    "probe_ids": item["probe_ids"],
                }
                for item in report["actions"]
            ],
        }
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
