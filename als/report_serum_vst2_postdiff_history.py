#!/usr/bin/env python3
"""
report_serum_vst2_postdiff_history.py

Summarize a sequence of Serum VST2 postdiff workpacks and their deltas.

Examples:
    python3 als/report_serum_vst2_postdiff_history.py --postdiff-dir /tmp/serum-postdiff-C --postdiff-dir /tmp/serum-postdiff-D
    python3 als/report_serum_vst2_postdiff_history.py --root-dir /tmp --pattern 'serum-postdiff*' --summary-only
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    from compare_serum_vst2_postdiff_runs import build_comparison
except ModuleNotFoundError:
    from .compare_serum_vst2_postdiff_runs import build_comparison


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Summarize a sequence of Serum VST2 postdiff workpacks.")
    parser.add_argument("--postdiff-dir", action="append", default=[], help="Explicit postdiff directory. Pass multiple times in order.")
    parser.add_argument("--root-dir", help="Optional root directory to scan for postdiff workpacks.")
    parser.add_argument("--pattern", default="serum-postdiff*", help="Glob pattern under --root-dir. Default: serum-postdiff*")
    parser.add_argument("--summary-only", action="store_true", help="Only print top-level counts and per-run summaries.")
    return parser


def _discover_dirs(args: argparse.Namespace) -> list[Path]:
    dirs = [Path(path) for path in args.postdiff_dir]
    if args.root_dir:
        root = Path(args.root_dir)
        discovered = sorted(path for path in root.glob(args.pattern) if path.is_dir())
        seen = {path.resolve() for path in dirs}
        for path in discovered:
            if path.resolve() not in seen:
                dirs.append(path)
    return [path for path in dirs if (path / "mapping.json").exists() and (path / "gaps.json").exists()]


def _load_counts(postdiff_dir: Path) -> dict:
    mapping = json.loads((postdiff_dir / "mapping.json").read_text())
    gaps = json.loads((postdiff_dir / "gaps.json").read_text())
    ready_module_count = 0
    coverage_path = postdiff_dir / "mapping_coverage.json"
    if coverage_path.exists():
        coverage = json.loads(coverage_path.read_text())
        ready_module_count = coverage.get("ready_module_count", 0)
    return {
        "postdiff_dir": str(postdiff_dir),
        "promoted_count": len(mapping.get("promoted", [])),
        "missing_count": len(mapping.get("missing", [])),
        "ready_module_count": ready_module_count,
        "checkpoint_status": gaps.get("checkpoint_status", {}),
        "has_mapping_coverage": coverage_path.exists(),
    }


def build_history(postdiff_dirs: list[Path]) -> dict:
    runs = [_load_counts(path) for path in postdiff_dirs]
    deltas = []
    for base_dir, head_dir in zip(postdiff_dirs, postdiff_dirs[1:]):
        deltas.append(build_comparison(base_dir, head_dir))
    return {
        "run_count": len(runs),
        "delta_count": len(deltas),
        "runs": runs,
        "deltas": deltas,
    }


def main() -> None:
    parser = make_parser()
    args = parser.parse_args()
    postdiff_dirs = _discover_dirs(args)
    report = build_history(postdiff_dirs)
    if args.summary_only:
        report = {
            "run_count": report["run_count"],
            "delta_count": report["delta_count"],
            "runs": [
                {
                    "postdiff_dir": item["postdiff_dir"],
                    "promoted_count": item["promoted_count"],
                    "missing_count": item["missing_count"],
                    "ready_module_count": item["ready_module_count"],
                    "has_mapping_coverage": item["has_mapping_coverage"],
                }
                for item in report["runs"]
            ],
            "deltas": [
                {
                    "base_dir": item["base_dir"],
                    "head_dir": item["head_dir"],
                    "promoted_probe_delta": item["promoted_probe_delta"],
                    "ready_module_delta": item["ready_module_delta"],
                    "missing_probe_delta": item["missing_probe_delta"],
                }
                for item in report["deltas"]
            ],
        }
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
