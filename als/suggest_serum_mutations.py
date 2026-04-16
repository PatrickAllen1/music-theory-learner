#!/usr/bin/env python3
"""
suggest_serum_mutations.py

Suggest targeted Serum parameter moves for a normalized preset profile based on
high-level sound goals.

Examples:
    python3 als/suggest_serum_mutations.py --profile-id mph-raw:bass:i1 --goal darker
    python3 als/suggest_serum_mutations.py --profile-id mph-raw:bass:i1 --goal tighter --goal mono_safer --format json
    python3 als/suggest_serum_mutations.py --list-goals
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    from serum_mutation_rules import MUTATION_GOALS, list_supported_goals, suggest_for_goal
except ModuleNotFoundError:
    from .serum_mutation_rules import MUTATION_GOALS, list_supported_goals, suggest_for_goal


DEFAULT_CATALOG_DIR = Path("als/catalog/profiles")


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Suggest Serum parameter changes from normalized profiles.")
    parser.add_argument("--catalog-dir", default=str(DEFAULT_CATALOG_DIR), help="Directory of generated *-profiles.json files.")
    parser.add_argument("--profile-id", help="Target profile id from the generated catalog.")
    parser.add_argument("--profile-json", help="Optional path to a single profile JSON file or a list containing one profile.")
    parser.add_argument("--goal", action="append", default=[], help="Sound-design goal. Pass multiple times.")
    parser.add_argument("--limit", type=int, default=12, help="Maximum number of suggestions to return. Default: 12")
    parser.add_argument("--format", choices=["json", "text"], default="text", help="Output format.")
    parser.add_argument("--list-goals", action="store_true", help="List supported goals and exit.")
    return parser


def load_profiles(catalog_dir: Path) -> list[dict]:
    profiles = []
    for path in sorted(catalog_dir.glob("*-profiles.json")):
        profiles.extend(json.loads(path.read_text()))
    return profiles


def load_profile_from_json(path: Path) -> dict:
    payload = json.loads(path.read_text())
    if isinstance(payload, list):
        if len(payload) != 1:
            raise ValueError("profile JSON list must contain exactly one profile")
        return payload[0]
    return payload


def render_text(report: dict) -> str:
    lines = []
    lines.append("# Serum Mutation Suggestions")
    lines.append("")
    lines.append(f"- profile: `{report['profile']['profile_id']}`")
    lines.append(f"- track: {report['profile']['source'].get('track') or '-'}")
    lines.append(f"- goals: {', '.join(report['goals'])}")
    lines.append("")
    for item in report["suggestions"]:
        lines.append(
            f"- `{item['path']}` :: {item['action']} "
            f"{item['current_value']} -> {item['suggested_value']} "
            f"[goal: {item['goal']}; section: {item['section']}]"
        )
        lines.append(f"  {item['rationale']}")
    if not report["suggestions"]:
        lines.append("- No actionable suggestions for the current parsed profile shape.")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = make_parser()
    args = parser.parse_args()
    if args.list_goals:
        payload = {"supported_goals": list_supported_goals()}
        if args.format == "json":
            print(json.dumps(payload, indent=2))
        else:
            for row in payload["supported_goals"]:
                print(f"- {row['goal']}: {row['description']}")
        return

    if not args.goal:
        parser.error("pass at least one --goal")
    if bool(args.profile_id) == bool(args.profile_json):
        parser.error("pass exactly one of --profile-id or --profile-json")

    invalid = [goal for goal in args.goal if goal not in MUTATION_GOALS]
    if invalid:
        parser.error(f"unsupported goals: {', '.join(sorted(invalid))}")

    if args.profile_json:
        profile = load_profile_from_json(Path(args.profile_json))
    else:
        profiles = load_profiles(Path(args.catalog_dir))
        by_id = {profile["profile_id"]: profile for profile in profiles}
        if args.profile_id not in by_id:
            parser.error(f"profile not found: {args.profile_id}")
        profile = by_id[args.profile_id]

    suggestions = []
    for goal in args.goal:
        suggestions.extend(suggest_for_goal(profile, goal))
    suggestions.sort(key=lambda row: (-row["priority"], row["goal"], row["path"]))
    suggestions = suggestions[: args.limit]
    report = {
        "profile": {
            "profile_id": profile["profile_id"],
            "track": profile["source"].get("track"),
            "role_candidates": profile["classification"]["role_candidates"],
            "tone_tags": profile["classification"]["tone_tags"],
            "mix_tags": profile["classification"]["mix_tags"],
        },
        "goals": args.goal,
        "suggestions": suggestions,
    }
    if args.format == "json":
        print(json.dumps(report, indent=2))
        return
    print(render_text(report), end="")


if __name__ == "__main__":
    main()
