#!/usr/bin/env python3
"""
compare_serum_vst2_postdiff_runs.py

Compare two Serum VST2 postdiff workpacks.

Examples:
    python3 als/compare_serum_vst2_postdiff_runs.py --base-dir /tmp/serum-postdiff-old --head-dir /tmp/serum-postdiff-new
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    from report_serum_vst2_mapping_coverage import build_mapping_coverage_report
except ModuleNotFoundError:
    from .report_serum_vst2_mapping_coverage import build_mapping_coverage_report


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Compare two Serum VST2 postdiff workpacks.")
    parser.add_argument("--base-dir", required=True, help="Older postdiff directory.")
    parser.add_argument("--head-dir", required=True, help="Newer postdiff directory.")
    parser.add_argument("--summary-only", action="store_true", help="Only print counts and newly gained items.")
    return parser


def _load(path: Path, name: str) -> dict:
    return json.loads((path / name).read_text())


def _load_optional(path: Path, name: str, default: dict) -> tuple[dict, bool]:
    file_path = path / name
    if not file_path.exists():
        return default, False
    return json.loads(file_path.read_text()), True


def _coverage_ready_modules(coverage: dict) -> set[str]:
    return {row["module"] for row in coverage.get("alignment_queue", [])}


def _missing_probe_ids(mapping: dict, gaps: dict) -> set[str]:
    missing = {row["probe_id"] for row in mapping.get("missing", [])}
    for item in gaps.get("unresolved", []):
        probe_id = item.get("probe_id")
        if probe_id:
            missing.add(probe_id)
    return missing


def build_comparison(base_dir: Path, head_dir: Path) -> dict:
    base_mapping = _load(base_dir, "mapping.json")
    head_mapping = _load(head_dir, "mapping.json")
    base_gaps = _load(base_dir, "gaps.json")
    head_gaps = _load(head_dir, "gaps.json")
    base_coverage, base_has_coverage = _load_optional(base_dir, "mapping_coverage.json", {})
    head_coverage, head_has_coverage = _load_optional(head_dir, "mapping_coverage.json", {})
    if not base_has_coverage:
        base_coverage = build_mapping_coverage_report(base_mapping)
    if not head_has_coverage:
        head_coverage = build_mapping_coverage_report(head_mapping)

    base_promoted = {row["probe_id"] for row in base_mapping.get("promoted", [])}
    head_promoted = {row["probe_id"] for row in head_mapping.get("promoted", [])}
    base_ready = _coverage_ready_modules(base_coverage)
    head_ready = _coverage_ready_modules(head_coverage)
    base_missing = _missing_probe_ids(base_mapping, base_gaps)
    head_missing = _missing_probe_ids(head_mapping, head_gaps)

    return {
        "base_dir": str(base_dir),
        "head_dir": str(head_dir),
        "promoted_probe_delta": len(head_promoted) - len(base_promoted),
        "ready_module_delta": len(head_ready) - len(base_ready),
        "missing_probe_delta": len(head_missing) - len(base_missing),
        "newly_promoted_probes": sorted(head_promoted - base_promoted),
        "newly_ready_modules": sorted(head_ready - base_ready),
        "resolved_missing_probes": sorted(base_missing - head_missing),
        "base": {
            "has_mapping_coverage": base_has_coverage,
            "promoted_count": len(base_promoted),
            "ready_module_count": base_coverage.get("ready_module_count", 0),
            "missing_count": len(base_missing),
            "checkpoint_status": base_gaps.get("checkpoint_status", {}),
        },
        "head": {
            "has_mapping_coverage": head_has_coverage,
            "promoted_count": len(head_promoted),
            "ready_module_count": head_coverage.get("ready_module_count", 0),
            "missing_count": len(head_missing),
            "checkpoint_status": head_gaps.get("checkpoint_status", {}),
        },
    }


def main() -> None:
    parser = make_parser()
    args = parser.parse_args()
    report = build_comparison(Path(args.base_dir), Path(args.head_dir))
    if args.summary_only:
        report = {
            "promoted_probe_delta": report["promoted_probe_delta"],
            "ready_module_delta": report["ready_module_delta"],
            "missing_probe_delta": report["missing_probe_delta"],
            "newly_promoted_probes": report["newly_promoted_probes"],
            "newly_ready_modules": report["newly_ready_modules"],
            "resolved_missing_probes": report["resolved_missing_probes"],
        }
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
