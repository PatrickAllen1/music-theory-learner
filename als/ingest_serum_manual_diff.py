#!/usr/bin/env python3
"""
ingest_serum_manual_diff.py

Sweep a folder of deferred-manual Serum .fxp before/after pairs, compute raw
slot diffs, and summarize the observed clusters against the expected probe
windows from serum-vst2-manual-probes.json.

Pair naming convention inside --pairs-dir:
    <probe_id>.before.fxp
    <probe_id>.after.fxp

Examples:
    python3 als/ingest_serum_manual_diff.py --pairs-dir /tmp/serum-probes
    python3 als/ingest_serum_manual_diff.py --pairs-dir /tmp/serum-probes --probe note_latch
    python3 als/ingest_serum_manual_diff.py --pairs-dir /tmp/serum-probes --manifest als/serum-vst2-manual-probes.json --manifest als/serum-vst2-expansion-probes.json
"""

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path

from parse_serum import (
    cluster_vst2_slot_rows,
    diff_vst2_float_slots,
    extract_serum_vst2_host_param_catalog,
    parse_fxp_file,
)


def parse_window(window: str) -> tuple[int, int]:
    if "-" not in window:
        index = int(window)
        return index, index
    start, end = window.split("-", 1)
    return int(start), int(end)


DEFAULT_MANIFEST = Path("als/serum-vst2-manual-probes.json")


def load_manifest(path: Path) -> dict:
    return json.loads(path.read_text())


def _normalize_label(label: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", label.lower())


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


def iter_probes(manifest_path: Path, manifest: dict):
    for checkpoint in manifest["checkpoints"]:
        for probe in checkpoint["probes"]:
            yield checkpoint, probe, manifest_path


def build_probe_lookup(manifest_paths: list[Path]) -> dict:
    lookup = {}
    duplicates = []
    for manifest_path in manifest_paths:
        manifest = load_manifest(manifest_path)
        for checkpoint, probe, source_manifest_path in iter_probes(manifest_path, manifest):
            probe_id = probe["id"]
            if probe_id in lookup:
                duplicates.append({
                    "probe_id": probe_id,
                    "first_manifest": str(lookup[probe_id][2]),
                    "second_manifest": str(source_manifest_path),
                })
                continue
            lookup[probe_id] = (checkpoint, probe, source_manifest_path)
    if duplicates:
        raise ValueError(f"duplicate probe ids across manifests: {duplicates}")
    return lookup


def overlap_with_expected(clusters: list[dict], windows: list[str]) -> list[dict]:
    parsed_windows = [parse_window(window) for window in windows]
    overlaps = []
    for cluster in clusters:
        start = cluster["start_index"]
        end = cluster["end_index"]
        hit_windows = []
        for raw_window, (w_start, w_end) in zip(windows, parsed_windows):
            if end < w_start or start > w_end:
                continue
            hit_windows.append(raw_window)
        overlaps.append({
            "cluster": f"{start}-{end}",
            "matched_windows": hit_windows,
        })
    return overlaps


def summarise_probe_result(
    checkpoint: dict,
    probe: dict,
    source_manifest_path: Path,
    before_path: Path,
    after_path: Path,
    slots: int,
    threshold: float,
    label_index: dict[str, list[dict]],
) -> dict:
    before = parse_fxp_file(before_path)
    after = parse_fxp_file(after_path)
    changes = diff_vst2_float_slots(
        before["_decompressed_data"],
        after["_decompressed_data"],
        count=slots,
        threshold=threshold,
    )
    clusters = cluster_vst2_slot_rows(changes, max_index_gap=0)
    matched_entries = _match_host_entries(probe.get("candidate_host_labels", []), label_index)
    return {
        "checkpoint": checkpoint["id"],
        "checkpoint_title": checkpoint["title"],
        "manifest_path": str(source_manifest_path),
        "probe_id": probe["id"],
        "label": probe["label"],
        "before_path": str(before_path),
        "after_path": str(after_path),
        "diff_count": len(changes),
        "clusters": clusters,
        "expected_windows": probe.get("candidate_slot_windows", []),
        "window_overlaps": overlap_with_expected(clusters, probe.get("candidate_slot_windows", [])),
        "candidate_host_labels": probe.get("candidate_host_labels", []),
        "matched_host_labels": [entry["label"] for entry in matched_entries],
        "matched_modules": sorted({entry["module"] for entry in matched_entries}),
    }


def main():
    parser = argparse.ArgumentParser(description="Ingest deferred manual Serum VST2 .fxp diffs.")
    parser.add_argument("--pairs-dir", required=True, help="Directory containing <probe_id>.before.fxp / <probe_id>.after.fxp pairs")
    parser.add_argument(
        "--manifest",
        action="append",
        default=[],
        help="Probe manifest JSON path. Pass multiple times to ingest across primary + phase-2 probe packs.",
    )
    parser.add_argument("--probe", action="append", default=[], help="Restrict to one or more probe ids")
    parser.add_argument("--slots", type=int, default=180, help="How many float slots to diff")
    parser.add_argument("--threshold", type=float, default=0.01, help="Minimum delta threshold")
    args = parser.parse_args()

    catalog = extract_serum_vst2_host_param_catalog()
    label_index = _build_label_index(catalog)
    manifest_paths = [Path(path) for path in args.manifest] if args.manifest else [DEFAULT_MANIFEST]
    lookup = build_probe_lookup(manifest_paths)
    pairs_dir = Path(args.pairs_dir)
    selected_probe_ids = args.probe or sorted(lookup.keys())

    results = []
    missing = []
    for probe_id in selected_probe_ids:
        if probe_id not in lookup:
            missing.append({"probe_id": probe_id, "reason": "unknown probe id"})
            continue
        checkpoint, probe, source_manifest_path = lookup[probe_id]
        before_path = pairs_dir / f"{probe_id}.before.fxp"
        after_path = pairs_dir / f"{probe_id}.after.fxp"
        if not before_path.exists() or not after_path.exists():
            missing.append({
                "probe_id": probe_id,
                "manifest_path": str(source_manifest_path),
                "reason": "missing pair",
                "expected_before": str(before_path),
                "expected_after": str(after_path),
            })
            continue
        results.append(
            summarise_probe_result(
                checkpoint,
                probe,
                source_manifest_path,
                before_path,
                after_path,
                slots=args.slots,
                threshold=args.threshold,
                label_index=label_index,
            )
        )

    print(json.dumps({
        "pairs_dir": str(pairs_dir),
        "manifest_paths": [str(path) for path in manifest_paths],
        "results": results,
        "missing": missing,
    }, indent=2))


if __name__ == "__main__":
    main()
