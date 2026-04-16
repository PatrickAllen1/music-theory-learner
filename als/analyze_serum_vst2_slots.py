#!/usr/bin/env python3
"""
analyze_serum_vst2_slots.py
Profile VST2 float-slot behavior across a corpus of Serum .fxp presets.

This helps reverse-engineering by classifying slot behavior:
- constant / mostly constant
- boolean-like
- discrete / enum-like
- continuous

Examples:
    python3 als/analyze_serum_vst2_slots.py --summary-only
    python3 als/analyze_serum_vst2_slots.py --unknown-only --top 80
    python3 als/analyze_serum_vst2_slots.py --bank garage
"""

import argparse
import json
import math
import statistics
from collections import Counter
from pathlib import Path

from parse_serum import (
    SERUM_VST2_PARAM_BY_INDEX,
    SERUM_VST2_PARAMS,
    SERUM_V2_PARAM_OFFSET,
    cluster_vst2_slot_rows,
    extract_vst2_float_slots,
    parse_fxp_file,
)

DEFAULT_BANKS = {
    "garage": Path("/Library/Audio/Presets/Xfer Records/Serum 2 Presets/Presets/S1 Presets/Garage"),
    "speed_garage": Path("/Library/Audio/Presets/Xfer Records/Serum 2 Presets/Presets/S1 Presets/Speed Garage"),
}


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Profile VST2 float-slot behavior across a Serum preset corpus.")
    parser.add_argument(
        "--bank",
        choices=["garage", "speed_garage", "all"],
        default="all",
        help="Which preset bank(s) to profile",
    )
    parser.add_argument(
        "--slots",
        type=int,
        default=180,
        help="How many float slots to inspect from the VST2 state block",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.01,
        help="Minimum spread required for a slot to count as varying",
    )
    parser.add_argument(
        "--top",
        type=int,
        default=120,
        help="Maximum number of slot summaries to print when not using --summary-only",
    )
    parser.add_argument(
        "--unknown-only",
        action="store_true",
        help="Hide slots already mapped in the current parser",
    )
    parser.add_argument(
        "--summary-only",
        action="store_true",
        help="Only print top-level stats and cluster summaries",
    )
    return parser


def _preset_paths(bank: str) -> list[Path]:
    if bank == "all":
        paths = []
        for folder in DEFAULT_BANKS.values():
            paths.extend(sorted(folder.glob("*.fxp")))
        return paths
    return sorted(DEFAULT_BANKS[bank].glob("*.fxp"))


def _rounded_counter(values: list[float], precision: int = 4) -> Counter:
    return Counter(round(v, precision) for v in values if math.isfinite(v))


def infer_slot_kind(values: list[float]) -> str:
    rounded = sorted(set(round(v, 4) for v in values if math.isfinite(v)))
    if not rounded:
        return "unknown"
    if len(rounded) == 1:
        return "constant"
    if all(val in (0.0, 1.0) for val in rounded):
        return "boolean"
    if len(rounded) <= 4:
        return "enum_like"
    if len(rounded) <= 12:
        return "discrete"
    return "continuous"


def summarise_slot(index: int, values: list[float]) -> dict:
    counts = _rounded_counter(values)
    common = counts.most_common(6)
    min_val = min(values)
    max_val = max(values)
    spread = max_val - min_val
    row = {
        "index": index,
        "sample_count": len(values),
        "min": round(min_val, 6),
        "max": round(max_val, 6),
        "spread": round(spread, 6),
        "mean": round(statistics.fmean(values), 6),
        "kind": infer_slot_kind(values),
        "distinct_rounded_values": len(counts),
        "most_common_values": [
            {"value": value, "count": count}
            for value, count in common
        ],
        "zero_fraction": round(sum(1 for v in values if abs(v) < 1e-6) / len(values), 4),
        "one_fraction": round(sum(1 for v in values if abs(v - 1.0) < 1e-6) / len(values), 4),
        "half_fraction": round(sum(1 for v in values if abs(v - 0.5) < 1e-6) / len(values), 4),
        "varying": spread >= 0.01,
    }

    meta = SERUM_VST2_PARAM_BY_INDEX.get(index)
    if meta:
        row["known_param"] = meta["key"]
        row["label"] = meta["label"]
        row["confidence"] = meta["confidence"]
    return row


def build_cluster_summaries(slot_rows: list[dict], threshold: float) -> list[dict]:
    varying_rows = [row for row in slot_rows if row["spread"] >= threshold]
    base_clusters = cluster_vst2_slot_rows(varying_rows, max_index_gap=1)
    by_index = {row["index"]: row for row in slot_rows}
    cluster_summaries = []

    for cluster in base_clusters:
        rows = [by_index[idx] for idx in cluster["indices"]]
        kind_counts = Counter(row["kind"] for row in rows)
        summary = {
            **cluster,
            "known_slot_count": sum(1 for row in rows if "known_param" in row),
            "unknown_slot_count": sum(1 for row in rows if "known_param" not in row),
            "kind_counts": dict(kind_counts),
            "avg_spread": round(statistics.fmean(row["spread"] for row in rows), 6),
        }
        cluster_summaries.append(summary)

    return cluster_summaries


def main():
    parser = make_parser()
    args = parser.parse_args()

    preset_paths = _preset_paths(args.bank)
    parsed_items = [parse_fxp_file(path) for path in preset_paths]
    slot_lists = [
        extract_vst2_float_slots(parsed["_decompressed_data"], start_offset=SERUM_V2_PARAM_OFFSET, count=args.slots)
        for parsed in parsed_items
    ]

    max_len = min(len(slots) for slots in slot_lists)
    slot_rows = []
    for idx in range(max_len):
        values = [slots[idx]["raw"] for slots in slot_lists]
        row = summarise_slot(idx, values)
        slot_rows.append(row)

    if args.unknown_only:
        slot_rows = [row for row in slot_rows if "known_param" not in row]

    cluster_summaries = build_cluster_summaries(slot_rows, threshold=args.threshold)
    summary = {
        "bank": args.bank,
        "preset_count": len(parsed_items),
        "slot_count": len(slot_rows),
        "threshold": args.threshold,
        "known_slot_rows": sum(1 for row in slot_rows if "known_param" in row),
        "unknown_slot_rows": sum(1 for row in slot_rows if "known_param" not in row),
        "varying_slot_rows": sum(1 for row in slot_rows if row["spread"] >= args.threshold),
        "clusters": cluster_summaries,
        "kind_counts": dict(Counter(row["kind"] for row in slot_rows)),
    }

    if args.summary_only:
        print(json.dumps(summary, indent=2))
        return

    ranked_rows = sorted(
        slot_rows,
        key=lambda row: (row["spread"], row["distinct_rounded_values"], row["index"]),
        reverse=True,
    )[:args.top]
    print(json.dumps({
        **summary,
        "slots": ranked_rows,
    }, indent=2))


if __name__ == "__main__":
    main()
