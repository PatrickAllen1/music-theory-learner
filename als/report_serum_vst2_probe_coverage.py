#!/usr/bin/env python3
"""
report_serum_vst2_probe_coverage.py

Cross-reference the deferred manual Serum VST2 probe manifest against the
discovered host control catalog and the current parser coverage report.

This answers:
- which uncovered host modules are already targeted by the manual probe pack
- which are only partially targeted
- which still have no obvious manual probe

Examples:
    python3 als/report_serum_vst2_probe_coverage.py --summary-only
    python3 als/report_serum_vst2_probe_coverage.py --module fx_eq
    python3 als/report_serum_vst2_probe_coverage.py --status none
    python3 als/report_serum_vst2_probe_coverage.py --manifest als/serum-vst2-manual-probes.json --manifest als/serum-vst2-expansion-probes.json --summary-only
    python3 als/report_serum_vst2_probe_coverage.py --manifest als/serum-vst2-manual-probes.json --manifest als/serum-vst2-expansion-probes.json --manifest als/serum-vst2-phase3-probes.json --summary-only
"""

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

try:
    from parse_serum import build_serum_vst2_host_coverage_report, extract_serum_vst2_host_param_catalog
except ModuleNotFoundError:
    from .parse_serum import build_serum_vst2_host_coverage_report, extract_serum_vst2_host_param_catalog


DEFAULT_MANIFEST = Path("als/serum-vst2-manual-probes.json")


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Report how deferred manual probes cover uncovered Serum VST2 host modules.")
    parser.add_argument(
        "--manifest",
        action="append",
        default=[],
        help="Path to a manual probe manifest JSON. Pass multiple times to report combined coverage.",
    )
    parser.add_argument("--summary-only", action="store_true", help="Only print top-level totals and per-module summaries")
    parser.add_argument("--module", help="Restrict output to one module, e.g. fx_eq or matrix_curve")
    parser.add_argument(
        "--status",
        choices=["full", "partial", "none"],
        help="Restrict output to modules with one probe status",
    )
    return parser


def _normalize_label(label: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", label.lower())


def _load_manifest(path: Path) -> dict:
    return json.loads(path.read_text())


def _build_label_index(catalog: dict) -> dict[str, list[dict]]:
    by_normalized = defaultdict(list)
    for entry in catalog["entries"]:
        by_normalized[_normalize_label(entry["label"])].append(entry)
    return by_normalized


def _match_host_entries(labels: list[str], label_index: dict[str, list[dict]]) -> list[dict]:
    matches = []
    seen = set()
    for label in labels:
        normalized = _normalize_label(label)
        for entry in label_index.get(normalized, []):
            key = (entry["module"], entry["label"])
            if key in seen:
                continue
            seen.add(key)
            matches.append(entry)
    return matches


def _build_probe_rows(manifest: dict, label_index: dict[str, list[dict]]) -> list[dict]:
    rows = []
    for checkpoint in manifest["checkpoints"]:
        for probe in checkpoint["probes"]:
            matched_entries = _match_host_entries(probe.get("candidate_host_labels", []), label_index)
            rows.append({
                "checkpoint_id": checkpoint["id"],
                "checkpoint_title": checkpoint["title"],
                "probe_id": probe["id"],
                "probe_label": probe["label"],
                "candidate_host_labels": probe.get("candidate_host_labels", []),
                "matched_labels": [entry["label"] for entry in matched_entries],
                "matched_modules": sorted({entry["module"] for entry in matched_entries}),
                "candidate_slot_windows": probe.get("candidate_slot_windows", []),
                "recommended_preset": probe.get("recommended_preset", ""),
            })
    return rows


def _classify_module_probe_status(uncovered_labels: list[str], probe_labels: set[str]) -> str:
    if not probe_labels:
        return "none"
    if all(label in probe_labels for label in uncovered_labels):
        return "full"
    return "partial"


def _load_manifests(paths: list[Path]) -> list[dict]:
    return [_load_manifest(path) for path in paths]


def build_probe_coverage_report(manifest_paths: list[Path]) -> dict:
    manifests = _load_manifests(manifest_paths)
    catalog = extract_serum_vst2_host_param_catalog()
    coverage = build_serum_vst2_host_coverage_report()
    label_index = _build_label_index(catalog)
    probe_rows = []
    for manifest_path, manifest in zip(manifest_paths, manifests):
        rows = _build_probe_rows(manifest, label_index)
        for row in rows:
            row["manifest_path"] = str(manifest_path)
        probe_rows.extend(rows)

    probe_rows_by_module = defaultdict(list)
    for row in probe_rows:
        for module in row["matched_modules"]:
            probe_rows_by_module[module].append(row)

    module_summaries = {}
    for module, summary in coverage["modules"].items():
        if summary["uncovered"] <= 0:
            continue
        module_probe_rows = probe_rows_by_module.get(module, [])
        probe_labels = {label for row in module_probe_rows for label in row["matched_labels"]}
        status = _classify_module_probe_status(summary["uncovered_labels"], probe_labels)
        module_summaries[module] = {
            "manual_section": summary["manual_section"],
            "total": summary["total"],
            "covered": summary["covered"],
            "uncovered": summary["uncovered"],
            "covered_pct": summary["covered_pct"],
            "uncovered_labels": summary["uncovered_labels"],
            "probe_status": status,
            "probe_ids": [row["probe_id"] for row in module_probe_rows],
            "probe_checkpoints": sorted({row["checkpoint_id"] for row in module_probe_rows}),
            "probe_labels": sorted(probe_labels),
        }

    status_counts = defaultdict(int)
    for summary in module_summaries.values():
        status_counts[summary["probe_status"]] += 1

    return {
        "manifest_paths": [str(path) for path in manifest_paths],
        "probe_count": len(probe_rows),
        "uncovered_module_count": len(module_summaries),
        "status_counts": dict(status_counts),
        "probe_rows": probe_rows,
        "modules": module_summaries,
    }


def _trim_summary(report: dict) -> dict:
    modules = {}
    for name, summary in sorted(report["modules"].items()):
        modules[name] = {
            "manual_section": summary["manual_section"],
            "uncovered": summary["uncovered"],
            "probe_status": summary["probe_status"],
            "probe_ids": summary["probe_ids"],
            "probe_checkpoints": summary["probe_checkpoints"],
            "probe_labels": summary["probe_labels"][:8],
        }
    return {
        "manifest_paths": report["manifest_paths"],
        "probe_count": report["probe_count"],
        "uncovered_module_count": report["uncovered_module_count"],
        "status_counts": report["status_counts"],
        "modules": modules,
    }


def main():
    parser = make_parser()
    args = parser.parse_args()

    try:
        manifest_args = [Path(path) for path in args.manifest] if args.manifest else [DEFAULT_MANIFEST]
        report = build_probe_coverage_report(manifest_args)
    except Exception as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        sys.exit(1)

    if args.module:
        module = args.module.strip()
        report["modules"] = {
            module: report["modules"].get(module, {
                "manual_section": "",
                "total": 0,
                "covered": 0,
                "uncovered": 0,
                "covered_pct": 0.0,
                "uncovered_labels": [],
                "probe_status": "none",
                "probe_ids": [],
                "probe_checkpoints": [],
                "probe_labels": [],
            })
        }

    if args.status:
        report["modules"] = {
            name: summary
            for name, summary in report["modules"].items()
            if summary["probe_status"] == args.status
        }

    if args.summary_only:
        report = _trim_summary(report)

    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
