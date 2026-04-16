#!/usr/bin/env python3
"""
validate_serum_manual_bundle.py

Validate the current deferred Serum manual bundle end to end.

Checks:
- manifest JSON parses
- every preset path referenced by the manifests exists
- the merged probe coverage report is fully covered
- the bundle renderer can load the manifests
- optional: a pairs directory contains every expected <probe_id>.before/.after file
"""

from __future__ import annotations

import json
import sys
from argparse import ArgumentParser
from pathlib import Path

try:
    from render_serum_manual_bundle import DEFAULT_MANIFESTS, filter_bundle, load_bundle
    from report_serum_vst2_probe_coverage import build_probe_coverage_report
except ModuleNotFoundError:
    from .render_serum_manual_bundle import DEFAULT_MANIFESTS, filter_bundle, load_bundle
    from .report_serum_vst2_probe_coverage import build_probe_coverage_report


def _collect_missing_preset_paths(manifest_paths: list[Path]) -> list[dict]:
    missing = []
    for manifest_path in manifest_paths:
        manifest = json.loads(manifest_path.read_text())
        for checkpoint in manifest["checkpoints"]:
            for probe in checkpoint["probes"]:
                recommended = probe.get("recommended_preset")
                if recommended and not Path(recommended).exists():
                    missing.append({
                        "manifest_path": str(manifest_path),
                        "probe_id": probe["id"],
                        "field": "recommended_preset",
                        "path": recommended,
                    })
                for index, preset_path in enumerate(probe.get("fallback_presets", []), 1):
                    if preset_path and not Path(preset_path).exists():
                        missing.append({
                            "manifest_path": str(manifest_path),
                            "probe_id": probe["id"],
                            "field": f"fallback_presets[{index - 1}]",
                            "path": preset_path,
                        })
    return missing


def _collect_pairs_status(bundle: dict, pairs_dir: Path) -> dict:
    expected = {}
    by_checkpoint = {}
    for probe in bundle["probes"]:
        before_path = pairs_dir / probe["before_filename"]
        after_path = pairs_dir / probe["after_filename"]
        pair = {
            "probe_id": probe["probe_id"],
            "checkpoint_id": probe["checkpoint_id"],
            "label": probe["label"],
            "before_filename": probe["before_filename"],
            "after_filename": probe["after_filename"],
            "before_exists": before_path.exists(),
            "after_exists": after_path.exists(),
        }
        pair["complete"] = pair["before_exists"] and pair["after_exists"]
        expected[pair["before_filename"]] = pair["probe_id"]
        expected[pair["after_filename"]] = pair["probe_id"]
        by_checkpoint.setdefault(probe["checkpoint_id"], []).append(pair)

    stray_files = []
    if pairs_dir.exists():
        for path in sorted(pairs_dir.iterdir()):
            if not path.is_file():
                continue
            if path.name not in expected:
                stray_files.append(path.name)

    checkpoint_summary = {}
    missing_pairs = []
    complete_probe_count = 0
    for checkpoint_id, pairs in by_checkpoint.items():
        complete = sum(1 for pair in pairs if pair["complete"])
        complete_probe_count += complete
        missing = [pair for pair in pairs if not pair["complete"]]
        missing_pairs.extend(missing)
        checkpoint_summary[checkpoint_id] = {
            "complete_probe_count": complete,
            "probe_count": len(pairs),
            "missing_pairs": missing,
        }

    return {
        "pairs_dir": str(pairs_dir),
        "probe_count": len(bundle["probes"]),
        "complete_probe_count": complete_probe_count,
        "missing_probe_count": len(bundle["probes"]) - complete_probe_count,
        "checkpoint_summary": checkpoint_summary,
        "missing_pairs": missing_pairs,
        "stray_files": stray_files,
    }


def main() -> None:
    parser = ArgumentParser(description="Validate the Serum VST2 manual bundle and optional pairs directory.")
    parser.add_argument(
        "--pairs-dir",
        help="Optional directory expected to contain <probe_id>.before.fxp / <probe_id>.after.fxp pairs.",
    )
    parser.add_argument("--checkpoint", action="append", default=[], help="Restrict validation to one or more checkpoint ids.")
    parser.add_argument("--probe", action="append", default=[], help="Restrict validation to one or more probe ids.")
    args = parser.parse_args()

    manifest_paths = list(DEFAULT_MANIFESTS)

    try:
        for manifest_path in manifest_paths:
            json.loads(manifest_path.read_text())
        bundle = load_bundle(manifest_paths)
        if args.checkpoint or args.probe:
            bundle = filter_bundle(bundle, checkpoint_ids=args.checkpoint, probe_ids=args.probe)
        coverage = build_probe_coverage_report(manifest_paths)
        missing_preset_paths = _collect_missing_preset_paths(manifest_paths)
        pairs_status = _collect_pairs_status(bundle, Path(args.pairs_dir)) if args.pairs_dir else None
    except Exception as exc:
        print(json.dumps({"ok": False, "error": str(exc)}), file=sys.stderr)
        sys.exit(1)

    partial_or_none = {
        module: summary["probe_status"]
        for module, summary in coverage["modules"].items()
        if summary["probe_status"] != "full"
    }

    result = {
        "ok": not missing_preset_paths and not partial_or_none and not (pairs_status and pairs_status["missing_probe_count"]),
        "manifest_count": len(manifest_paths),
        "probe_count": bundle["probe_count"],
        "coverage_status_counts": coverage["status_counts"],
        "missing_preset_paths": missing_preset_paths,
        "non_full_modules": partial_or_none,
    }
    if pairs_status:
        result["pairs_status"] = pairs_status
    print(json.dumps(result, indent=2))
    if not result["ok"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
