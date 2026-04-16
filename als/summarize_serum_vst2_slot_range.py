#!/usr/bin/env python3
"""
summarize_serum_vst2_slot_range.py
Summarize a Serum VST2 slot range using existing corpus evidence.

This is a small inspection helper for reverse-engineering waves. It combines:
- per-slot prevalence and kind summaries from the current corpus
- module/family signature matching from the host catalog
- a few current hot-zone hints from prior evidence

Examples:
    python3 als/summarize_serum_vst2_slot_range.py --start 88 --end 96
    python3 als/summarize_serum_vst2_slot_range.py --start 154 --end 163 --top 5
    python3 als/summarize_serum_vst2_slot_range.py --start 121 --end 130 --bank garage --json
"""

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

try:
    from analyze_serum_vst2_slots import DEFAULT_BANKS, summarise_slot
    from parse_serum import (
        SERUM_V2_PARAM_OFFSET,
        cluster_vst2_slot_rows,
        extract_serum_vst2_host_param_catalog,
        extract_vst2_float_slots,
        parse_fxp_file,
    )
    from rank_serum_vst2_module_candidates import SYNTHETIC_FAMILY_FILTERS, rank_target_candidates
except ModuleNotFoundError:
    from .analyze_serum_vst2_slots import DEFAULT_BANKS, summarise_slot
    from .parse_serum import (
        SERUM_V2_PARAM_OFFSET,
        cluster_vst2_slot_rows,
        extract_serum_vst2_host_param_catalog,
        extract_vst2_float_slots,
        parse_fxp_file,
    )
    from .rank_serum_vst2_module_candidates import SYNTHETIC_FAMILY_FILTERS, rank_target_candidates


DEFAULT_HINT_RANGES = [
    {"range": (40, 44), "label": "mixed boolean strip around enable/voicing flags"},
    {"range": (88, 96), "label": "EQ / distortion / filter corridor"},
    {"range": (121, 132), "label": "delay / flanger / chorus / phaser corridor"},
    {"range": (137, 145), "label": "distortion / filter / EQ corridor"},
    {"range": (154, 163), "label": "FX enable block"},
    {"range": (166, 175), "label": "enum / discrete tail"},
]

FOCUSED_MODULES = {
    "global_master",
    "global_portamento",
    "global_pitch",
    "global_voicing",
    "filter_core",
    "filter_routing",
    "fx_distortion",
    "fx_flanger",
    "fx_phaser",
    "fx_chorus",
    "fx_delay",
    "fx_compressor",
    "fx_eq",
    "fx_filter",
    "fx_hyper_dimension",
    "fx_reverb",
    "matrix_depth",
    "matrix_output",
    "matrix_source",
    "matrix_aux_source",
    "matrix_destination",
    "matrix_curve",
    "osc_a",
    "osc_b",
    "osc_noise",
    "osc_sub",
}


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Summarize a Serum VST2 slot range from current corpus evidence.")
    parser.add_argument("--start", type=int, required=True, help="Start slot index, inclusive")
    parser.add_argument("--end", type=int, required=True, help="End slot index, inclusive")
    parser.add_argument(
        "--bank",
        choices=["garage", "speed_garage", "all"],
        default="all",
        help="Which preset bank(s) to profile",
    )
    parser.add_argument("--slots", type=int, default=180, help="How many VST2 float slots to inspect")
    parser.add_argument("--threshold", type=float, default=0.01, help="Minimum spread required for a slot to count as varying")
    parser.add_argument("--top", type=int, default=5, help="How many candidate targets to show")
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print structured JSON instead of the compact human-readable summary",
    )
    return parser


def _preset_paths(bank: str) -> list[Path]:
    if bank == "all":
        paths = []
        for folder in DEFAULT_BANKS.values():
            paths.extend(sorted(folder.glob("*.fxp")))
        return paths
    return sorted(DEFAULT_BANKS[bank].glob("*.fxp"))


def _load_slot_matrix(bank: str, slot_count: int) -> tuple[list[Path], list[list[float]]]:
    paths = _preset_paths(bank)
    matrix = []
    for path in paths:
        parsed = parse_fxp_file(path)
        slots = extract_vst2_float_slots(parsed["_decompressed_data"], start_offset=SERUM_V2_PARAM_OFFSET, count=slot_count)
        matrix.append([slot["raw"] for slot in slots])
    return paths, matrix


def _normalize_kind(kind: str) -> str:
    if kind == "boolean":
        return "boolean_or_toggle"
    if kind in {"discrete", "enum_like"}:
        return "discrete_or_enum"
    if kind == "constant":
        return "constant"
    return kind


def _range_distance(left_start: int, left_end: int, right_start: int, right_end: int) -> int:
    if left_end < right_start:
        return right_start - left_end - 1
    if right_end < left_start:
        return left_start - right_end - 1
    return 0


def _build_target_signatures() -> list[dict]:
    catalog = extract_serum_vst2_host_param_catalog()
    by_module: dict[str, list[dict]] = defaultdict(list)
    for entry in catalog["entries"]:
        by_module[entry["module"]].append(entry)

    signatures = []
    for module, entries in by_module.items():
        if module not in FOCUSED_MODULES:
            continue
        if not entries:
            continue
        signatures.append({
            "target": module,
            "target_type": "module",
            "entry_count": len(entries),
            "manual_section": entries[0]["manual_section"],
            "kind_counts": dict(Counter(entry["control_kind_hint"] for entry in entries)),
            "labels": [entry["label"] for entry in entries],
        })

    for family, predicate in SYNTHETIC_FAMILY_FILTERS.items():
        entries = [entry for entry in catalog["entries"] if predicate(entry)]
        if not entries:
            continue
        signatures.append({
            "target": family,
            "target_type": "family",
            "entry_count": len(entries),
            "manual_section": "Synthetic family",
            "kind_counts": dict(Counter(entry["control_kind_hint"] for entry in entries)),
            "labels": [entry["label"] for entry in entries],
        })

    return signatures


def _score_signature(range_rows: list[dict], signature: dict) -> dict:
    signal_rows = [row for row in range_rows if row["kind"] != "constant" and row["spread"] >= 0.01]
    if not signal_rows:
        signal_rows = [row for row in range_rows if row["kind"] != "constant"] or range_rows

    range_counts = Counter(_normalize_kind(row["kind"]) for row in signal_rows)
    target_counts = Counter(signature["kind_counts"])
    overlap = sum(min(range_counts[k], target_counts[k]) for k in set(range_counts) | set(target_counts))
    count_total = max(sum(range_counts.values()), sum(target_counts.values()), 1)
    kind_fit = overlap / count_total

    signal_len = len(signal_rows)
    target_len = signature["entry_count"]
    size_fit = 1.0 - abs(signal_len - target_len) / max(signal_len, target_len, 1)

    score = round(kind_fit * 0.75 + size_fit * 0.25, 6)
    return {
        "score": score,
        "kind_fit": round(kind_fit, 6),
        "size_fit": round(size_fit, 6),
        "signal_row_count": signal_len,
        "signal_kind_counts": dict(range_counts),
        "kind_overlap": overlap,
        "kind_mismatches": {
            kind: range_counts.get(kind, 0) - target_counts.get(kind, 0)
            for kind in sorted(set(range_counts) | set(target_counts))
            if range_counts.get(kind, 0) != target_counts.get(kind, 0)
        },
    }


def _build_range_rows(matrix: list[list[float]], start: int, end: int) -> list[dict]:
    rows = []
    for idx in range(start, end + 1):
        values = [preset[idx] for preset in matrix]
        rows.append(summarise_slot(idx, values))
    return rows


def summarize_slot_range(
    start: int,
    end: int,
    bank: str,
    slots: int,
    threshold: float,
    top: int,
) -> dict:
    if start > end:
        start, end = end, start

    paths, matrix = _load_slot_matrix(bank=bank, slot_count=slots)
    range_rows = _build_range_rows(matrix, start, end)
    varying_rows = [row for row in range_rows if row["spread"] >= threshold]
    cluster_rows = varying_rows or range_rows
    clusters = cluster_vst2_slot_rows(cluster_rows, max_index_gap=1)

    target_signatures = _build_target_signatures()
    ranked_targets = []
    for signature in target_signatures:
        scored = _score_signature(range_rows, signature)
        current_best = rank_target_candidates(
            target=signature["target"],
            target_type=signature["target_type"],
            bank=bank,
            slots=slots,
            threshold=threshold,
            top=1,
            window_size=0,
        )
        best_window = current_best["top_windows"][0] if current_best["top_windows"] else None
        if best_window:
            overlap = not (best_window["end_index"] < start or best_window["start_index"] > end)
            gap = _range_distance(start, end, best_window["start_index"], best_window["end_index"])
            scored["current_best_window"] = {
                "start_index": best_window["start_index"],
                "end_index": best_window["end_index"],
                "score": best_window["score"],
                "kind_match_score": best_window["kind_match_score"],
                "window_kind_counts": best_window["window_kind_counts"],
                "overlaps_range": overlap,
                "gap_to_range": gap,
            }
            scored["relevance_score"] = round(scored["score"] + (0.15 if overlap else -min(0.15, gap * 0.01)), 6)
        else:
            scored["current_best_window"] = None
            scored["relevance_score"] = scored["score"]
        ranked_targets.append({
            **signature,
            **scored,
        })
    ranked_targets.sort(key=lambda item: (item["relevance_score"], item["score"], item["kind_fit"], item["size_fit"]), reverse=True)
    enriched_targets = ranked_targets[:top]

    hint_matches = []
    for hint in DEFAULT_HINT_RANGES:
        hint_start, hint_end = hint["range"]
        gap = _range_distance(start, end, hint_start, hint_end)
        if gap <= 2:
            hint_matches.append({
                "range": [hint_start, hint_end],
                "label": hint["label"],
                "gap": gap,
            })

    return {
        "bank": bank,
        "preset_count": len(paths),
        "slots": slots,
        "threshold": threshold,
        "range": {"start": start, "end": end},
        "slot_rows": range_rows,
        "varying_slot_rows": len(varying_rows),
        "kind_counts": dict(Counter(row["kind"] for row in range_rows)),
        "varying_kind_counts": dict(Counter(row["kind"] for row in varying_rows)),
        "clusters": [
            {
                "start_index": cluster["start_index"],
                "end_index": cluster["end_index"],
                "count": cluster["count"],
                "kind_counts": dict(Counter(row["kind"] for row in cluster_rows if cluster["start_index"] <= row["index"] <= cluster["end_index"])),
            }
            for cluster in clusters
        ],
        "candidate_targets": enriched_targets,
        "hint_matches": hint_matches,
    }


def _format_row(row: dict) -> str:
    label = row.get("label", "")
    if label:
        label = f" | {label}"
    return (
        f"{row['index']:>3}: {row['kind']:<10} spread={row['spread']:.4f} "
        f"zero={row['zero_fraction']:.2f} one={row['one_fraction']:.2f} "
        f"distinct={row['distinct_rounded_values']}{label}"
    )


def _format_target(target: dict) -> str:
    window = target.get("current_best_window")
    window_text = "no current window"
    if window:
        window_text = (
            f"best {window['start_index']}-{window['end_index']} "
            f"score={window['score']:.6f} overlap={str(window['overlaps_range']).lower()}"
        )
    return (
        f"{target['target_type']:<6} {target['target']:<24} "
        f"score={target['score']:.6f} relevance={target['relevance_score']:.6f} "
        f"kind_fit={target['kind_fit']:.6f} size_fit={target['size_fit']:.6f} "
        f"{window_text}"
    )


def print_summary(result: dict, top: int) -> None:
    start = result["range"]["start"]
    end = result["range"]["end"]
    print(f"Corpus: {result['preset_count']} presets | bank={result['bank']} | range={start}-{end}")
    print(
        f"Rows: {len(result['slot_rows'])} | varying: {result['varying_slot_rows']} | "
        f"kind counts: {result['kind_counts']}"
    )
    if result["hint_matches"]:
        print("Hints:")
        for hint in result["hint_matches"]:
            relation = "overlaps" if hint["gap"] == 0 else f"{hint['gap']} slots away"
            print(f"  - {hint['label']} [{hint['range'][0]}-{hint['range'][1]}] ({relation})")
    print("")

    print("Slot rows:")
    for row in result["slot_rows"]:
        print(f"  {_format_row(row)}")
    print("")

    print(f"Top {top} candidate targets:")
    for target in result["candidate_targets"][:top]:
        print(f"  - {_format_target(target)}")


def main():
    args = make_parser().parse_args()
    result = summarize_slot_range(
        start=args.start,
        end=args.end,
        bank=args.bank,
        slots=args.slots,
        threshold=args.threshold,
        top=args.top,
    )
    if args.json:
        print(json.dumps(result, indent=2))
        return
    print_summary(result, top=args.top)


if __name__ == "__main__":
    main()
