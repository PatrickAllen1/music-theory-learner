#!/usr/bin/env python3
"""
recommend_serum_part.py

Recommend Serum profiles for a musical role and include mutation suggestions
for target sound goals.

Examples:
    python3 als/recommend_serum_part.py --role bass --goal darker --goal mono_safer
    python3 als/recommend_serum_part.py --role lead --tone bright --prefer-rendered --goal tighter --goal more_presence
"""

from __future__ import annotations

import argparse
import json
from argparse import Namespace
from pathlib import Path

try:
    from search_serum_profiles import load_profiles, profile_matches, score_profile, _audio_summary
    from suggest_serum_mutations import MUTATION_GOALS, render_text as render_mutation_text
    from serum_mutation_rules import suggest_for_goal
except ModuleNotFoundError:
    from .search_serum_profiles import load_profiles, profile_matches, score_profile, _audio_summary
    from .suggest_serum_mutations import MUTATION_GOALS
    from .serum_mutation_rules import suggest_for_goal


DEFAULT_CATALOG_DIR = Path("als/catalog/profiles")


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Recommend Serum presets for a specific musical part.")
    parser.add_argument("--catalog-dir", default=str(DEFAULT_CATALOG_DIR), help="Directory of generated *-profiles.json files.")
    parser.add_argument("--role", required=True, help="Required role candidate, e.g. bass, pad, lead.")
    parser.add_argument("--tone", action="append", default=[], help="Preferred tone tags. Pass multiple times.")
    parser.add_argument("--mix", action="append", default=[], help="Preferred mix tags. Pass multiple times.")
    parser.add_argument("--track", help="Case-insensitive substring match against track name.")
    parser.add_argument("--analysis", help="Case-insensitive substring match against analysis slug.")
    parser.add_argument("--wavetable", action="append", default=[], help="Case-insensitive substring match against wavetable refs.")
    parser.add_argument("--dest-module", action="append", default=[], help="Substring match against mod-matrix destination modules.")
    parser.add_argument("--rendered-only", action="store_true", help="Only consider profiles with attached rendered audio.")
    parser.add_argument("--prefer-rendered", action="store_true", help="Slightly prefer profiles with attached rendered audio.")
    parser.add_argument("--min-centroid-hz", type=float, help="Minimum mean spectral centroid from attached audio summaries.")
    parser.add_argument("--max-centroid-hz", type=float, help="Maximum mean spectral centroid from attached audio summaries.")
    parser.add_argument("--min-side-ratio", type=float, help="Minimum mean stereo side ratio from attached audio summaries.")
    parser.add_argument("--max-side-ratio", type=float, help="Maximum mean stereo side ratio from attached audio summaries.")
    parser.add_argument("--min-attack-ms", type=float, help="Minimum mean attack time from attached audio summaries.")
    parser.add_argument("--max-attack-ms", type=float, help="Maximum mean attack time from attached audio summaries.")
    parser.add_argument("--min-rms-dbfs", type=float, help="Minimum mean RMS dBFS from attached audio summaries.")
    parser.add_argument("--max-rms-dbfs", type=float, help="Maximum mean RMS dBFS from attached audio summaries.")
    parser.add_argument("--goal", action="append", default=[], help="Desired sound-design goals to attach mutation suggestions to.")
    parser.add_argument("--limit", type=int, default=5, help="Maximum candidates to return. Default: 5")
    parser.add_argument("--mutation-limit", type=int, default=6, help="Maximum mutation suggestions per candidate. Default: 6")
    parser.add_argument("--format", choices=["json", "text"], default="text", help="Output format.")
    return parser


def _search_namespace(args: argparse.Namespace) -> Namespace:
    return Namespace(
        role=[args.role],
        tone=args.tone,
        mix=args.mix,
        track=args.track,
        analysis=args.analysis,
        wavetable=args.wavetable,
        dest_module=args.dest_module,
        rendered_only=args.rendered_only,
        min_centroid_hz=args.min_centroid_hz,
        max_centroid_hz=args.max_centroid_hz,
        min_side_ratio=args.min_side_ratio,
        max_side_ratio=args.max_side_ratio,
        min_attack_ms=args.min_attack_ms,
        max_attack_ms=args.max_attack_ms,
        min_rms_dbfs=args.min_rms_dbfs,
        max_rms_dbfs=args.max_rms_dbfs,
    )


def _validate_goals(goals: list[str]) -> None:
    invalid = [goal for goal in goals if goal not in MUTATION_GOALS]
    if invalid:
        raise ValueError(f"unsupported goals: {', '.join(sorted(invalid))}")


def build_report(args: argparse.Namespace) -> dict:
    profiles = load_profiles(Path(args.catalog_dir))
    search_args = _search_namespace(args)
    matches = [profile for profile in profiles if profile_matches(profile, search_args)]
    matches.sort(
        key=lambda profile: (
            -(score_profile(profile, search_args) + (1 if args.prefer_rendered and profile.get("audio_reference", {}).get("status") == "rendered" else 0)),
            profile["profile_id"],
        )
    )
    candidates = []
    for profile in matches[: args.limit]:
        suggestions = []
        for goal in args.goal:
            suggestions.extend(suggest_for_goal(profile, goal))
        suggestions.sort(key=lambda row: (-row["priority"], row["goal"], row["path"]))
        suggestions = suggestions[: args.mutation_limit]
        candidates.append({
            "profile_id": profile["profile_id"],
            "track": profile["source"].get("track"),
            "analysis_slug": profile["source"].get("analysis_slug"),
            "role_candidates": profile["classification"]["role_candidates"],
            "tone_tags": profile["classification"]["tone_tags"],
            "mix_tags": profile["classification"]["mix_tags"],
            "notes": profile["classification"].get("notes") or [],
            "audio_status": profile.get("audio_reference", {}).get("status"),
            "audio_summary": (_audio_summary(profile) or {}).get("summary"),
            "mutation_suggestions": suggestions,
        })
    return {
        "role": args.role,
        "filters": {
            "tone": args.tone,
            "mix": args.mix,
            "track": args.track,
            "analysis": args.analysis,
            "wavetable": args.wavetable,
            "dest_module": args.dest_module,
            "rendered_only": args.rendered_only,
            "prefer_rendered": args.prefer_rendered,
        },
        "goals": args.goal,
        "candidate_count": len(candidates),
        "candidates": candidates,
    }


def render_text(report: dict) -> str:
    lines = []
    lines.append("# Serum Part Recommendations")
    lines.append("")
    lines.append(f"- role: `{report['role']}`")
    lines.append(f"- goals: {', '.join(report['goals']) or '-'}")
    lines.append(f"- candidates: {report['candidate_count']}")
    lines.append("")
    for candidate in report["candidates"]:
        lines.append(
            f"- `{candidate['profile_id']}` :: {candidate['track'] or '-'} "
            f"[tone: {', '.join(candidate['tone_tags'])}; mix: {', '.join(candidate['mix_tags'])}; "
            f"audio: {candidate['audio_status']}]"
        )
        if candidate.get("audio_summary"):
            summary = candidate["audio_summary"]
            lines.append(
                f"  audio summary: centroid={summary.get('mean_centroid_hz')}, "
                f"attack_ms={summary.get('mean_attack_time_ms')}, "
                f"side_ratio={summary.get('mean_side_ratio')}, "
                f"rms_dbfs={summary.get('mean_rms_dbfs')}"
            )
        if candidate["notes"]:
            lines.append(f"  notes: {' | '.join(candidate['notes'])}")
        for item in candidate["mutation_suggestions"]:
            lines.append(
                f"  mutate `{item['path']}` :: {item['action']} "
                f"{item['current_value']} -> {item['suggested_value']} "
                f"[goal: {item['goal']}]"
            )
        lines.append("")
    if not report["candidates"]:
        lines.append("No candidates matched the requested part constraints.")
        lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = make_parser()
    args = parser.parse_args()
    _validate_goals(args.goal)
    report = build_report(args)
    if args.format == "json":
        print(json.dumps(report, indent=2))
        return
    print(render_text(report), end="")


if __name__ == "__main__":
    main()
