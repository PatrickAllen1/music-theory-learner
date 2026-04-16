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
    python3 als/build_serum_profile.py --analysis-dir als/analysis --catalog-dir als/catalog/profiles --index-out als/catalog/index.json
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


PROFILE_VERSION = "0.1.0"


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build normalized Serum preset profiles from existing analysis JSON.")
    parser.add_argument("--analysis-json", help="Path to an existing als/analysis/*-serum.json file.")
    parser.add_argument("--analysis-dir", help="Directory containing existing als/analysis/*-serum.json files.")
    parser.add_argument("--glob", default="*-serum.json", help="Glob to use with --analysis-dir. Default: *-serum.json")
    parser.add_argument("--out", help="Optional output JSON path.")
    parser.add_argument("--catalog-dir", help="Optional directory to receive one profile JSON per analysis file.")
    parser.add_argument("--index-out", help="Optional path for a catalog index JSON.")
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


def _mapping_section(value) -> dict:
    return value if isinstance(value, dict) else {}


def _wavetable_refs(instance: dict) -> list[str]:
    value = instance.get("wavetables")
    if isinstance(value, dict):
        refs = value.values()
    elif isinstance(value, list):
        refs = value
    else:
        refs = []
    return sorted({ref for ref in refs if isinstance(ref, str) and ref})


def _first_filter_freq(instance: dict) -> float | None:
    for filter_row in _mapping_section(instance.get("filters")).values():
        value = filter_row.get("kParamFreq")
        if isinstance(value, (int, float)):
            return float(value)
    return None


def _max_filter_drive(instance: dict) -> float | None:
    drives = []
    for filter_row in _mapping_section(instance.get("filters")).values():
        value = filter_row.get("kParamDrive")
        if isinstance(value, (int, float)):
            drives.append(float(value))
    return max(drives) if drives else None


def _has_unisonish_hint(instance: dict) -> bool:
    for osc_row in _mapping_section(instance.get("oscillators")).values():
        for key, value in osc_row.items():
            if "unison" in key.lower() and isinstance(value, (int, float)) and value not in (0, 1):
                return True
    return False


def _low_octave_hint(instance: dict) -> bool:
    for osc_row in _mapping_section(instance.get("oscillators")).values():
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
            "wavetable_refs": _wavetable_refs(instance),
            "oscillator_count": len(_mapping_section(instance.get("oscillators"))),
            "filter_count": len(_mapping_section(instance.get("filters"))),
            "envelope_count": len(_mapping_section(instance.get("envelopes"))),
            "lfo_count": len(_mapping_section(instance.get("lfos"))),
            "mod_route_count": len(_mapping_section(instance.get("mod_matrix")))
        },
        "synthesis": {
            "wavetables": instance.get("wavetables") if instance.get("wavetables") is not None else {},
            "oscillators": _mapping_section(instance.get("oscillators")),
            "filters": _mapping_section(instance.get("filters")),
            "envelopes": _mapping_section(instance.get("envelopes")),
            "lfos": _mapping_section(instance.get("lfos")),
            "mod_matrix": _mapping_section(instance.get("mod_matrix")),
            "global": _mapping_section(instance.get("global")),
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


def build_catalog(analysis_paths: list[Path]) -> dict:
    analyses = []
    total_profiles = 0
    role_counts: dict[str, int] = {}
    tone_counts: dict[str, int] = {}
    mix_counts: dict[str, int] = {}
    profile_summaries = []
    for analysis_path in analysis_paths:
        profiles = build_profiles(analysis_path)
        total_profiles += len(profiles)
        for profile in profiles:
            for role in profile["classification"]["role_candidates"]:
                role_counts[role] = role_counts.get(role, 0) + 1
            for tone in profile["classification"]["tone_tags"]:
                tone_counts[tone] = tone_counts.get(tone, 0) + 1
            for mix in profile["classification"]["mix_tags"]:
                mix_counts[mix] = mix_counts.get(mix, 0) + 1
            profile_summaries.append({
                "profile_id": profile["profile_id"],
                "analysis_slug": profile["source"]["analysis_slug"],
                "track": profile["source"]["track"],
                "role_candidates": profile["classification"]["role_candidates"],
                "tone_tags": profile["classification"]["tone_tags"],
                "mix_tags": profile["classification"]["mix_tags"],
                "wavetable_refs": profile["summary"]["wavetable_refs"],
            })
        analyses.append({
            "analysis_path": str(analysis_path),
            "analysis_stem": analysis_path.stem,
            "profile_count": len(profiles),
            "profile_ids": [profile["profile_id"] for profile in profiles],
            "tracks": [profile["source"]["track"] for profile in profiles],
        })
    return {
        "profile_version": PROFILE_VERSION,
        "analysis_count": len(analysis_paths),
        "profile_count": total_profiles,
        "role_counts": dict(sorted(role_counts.items())),
        "tone_counts": dict(sorted(tone_counts.items())),
        "mix_counts": dict(sorted(mix_counts.items())),
        "profiles": profile_summaries,
        "analyses": analyses,
    }


def main() -> None:
    parser = make_parser()
    args = parser.parse_args()
    if bool(args.analysis_json) == bool(args.analysis_dir):
        parser.error("pass exactly one of --analysis-json or --analysis-dir")

    if args.analysis_json:
        analysis_path = Path(args.analysis_json)
        profiles = build_profiles(analysis_path)
        output = json.dumps(profiles, indent=2) + "\n"
        if args.out:
            Path(args.out).write_text(output)
        print(output, end="")
        return

    analysis_dir = Path(args.analysis_dir)
    analysis_paths = sorted(analysis_dir.glob(args.glob))
    if not analysis_paths:
        parser.error(f"no files matched {args.glob!r} under {analysis_dir}")

    catalog = build_catalog(analysis_paths)
    if args.catalog_dir:
        catalog_dir = Path(args.catalog_dir)
        catalog_dir.mkdir(parents=True, exist_ok=True)
        for analysis_path in analysis_paths:
            out_path = catalog_dir / f"{analysis_path.stem}-profiles.json"
            out_path.write_text(json.dumps(build_profiles(analysis_path), indent=2) + "\n")
    if args.index_out:
        Path(args.index_out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.index_out).write_text(json.dumps(catalog, indent=2) + "\n")
    print(json.dumps(catalog, indent=2))


if __name__ == "__main__":
    main()
