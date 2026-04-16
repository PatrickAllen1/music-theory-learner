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


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build small Serum preset palettes from the generated profile catalog.")
    parser.add_argument("--catalog-dir", default=str(DEFAULT_CATALOG_DIR), help="Directory of generated *-profiles.json files.")
    parser.add_argument("--role", action="append", required=True, help="Required palette role. Pass multiple times.")
    parser.add_argument("--target-tone", action="append", default=[], help="Preferred tone tags for the whole palette.")
    parser.add_argument("--target-mix", action="append", default=[], help="Preferred mix tags for the whole palette.")
    parser.add_argument("--per-role-limit", type=int, default=5, help="Max candidates per requested role. Default: 5")
    parser.add_argument("--palette-limit", type=int, default=5, help="Max palette suggestions to return. Default: 5")
    parser.add_argument("--format", choices=["json", "text"], default="text", help="Output format.")
    return parser


def candidate_profiles(profiles: list[dict], role: str, per_role_limit: int, target_tones: list[str], target_mixes: list[str]) -> list[dict]:
    matches = []
    for profile in profiles:
        roles = set(profile["classification"]["role_candidates"])
        if role not in roles:
            continue
        score = 0
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
        matches.append((score, profile))
    matches.sort(key=lambda item: (-item[0], item[1]["profile_id"]))
    return [profile for _, profile in matches[:per_role_limit]]


def palette_score(palette: list[tuple[str, dict]], target_tones: list[str], target_mixes: list[str]) -> tuple[int, list[str]]:
    score = 0
    notes = []
    seen_ids = {profile["profile_id"] for _, profile in palette}
    if len(seen_ids) != len(palette):
        return -9999, ["Duplicate profile reused across roles."]

    side_heavy_count = 0
    low_end_count = 0
    background_count = 0
    mid_focus_count = 0
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

        if role in ("bass", "sub", "reese") and "low_end_anchor" in mixes:
            score += 4
        if role == "pad" and "background" in mixes:
            score += 4
        if role in ("lead", "pluck", "stab") and "mid_focus" in mixes:
            score += 4

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
    return score, notes


def build_report(profiles: list[dict], roles: list[str], target_tones: list[str], target_mixes: list[str], per_role_limit: int, palette_limit: int) -> dict:
    by_role = {
        role: candidate_profiles(profiles, role, per_role_limit, target_tones, target_mixes)
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
        score, notes = palette_score(palette, target_tones, target_mixes)
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
                }
                for role, profile in palette
            ],
        })
    combos.sort(key=lambda row: (-row["score"], [entry["profile_id"] for entry in row["entries"]]))
    return {
        "roles": roles,
        "target_tones": target_tones,
        "target_mixes": target_mixes,
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
    )
    if args.format == "json":
        print(json.dumps(report, indent=2))
        return
    print(render_text(report), end="")


if __name__ == "__main__":
    main()
