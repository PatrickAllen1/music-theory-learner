#!/usr/bin/env python3
"""
palette_builder.py

Build small preset palettes from the generated Serum profile catalog.

Examples:
    python3 als/palette_builder.py --role bass --role pad --role lead
    python3 als/palette_builder.py --role bass --role pad --role pluck --target-tone dark
"""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path

try:
    from search_serum_profiles import load_profiles
except ModuleNotFoundError:
    from .search_serum_profiles import load_profiles


DEFAULT_CATALOG_DIR = Path("als/catalog/profiles")
_AUDIO_SUMMARY_CACHE: dict[str, dict | None] = {}


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build small Serum preset palettes from the generated profile catalog.")
    parser.add_argument("--catalog-dir", default=str(DEFAULT_CATALOG_DIR), help="Directory of generated *-profiles.json files.")
    parser.add_argument("--role", action="append", required=True, help="Required palette role. Pass multiple times.")
    parser.add_argument("--target-tone", action="append", default=[], help="Preferred tone tags for the whole palette.")
    parser.add_argument("--target-mix", action="append", default=[], help="Preferred mix tags for the whole palette.")
    parser.add_argument("--prefer-rendered", action="store_true", help="Prefer profiles with attached rendered audio summaries.")
    parser.add_argument("--per-role-limit", type=int, default=5, help="Max candidates per requested role. Default: 5")
    parser.add_argument("--palette-limit", type=int, default=5, help="Max palette suggestions to return. Default: 5")
    parser.add_argument("--format", choices=["json", "text"], default="text", help="Output format.")
    return parser


def _audio_summary(profile: dict) -> dict | None:
    descriptor_path = profile.get("audio_reference", {}).get("descriptor_path")
    if not descriptor_path:
        return None
    if descriptor_path in _AUDIO_SUMMARY_CACHE:
        return _AUDIO_SUMMARY_CACHE[descriptor_path]
    path = Path(descriptor_path)
    if not path.exists():
        _AUDIO_SUMMARY_CACHE[descriptor_path] = None
        return None
    summary = json.loads(path.read_text())
    _AUDIO_SUMMARY_CACHE[descriptor_path] = summary
    return summary


def _audio_metric(profile: dict, key: str) -> float | None:
    summary = _audio_summary(profile)
    if not summary:
        return None
    value = summary.get("summary", {}).get(key)
    return value if isinstance(value, (int, float)) else None


def _role_audio_score(role: str, profile: dict) -> tuple[int, list[str]]:
    score = 0
    notes = []
    audio = _audio_summary(profile)
    if not audio:
        return score, notes

    centroid = _audio_metric(profile, "mean_centroid_hz")
    side_ratio = _audio_metric(profile, "mean_side_ratio")
    attack_ms = _audio_metric(profile, "mean_attack_time_ms")
    score += 1
    notes.append("Rendered audio summary available.")

    if role in {"bass", "sub", "reese"}:
        if centroid is not None and centroid <= 900:
            score += 2
            notes.append("Audio centroid stays low enough for bass duty.")
        if side_ratio is not None and side_ratio <= 0.45:
            score += 2
            notes.append("Audio side ratio is restrained for a steadier low-end anchor.")
    if role == "pad":
        if side_ratio is not None and side_ratio >= 0.2:
            score += 2
            notes.append("Pad render has enough stereo spread to sit behind the center.")
        if attack_ms is not None and attack_ms >= 8:
            score += 1
            notes.append("Pad render has a slower attack profile.")
    if role in {"lead", "pluck", "stab"}:
        if centroid is not None and centroid >= 700:
            score += 2
            notes.append("Lead/pluck render has enough top-end presence.")
        if attack_ms is not None and attack_ms <= 80:
            score += 1
            notes.append("Lead/pluck render stays reasonably immediate.")
    if role == "fx":
        if side_ratio is not None and side_ratio >= 0.3:
            score += 1
            notes.append("FX render has useful width for transitional placement.")
    return score, notes


def candidate_profiles(
    profiles: list[dict],
    role: str,
    per_role_limit: int,
    target_tones: list[str],
    target_mixes: list[str],
    prefer_rendered: bool,
) -> list[dict]:
    matches = []
    for profile in profiles:
        roles = set(profile["classification"]["role_candidates"])
        if role not in roles:
            continue
        score = 0
        notes = []
        tones = set(profile["classification"]["tone_tags"])
        mixes = set(profile["classification"]["mix_tags"])
        score += len(set(target_tones) & tones) * 4
        score += len(set(target_mixes) & mixes) * 3
        if role == "bass" and "low_end_anchor" in mixes:
            score += 5
        if role == "pad" and "background" in mixes:
            score += 5
        if role in ("lead", "pluck", "stab") and "mid_focus" in mixes:
            score += 5
        if role == "sub" and "low_end_anchor" in mixes:
            score += 6
        audio_score, audio_notes = _role_audio_score(role, profile)
        if prefer_rendered:
            score += audio_score
            notes.extend(audio_notes)
        matches.append((score, profile, notes))
    matches.sort(key=lambda item: (-item[0], item[1]["profile_id"]))
    result = []
    for score, profile, notes in matches[:per_role_limit]:
        enriched = dict(profile)
        enriched["_palette_candidate_score"] = score
        enriched["_palette_candidate_notes"] = notes
        result.append(enriched)
    return result


def palette_score(palette: list[tuple[str, dict]], target_tones: list[str], target_mixes: list[str], prefer_rendered: bool) -> tuple[int, list[str]]:
    score = 0
    notes = []
    seen_ids = {profile["profile_id"] for _, profile in palette}
    if len(seen_ids) != len(palette):
        return -9999, ["Duplicate profile reused across roles."]

    side_heavy_count = 0
    low_end_count = 0
    background_count = 0
    mid_focus_count = 0
    rendered_count = 0
    analysis_slugs = set()

    for role, profile in palette:
        tones = set(profile["classification"]["tone_tags"])
        mixes = set(profile["classification"]["mix_tags"])
        analysis_slug = profile["source"].get("analysis_slug")
        if analysis_slug:
            analysis_slugs.add(analysis_slug)
        score += len(set(target_tones) & tones) * 3
        score += len(set(target_mixes) & mixes) * 2
        if "side_heavy" in mixes:
            side_heavy_count += 1
        if "low_end_anchor" in mixes:
            low_end_count += 1
        if "background" in mixes:
            background_count += 1
        if "mid_focus" in mixes:
            mid_focus_count += 1
        if profile.get("audio_reference", {}).get("status") == "rendered":
            rendered_count += 1

        if role in ("bass", "sub", "reese") and "low_end_anchor" in mixes:
            score += 4
        if role == "pad" and "background" in mixes:
            score += 4
        if role in ("lead", "pluck", "stab") and "mid_focus" in mixes:
            score += 4
        if prefer_rendered:
            score += profile.get("_palette_candidate_score", 0)
            notes.extend(profile.get("_palette_candidate_notes", []))

    if low_end_count >= 2:
        score -= 6
        notes.append("Multiple low-end anchors may compete.")
    if side_heavy_count >= 2:
        score -= 5
        notes.append("Multiple side-heavy parts may crowd the stereo field.")
    if background_count == 0 and any(role == "pad" for role, _ in palette):
        score -= 2
        notes.append("Pad choice is not clearly background-oriented.")
    if mid_focus_count == 0 and any(role in ("lead", "pluck", "stab") for role, _ in palette):
        score -= 2
        notes.append("Melodic choice is not clearly forward in the mids.")
    if len(analysis_slugs) >= 2:
        score += 1
        notes.append("Palette pulls from more than one reference analysis set.")
    if prefer_rendered and rendered_count == len(palette):
        score += 3
        notes.append("Every palette part has rendered audio evidence.")
    return score, notes


def build_report(
    profiles: list[dict],
    roles: list[str],
    target_tones: list[str],
    target_mixes: list[str],
    per_role_limit: int,
    palette_limit: int,
    prefer_rendered: bool,
) -> dict:
    by_role = {
        role: candidate_profiles(profiles, role, per_role_limit, target_tones, target_mixes, prefer_rendered)
        for role in roles
    }
    combos = []
    role_lists = [by_role[role] for role in roles]
    if any(not candidates for candidates in role_lists):
        return {
            "roles": roles,
            "target_tones": target_tones,
            "target_mixes": target_mixes,
            "candidate_counts": {role: len(rows) for role, rows in by_role.items()},
            "palettes": [],
        }

    for combo in itertools.product(*role_lists):
        palette = list(zip(roles, combo))
        score, notes = palette_score(palette, target_tones, target_mixes, prefer_rendered)
        combos.append({
            "score": score,
            "notes": notes,
            "entries": [
                {
                    "role": role,
                    "profile_id": profile["profile_id"],
                    "track": profile["source"].get("track"),
                    "analysis_slug": profile["source"].get("analysis_slug"),
                    "tone_tags": profile["classification"]["tone_tags"],
                    "mix_tags": profile["classification"]["mix_tags"],
                    "audio_status": profile.get("audio_reference", {}).get("status"),
                    "audio_summary": (_audio_summary(profile) or {}).get("summary"),
                }
                for role, profile in palette
            ],
        })
    combos.sort(key=lambda row: (-row["score"], [entry["profile_id"] for entry in row["entries"]]))
    return {
        "roles": roles,
        "target_tones": target_tones,
        "target_mixes": target_mixes,
        "prefer_rendered": prefer_rendered,
        "candidate_counts": {role: len(rows) for role, rows in by_role.items()},
        "palettes": combos[:palette_limit],
    }


def render_text(report: dict) -> str:
    lines = []
    lines.append("# Serum Palette Suggestions")
    lines.append("")
    lines.append(f"- roles: {', '.join(report['roles'])}")
    lines.append(f"- target tones: {', '.join(report['target_tones']) or '-'}")
    lines.append(f"- target mixes: {', '.join(report['target_mixes']) or '-'}")
    lines.append(f"- prefer rendered: {'yes' if report['prefer_rendered'] else 'no'}")
    lines.append("")
    lines.append("## Candidate Counts")
    for role, count in report["candidate_counts"].items():
        lines.append(f"- `{role}`: {count}")
    lines.append("")
    for index, palette in enumerate(report["palettes"], 1):
        lines.append(f"## Palette {index} (score: {palette['score']})")
        for entry in palette["entries"]:
            lines.append(
                f"- `{entry['role']}` -> `{entry['profile_id']}` "
                f"({entry['track'] or '-'}; tone: {', '.join(entry['tone_tags'])}; mix: {', '.join(entry['mix_tags'])})"
            )
            if entry.get("audio_summary"):
                summary = entry["audio_summary"]
                lines.append(
                    f"  audio: status={entry['audio_status']}; centroid={summary.get('mean_centroid_hz')}; "
                    f"attack_ms={summary.get('mean_attack_time_ms')}; side_ratio={summary.get('mean_side_ratio')}"
                )
        if palette["notes"]:
            lines.append(f"- notes: {' | '.join(palette['notes'])}")
        lines.append("")
    if not report["palettes"]:
        lines.append("No palette suggestions found for the requested role set.")
        lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = make_parser()
    args = parser.parse_args()
    profiles = load_profiles(Path(args.catalog_dir))
    report = build_report(
        profiles=profiles,
        roles=args.role,
        target_tones=args.target_tone,
        target_mixes=args.target_mix,
        per_role_limit=args.per_role_limit,
        palette_limit=args.palette_limit,
        prefer_rendered=args.prefer_rendered,
    )
    if args.format == "json":
        print(json.dumps(report, indent=2))
        return
    print(render_text(report), end="")


if __name__ == "__main__":
    main()
