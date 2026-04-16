#!/usr/bin/env python3
"""
report_serum_vst2_mapping_coverage.py

Compare a promoted Serum VST2 mapping artifact against current parser coverage.

Examples:
    python3 als/report_serum_vst2_mapping_coverage.py --mapping-json /tmp/serum-postdiff/mapping.json
    python3 als/report_serum_vst2_mapping_coverage.py --mapping-json /tmp/serum-postdiff/mapping.json --summary-only
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

try:
    from parse_serum import build_serum_vst2_host_coverage_report
    from serum_vst2_label_overrides import apply_serum_vst2_label_overrides, canonicalize_label_iter
except ModuleNotFoundError:
    from .parse_serum import build_serum_vst2_host_coverage_report
    from .serum_vst2_label_overrides import apply_serum_vst2_label_overrides, canonicalize_label_iter


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Report how a promoted mapping artifact covers the remaining Serum VST2 host surface.")
    parser.add_argument("--mapping-json", required=True, help="Path to mapping.json from run_serum_vst2_postdiff.py.")
    parser.add_argument("--summary-only", action="store_true", help="Only print top-level counts and module summaries.")
    parser.add_argument("--module", help="Restrict output to one module, e.g. fx_delay or matrix_curve.")
    return parser


def build_mapping_coverage_report(mapping: dict) -> dict:
    coverage = apply_serum_vst2_label_overrides(build_serum_vst2_host_coverage_report())

    evidence_by_module = defaultdict(lambda: {
        "labels": set(),
        "probe_ids": set(),
        "clusters": set(),
        "windows": set(),
    })

    for row in mapping.get("promoted", []):
        labels = canonicalize_label_iter(row.get("matched_host_labels", []) or row.get("candidate_host_labels", []))
        for module in row.get("matched_modules", []):
            evidence = evidence_by_module[module]
            evidence["labels"].update(labels)
            evidence["probe_ids"].add(row["probe_id"])
            if row.get("primary_cluster"):
                evidence["clusters"].add(row["primary_cluster"])
            evidence["windows"].update(row.get("matched_windows", []))

    module_rows = {}
    ready_modules = []
    dark_modules = []
    evidenced_label_count = 0

    for module, summary in sorted(coverage["modules"].items()):
        if summary["uncovered"] <= 0:
            continue
        evidence = evidence_by_module.get(module, {"labels": set(), "probe_ids": set(), "clusters": set(), "windows": set()})
        evidenced_uncovered = sorted(label for label in summary["uncovered_labels"] if label in evidence["labels"])
        still_dark = sorted(label for label in summary["uncovered_labels"] if label not in evidence["labels"])
        evidenced_label_count += len(evidenced_uncovered)
        status = "ready_for_alignment" if evidenced_uncovered else "still_dark"
        row = {
            "manual_section": summary["manual_section"],
            "parser_covered": summary["covered"],
            "parser_uncovered": summary["uncovered"],
            "evidenced_uncovered_count": len(evidenced_uncovered),
            "dark_uncovered_count": len(still_dark),
            "status": status,
            "evidenced_uncovered_labels": evidenced_uncovered,
            "dark_uncovered_labels": still_dark,
            "probe_ids": sorted(evidence["probe_ids"]),
            "clusters": sorted(evidence["clusters"]),
            "windows": sorted(evidence["windows"]),
        }
        module_rows[module] = row
        if evidenced_uncovered:
            ready_modules.append(module)
        else:
            dark_modules.append(module)

    alignment_queue = sorted(
        (
            {
                "module": module,
                "manual_section": row["manual_section"],
                "evidenced_uncovered_count": row["evidenced_uncovered_count"],
                "dark_uncovered_count": row["dark_uncovered_count"],
                "probe_ids": row["probe_ids"],
                "clusters": row["clusters"],
                "windows": row["windows"],
            }
            for module, row in module_rows.items()
            if row["evidenced_uncovered_count"] > 0
        ),
        key=lambda item: (-item["evidenced_uncovered_count"], item["dark_uncovered_count"], item["module"]),
    )

    return {
        "mapping_json": mapping.get("pairs_dir"),
        "promoted_probe_count": len(mapping.get("promoted", [])),
        "module_count": len(module_rows),
        "ready_module_count": len(ready_modules),
        "still_dark_module_count": len(dark_modules),
        "evidenced_uncovered_label_count": evidenced_label_count,
        "alignment_queue": alignment_queue,
        "modules": module_rows,
    }


def main() -> None:
    parser = make_parser()
    args = parser.parse_args()
    mapping = json.loads(Path(args.mapping_json).read_text())
    report = build_mapping_coverage_report(mapping)
    if args.module:
        module = args.module.strip()
        report["modules"] = {module: report["modules"].get(module, {})}
        report["alignment_queue"] = [row for row in report["alignment_queue"] if row["module"] == module]
    if args.summary_only:
        report = {
            "promoted_probe_count": report["promoted_probe_count"],
            "module_count": report["module_count"],
            "ready_module_count": report["ready_module_count"],
            "still_dark_module_count": report["still_dark_module_count"],
            "evidenced_uncovered_label_count": report["evidenced_uncovered_label_count"],
            "alignment_queue": report["alignment_queue"],
            "modules": {
                module: {
                    "status": row["status"],
                    "evidenced_uncovered_count": row["evidenced_uncovered_count"],
                    "dark_uncovered_count": row["dark_uncovered_count"],
                    "probe_ids": row["probe_ids"],
                }
                for module, row in report["modules"].items()
            },
        }
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
