#!/usr/bin/env python3
"""
generate_serum_guided_build_steps.py

Generate guided-build-style synth step scaffolds in the same general shape as
the lesson JSON step objects, using the brief-specific synth plan as the source
of truth.

Examples:
    python3 als/generate_serum_guided_build_steps.py --brief ukg-2step-dark-stab
    python3 als/generate_serum_guided_build_steps.py --brief ukg-4x4-pluck-driver --format json
"""

from __future__ import annotations

import argparse
import json
from argparse import Namespace
from pathlib import Path

try:
    from generate_serum_guided_build_synth_plan import build_report as build_synth_plan_report
except ModuleNotFoundError:
    from .generate_serum_guided_build_synth_plan import build_report as build_synth_plan_report


DEFAULT_CATALOG_DIR = Path("als/catalog/profiles")
DEFAULT_BRIEFS_PATH = Path("als/serum-track-briefs.json")

CATEGORY_MAP = {
    "bass": "bass",
    "sub": "bass",
    "reese": "bass",
    "pad": "chords",
    "lead": "melody",
    "pluck": "melody",
    "stab": "melody",
    "fx": "mix",
}

CHEATSHEET_MAP = {
    "bass": "serum-v2-oscillators",
    "sub": "serum-v2-oscillators",
    "reese": "serum-v2-oscillators",
    "pad": "serum-v2-envelopes",
    "lead": "serum-v2-envelopes",
    "pluck": "serum-v2-envelopes",
    "stab": "serum-v2-envelopes",
}


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate guided-build-style synth step scaffolds from a Serum brief.")
    parser.add_argument("--brief", required=True, help="Brief id from the manifest.")
    parser.add_argument("--catalog-dir", default=str(DEFAULT_CATALOG_DIR), help="Directory of generated *-profiles.json files.")
    parser.add_argument("--briefs", default=str(DEFAULT_BRIEFS_PATH), help="Track brief manifest JSON.")
    parser.add_argument("--prefer-rendered", action="store_true", help="Prefer rendered profiles where available.")
    parser.add_argument("--limit-per-part", type=int, default=5, help="Max candidates to inspect per part. Default: 5")
    parser.add_argument("--mutation-limit", type=int, default=6, help="Max mutation suggestions per part. Default: 6")
    parser.add_argument("--max-swaps", type=int, default=2, help="Maximum refinement swaps to apply. Default: 2")
    parser.add_argument("--bank-dir", action="append", default=[], help="Preset bank directory to scan. Pass multiple times.")
    parser.add_argument("--bank-top-per-part", type=int, default=3, help="Maximum bank alternatives per part. Default: 3")
    parser.add_argument("--render-limit", type=int, default=6, help="Maximum brief render blockers to inspect. Default: 6")
    parser.add_argument("--format", choices=["json", "text"], default="text", help="Output format.")
    return parser


def _synth_plan_namespace(args: argparse.Namespace) -> Namespace:
    return Namespace(
        brief=args.brief,
        catalog_dir=args.catalog_dir,
        briefs=args.briefs,
        prefer_rendered=args.prefer_rendered,
        limit_per_part=args.limit_per_part,
        mutation_limit=args.mutation_limit,
        max_swaps=args.max_swaps,
        bank_dir=args.bank_dir,
        bank_top_per_part=args.bank_top_per_part,
        render_limit=args.render_limit,
        format="json",
    )


def _instruction(section: dict) -> str:
    details = []
    if section.get("current_track"):
        details.append(
            f"On your `{section['part_id']}` track, load Serum and start from `{section['current_track']}` (`{section['current_profile_id']}`)."
        )
    else:
        details.append(f"On your `{section['part_id']}` track, choose a starting Serum sound that matches the `{section['role']}` role.")

    tweaks = section.get("starting_tweaks") or []
    if tweaks:
        tweak_text = "; ".join(
            f"`{row['path']}` {row['action']} {row['from']} -> {row['to']} for `{row['goal']}`"
            for row in tweaks[:4]
        )
        details.append(f"Make these first changes immediately: {tweak_text}.")
    else:
        details.append("Leave the preset as loaded at first and judge whether it already fills the role cleanly.")

    listen_for = section.get("listen_for") or []
    if listen_for:
        details.append(f"While looping the section, listen for this first: {listen_for[0]}")

    alternatives = section.get("bank_alternatives") or []
    if alternatives and ("replacement_lane_open" in section.get("flags", []) or "fallback_selected" in section.get("flags", [])):
        alt_text = "; ".join(f"`{row['track']}` from `{row.get('bank') or '-'}`" for row in alternatives[:2])
        details.append(f"If the base sound still feels weak, keep these alternates ready to audition next: {alt_text}.")

    return " ".join(details)


def _why(section: dict) -> str:
    why_rows = section.get("why_this_sound") or []
    if why_rows:
        return f"{why_rows[0]} In the arrangement, this part should {section['job_in_track']}."
    return f"This part should {section['job_in_track']}."


def _tip(section: dict) -> str:
    flags = set(section.get("flags") or [])
    listen_for = section.get("listen_for") or []
    if "needs_render_validation" in flags:
        return "Do not fully trust the preset choice until the part has been rendered and checked against the rest of the stack."
    if "no_actionable_mutations" in flags:
        return "If the sound already fits, keep it simple. If it does not, audition the alternate presets before inventing new tweaks."
    if listen_for:
        return listen_for[-1]
    return "Keep the role narrow. The point is to make this layer do one job clearly."


def _step_title(section: dict) -> str:
    return f"Choose and shape the {section['part_id']} synth"


def build_report(args: argparse.Namespace) -> dict:
    synth_plan = build_synth_plan_report(_synth_plan_namespace(args))
    steps = []
    for index, section in enumerate(synth_plan["synth_sections"], start=1):
        steps.append({
            "id": index,
            "title": _step_title(section),
            "category": CATEGORY_MAP.get(section["role"], "ableton"),
            "instruction": _instruction(section),
            "why": _why(section),
            "ableton_cheatsheet_id": CHEATSHEET_MAP.get(section["role"]),
            "splice_search": None,
            "tip": _tip(section),
            "source_part_id": section["part_id"],
            "flags": section["flags"],
        })
    return {
        "brief_id": synth_plan["brief_id"],
        "description": synth_plan["description"],
        "readiness": synth_plan["readiness"],
        "step_count": len(steps),
        "steps": steps,
    }


def render_text(report: dict) -> str:
    lines = []
    lines.append("# Serum Guided-Build Steps")
    lines.append("")
    lines.append(f"- brief: `{report['brief_id']}`")
    lines.append(f"- readiness: `{report['readiness']}`")
    lines.append(f"- step count: {report['step_count']}")
    lines.append("")
    for step in report["steps"]:
        lines.append(f"## {step['id']}. {step['title']}")
        lines.append(f"- category: {step['category']}")
        lines.append(f"- source part: `{step['source_part_id']}`")
        if step.get("flags"):
            lines.append(f"- flags: {', '.join(step['flags'])}")
        lines.append(f"- instruction: {step['instruction']}")
        lines.append(f"- why: {step['why']}")
        lines.append(f"- tip: {step['tip']}")
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
