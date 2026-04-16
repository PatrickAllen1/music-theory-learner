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
"""

import argparse
import json
from pathlib import Path

from parse_serum import cluster_vst2_slot_rows, diff_vst2_float_slots, parse_fxp_file


def parse_window(window: str) -> tuple[int, int]:
    if "-" not in window:
        index = int(window)
        return index, index
    start, end = window.split("-", 1)
    return int(start), int(end)


def load_manifest(path: Path) -> dict:
    return json.loads(path.read_text())


def iter_probes(manifest: dict):
    for checkpoint in manifest["checkpoints"]:
        for probe in checkpoint["probes"]:
            yield checkpoint, probe


def build_probe_lookup(manifest: dict) -> dict:
    return {probe["id"]: (checkpoint, probe) for checkpoint, probe in iter_probes(manifest)}


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


def summarise_probe_result(checkpoint: dict, probe: dict, before_path: Path, after_path: Path, slots: int, threshold: float) -> dict:
    before = parse_fxp_file(before_path)
    after = parse_fxp_file(after_path)
    changes = diff_vst2_float_slots(
        before["_decompressed_data"],
        after["_decompressed_data"],
        count=slots,
        threshold=threshold,
    )
    clusters = cluster_vst2_slot_rows(changes, max_index_gap=0)
    return {
        "checkpoint": checkpoint["id"],
        "checkpoint_title": checkpoint["title"],
        "probe_id": probe["id"],
        "label": probe["label"],
        "before_path": str(before_path),
        "after_path": str(after_path),
        "diff_count": len(changes),
        "clusters": clusters,
        "expected_windows": probe.get("candidate_slot_windows", []),
        "window_overlaps": overlap_with_expected(clusters, probe.get("candidate_slot_windows", [])),
        "candidate_host_labels": probe.get("candidate_host_labels", []),
    }


def main():
    parser = argparse.ArgumentParser(description="Ingest deferred manual Serum VST2 .fxp diffs.")
    parser.add_argument("--pairs-dir", required=True, help="Directory containing <probe_id>.before.fxp / <probe_id>.after.fxp pairs")
    parser.add_argument("--manifest", default="als/serum-vst2-manual-probes.json", help="Probe manifest JSON path")
    parser.add_argument("--probe", action="append", default=[], help="Restrict to one or more probe ids")
    parser.add_argument("--slots", type=int, default=180, help="How many float slots to diff")
    parser.add_argument("--threshold", type=float, default=0.01, help="Minimum delta threshold")
    args = parser.parse_args()

    manifest = load_manifest(Path(args.manifest))
    lookup = build_probe_lookup(manifest)
    pairs_dir = Path(args.pairs_dir)
    selected_probe_ids = args.probe or sorted(lookup.keys())

    results = []
    missing = []
    for probe_id in selected_probe_ids:
        if probe_id not in lookup:
            missing.append({"probe_id": probe_id, "reason": "unknown probe id"})
            continue
        checkpoint, probe = lookup[probe_id]
        before_path = pairs_dir / f"{probe_id}.before.fxp"
        after_path = pairs_dir / f"{probe_id}.after.fxp"
        if not before_path.exists() or not after_path.exists():
            missing.append({
                "probe_id": probe_id,
                "reason": "missing pair",
                "expected_before": str(before_path),
                "expected_after": str(after_path),
            })
            continue
        results.append(
            summarise_probe_result(
                checkpoint,
                probe,
                before_path,
                after_path,
                slots=args.slots,
                threshold=args.threshold,
            )
        )

    print(json.dumps({
        "pairs_dir": str(pairs_dir),
        "manifest": str(Path(args.manifest)),
        "results": results,
        "missing": missing,
    }, indent=2))


if __name__ == "__main__":
    main()
