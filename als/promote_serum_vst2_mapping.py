#!/usr/bin/env python3
"""
promote_serum_vst2_mapping.py

Promote a Serum VST2 ingest artifact into a smaller reusable mapping artifact.

Examples:
    python3 als/promote_serum_vst2_mapping.py --ingest-json /tmp/serum-postdiff/ingest.json
    python3 als/promote_serum_vst2_mapping.py --ingest-json /tmp/serum-postdiff/ingest.json --out /tmp/serum-postdiff/mapping.json
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Promote a Serum VST2 ingest artifact into a mapping artifact.")
    parser.add_argument("--ingest-json", required=True, help="Path to ingest.json from run_serum_vst2_postdiff.py or ingest_serum_manual_diff.py.")
    parser.add_argument("--out", help="Optional output path for the promoted mapping artifact.")
    parser.add_argument(
        "--accept-status",
        action="append",
        default=["confirmed", "expected_hit"],
        help="Consensus outcome statuses to promote into the mapping artifact.",
    )
    return parser


def build_mapping(ingest: dict, accepted_statuses: set[str]) -> dict:
    promoted = []
    cluster_index = defaultdict(list)
    window_index = defaultdict(list)

    for result in ingest.get("results", []):
        outcome = result.get("outcome", {})
        if outcome.get("status") not in accepted_statuses:
            continue
        row = {
            "probe_id": result["probe_id"],
            "label": result["label"],
            "checkpoint": result["checkpoint"],
            "status": outcome.get("status"),
            "primary_cluster": outcome.get("primary_cluster"),
            "matched_windows": outcome.get("matched_windows", []),
            "matched_modules": result.get("matched_modules", []),
            "candidate_host_labels": result.get("candidate_host_labels", []),
            "matched_host_labels": result.get("matched_host_labels", []),
        }
        promoted.append(row)
        if row["primary_cluster"]:
            cluster_index[row["primary_cluster"]].append(row["probe_id"])
        for window in row["matched_windows"]:
            window_index[window].append(row["probe_id"])

    return {
        "pairs_dir": ingest.get("pairs_dir"),
        "manifest_paths": ingest.get("manifest_paths", []),
        "accepted_statuses": sorted(accepted_statuses),
        "promoted_count": len(promoted),
        "promoted": promoted,
        "cluster_index": {key: sorted(values) for key, values in sorted(cluster_index.items())},
        "window_index": {key: sorted(values) for key, values in sorted(window_index.items())},
        "follow_up_queue": ingest.get("consensus", {}).get("follow_up_queue", []),
        "missing": ingest.get("missing", []),
    }


def main() -> None:
    parser = make_parser()
    args = parser.parse_args()
    ingest = json.loads(Path(args.ingest_json).read_text())
    mapping = build_mapping(ingest, set(args.accept_status))
    payload = json.dumps(mapping, indent=2)
    if args.out:
        Path(args.out).write_text(payload + "\n")
    print(payload)


if __name__ == "__main__":
    main()
