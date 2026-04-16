#!/usr/bin/env python3
"""
parse_serum_preset.py
Standalone Serum VST2 (.fxp) preset inspector built on the same parser used for
Serum chunks embedded in Ableton .als files.

Examples:
    python3 als/parse_serum_preset.py preset.fxp
    python3 als/parse_serum_preset.py preset.fxp --slots 160 --nonzero-only
    python3 als/parse_serum_preset.py --diff preset-a.fxp preset-b.fxp --slots 220
    python3 als/parse_serum_preset.py preset-a.fxp preset-b.fxp preset-c.fxp --varying --slots 220
"""

import argparse
import json
import math
import sys
from pathlib import Path

from parse_serum import (
    SERUM_V2_PARAM_OFFSET,
    cluster_vst2_slot_rows,
    diff_vst2_float_slots,
    extract_printable_strings,
    extract_vst2_float_slots,
    parse_fxp_file,
    summarise_instance,
)


def summarise_preset(parsed: dict) -> dict:
    summary = summarise_instance({
        "track": Path(parsed["path"]).stem,
        "plugin": parsed.get("header", {}).get("plugin_id", "Serum"),
        **parsed,
    })
    summary["path"] = parsed["path"]
    if "header" in parsed:
        summary["header"] = parsed["header"]
    return summary


def _is_effectively_zero(value: float, epsilon: float = 1e-6) -> bool:
    return math.isfinite(value) and abs(value) < epsilon


def build_slot_view(parsed: dict, count: int, nonzero_only: bool, start_offset: int) -> list[dict]:
    slots = extract_vst2_float_slots(parsed["_decompressed_data"], start_offset=start_offset, count=count)
    if nonzero_only:
        slots = [slot for slot in slots if not _is_effectively_zero(slot["raw"])]
    return slots


def build_varying_view(parsed_items: list[dict], count: int, threshold: float, nonzero_only: bool, start_offset: int) -> list[dict]:
    slot_lists = [
        extract_vst2_float_slots(p["_decompressed_data"], start_offset=start_offset, count=count)
        for p in parsed_items
    ]
    varying = []
    max_len = min(len(slots) for slots in slot_lists)

    for idx in range(max_len):
        values = [slots[idx]["raw"] for slots in slot_lists]
        lo = min(values)
        hi = max(values)
        if hi - lo < threshold:
            continue
        if nonzero_only and all(_is_effectively_zero(v) for v in values):
            continue

        base_slot = slot_lists[0][idx]
        row = {
            "index": base_slot["index"],
            "offset": base_slot["offset"],
            "values": {
                Path(p["path"]).name: round(values[i], 6)
                for i, p in enumerate(parsed_items)
            },
            "spread": round(hi - lo, 6),
        }
        for key in ("known_param", "label", "confidence"):
            if key in base_slot:
                row[key] = base_slot[key]
        varying.append(row)

    return varying


def _load_parsed(path_str: str) -> dict:
    path = Path(path_str).expanduser()
    if not path.exists():
        raise FileNotFoundError(path)
    return parse_fxp_file(path)


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Inspect standalone Serum VST2 .fxp preset files.")
    parser.add_argument("paths", nargs="*", help="Path(s) to .fxp preset files")
    parser.add_argument("--slots", type=int, default=0, help="Include raw float slots from the VST2 parameter block")
    parser.add_argument("--slot-offset", type=int, default=SERUM_V2_PARAM_OFFSET, help="Byte offset where float slot extraction starts")
    parser.add_argument("--cluster-gap", type=int, default=1, help="Maximum untouched slot gap allowed when clustering slot changes")
    parser.add_argument("--nonzero-only", action="store_true", help="Hide slots that are effectively zero")
    parser.add_argument("--strings", type=int, default=0, help="Include up to N printable ASCII strings from the decompressed chunk")
    parser.add_argument("--strings-min-length", type=int, default=4, help="Minimum printable string length for --strings")
    parser.add_argument("--strings-start", type=int, default=0, help="Start byte offset for --strings scan")
    parser.add_argument("--strings-end", type=int, default=0, help="End byte offset for --strings scan (0 means end of chunk)")
    parser.add_argument("--diff", action="store_true", help="Diff two presets instead of printing summaries")
    parser.add_argument("--varying", action="store_true", help="Across 2+ presets, show only slot indices whose values vary")
    parser.add_argument("--threshold", type=float, default=0.001, help="Minimum float delta for diff/varying views")
    return parser


def main():
    parser = make_parser()
    args = parser.parse_args()

    if not args.paths:
        parser.error("at least one preset path is required")

    if args.diff and len(args.paths) != 2:
        parser.error("--diff requires exactly two preset paths")

    try:
        parsed_items = [_load_parsed(path_str) for path_str in args.paths]
    except Exception as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        sys.exit(1)

    if args.diff:
        left, right = parsed_items
        diff_rows = diff_vst2_float_slots(
            left["_decompressed_data"],
            right["_decompressed_data"],
            start_offset=args.slot_offset,
            count=args.slots or 256,
            threshold=args.threshold,
        )
        output = {
            "left": summarise_preset(left),
            "right": summarise_preset(right),
            "diff": diff_rows,
            "diff_clusters": cluster_vst2_slot_rows(diff_rows, max_index_gap=args.cluster_gap),
        }
        output["left"].pop("_decompressed_data", None)
        output["right"].pop("_decompressed_data", None)
        print(json.dumps(output, indent=2))
        return

    if args.varying:
        if len(parsed_items) < 2:
            parser.error("--varying requires at least two preset paths")
        varying_rows = build_varying_view(
            parsed_items,
            count=args.slots or 256,
            threshold=args.threshold,
            nonzero_only=args.nonzero_only,
            start_offset=args.slot_offset,
        )
        output = {
            "presets": [summarise_preset(p) for p in parsed_items],
            "varying_slots": varying_rows,
            "varying_clusters": cluster_vst2_slot_rows(varying_rows, max_index_gap=args.cluster_gap),
        }
        for preset in output["presets"]:
            preset.pop("_decompressed_data", None)
        print(json.dumps(output, indent=2))
        return

    results = []
    for parsed in parsed_items:
        result = summarise_preset(parsed)
        result.pop("_decompressed_data", None)
        if args.slots:
            result["slots"] = build_slot_view(parsed, args.slots, args.nonzero_only, args.slot_offset)
        if args.strings:
            end_offset = args.strings_end or len(parsed["_decompressed_data"])
            result["strings"] = extract_printable_strings(
                parsed["_decompressed_data"],
                min_length=args.strings_min_length,
                start_offset=args.strings_start,
                end_offset=end_offset,
                max_results=args.strings,
            )
        results.append(result)

    print(json.dumps(results if len(results) > 1 else results[0], indent=2))


if __name__ == "__main__":
    main()
