#!/usr/bin/env python3
"""Alias and residue handling for Serum VST2 host-label reports."""

from __future__ import annotations

import re
from typing import Iterable


SERUM_VST2_LABEL_ALIASES = {
    "Comp_On": "Comp Enable",
    "Comp_Wet #2": "Comp_Wet",
    "FX Fil On": "FX Fil Enable",
    "FX Fil Pan #2": "FX Fil Pan",
    "Attack Curve #2": "Attack Curve",
    "Decay Curve #2": "Decay Curve",
    "Release Curve #2": "Release Curve",
    "Attack Curve #3": "Attack Curve",
    "Decay Curve #3": "Decay Curve",
    "Release Curve #3": "Release Curve",
    "OscAPitchTrack": "Osc A PitchTrack",
    "OscBPitchTrack": "Osc B PitchTrack",
    "Bend U": "Bend Range Up",
    "Bend D": "Bend Range Down",
    "WarpOscA": "A Warp",
    "WarpOscB": "B Warp",
    "Osc N On": "Osc Enable noise",
    "Osc S On": "Osc Enable sub",
    "(LFO1 Smooth)": "LFO1 smooth",
    "(LFO2 Smooth)": "LFO2 smooth",
    "(LFO3 Smooth)": "LFO3 smooth",
    "(LFO4 Smooth)": "LFO4 smooth",
}


SERUM_VST2_LABEL_IGNORE_EXACT = {
    "ERROR",
    "kReservedMT",
    "this should NEVER appear (knp)",
    "CompMB L",
    "CompMB M",
    "CompMB H",
    "MultBand",
    "(Mod Source off)",
    "Modwheel Source",
    "Env 1 Source",
    "Env 2 Source",
    "Env 3 Source",
    "Velocity Source",
    "Note # Source",
    "Aftertouch Mod Source",
    "Aftertouch Mod Source (Poly)",
    "NoiseOsc ModSource",
    "Trig",
    "Env",
    "Off",
    "Envelope display",
    "View Selector",
    "LFO Rate",
    "LFO Anchor",
    "LFO Dotteds",
    "LFO Triplets",
    "LFO Mode",
    "LFO Beat Sync",
    "LFO Rise",
    "LFO Delay",
    "LFO Smooth",
    "LFO Grid",
    "LFO Display",
}


SERUM_VST2_LABEL_IGNORE_PATTERNS = [
    re.compile(r"^Mod ?\d+ amt$"),
    re.compile(r"^Mod ?\d+ out$"),
    re.compile(r"^Matrix OSC->Curve \d+$"),
    re.compile(r"^LFO Bus \d+$"),
    re.compile(r"^LFO [1-8] Source$"),
    re.compile(r"^LFO[5-8] Rate$"),
    re.compile(r"^LFO[5-8]Rate$"),
    re.compile(r"^LFO[5-8] smooth$"),
    re.compile(r"^LFO[5-8] Rise$"),
    re.compile(r"^LFO[5-8] Delay$"),
]


def canonicalize_serum_vst2_label(label: str) -> str:
    return SERUM_VST2_LABEL_ALIASES.get(label, label)


def should_ignore_serum_vst2_label(label: str) -> bool:
    if label in SERUM_VST2_LABEL_IGNORE_EXACT:
        return True
    return any(pattern.match(label) for pattern in SERUM_VST2_LABEL_IGNORE_PATTERNS)


def apply_serum_vst2_label_overrides(report: dict) -> dict:
    """Return a coverage report with duplicate and residue labels collapsed."""
    raw_entries = report["entries"]
    raw_by_label = {entry["label"]: entry for entry in raw_entries}

    grouped: dict[tuple[str, str, str], dict] = {}
    for entry in raw_entries:
        original_label = entry["label"]
        if should_ignore_serum_vst2_label(original_label):
            continue

        canonical_label = canonicalize_serum_vst2_label(original_label)
        meta_source = raw_by_label.get(canonical_label, entry)
        key = (meta_source["module"], meta_source["category"], canonical_label)
        grouped_entry = grouped.setdefault(key, {
            **meta_source,
            "label": canonical_label,
            "key": canonical_label,
            "covered": False,
            "coverage_sources": [],
        })
        grouped_entry["covered"] = grouped_entry["covered"] or entry["covered"] or meta_source.get("covered", False)

        seen_sources = {
            tuple(sorted(source.items()))
            for source in grouped_entry.get("coverage_sources", [])
        }
        for source in entry.get("coverage_sources", []) + meta_source.get("coverage_sources", []):
            frozen = tuple(sorted(source.items()))
            if frozen in seen_sources:
                continue
            seen_sources.add(frozen)
            grouped_entry.setdefault("coverage_sources", []).append(source)

    entries = sorted(grouped.values(), key=lambda item: (item["module"], item["key"]))

    categories = {}
    modules = {}
    covered_count = 0
    for entry in entries:
        if entry["covered"]:
            covered_count += 1

        category_summary = categories.setdefault(entry["category"], {
            "total": 0,
            "covered": 0,
            "uncovered": 0,
            "covered_labels": [],
            "uncovered_labels": [],
        })
        category_summary["total"] += 1
        if entry["covered"]:
            category_summary["covered"] += 1
            category_summary["covered_labels"].append(entry["key"])
        else:
            category_summary["uncovered"] += 1
            category_summary["uncovered_labels"].append(entry["key"])

        module_summary = modules.setdefault(entry["module"], {
            "manual_section": entry["manual_section"],
            "total": 0,
            "covered": 0,
            "uncovered": 0,
            "covered_labels": [],
            "uncovered_labels": [],
        })
        module_summary["total"] += 1
        if entry["covered"]:
            module_summary["covered"] += 1
            module_summary["covered_labels"].append(entry["key"])
        else:
            module_summary["uncovered"] += 1
            module_summary["uncovered_labels"].append(entry["key"])

    for summary in categories.values():
        total = summary["total"] or 1
        summary["covered_pct"] = round(summary["covered"] / total * 100, 1)
    for summary in modules.values():
        total = summary["total"] or 1
        summary["covered_pct"] = round(summary["covered"] / total * 100, 1)

    return {
        **report,
        "catalog_entry_count": len(entries),
        "covered_entry_count": covered_count,
        "uncovered_entry_count": len(entries) - covered_count,
        "covered_pct": round(covered_count / max(len(entries), 1) * 100, 1),
        "categories": categories,
        "modules": modules,
        "entries": entries,
    }


def canonicalize_label_iter(labels: Iterable[str]) -> list[str]:
    result = []
    for label in labels:
        if should_ignore_serum_vst2_label(label):
            continue
        result.append(canonicalize_serum_vst2_label(label))
    return result
