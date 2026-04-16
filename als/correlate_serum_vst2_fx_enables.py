#!/usr/bin/env python3
"""
correlate_serum_vst2_fx_enables.py
Compare the boolean FX-enable candidate block against each FX module's best
candidate parameter window across the preset corpus.

This does NOT prove exact mappings. It tries to prioritize likely pairings by
checking whether presets with a given enable boolean set to 1 also show more
activity in that module's candidate parameter window.

Examples:
    python3 als/correlate_serum_vst2_fx_enables.py
    python3 als/correlate_serum_vst2_fx_enables.py --enable-start 154 --enable-end 163
    python3 als/correlate_serum_vst2_fx_enables.py --module-exclude-range 40-44 --module-exclude-range 137-145 --module-exclude-range 154-163
"""

import argparse
import json
import math
from pathlib import Path

try:
    from parse_serum import SERUM_V2_PARAM_OFFSET, extract_vst2_float_slots, parse_fxp_file
    from rank_serum_vst2_module_candidates import rank_target_candidates
except ModuleNotFoundError:
    from .parse_serum import SERUM_V2_PARAM_OFFSET, extract_vst2_float_slots, parse_fxp_file
    from .rank_serum_vst2_module_candidates import rank_target_candidates


DEFAULT_BANKS = [
    Path("/Library/Audio/Presets/Xfer Records/Serum 2 Presets/Presets/S1 Presets/Garage"),
    Path("/Library/Audio/Presets/Xfer Records/Serum 2 Presets/Presets/S1 Presets/Speed Garage"),
]
FX_MODULES = [
    "fx_distortion",
    "fx_flanger",
    "fx_phaser",
    "fx_chorus",
    "fx_delay",
    "fx_compressor",
    "fx_eq",
    "fx_filter",
    "fx_hyper_dimension",
]


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Correlate FX enable booleans with candidate FX module windows.")
    parser.add_argument("--slots", type=int, default=180, help="How many VST2 float slots to inspect")
    parser.add_argument("--enable-start", type=int, default=154, help="Start index for the FX enable boolean block")
    parser.add_argument("--enable-end", type=int, default=163, help="End index for the FX enable boolean block")
    parser.add_argument("--top", type=int, default=3, help="How many best pairings to print per slot/module")
    parser.add_argument(
        "--module-exclude-range",
        action="append",
        default=[],
        help="Exclude candidate module windows overlapping a range like 137-145. May be passed multiple times.",
    )
    return parser


def _preset_paths() -> list[Path]:
    paths = []
    for bank in DEFAULT_BANKS:
        paths.extend(sorted(bank.glob("*.fxp")))
    return paths


def _load_slot_matrix(slot_count: int) -> tuple[list[Path], list[list[float]]]:
    paths = _preset_paths()
    matrix = []
    for path in paths:
        parsed = parse_fxp_file(path)
        slots = extract_vst2_float_slots(parsed["_decompressed_data"], start_offset=SERUM_V2_PARAM_OFFSET, count=slot_count)
        matrix.append([slot["raw"] for slot in slots])
    return paths, matrix


def _parse_ranges(items: list[str]) -> list[tuple[int, int]]:
    parsed = []
    for item in items:
        left, right = item.split("-", 1)
        start = int(left)
        end = int(right)
        if start > end:
            start, end = end, start
        parsed.append((start, end))
    return parsed


def _mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def _pearson(xs: list[float], ys: list[float]) -> float:
    if len(xs) != len(ys) or not xs:
        return 0.0
    mean_x = _mean(xs)
    mean_y = _mean(ys)
    num = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys))
    den_x = math.sqrt(sum((x - mean_x) ** 2 for x in xs))
    den_y = math.sqrt(sum((y - mean_y) ** 2 for y in ys))
    if den_x == 0.0 or den_y == 0.0:
        return 0.0
    return num / (den_x * den_y)


def _slot_modes(matrix: list[list[float]]) -> list[float]:
    if not matrix:
        return []
    width = len(matrix[0])
    modes = []
    for idx in range(width):
        counts = {}
        for row in matrix:
            value = round(row[idx], 4)
            counts[value] = counts.get(value, 0) + 1
        best_value = max(counts.items(), key=lambda item: item[1])[0]
        modes.append(best_value)
    return modes


def _slot_spreads(matrix: list[list[float]]) -> list[float]:
    if not matrix:
        return []
    width = len(matrix[0])
    spreads = []
    for idx in range(width):
        vals = [row[idx] for row in matrix]
        spreads.append(max(vals) - min(vals))
    return spreads


def _window_activity_scores(matrix: list[list[float]], indices: list[int], modes: list[float], spreads: list[float]) -> list[float]:
    scores = []
    for row in matrix:
        distances = []
        for idx in indices:
            spread = spreads[idx]
            if spread <= 1e-9:
                continue
            distances.append(abs(row[idx] - modes[idx]) / spread)
        scores.append(_mean(distances))
    return scores


def analyze_fx_enable_correlations(
    slot_count: int,
    enable_start: int,
    enable_end: int,
    top: int,
    module_exclude_ranges: list[tuple[int, int]] | None = None,
) -> dict:
    paths, matrix = _load_slot_matrix(slot_count)
    modes = _slot_modes(matrix)
    spreads = _slot_spreads(matrix)
    module_exclude_ranges = module_exclude_ranges or []

    module_windows = {}
    for module in FX_MODULES:
        ranked = rank_target_candidates(
            module,
            "module",
            bank="all",
            slots=slot_count,
            threshold=0.01,
            top=1,
            window_size=0,
            exclude_ranges=module_exclude_ranges,
        )
        if not ranked["top_windows"]:
            continue
        top_window = ranked["top_windows"][0]
        module_windows[module] = {
            "start_index": top_window["start_index"],
            "end_index": top_window["end_index"],
            "indices": top_window["indices"],
            "score": top_window["score"],
        }

    module_activity = {
        module: _window_activity_scores(matrix, window["indices"], modes, spreads)
        for module, window in module_windows.items()
    }

    grouped_windows = {}
    for module, window in module_windows.items():
        key = tuple(window["indices"])
        group = grouped_windows.setdefault(key, {
            "indices": window["indices"],
            "start_index": window["start_index"],
            "end_index": window["end_index"],
            "modules": [],
            "score": window["score"],
        })
        group["modules"].append(module)

    grouped_activity = {
        key: _window_activity_scores(matrix, group["indices"], modes, spreads)
        for key, group in grouped_windows.items()
    }

    enable_slots = {}
    enable_slot_groups = {}
    for idx in range(enable_start, enable_end + 1):
        values = [1.0 if row[idx] >= 0.5 else 0.0 for row in matrix]
        slot_results = []
        for module, activity_scores in module_activity.items():
            on_scores = [score for score, flag in zip(activity_scores, values) if flag == 1.0]
            off_scores = [score for score, flag in zip(activity_scores, values) if flag == 0.0]
            mean_on = _mean(on_scores)
            mean_off = _mean(off_scores)
            delta = mean_on - mean_off
            corr = _pearson(values, activity_scores)
            slot_results.append({
                "module": module,
                "candidate_window": module_windows[module],
                "mean_activity_when_on": round(mean_on, 6),
                "mean_activity_when_off": round(mean_off, 6),
                "activity_delta": round(delta, 6),
                "pearson": round(corr, 6),
            })
        slot_results.sort(key=lambda item: (item["activity_delta"], item["pearson"]), reverse=True)
        enable_slots[idx] = slot_results

        group_results = []
        for key, activity_scores in grouped_activity.items():
            group = grouped_windows[key]
            on_scores = [score for score, flag in zip(activity_scores, values) if flag == 1.0]
            off_scores = [score for score, flag in zip(activity_scores, values) if flag == 0.0]
            mean_on = _mean(on_scores)
            mean_off = _mean(off_scores)
            delta = mean_on - mean_off
            corr = _pearson(values, activity_scores)
            group_results.append({
                "modules": group["modules"],
                "candidate_window": {
                    "start_index": group["start_index"],
                    "end_index": group["end_index"],
                    "indices": group["indices"],
                    "score": group["score"],
                },
                "mean_activity_when_on": round(mean_on, 6),
                "mean_activity_when_off": round(mean_off, 6),
                "activity_delta": round(delta, 6),
                "pearson": round(corr, 6),
            })
        group_results.sort(key=lambda item: (item["activity_delta"], item["pearson"]), reverse=True)
        enable_slot_groups[idx] = group_results

    best_by_module = {}
    for module in module_windows:
        rows = []
        for idx, results in enable_slots.items():
            hit = next(result for result in results if result["module"] == module)
            rows.append({
                "enable_slot": idx,
                **hit,
            })
        rows.sort(key=lambda item: (item["activity_delta"], item["pearson"]), reverse=True)
        best_by_module[module] = rows[:top]

    return {
        "preset_count": len(paths),
        "enable_range": [enable_start, enable_end],
        "module_exclude_ranges": module_exclude_ranges,
        "module_windows": module_windows,
        "window_groups": list(grouped_windows.values()),
        "best_by_enable_slot": {
            str(idx): results[:top]
            for idx, results in enable_slots.items()
        },
        "best_by_enable_slot_groups": {
            str(idx): results[:top]
            for idx, results in enable_slot_groups.items()
        },
        "best_by_module": best_by_module,
        "note": "This is a statistical hint only. Controlled preset save-diffs are still required to prove exact ordering inside 154-163.",
    }


def main():
    args = make_parser().parse_args()
    result = analyze_fx_enable_correlations(
        slot_count=args.slots,
        enable_start=args.enable_start,
        enable_end=args.enable_end,
        top=args.top,
        module_exclude_ranges=_parse_ranges(args.module_exclude_range),
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
