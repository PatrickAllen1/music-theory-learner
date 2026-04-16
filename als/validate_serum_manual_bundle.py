#!/usr/bin/env python3
"""
validate_serum_manual_bundle.py

Validate the current deferred Serum manual bundle end to end.

Checks:
- manifest JSON parses
- every preset path referenced by the manifests exists
- the merged probe coverage report is fully covered
- the bundle renderer can load the manifests
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from render_serum_manual_bundle import DEFAULT_MANIFESTS, load_bundle
from report_serum_vst2_probe_coverage import build_probe_coverage_report


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


def main() -> None:
    manifest_paths = list(DEFAULT_MANIFESTS)

    try:
        for manifest_path in manifest_paths:
            json.loads(manifest_path.read_text())
        bundle = load_bundle(manifest_paths)
        coverage = build_probe_coverage_report(manifest_paths)
        missing_preset_paths = _collect_missing_preset_paths(manifest_paths)
    except Exception as exc:
        print(json.dumps({"ok": False, "error": str(exc)}), file=sys.stderr)
        sys.exit(1)

    partial_or_none = {
        module: summary["probe_status"]
        for module, summary in coverage["modules"].items()
        if summary["probe_status"] != "full"
    }

    result = {
        "ok": not missing_preset_paths and not partial_or_none,
        "manifest_count": len(manifest_paths),
        "probe_count": bundle["probe_count"],
        "coverage_status_counts": coverage["status_counts"],
        "missing_preset_paths": missing_preset_paths,
        "non_full_modules": partial_or_none,
    }
    print(json.dumps(result, indent=2))
    if not result["ok"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
