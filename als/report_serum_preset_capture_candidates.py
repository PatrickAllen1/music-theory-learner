#!/usr/bin/env python3
"""
report_serum_preset_capture_candidates.py

Recommend real Garage/Speed Garage Serum preset files to capture next based on
the current catalog gap report.

Examples:
    python3 als/report_serum_preset_capture_candidates.py
    python3 als/report_serum_preset_capture_candidates.py --format json
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

try:
    from parse_serum import parse_fxp_file, summarise_instance
    from report_serum_catalog_gaps import build_report as build_catalog_gaps_report
except ModuleNotFoundError:
    from .parse_serum import parse_fxp_file, summarise_instance
    from .report_serum_catalog_gaps import build_report as build_catalog_gaps_report


DEFAULT_BANK_DIRS = [
    Path("/Library/Audio/Presets/Xfer Records/Serum 2 Presets/Presets/S1 Presets/Garage"),
    Path("/Library/Audio/Presets/Xfer Records/Serum 2 Presets/Presets/S1 Presets/Speed Garage"),
]
ROLE_MIX_MAP = {
    "sub": {"low_end_anchor"},
    "bass": {"low_end_anchor"},
    "reese": {"low_end_anchor", "side_heavy"},
    "pad": {"background"},
    "lead": {"mid_focus"},
    "pluck": {"mid_focus"},
    "stab": {"mid_focus", "background"},
    "fx": {"background", "side_heavy"},
}


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Recommend actual Serum preset files to capture for current catalog gaps.")
    parser.add_argument("--catalog-dir", default="als/catalog/profiles", help="Directory of generated *-profiles.json files.")
    parser.add_argument("--briefs", default="als/serum-track-briefs.json", help="Track brief manifest JSON.")
    parser.add_argument("--prefer-rendered", action="store_true", help="Prefer rendered profiles where available when computing gaps.")
    parser.add_argument("--limit-per-part", type=int, default=5, help="Max candidates to inspect per part. Default: 5")
    parser.add_argument("--mutation-limit", type=int, default=6, help="Max mutation suggestions per part. Default: 6")
    parser.add_argument("--max-swaps", type=int, default=2, help="Maximum refinement swaps to apply. Default: 2")
    parser.add_argument("--bank-dir", action="append", default=[], help="Preset bank directory to scan. Pass multiple times.")
    parser.add_argument("--top-per-gap", type=int, default=5, help="Maximum preset candidates per gap. Default: 5")
    parser.add_argument("--overall-limit", type=int, default=12, help="Maximum unique presets in the overall shortlist. Default: 12")
    parser.add_argument("--format", choices=["json", "text"], default="text", help="Output format.")
    return parser


def _normalized_tokens(text: str) -> set[str]:
    return {token for token in re.split(r"[^a-z0-9]+", text.lower()) if token}


def _primary_role(name: str) -> str:
    tokens = _normalized_tokens(name)
    if {"sub"} & tokens:
        return "sub"
    if {"reese"} & tokens:
        return "reese"
    if {"bass", "wobble"} & tokens:
        return "bass"
    if {"pluck"} & tokens:
        return "pluck"
    if {"lead"} & tokens:
        return "lead"
    if {"stab", "organ", "piano", "chord"} & tokens:
        return "stab" if {"stab", "organ", "piano"} & tokens else "pad"
    if {"pad", "atmo", "atmos", "atmosphere", "string"} & tokens:
        return "pad"
    if {"fx", "laser", "riser", "sweep", "noise", "impact"} & tokens:
        return "fx"
    return "unknown"


def _tone_tags(summary: dict) -> set[str]:
    tags = set()
    name = summary["track"].lower()
    tokens = _normalized_tokens(name)
    role = _primary_role(summary["track"])
    osc_uni = summary.get("key_params", {}).get("osc_a_uni_voices")

    if role in {"bass", "sub", "reese", "pad"} or {"dark", "deep", "night", "shadow"} & tokens:
        tags.add("dark")
    if role in {"lead", "pluck", "stab"} or {"bright", "glass", "sharp", "shine"} & tokens:
        tags.add("bright")
    if role == "pad" or {"soft", "smooth", "gentle", "warm"} & tokens:
        tags.add("soft")
    if role in {"reese", "fx"} or {"raw", "dirty", "grit", "rough"} & tokens:
        tags.add("gritty")
    if (isinstance(osc_uni, (int, float)) and osc_uni > 1) or {"wide", "stereo", "spread"} & tokens:
        tags.add("wide")
    if {"motion", "moving", "pulse", "lfo", "laser", "riser"} & tokens:
        tags.add("modulated")
    return tags


def _mix_tags(role: str) -> set[str]:
    return set(ROLE_MIX_MAP.get(role, set()))


def _scan_presets(bank_dirs: list[Path]) -> list[dict]:
    presets = []
    for bank_dir in bank_dirs:
        if not bank_dir.exists():
            continue
        for path in sorted(bank_dir.rglob("*.fxp")):
            parsed = parse_fxp_file(path)
            summary = summarise_instance({
                "track": path.stem,
                "plugin": parsed.get("header", {}).get("plugin_id", "Serum"),
                **parsed,
            })
            role = _primary_role(summary["track"])
            presets.append({
                "path": str(path),
                "track": summary["track"],
                "vendor": summary.get("vendor"),
                "bank": summary.get("bank"),
                "role": role,
                "tone_tags": sorted(_tone_tags(summary)),
                "mix_tags": sorted(_mix_tags(role)),
                "wavetables": summary.get("wavetables", []),
                "macro_labels": summary.get("macro_labels", {}),
                "key_params": summary.get("key_params", {}),
            })
    return presets


def _score_candidate(gap: dict, preset: dict) -> tuple[float, list[str]]:
    score = 0.0
    reasons = []
    if preset["role"] == gap["role"]:
        score += 6.0
        reasons.append("role matches")
    elif gap["role"] == "pad" and preset["role"] == "stab":
        score += 2.0
        reasons.append("adjacent pad/stab role")

    tone_overlap = sorted(set(gap["target_tone"]) & set(preset["tone_tags"]))
    if tone_overlap:
        score += len(tone_overlap) * 2.0
        reasons.append(f"tone overlap: {', '.join(tone_overlap)}")

    mix_overlap = sorted(set(gap["target_mix"]) & set(preset["mix_tags"]))
    if mix_overlap:
        score += len(mix_overlap) * 1.5
        reasons.append(f"mix overlap: {', '.join(mix_overlap)}")

    if preset["vendor"] == "Production Hut":
        score += 0.5

    return score, reasons


def build_report(args: argparse.Namespace) -> dict:
    gaps = build_catalog_gaps_report(args)
    bank_dirs = [Path(path) for path in (args.bank_dir or [])] or DEFAULT_BANK_DIRS
    presets = _scan_presets(bank_dirs)

    gap_rows = []
    overall: dict[str, dict] = {}
    for gap in gaps["gaps"]:
        matches = []
        for preset in presets:
            score, reasons = _score_candidate(gap, preset)
            if score <= 0:
                continue
            row = {
                **preset,
                "score": round(score, 4),
                "reasons": reasons,
                "gap_label": gap["gap_label"],
            }
            matches.append(row)
        matches.sort(key=lambda row: (-row["score"], row["path"]))
        top = matches[: args.top_per_gap]
        gap_rows.append({
            "gap_label": gap["gap_label"],
            "severity": gap["severity"],
            "suggested_action": gap["suggested_action"],
            "candidates": top,
        })
        for row in top:
            entry = overall.setdefault(row["path"], {
                **row,
                "gap_labels": [],
                "score_total": 0.0,
            })
            entry["gap_labels"].append(gap["gap_label"])
            entry["score_total"] += row["score"]

    overall_rows = list(overall.values())
    overall_rows.sort(key=lambda row: (-row["score_total"], row["path"]))
    for row in overall_rows:
        row["score_total"] = round(row["score_total"], 4)

    return {
        "gap_count": len(gap_rows),
        "preset_count": len(presets),
        "bank_dirs": [str(path) for path in bank_dirs],
        "gaps": gap_rows,
        "overall_shortlist": overall_rows[: args.overall_limit],
    }


def render_text(report: dict) -> str:
    lines = []
    lines.append("# Serum Preset Capture Candidates")
    lines.append("")
    lines.append(f"- scanned presets: {report['preset_count']}")
    lines.append(f"- gaps: {report['gap_count']}")
    lines.append("")
    lines.append("## Overall Shortlist")
    for row in report["overall_shortlist"]:
        lines.append(
            f"- `{row['track']}` :: score_total={row['score_total']} "
            f"[role: {row['role']}; tone: {', '.join(row['tone_tags']) or '-'}; bank: {row.get('bank') or '-'}]"
        )
        lines.append(f"  path: {row['path']}")
        lines.append(f"  gaps: {' | '.join(row['gap_labels'])}")
    lines.append("")
    lines.append("## By Gap")
    for gap in report["gaps"]:
        lines.append(f"- `{gap['gap_label']}` :: severity={gap['severity']}")
        lines.append(f"  action: {gap['suggested_action']}")
        for row in gap["candidates"]:
            lines.append(
                f"  candidate: `{row['track']}` score={row['score']} "
                f"[role: {row['role']}; tone: {', '.join(row['tone_tags']) or '-'}; bank: {row.get('bank') or '-'}]"
            )
            lines.append(f"  path: {row['path']}")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = make_parser()
    args = parser.parse_args()
    report = build_report(args)
    if args.format == "json":
        print(json.dumps(report, indent=2))
        return
    print(render_text(report), end="")


if __name__ == "__main__":
    main()
