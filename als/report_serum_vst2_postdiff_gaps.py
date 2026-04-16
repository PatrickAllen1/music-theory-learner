#!/usr/bin/env python3
"""
report_serum_vst2_postdiff_gaps.py

Summarize what remains unresolved after promoting a Serum VST2 post-diff run.

Examples:
    python3 als/report_serum_vst2_postdiff_gaps.py --mapping-json /tmp/serum-postdiff/mapping.json
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

try:
    from render_serum_manual_bundle import DEFAULT_MANIFESTS, load_bundle
except ModuleNotFoundError:
    from .render_serum_manual_bundle import DEFAULT_MANIFESTS, load_bundle


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Report unresolved gaps after a Serum VST2 post-diff promotion.")
    parser.add_argument("--mapping-json", required=True, help="Path to mapping.json from run_serum_vst2_postdiff.py.")
    parser.add_argument(
        "--manifest",
        action="append",
        default=[],
        help="Optional manifest override. Pass multiple times to replace the default A-H bundle.",
    )
    parser.add_argument("--summary-only", action="store_true", help="Only print top-level counts and per-checkpoint statuses.")
    return parser


def build_gap_report(mapping: dict, bundle: dict) -> dict:
    promoted_probe_ids = {row["probe_id"] for row in mapping.get("promoted", [])}
    follow_up_probe_ids = {row["probe_id"] for row in mapping.get("follow_up_queue", [])}
    missing_probe_ids = {row["probe_id"] for row in mapping.get("missing", [])}

    checkpoint_rows = defaultdict(lambda: {
        "probe_ids": [],
        "promoted": [],
        "follow_up": [],
        "missing": [],
    })
    unresolved = []

    for probe in bundle["probes"]:
        checkpoint = checkpoint_rows[probe["checkpoint_id"]]
        checkpoint["probe_ids"].append(probe["probe_id"])
        if probe["probe_id"] in promoted_probe_ids:
            checkpoint["promoted"].append(probe["probe_id"])
        elif probe["probe_id"] in follow_up_probe_ids:
            checkpoint["follow_up"].append(probe["probe_id"])
            unresolved.append({
                "probe_id": probe["probe_id"],
                "checkpoint_id": probe["checkpoint_id"],
                "reason": "follow_up",
            })
        else:
            checkpoint["missing"].append(probe["probe_id"])
            unresolved.append({
                "probe_id": probe["probe_id"],
                "checkpoint_id": probe["checkpoint_id"],
                "reason": "missing" if probe["probe_id"] in missing_probe_ids else "not_promoted",
            })

    checkpoints = {}
    for checkpoint_id, row in sorted(checkpoint_rows.items()):
        total = len(row["probe_ids"])
        status = "resolved" if len(row["promoted"]) == total else "partial"
        checkpoints[checkpoint_id] = {
            "probe_count": total,
            "promoted_count": len(row["promoted"]),
            "follow_up_count": len(row["follow_up"]),
            "missing_count": len(row["missing"]),
            "status": status,
            "promoted": sorted(row["promoted"]),
            "follow_up": sorted(row["follow_up"]),
            "missing": sorted(row["missing"]),
        }

    return {
        "mapping_json": mapping.get("pairs_dir"),
        "accepted_statuses": mapping.get("accepted_statuses", []),
        "probe_count": bundle["probe_count"],
        "promoted_count": len(promoted_probe_ids),
        "follow_up_count": len(follow_up_probe_ids),
        "missing_count": len(missing_probe_ids),
        "checkpoint_status": checkpoints,
        "unresolved": unresolved,
    }


def main() -> None:
    parser = make_parser()
    args = parser.parse_args()
    manifest_paths = [Path(path) for path in args.manifest] if args.manifest else DEFAULT_MANIFESTS
    mapping = json.loads(Path(args.mapping_json).read_text())
    bundle = load_bundle(manifest_paths)
    report = build_gap_report(mapping, bundle)
    if args.summary_only:
        report = {
            "probe_count": report["probe_count"],
            "promoted_count": report["promoted_count"],
            "follow_up_count": report["follow_up_count"],
            "missing_count": report["missing_count"],
            "checkpoint_status": report["checkpoint_status"],
        }
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
