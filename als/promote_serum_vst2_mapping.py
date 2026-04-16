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

try:
    from serum_vst2_label_overrides import canonicalize_label_iter
    from parse_serum import build_serum_vst2_host_coverage_report
    from serum_vst2_label_overrides import apply_serum_vst2_label_overrides
except ModuleNotFoundError:
    from .serum_vst2_label_overrides import canonicalize_label_iter
    from .parse_serum import build_serum_vst2_host_coverage_report
    from .serum_vst2_label_overrides import apply_serum_vst2_label_overrides


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


def _derive_implementation_targets(row: dict) -> list[str]:
    targets = []
    if row.get("matched_modules"):
        targets.append("als/parse_serum.py")

    raw_labels = row.get("candidate_host_labels", [])
    canonical_labels = canonicalize_label_iter(raw_labels)
    if raw_labels and canonical_labels != raw_labels:
        targets.append("als/serum_vst2_label_overrides.py")

    if not targets:
        targets.append("als/parse_serum.py")
    return sorted(dict.fromkeys(targets))


def build_mapping(ingest: dict, accepted_statuses: set[str]) -> dict:
    promoted = []
    cluster_index = defaultdict(list)
    window_index = defaultdict(list)
    implementation_targets = []
    coverage = apply_serum_vst2_label_overrides(build_serum_vst2_host_coverage_report())
    module_sections = {
        module: summary["manual_section"]
        for module, summary in coverage["modules"].items()
    }
    parser_work_items = defaultdict(lambda: {
        "implementation_target": "",
        "manual_sections": set(),
        "modules": set(),
        "probe_ids": set(),
        "labels": set(),
        "windows": set(),
        "clusters": set(),
    })

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
            "expected_windows": result.get("expected_windows", []),
        }
        row["implementation_targets"] = _derive_implementation_targets(row)
        row["manual_sections"] = sorted({module_sections.get(module, "") for module in row["matched_modules"] if module_sections.get(module, "")})
        promoted.append(row)
        if row["primary_cluster"]:
            cluster_index[row["primary_cluster"]].append(row["probe_id"])
        for window in row["matched_windows"]:
            window_index[window].append(row["probe_id"])
        implementation_targets.append({
            "probe_id": row["probe_id"],
            "label": row["label"],
            "checkpoint": row["checkpoint"],
            "status": row["status"],
            "matched_modules": row["matched_modules"],
            "candidate_host_labels": row["candidate_host_labels"],
            "matched_host_labels": row["matched_host_labels"],
            "expected_windows": row["expected_windows"],
            "primary_cluster": row["primary_cluster"],
            "manual_sections": row["manual_sections"],
            "implementation_targets": row["implementation_targets"],
        })
        for target in row["implementation_targets"]:
            item = parser_work_items[target]
            item["implementation_target"] = target
            item["manual_sections"].update(row["manual_sections"])
            item["modules"].update(row["matched_modules"])
            item["probe_ids"].add(row["probe_id"])
            item["labels"].update(row["matched_host_labels"] or row["candidate_host_labels"])
            item["windows"].update(row["expected_windows"])
            if row["primary_cluster"]:
                item["clusters"].add(row["primary_cluster"])

    return {
        "pairs_dir": ingest.get("pairs_dir"),
        "manifest_paths": ingest.get("manifest_paths", []),
        "accepted_statuses": sorted(accepted_statuses),
        "promoted_count": len(promoted),
        "promoted": promoted,
        "implementation_targets": implementation_targets,
        "parser_work_items": [
            {
                "implementation_target": target,
                "manual_sections": sorted(item["manual_sections"]),
                "modules": sorted(item["modules"]),
                "probe_ids": sorted(item["probe_ids"]),
                "labels": sorted(item["labels"]),
                "windows": sorted(item["windows"]),
                "clusters": sorted(item["clusters"]),
            }
            for target, item in sorted(parser_work_items.items())
        ],
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
