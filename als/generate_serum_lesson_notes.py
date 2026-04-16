#!/usr/bin/env python3
"""
generate_serum_lesson_notes.py

Render a Serum track blueprint into lesson-facing notes that explain why each
sound was chosen, what to listen for, and what to tweak first.

Examples:
    python3 als/generate_serum_lesson_notes.py --brief ukg-4x4-pluck-driver
    python3 als/generate_serum_lesson_notes.py --brief ukg-4x4-lead-driver --format json
"""

from __future__ import annotations

import argparse
import json
from argparse import Namespace
from pathlib import Path

try:
    from design_serum_track_blueprint import build_report as build_blueprint_report
    from refine_serum_track_blueprint import build_report as build_refined_blueprint_report
except ModuleNotFoundError:
    from .design_serum_track_blueprint import build_report as build_blueprint_report
    from .refine_serum_track_blueprint import build_report as build_refined_blueprint_report


DEFAULT_CATALOG_DIR = Path("als/catalog/profiles")
DEFAULT_BRIEFS_PATH = Path("als/serum-track-briefs.json")


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate lesson-facing notes from a Serum track blueprint.")
    parser.add_argument("--catalog-dir", default=str(DEFAULT_CATALOG_DIR), help="Directory of generated *-profiles.json files.")
    parser.add_argument("--briefs", default=str(DEFAULT_BRIEFS_PATH), help="Track brief manifest JSON.")
    parser.add_argument("--brief", required=True, help="Brief id from the manifest.")
    parser.add_argument("--prefer-rendered", action="store_true", help="Prefer rendered profiles where available.")
    parser.add_argument("--limit-per-part", type=int, default=5, help="Max candidates to inspect per blueprint part. Default: 5")
    parser.add_argument("--mutation-limit", type=int, default=6, help="Max mutation suggestions per part. Default: 6")
    parser.add_argument("--refine", action="store_true", help="Refine the blueprint before generating lesson notes.")
    parser.add_argument("--max-swaps", type=int, default=2, help="Maximum refinement swaps to apply when --refine is set. Default: 2")
    parser.add_argument("--format", choices=["json", "text"], default="text", help="Output format.")
    return parser


def _blueprint_namespace(args: argparse.Namespace) -> Namespace:
    return Namespace(
        catalog_dir=args.catalog_dir,
        briefs=args.briefs,
        brief=args.brief,
        prefer_rendered=args.prefer_rendered,
        limit_per_part=args.limit_per_part,
        mutation_limit=args.mutation_limit,
        format="json",
    )


def _refine_namespace(args: argparse.Namespace) -> Namespace:
    return Namespace(
        **vars(_blueprint_namespace(args)),
        alternative_limit=max(args.limit_per_part, 5),
        max_swaps=args.max_swaps,
    )


def _listen_for(part: dict) -> list[str]:
    selection = part["selection"]
    if not selection:
        return []
    notes = []
    mix_tags = set(selection["mix_tags"])
    tone_tags = set(selection["tone_tags"])
    role = part["role"]
    audio_summary = selection.get("audio_summary") or {}

    if role in {"bass", "sub", "reese"}:
        notes.append("Listen for a stable low-end anchor that does not blur the kick pattern.")
    if role == "pad":
        notes.append("Listen for the pad sitting behind the drums instead of fighting the hook.")
    if role in {"lead", "pluck", "stab"}:
        notes.append("Listen for the melodic part reading clearly above the chord bed.")
    if "side_heavy" in mix_tags:
        notes.append("Listen for stereo width that supports the groove without washing out the center.")
    if "dark" in tone_tags:
        notes.append("Listen for enough warmth without losing note definition.")
    if "bright" in tone_tags:
        notes.append("Listen for enough edge to cut through without getting harsh.")

    centroid = audio_summary.get("mean_centroid_hz")
    attack_ms = audio_summary.get("mean_attack_time_ms")
    if centroid is not None and centroid <= 300:
        notes.append("The rendered centroid is low, so expect this part to occupy the lower spectrum.")
    elif centroid is not None and centroid >= 1200:
        notes.append("The rendered centroid is high, so expect this part to speak in the upper mids and highs.")
    if attack_ms is not None and attack_ms <= 20:
        notes.append("The rendered attack is fast, so the transient should feel immediate.")
    elif attack_ms is not None and attack_ms >= 120:
        notes.append("The rendered attack is slower, so the sound should bloom rather than snap.")

    deduped = []
    for note in notes:
        if note not in deduped:
            deduped.append(note)
    return deduped[:5]


def _part_teaching_notes(part: dict) -> dict:
    selection = part["selection"]
    if not selection:
        return {
            "part_id": part["part_id"],
            "role": part["role"],
            "status": "unresolved",
            "summary": "No profile matched the requested constraints.",
            "why_this_sound": [],
            "listen_for": [],
            "starting_tweaks": [],
        }

    why_this_sound = []
    why_this_sound.append(
        f"This part uses `{selection['profile_id']}` because it matches the `{part['role']}` role with tone `{', '.join(selection['tone_tags'])}` and mix `{', '.join(selection['mix_tags'])}`."
    )
    if part["constraint_mode"] != "full":
        why_this_sound.append(
            f"The catalog did not satisfy the full brief, so selection relaxed to `{part['constraint_mode']}` constraints."
        )
    for note in selection.get("notes") or []:
        why_this_sound.append(note)

    starting_tweaks = [
        {
            "path": row["path"],
            "goal": row["goal"],
            "action": row["action"],
            "from": row["current_value"],
            "to": row["suggested_value"],
            "rationale": row["rationale"],
        }
        for row in (selection.get("mutation_suggestions") or [])[:4]
    ]

    return {
        "part_id": part["part_id"],
        "role": part["role"],
        "status": "selected",
        "profile_id": selection["profile_id"],
        "track": selection["track"],
        "summary": (
            f"{part['part_id']} uses `{selection['profile_id']}` as the starting {part['role']} sound."
        ),
        "why_this_sound": why_this_sound,
        "listen_for": _listen_for(part),
        "starting_tweaks": starting_tweaks,
    }


def build_report(args: argparse.Namespace) -> dict:
    refined = getattr(args, "refine", False)
    blueprint = build_refined_blueprint_report(_refine_namespace(args)) if refined else build_blueprint_report(_blueprint_namespace(args))
    part_notes = [_part_teaching_notes(part) for part in blueprint["parts"]]
    return {
        "brief_id": blueprint["brief_id"],
        "description": blueprint["description"],
        "prefer_rendered": blueprint["prefer_rendered"],
        "refined": refined,
        "selected_profile_ids": blueprint["selected_profile_ids"],
        "overview": [
            f"This blueprint is designed for `{blueprint['brief_id']}`.",
            blueprint["description"],
        ],
        "parts": part_notes,
        "conflict_notes": blueprint["conflict_notes"],
        "pairwise_analysis": blueprint["pairwise_analysis"],
        "refinement_swaps": blueprint.get("refinement_swaps") or [],
    }


def render_text(report: dict) -> str:
    lines = []
    lines.append("# Serum Lesson Notes")
    lines.append("")
    lines.append(f"- brief: `{report['brief_id']}`")
    lines.append(f"- description: {report['description']}")
    lines.append(f"- prefer rendered: {'yes' if report['prefer_rendered'] else 'no'}")
    lines.append(f"- refined: {'yes' if report['refined'] else 'no'}")
    lines.append("")
    lines.append("## Overview")
    for row in report["overview"]:
        lines.append(f"- {row}")
    lines.append("")
    for part in report["parts"]:
        lines.append(f"## {part['part_id']} ({part['role']})")
        lines.append(f"- summary: {part['summary']}")
        for row in part["why_this_sound"]:
            lines.append(f"- why: {row}")
        for row in part["listen_for"]:
            lines.append(f"- listen for: {row}")
        for tweak in part["starting_tweaks"]:
            lines.append(
                f"- starting tweak: `{tweak['path']}` {tweak['action']} "
                f"{tweak['from']} -> {tweak['to']} "
                f"[goal: {tweak['goal']}]"
            )
        lines.append("")
    if report["conflict_notes"]:
        lines.append("## Conflict Notes")
        for row in report["conflict_notes"]:
            lines.append(f"- {row}")
        lines.append("")
    if report["refinement_swaps"]:
        lines.append("## Refinement Swaps")
        for row in report["refinement_swaps"]:
            lines.append(
                f"- `{row['part_id']}`: `{row['from_profile_id']}` -> `{row['to_profile_id']}` "
                f"(mode {row['from_constraint_mode']} -> {row['to_constraint_mode']})"
            )
        lines.append("")
    if report["pairwise_analysis"]:
        lines.append("## Pairwise Analysis")
        for row in report["pairwise_analysis"]:
            lines.append(
                f"- `{row['left_part_id']}` vs `{row['right_part_id']}`: "
                f"conflicts={len(row['conflicts'])}, complements={len(row['complements'])}"
            )
            for note in row["conflicts"]:
                lines.append(f"  conflict: {note}")
            for note in row["complements"]:
                lines.append(f"  complement: {note}")
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
