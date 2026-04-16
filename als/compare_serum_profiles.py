#!/usr/bin/env python3
"""
compare_serum_profiles.py

Compare two Serum profiles, highlight likely clashes or complements, and attach
targeted mutation goals to separate them when needed.

Examples:
    python3 als/compare_serum_profiles.py --left mph-raw:bass:i1 --right mph-raw:lead:i3
    python3 als/compare_serum_profiles.py --left mph-raw:bass:i1 --right mph-raw:reese:i5 --format json
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    from search_serum_profiles import load_profiles, _audio_summary
    from serum_mutation_rules import suggest_for_goal
except ModuleNotFoundError:
    from .search_serum_profiles import load_profiles, _audio_summary
    from .serum_mutation_rules import suggest_for_goal


DEFAULT_CATALOG_DIR = Path("als/catalog/profiles")


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Compare two Serum profiles for clash/complement analysis.")
    parser.add_argument("--catalog-dir", default=str(DEFAULT_CATALOG_DIR), help="Directory of generated *-profiles.json files.")
    parser.add_argument("--left", required=True, help="Left profile id.")
    parser.add_argument("--right", required=True, help="Right profile id.")
    parser.add_argument("--mutation-limit", type=int, default=4, help="Maximum mutation suggestions per side. Default: 4")
    parser.add_argument("--format", choices=["json", "text"], default="text", help="Output format.")
    return parser


def _profile_map(catalog_dir: Path) -> dict[str, dict]:
    return {profile["profile_id"]: profile for profile in load_profiles(catalog_dir)}


def _audio_metric(profile: dict, key: str) -> float | None:
    summary = _audio_summary(profile)
    if not summary:
        return None
    value = summary.get("summary", {}).get(key)
    return value if isinstance(value, (int, float)) else None


def _suggest(profile: dict, goals: list[str], limit: int) -> list[dict]:
    suggestions = []
    for goal in goals:
        suggestions.extend(suggest_for_goal(profile, goal))
    suggestions.sort(key=lambda row: (-row["priority"], row["goal"], row["path"]))
    return suggestions[:limit]


def build_report(left: dict, right: dict, mutation_limit: int) -> dict:
    left_roles = set(left["classification"]["role_candidates"])
    right_roles = set(right["classification"]["role_candidates"])
    left_tone = set(left["classification"]["tone_tags"])
    right_tone = set(right["classification"]["tone_tags"])
    left_mix = set(left["classification"]["mix_tags"])
    right_mix = set(right["classification"]["mix_tags"])

    conflicts = []
    complements = []
    left_goals: list[str] = []
    right_goals: list[str] = []

    if "low_end_anchor" in left_mix and "low_end_anchor" in right_mix:
        conflicts.append("Both parts read as low_end_anchor, so the low end may stack up too heavily.")
        if "bass" in left_roles or "sub" in left_roles:
            right_goals.extend(["less_sub", "cleaner"])
            left_goals.append("mono_safer")
        elif "bass" in right_roles or "sub" in right_roles:
            left_goals.extend(["less_sub", "cleaner"])
            right_goals.append("mono_safer")
        else:
            left_goals.append("less_sub")
            right_goals.append("less_sub")

    if "side_heavy" in left_mix and "side_heavy" in right_mix:
        conflicts.append("Both parts are side-heavy, which risks stereo crowding.")
        left_goals.append("mono_safer")
        right_goals.append("mono_safer")

    if "mid_focus" in left_mix and "mid_focus" in right_mix:
        conflicts.append("Both parts want the forward midrange position.")
        if "lead" in left_roles or "pluck" in left_roles or "stab" in left_roles:
            left_goals.append("more_presence")
            right_goals.append("less_busy")
        if "lead" in right_roles or "pluck" in right_roles or "stab" in right_roles:
            right_goals.append("more_presence")
            left_goals.append("less_busy")

    if "background" in left_mix and "mid_focus" in right_mix:
        complements.append("Left part sits back while right part reads forward, which is a useful arrangement split.")
    if "background" in right_mix and "mid_focus" in left_mix:
        complements.append("Right part sits back while left part reads forward, which is a useful arrangement split.")

    left_centroid = _audio_metric(left, "mean_centroid_hz")
    right_centroid = _audio_metric(right, "mean_centroid_hz")
    if left_centroid is not None and right_centroid is not None:
        delta = abs(left_centroid - right_centroid)
        if delta <= 180:
            conflicts.append("Rendered centroids are very close, suggesting spectral overlap.")
            if left_centroid <= right_centroid:
                left_goals.append("darker")
                right_goals.append("more_presence")
            else:
                right_goals.append("darker")
                left_goals.append("more_presence")
        elif delta >= 700:
            complements.append("Rendered centroids are well separated, suggesting a clearer spectral split.")

    left_attack = _audio_metric(left, "mean_attack_time_ms")
    right_attack = _audio_metric(right, "mean_attack_time_ms")
    if left_attack is not None and right_attack is not None and left_attack <= 40 and right_attack <= 40:
        conflicts.append("Both rendered attacks are fast, so transient collisions are likely.")
        left_goals.append("softer_attack")
        right_goals.append("softer_attack")

    if "wide" in left_tone and "dark" in right_tone:
        complements.append("A wide left part against a darker right part can create a useful contrast.")
    if "wide" in right_tone and "dark" in left_tone:
        complements.append("A wide right part against a darker left part can create a useful contrast.")

    left_goal_list = sorted(dict.fromkeys(left_goals))
    right_goal_list = sorted(dict.fromkeys(right_goals))

    return {
        "left": {
            "profile_id": left["profile_id"],
            "track": left["source"].get("track"),
            "roles": left["classification"]["role_candidates"],
            "tone_tags": left["classification"]["tone_tags"],
            "mix_tags": left["classification"]["mix_tags"],
            "audio_status": left.get("audio_reference", {}).get("status"),
            "audio_summary": (_audio_summary(left) or {}).get("summary"),
            "suggested_goals": left_goal_list,
            "mutation_suggestions": _suggest(left, left_goal_list, mutation_limit),
        },
        "right": {
            "profile_id": right["profile_id"],
            "track": right["source"].get("track"),
            "roles": right["classification"]["role_candidates"],
            "tone_tags": right["classification"]["tone_tags"],
            "mix_tags": right["classification"]["mix_tags"],
            "audio_status": right.get("audio_reference", {}).get("status"),
            "audio_summary": (_audio_summary(right) or {}).get("summary"),
            "suggested_goals": right_goal_list,
            "mutation_suggestions": _suggest(right, right_goal_list, mutation_limit),
        },
        "conflicts": conflicts,
        "complements": complements,
    }


def render_text(report: dict) -> str:
    lines = []
    lines.append("# Serum Profile Comparison")
    lines.append("")
    for side_name in ("left", "right"):
        side = report[side_name]
        lines.append(
            f"- `{side_name}` `{side['profile_id']}` :: {side['track'] or '-'} "
            f"[roles: {', '.join(side['roles'])}; tone: {', '.join(side['tone_tags'])}; "
            f"mix: {', '.join(side['mix_tags'])}; audio: {side['audio_status']}]"
        )
        if side.get("audio_summary"):
            summary = side["audio_summary"]
            lines.append(
                f"  audio summary: centroid={summary.get('mean_centroid_hz')}, "
                f"attack_ms={summary.get('mean_attack_time_ms')}, "
                f"side_ratio={summary.get('mean_side_ratio')}, "
                f"rms_dbfs={summary.get('mean_rms_dbfs')}"
            )
        if side["suggested_goals"]:
            lines.append(f"  suggested goals: {', '.join(side['suggested_goals'])}")
        for item in side["mutation_suggestions"]:
            lines.append(
                f"  mutate `{item['path']}` :: {item['action']} "
                f"{item['current_value']} -> {item['suggested_value']} "
                f"[goal: {item['goal']}]"
            )
    lines.append("")
    lines.append("## Conflicts")
    if report["conflicts"]:
        for note in report["conflicts"]:
            lines.append(f"- {note}")
    else:
        lines.append("- none")
    lines.append("")
    lines.append("## Complements")
    if report["complements"]:
        for note in report["complements"]:
            lines.append(f"- {note}")
    else:
        lines.append("- none")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = make_parser()
    args = parser.parse_args()
    profiles = _profile_map(Path(args.catalog_dir))
    if args.left not in profiles:
        parser.error(f"profile not found: {args.left}")
    if args.right not in profiles:
        parser.error(f"profile not found: {args.right}")
    report = build_report(profiles[args.left], profiles[args.right], args.mutation_limit)
    if args.format == "json":
        print(json.dumps(report, indent=2))
        return
    print(render_text(report), end="")


if __name__ == "__main__":
    main()
