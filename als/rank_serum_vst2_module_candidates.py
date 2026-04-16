#!/usr/bin/env python3
"""
rank_serum_vst2_module_candidates.py
Rank unknown VST2 slot windows by how well they match a named Serum host module.

This does NOT prove mappings. It narrows the next controlled-diff target by
comparing a module's expected control kinds (continuous / toggle / enum) with
the observed behavior of unknown VST2 slots across a preset corpus.

Examples:
    python3 als/rank_serum_vst2_module_candidates.py --module global_portamento
    python3 als/rank_serum_vst2_module_candidates.py --module fx_filter --top 20
    python3 als/rank_serum_vst2_module_candidates.py --module global_portamento --window-size 4
"""

import argparse
import json
import statistics
from collections import Counter
from pathlib import Path

from analyze_serum_vst2_slots import DEFAULT_BANKS, summarise_slot
from parse_serum import (
    SERUM_V2_PARAM_OFFSET,
    build_serum_vst2_module_signature,
    cluster_vst2_slot_rows,
    extract_vst2_float_slots,
    parse_fxp_file,
)


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Rank unknown VST2 slot windows against a target Serum module.")
    parser.add_argument("--module", required=True, help="Target module, e.g. global_portamento, fx_filter, fx_delay")
    parser.add_argument(
        "--bank",
        choices=["garage", "speed_garage", "all"],
        default="all",
        help="Which preset bank(s) to profile",
    )
    parser.add_argument("--slots", type=int, default=180, help="How many VST2 float slots to inspect")
    parser.add_argument("--threshold", type=float, default=0.01, help="Minimum spread required for a slot to count as varying")
    parser.add_argument("--top", type=int, default=12, help="How many candidate windows to return")
    parser.add_argument(
        "--window-size",
        type=int,
        default=0,
        help="Override the default window size derived from the target module entry count",
    )
    return parser


def _preset_paths(bank: str) -> list[Path]:
    if bank == "all":
        paths = []
        for folder in DEFAULT_BANKS.values():
            paths.extend(sorted(folder.glob("*.fxp")))
        return paths
    return sorted(DEFAULT_BANKS[bank].glob("*.fxp"))


def _load_unknown_slot_rows(bank: str, slots: int, threshold: float) -> list[dict]:
    preset_paths = _preset_paths(bank)
    parsed_items = [parse_fxp_file(path) for path in preset_paths]
    slot_lists = [
        extract_vst2_float_slots(parsed["_decompressed_data"], start_offset=SERUM_V2_PARAM_OFFSET, count=slots)
        for parsed in parsed_items
    ]
    max_len = min(len(items) for items in slot_lists)
    rows = []
    for idx in range(max_len):
        values = [items[idx]["raw"] for items in slot_lists]
        row = summarise_slot(idx, values)
        if "known_param" in row:
            continue
        if row["spread"] < threshold:
            continue
        rows.append(row)
    return rows


def _iter_contiguous_windows(rows: list[dict], window_size: int) -> list[list[dict]]:
    if window_size <= 0:
        return []
    rows = sorted(rows, key=lambda row: row["index"])
    windows = []
    for i in range(len(rows) - window_size + 1):
        window = rows[i:i + window_size]
        indexes = [row["index"] for row in window]
        if indexes[-1] - indexes[0] != window_size - 1:
            continue
        if any((b - a) != 1 for a, b in zip(indexes, indexes[1:])):
            continue
        windows.append(window)
    return windows


def _normalize_slot_kind(kind: str) -> str:
    if kind == "boolean":
        return "boolean_or_toggle"
    if kind in {"discrete", "enum_like"}:
        return "discrete_or_enum"
    return kind


def _score_window(window: list[dict], target_signature: dict) -> dict:
    target_counts = Counter(target_signature["control_kind_counts"])
    raw_window_counts = Counter(row["kind"] for row in window)
    window_counts = Counter(_normalize_slot_kind(row["kind"]) for row in window)
    target_len = target_signature["entry_count"] or len(window)

    exact_overlap = sum(min(target_counts[k], window_counts.get(k, 0)) for k in target_counts)
    kind_match_score = exact_overlap / max(target_len, 1)

    # Favor windows with high-activity slots, but keep kind-match dominant.
    avg_spread = statistics.fmean(row["spread"] for row in window)
    spread_score = avg_spread
    final_score = round(kind_match_score * 0.85 + spread_score * 0.15, 6)

    mismatches = {
        kind: window_counts.get(kind, 0) - target_counts.get(kind, 0)
        for kind in sorted(set(target_counts) | set(window_counts))
        if window_counts.get(kind, 0) != target_counts.get(kind, 0)
    }

    return {
        "score": final_score,
        "kind_match_score": round(kind_match_score, 6),
        "avg_spread": round(avg_spread, 6),
        "raw_window_kind_counts": dict(raw_window_counts),
        "window_kind_counts": dict(window_counts),
        "target_kind_counts": dict(target_counts),
        "kind_mismatches": mismatches,
    }


def rank_module_candidates(module: str, bank: str, slots: int, threshold: float, top: int, window_size: int) -> dict:
    target_signature = build_serum_vst2_module_signature(module)
    if target_signature["entry_count"] == 0:
        raise ValueError(f"unknown or empty module: {module}")

    if window_size <= 0:
        window_size = target_signature["entry_count"]

    rows = _load_unknown_slot_rows(bank=bank, slots=slots, threshold=threshold)
    windows = _iter_contiguous_windows(rows, window_size=window_size)
    ranked = []
    for window in windows:
        scored = _score_window(window, target_signature)
        ranked.append({
            "start_index": window[0]["index"],
            "end_index": window[-1]["index"],
            "indices": [row["index"] for row in window],
            "rows": [
                {
                    "index": row["index"],
                    "kind": row["kind"],
                    "spread": row["spread"],
                    "distinct_rounded_values": row["distinct_rounded_values"],
                    "zero_fraction": row["zero_fraction"],
                    "one_fraction": row["one_fraction"],
                }
                for row in window
            ],
            **scored,
        })

    ranked.sort(key=lambda item: (item["score"], item["kind_match_score"], item["avg_spread"], -item["start_index"]), reverse=True)
    top_ranked = ranked[:top]

    cluster_summaries = []
    clusters = cluster_vst2_slot_rows(rows, max_index_gap=1)
    for cluster in clusters:
        cluster_rows = [row for row in rows if cluster["start_index"] <= row["index"] <= cluster["end_index"]]
        cluster_counts = Counter(_normalize_slot_kind(row["kind"]) for row in cluster_rows)
        overlap = sum(min(cluster_counts[k], target_signature["control_kind_counts"].get(k, 0)) for k in target_signature["control_kind_counts"])
        cluster_summaries.append({
            "start_index": cluster["start_index"],
            "end_index": cluster["end_index"],
            "count": cluster["count"],
            "kind_counts": dict(cluster_counts),
            "signature_overlap": overlap,
        })

    cluster_summaries.sort(key=lambda item: (item["signature_overlap"], -item["start_index"]), reverse=True)

    return {
        "module": module,
        "manual_section": target_signature["manual_section"],
        "target_entry_count": target_signature["entry_count"],
        "target_labels": target_signature["labels"],
        "target_kind_counts": target_signature["control_kind_counts"],
        "bank": bank,
        "slots_profiled": slots,
        "threshold": threshold,
        "candidate_window_size": window_size,
        "top_windows": top_ranked,
        "clusters": cluster_summaries,
        "note": "These are behavior-based candidates only; controlled Serum save-diffs are still required to prove mappings.",
    }


def main():
    parser = make_parser()
    args = parser.parse_args()
    result = rank_module_candidates(
        module=args.module,
        bank=args.bank,
        slots=args.slots,
        threshold=args.threshold,
        top=args.top,
        window_size=args.window_size,
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
