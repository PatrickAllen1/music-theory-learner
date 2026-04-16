#!/usr/bin/env python3
"""
Shared plan metadata for the deferred Serum VST2 manual probe workflow.
"""

from __future__ import annotations

import re


CHECKPOINT_DEFER_UNTIL = {
    "A": [],
    "B": ["A"],
    "C": ["B"],
    "D": ["C"],
    "E": ["D"],
    "F": ["E"],
    "G": ["F"],
    "H": ["G"],
}


def checkpoint_defer_until(checkpoint_id: str) -> list[str]:
    return CHECKPOINT_DEFER_UNTIL.get(checkpoint_id, [])


def _chunk_numeric_labels(labels: list[str], prefix: str, size: int) -> list[dict]:
    pattern = re.compile(rf"^{re.escape(prefix)}\s+(\d+)$")
    indexed = []
    for label in labels:
        match = pattern.match(label)
        if not match:
            continue
        indexed.append((int(match.group(1)), label))
    indexed.sort()

    chunks = []
    for start in range(0, len(indexed), size):
        chunk = indexed[start:start + size]
        if not chunk:
            continue
        start_index = chunk[0][0]
        end_index = chunk[-1][0]
        chunks.append({
            "title": f"{prefix} {start_index}-{end_index}",
            "labels": [label for _, label in chunk],
        })
    return chunks


def _chunk_matrix_curve(labels: list[str], size: int = 8) -> list[dict]:
    pattern = re.compile(r"^Matrix Curve ([AB]) (\d+)$")
    grouped = {}
    for label in labels:
        match = pattern.match(label)
        if not match:
            continue
        lane = match.group(1)
        index = int(match.group(2))
        grouped.setdefault(index, {})[lane] = label

    chunks = []
    ordered_indices = sorted(grouped)
    for start in range(0, len(ordered_indices), size):
        indices = ordered_indices[start:start + size]
        chunk_labels = []
        for index in indices:
            for lane in ("A", "B"):
                label = grouped[index].get(lane)
                if label:
                    chunk_labels.append(label)
        if chunk_labels:
            chunks.append({
                "title": f"Matrix Curve {indices[0]}-{indices[-1]}",
                "labels": chunk_labels,
            })
    return chunks


def _oscillator_detail_groups(labels: list[str]) -> list[dict]:
    groups = [
        ("Osc A core", ["Osc A On", "Osc Enable (Osc A)", "A Fine", "A Coarse Pitch", "A Random Phase", "A Initial Phase", "Osc A PitchTrack", "A Warp", "Warp Menu OSC A"]),
        ("Osc A unison", ["A Uni LR", "A Uni Warp", "A Uni WTPos", "A Uni Stack"]),
        ("Osc B core", ["Osc B On", "Osc Enable B", "B Fine", "B Coarse Pitch", "B Random Phase", "B Initial Phase", "Osc B PitchTrack", "B Warp"]),
        ("Osc B unison", ["B Uni LR", "B Uni Warp", "B Uni WTPos", "B Uni Stack"]),
    ]
    available = set(labels)
    rows = []
    for title, ordered in groups:
        chunk = [label for label in ordered if label in available]
        if chunk:
            rows.append({"title": title, "labels": chunk})
    leftovers = [label for label in labels if label not in {item for row in rows for item in row["labels"]}]
    if leftovers:
        rows.append({"title": "Oscillator detail leftovers", "labels": leftovers})
    return rows


def _lfo_extended_groups(labels: list[str]) -> list[dict]:
    rows = []
    for lfo_index in range(1, 5):
        prefix = f"LFO{lfo_index}"
        chunk = [label for label in labels if label.startswith(prefix)]
        if chunk:
            rows.append({"title": f"{prefix} family", "labels": chunk})
    leftovers = [label for label in labels if label not in {item for row in rows for item in row["labels"]}]
    if leftovers:
        rows.append({"title": "LFO extended leftovers", "labels": leftovers})
    return rows


def build_probe_subgroups(probe: dict) -> list[dict]:
    labels = probe.get("candidate_host_labels", [])
    probe_id = probe.get("probe_id") or probe.get("id") or ""
    if not labels:
        return []
    if probe_id == "mod_route":
        return (
            _chunk_numeric_labels(labels, "Mod Source", 8)
            + _chunk_numeric_labels(labels, "Mod Dest", 8)
            + _chunk_numeric_labels(labels, "Mod Matrix Depth", 8)
        )
    if probe_id == "matrix_curve":
        return _chunk_matrix_curve(labels, size=8)
    if probe_id == "matrix_aux_source_family":
        return _chunk_numeric_labels(labels, "Mod Aux Source", 8)
    if probe_id == "matrix_output_family":
        return _chunk_numeric_labels(labels, "Mod Matrix Output", 8)
    if probe_id == "oscillator_detail_core":
        return _oscillator_detail_groups(labels)
    if probe_id == "lfo_extended_family":
        return _lfo_extended_groups(labels)
    if len(labels) > 12:
        return [{"title": f"{probe_id} labels", "labels": labels}]
    return []
