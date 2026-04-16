#!/usr/bin/env python3
"""
build_serum_profile.py

Normalize existing Serum analysis JSON into the canonical Serum preset profile
shape.

This is the first implementation step toward a broader Serum sound-intelligence
catalog. It currently targets the existing `als/analysis/*-serum.json` outputs
produced from Ableton sessions containing Serum instances.

Examples:
    python3 als/build_serum_profile.py --analysis-json als/analysis/mph-raw-serum.json
    python3 als/build_serum_profile.py --analysis-json als/analysis/mph-raw-serum.json --out als/catalog/mph-raw-profiles.json
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


PROFILE_VERSION = "0.1.0"


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build normalized Serum preset profiles from existing analysis JSON.")
    parser.add_argument("--analysis-json", required=True, help="Path to an existing als/analysis/*-serum.json file.")
    parser.add_argument("--out", help="Optional output JSON path.")
    return parser


def _slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or "unknown"


def infer_role_candidates(track_name: str | None) -> list[str]:
    text = (track_name or "").lower()
    roles = []
    if "sub" in text:
        roles.append("sub")
    if "reese" in text:
        roles.append("reese")
    if "bass" in text:
        roles.append("bass")
    if "pad" in text or "chord" in text:
        roles.append("pad")
    if "lead" in text:
        roles.append("lead")
    if "pluck" in text:
        roles.append("pluck")
    if "stab" in text:
        roles.append("stab")
    if "fx" in text or "sweep" in text:
        roles.append("fx")
    return roles or ["unknown"]


def _first_filter_freq(instance: dict) -> float | None:
    for filter_row in (instance.get("filters") or {}).values():
        value = filter_row.get("kParamFreq")
        if isinstance(value, (int, float)):
            return float(value)
    return None


def _max_filter_drive(instance: dict) -> float | None:
    drives = []
    for filter_row in (instance.get("filters") or {}).values():
        value = filter_row.get("kParamDrive")
        if isinstance(value, (int, float)):
            drives.append(float(value))
    return max(drives) if drives else None


def _has_unisonish_hint(instance: dict) -> bool:
    for osc_row in (instance.get("oscillators") or {}).values():
        for key, value in osc_row.items():
            if "unison" in key.lower() and isinstance(value, (int, float)) and value not in (0, 1):
                return True
    return False


def _low_octave_hint(instance: dict) -> bool:
    for osc_row in (instance.get("oscillators") or {}).values():
        value = osc_row.get("kParamOctave")
        if isinstance(value, (int, float)) and value <= -1:
            return True
    return False


def infer_tone_tags(instance: dict) -> list[str]:
    tags = set()
    freq = _first_filter_freq(instance)
    if freq is not None:
        if freq <= 0.33:
            tags.add("dark")
        elif freq >= 0.66:
            tags.add("bright")
    drive = _max_filter_drive(instance)
    if drive is not None and drive >= 20:
        tags.add("gritty")
    if _has_unisonish_hint(instance):
        tags.add("wide")
    if len(instance.get("mod_matrix") or {}) >= 4:
        tags.add("modulated")
    if not tags:
        tags.add("unknown")
    return sorted(tags)


def infer_mix_tags(instance: dict, roles: list[str]) -> tuple[list[str], list[str]]:
    tags = set()
    notes = []
    if any(role in roles for role in ("sub", "bass", "reese")) or _low_octave_hint(instance):
        tags.add("low_end_anchor")
        notes.append("Likely carries low-end weight or bass function.")
    if "pad" in roles:
        tags.add("background")
        notes.append("Pad-like role suggests supportive/background placement.")
    if "lead" in roles or "pluck" in roles or "stab" in roles:
        tags.add("mid_focus")
        notes.append("Lead/pluck/stab role suggests a more forward midrange position.")
    if "wide" in infer_tone_tags(instance):
        tags.add("side_heavy")
        notes.append("Detected unison-style width hints; likely side-heavy unless collapsed in the mix.")
    if not tags:
        tags.add("unknown")
    return sorted(tags), notes


def build_profile(analysis_path: Path, analysis: dict, instance: dict, instance_index: int) -> dict:
    track_name = instance.get("track")
    roles = infer_role_candidates(track_name)
    tone_tags = infer_tone_tags(instance)
    mix_tags, notes = infer_mix_tags(instance, roles)

    return {
        "profile_version": PROFILE_VERSION,
        "profile_id": f"{analysis.get('slug', analysis_path.stem)}:{_slugify(track_name or f'instance-{instance_index}')}:i{instance_index}",
        "source": {
            "kind": "als_serum2_instance" if instance.get("plugin") == "Serum 2" else "unknown",
            "plugin": instance.get("plugin", "unknown"),
            "analysis_path": str(analysis_path),
            "analysis_slug": analysis.get("slug"),
            "track": track_name,
            "instance_index": instance_index,
            "preset_name": None,
            "bank": None,
            "vendor": None,
            "source_path": None
        },
        "classification": {
            "role_candidates": roles,
            "tone_tags": tone_tags,
            "mix_tags": mix_tags,
            "notes": notes
        },
        "summary": {
            "wavetable_refs": sorted(set((instance.get("wavetables") or {}).values())),
            "oscillator_count": len(instance.get("oscillators") or {}),
            "filter_count": len(instance.get("filters") or {}),
            "envelope_count": len(instance.get("envelopes") or {}),
            "lfo_count": len(instance.get("lfos") or {}),
            "mod_route_count": len(instance.get("mod_matrix") or {})
        },
        "synthesis": {
            "wavetables": instance.get("wavetables") or {},
            "oscillators": instance.get("oscillators") or {},
            "filters": instance.get("filters") or {},
            "envelopes": instance.get("envelopes") or {},
            "lfos": instance.get("lfos") or {},
            "mod_matrix": instance.get("mod_matrix") or {},
            "global": instance.get("global") or {},
            "effects": instance.get("effects") or instance.get("fx")
        },
        "audio_reference": {
            "status": "not_rendered",
            "render_paths": [],
            "descriptor_path": None
        },
        "confidence": {
            "source": 0.95 if instance.get("plugin") == "Serum 2" else 0.5,
            "classification": 0.45,
            "mix_hints": 0.35
        }
    }


def build_profiles(analysis_path: Path) -> list[dict]:
    analysis = json.loads(analysis_path.read_text())
    profiles = []
    for index, instance in enumerate(analysis.get("serum_instances", []), 1):
        profiles.append(build_profile(analysis_path, analysis, instance, index))
    return profiles


def main() -> None:
    parser = make_parser()
    args = parser.parse_args()
    analysis_path = Path(args.analysis_json)
    profiles = build_profiles(analysis_path)
    output = json.dumps(profiles, indent=2) + "\n"
    if args.out:
        Path(args.out).write_text(output)
    print(output, end="")


if __name__ == "__main__":
    main()
