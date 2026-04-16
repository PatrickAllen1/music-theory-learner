#!/usr/bin/env python3
"""
report_serum_vst2_partial_gaps.py

Explain why remaining Serum VST2 host modules are still only partially covered
by the deferred manual probe manifests.

Examples:
    python3 als/report_serum_vst2_partial_gaps.py
    python3 als/report_serum_vst2_partial_gaps.py --module fx_delay
    python3 als/report_serum_vst2_partial_gaps.py --manifest als/serum-vst2-manual-probes.json --manifest als/serum-vst2-expansion-probes.json --manifest als/serum-vst2-phase3-probes.json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

try:
    from parse_serum import extract_serum_vst2_host_param_catalog
    from report_serum_vst2_probe_coverage import build_probe_coverage_report
except ModuleNotFoundError:
    from .parse_serum import extract_serum_vst2_host_param_catalog
    from .report_serum_vst2_probe_coverage import build_probe_coverage_report


DEFAULT_MANIFESTS = [
    Path("als/serum-vst2-manual-probes.json"),
    Path("als/serum-vst2-expansion-probes.json"),
    Path("als/serum-vst2-phase3-probes.json"),
    Path("als/serum-vst2-phase4-probes.json"),
]


def _normalize_label(label: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", label.lower())


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Audit why Serum VST2 probe coverage remains partial.")
    parser.add_argument(
        "--manifest",
        action="append",
        default=[],
        help="Path to a manual probe manifest JSON. Pass multiple times to inspect a combined bundle.",
    )
    parser.add_argument("--module", help="Restrict output to one partial module")
    return parser


def build_partial_gap_report(manifest_paths: list[Path]) -> dict:
    report = build_probe_coverage_report(manifest_paths)
    catalog = extract_serum_vst2_host_param_catalog()

    catalog_by_norm: dict[str, list[str]] = {}
    for entry in catalog["entries"]:
        normalized = _normalize_label(entry["label"])
        catalog_by_norm.setdefault(normalized, []).append(entry["label"])

    module_gap_details = {}
    for module, summary in report["modules"].items():
        if summary["probe_status"] != "partial":
            continue
        probe_labels = summary["probe_labels"]
        probe_norms = {_normalize_label(label) for label in probe_labels}
        missing_rows = []
        for missing_label in summary["uncovered_labels"]:
            normalized = _normalize_label(missing_label)
            if normalized in probe_norms:
                reason = "alias_collision"
            elif normalized in catalog_by_norm:
                reason = "real_missing_surface"
            else:
                reason = "catalog_residue"
            missing_rows.append({
                "label": missing_label,
                "normalized": normalized,
                "reason": reason,
                "catalog_matches": catalog_by_norm.get(normalized, [])[:8],
            })
        module_gap_details[module] = {
            "manual_section": summary["manual_section"],
            "uncovered": summary["uncovered"],
            "probe_ids": summary["probe_ids"],
            "reason_counts": {
                "alias_collision": sum(row["reason"] == "alias_collision" for row in missing_rows),
                "real_missing_surface": sum(row["reason"] == "real_missing_surface" for row in missing_rows),
                "catalog_residue": sum(row["reason"] == "catalog_residue" for row in missing_rows),
            },
            "missing": missing_rows,
        }

    return {
        "manifest_paths": [str(path) for path in manifest_paths],
        "partial_module_count": len(module_gap_details),
        "modules": module_gap_details,
    }


def main() -> None:
    parser = make_parser()
    args = parser.parse_args()
    manifest_paths = [Path(path) for path in args.manifest] if args.manifest else DEFAULT_MANIFESTS

    try:
        report = build_partial_gap_report(manifest_paths)
    except Exception as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        sys.exit(1)

    if args.module:
        report["modules"] = {
            args.module: report["modules"].get(args.module, {
                "manual_section": "",
                "uncovered": 0,
                "probe_ids": [],
                "reason_counts": {
                    "alias_collision": 0,
                    "real_missing_surface": 0,
                    "catalog_residue": 0,
                },
                "missing": [],
            })
        }

    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
