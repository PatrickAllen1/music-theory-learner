#!/usr/bin/env python3
"""
compile_guided_build_lesson.py

Compile a full-song blueprint into a guided-build-style lesson draft in the
same general shape as the app's originals JSON files, while preserving
diagnostics about what still needs manual authoring before the lesson is truly
ready.

Examples:
    python3 als/compile_guided_build_lesson.py --brief ukg-2step-dark-stab
    python3 als/compile_guided_build_lesson.py --brief ukg-4x4-pluck-driver --lesson-only --format json
"""

from __future__ import annotations

import argparse
import json
import re
from argparse import Namespace
from pathlib import Path

try:
    from design_full_song_blueprint import build_report as build_full_song_blueprint_report
    from generate_serum_guided_build_steps import build_report as build_synth_steps_report
except ModuleNotFoundError:
    from .design_full_song_blueprint import build_report as build_full_song_blueprint_report
    from .generate_serum_guided_build_steps import build_report as build_synth_steps_report


DEFAULT_CATALOG_DIR = Path("als/catalog/profiles")
DEFAULT_SERUM_BRIEFS_PATH = Path("als/serum-track-briefs.json")
DEFAULT_SONG_BRIEFS_PATH = Path("als/song-blueprint-briefs.json")
DEFAULT_TEMPLATES_PATH = Path("als/song-production-templates.json")

VAGUE_PATTERNS = [
    r"\bchoose\b",
    r"\bdecide\b",
    r"\baudition\b",
    r"\bif needed\b",
    r"\boptional\b",
    r"\bkeep .* ready\b",
]


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Compile a full-song blueprint into a guided-build lesson draft.")
    parser.add_argument("--brief", required=True, help="Song brief id from the manifest.")
    parser.add_argument("--song-briefs", default=str(DEFAULT_SONG_BRIEFS_PATH), help="Song-level brief manifest JSON.")
    parser.add_argument("--templates", default=str(DEFAULT_TEMPLATES_PATH), help="Song production templates JSON.")
    parser.add_argument("--catalog-dir", default=str(DEFAULT_CATALOG_DIR), help="Directory of generated *-profiles.json files.")
    parser.add_argument("--serum-briefs", default=str(DEFAULT_SERUM_BRIEFS_PATH), help="Serum brief manifest JSON.")
    parser.add_argument("--prefer-rendered", action="store_true", help="Prefer rendered profiles where available.")
    parser.add_argument("--limit-per-part", type=int, default=5, help="Max candidates to inspect per part. Default: 5")
    parser.add_argument("--mutation-limit", type=int, default=6, help="Max mutation suggestions per part. Default: 6")
    parser.add_argument("--max-swaps", type=int, default=2, help="Maximum refinement swaps to apply. Default: 2")
    parser.add_argument("--format", choices=["json", "text"], default="text", help="Output format.")
    parser.add_argument("--lesson-only", action="store_true", help="Output only the compiled lesson object.")
    return parser


def _full_song_namespace(args: argparse.Namespace) -> Namespace:
    return Namespace(
        brief=args.brief,
        song_briefs=args.song_briefs,
        templates=args.templates,
        catalog_dir=args.catalog_dir,
        serum_briefs=args.serum_briefs,
        prefer_rendered=args.prefer_rendered,
        limit_per_part=args.limit_per_part,
        mutation_limit=args.mutation_limit,
        max_swaps=args.max_swaps,
        format="json",
    )


def _synth_steps_namespace(args: argparse.Namespace, blueprint: dict) -> Namespace:
    return Namespace(
        brief=blueprint["serum_brief_id"],
        catalog_dir=args.catalog_dir,
        briefs=args.serum_briefs,
        prefer_rendered=args.prefer_rendered,
        limit_per_part=args.limit_per_part,
        mutation_limit=args.mutation_limit,
        max_swaps=args.max_swaps,
        bank_dir=[],
        bank_top_per_part=3,
        render_limit=6,
        format="json",
    )


def _titleize(brief_id: str) -> str:
    text = brief_id.replace("ukg-", "").replace("-", " ")
    return " ".join(word.capitalize() for word in text.split())


def _estimate_minutes(blueprint: dict) -> int:
    base = 55
    base += len(blueprint["synth_layers"]) * 8
    base += len(blueprint["sample_lanes"]) * 2
    base += len(blueprint["arrangement"]) * 3
    return max(75, min(150, base))


def _learn_list(blueprint: dict) -> list[str]:
    harmony = blueprint["harmonic_plan"]
    return [
        f"How to stage a {blueprint['bpm']} BPM {blueprint['key']} UK garage idea into a release-shaped arrangement",
        f"How the {', '.join(harmony['progression'])} harmonic move supports the track's mood",
        f"How to separate drum lanes, synth layers, returns, and reserved sample spaces so the song stays mixable",
        "How to treat effects, automation, and export as part of the composition instead of a late cleanup step",
    ]


def _track_list(blueprint: dict) -> list[str]:
    names = ["DRUMS"]
    for layer in blueprint["synth_layers"]:
        names.append(layer["part_id"].upper().replace("-", "_"))
    names.extend(return_row["name"].upper().replace(" ", "_") for return_row in blueprint["returns"])
    return names


def _chain_text(chain: dict | None) -> str:
    if not chain:
        return "No processing chain has been assigned yet."
    return " -> ".join(chain.get("devices") or [])


def _arrangement_text(blueprint: dict) -> str:
    pieces = []
    for section in blueprint["arrangement"]:
        pieces.append(
            f"bars {section['start_bar']}-{section['end_bar']} = {section['section_id']} ({section['goal']})"
        )
    return "; ".join(pieces) + "."


def _required_slots(blueprint: dict) -> list[dict]:
    return [row for row in blueprint["sample_lanes"] if row["required"]]


def _optional_slots(blueprint: dict) -> list[dict]:
    return [row for row in blueprint["sample_lanes"] if not row["required"]]


def _make_static_steps(blueprint: dict, synth_steps: list[dict]) -> list[dict]:
    required_slots = _required_slots(blueprint)
    optional_slots = _optional_slots(blueprint)
    drum_slots = [row for row in blueprint["sample_lanes"] if row["slot_type"] in {"kick", "clap_snare", "closed_hat", "top_loop_support", "perc", "drum_loop"}]
    synth_names = ", ".join(layer["part_id"].upper().replace("-", "_") for layer in blueprint["synth_layers"])
    return_names = ", ".join(f"{row['return_id']}={row['name']}" for row in blueprint["returns"])
    reserved_space_text = "; ".join(blueprint["reserved_spaces"]) or "No reserved spaces were declared."
    automation_text = " ".join(blueprint["automation_rules"])
    mix_text = " ".join(blueprint["mix_rules"])
    export_checks = "; ".join(blueprint["export_plan"]["final_checks"])

    static_steps = [
        {
            "title": "Concept and session setup",
            "category": "ableton",
            "instruction": (
                f"Create a new Ableton Live set at {blueprint['bpm']} BPM in {blueprint['key']} and save it with the brief id "
                f"`{blueprint['brief_id']}`. Build these tracks in order: DRUMS, {synth_names}. Create these return tracks next: "
                f"{return_names}. Keep the energy profile in front of you while you work: {blueprint['energy_profile']}"
            ),
            "why": (
                "The whole lesson should behave like a full production, not a loop exercise. "
                f"Starting with the exact track map and return layout keeps the arrangement and mix decisions locked from the beginning."
            ),
            "ableton_cheatsheet_id": "arrangement-view",
            "splice_search": None,
            "tip": "Do not add extra tracks until the core blueprint is working. Empty lanes are already reserved on purpose.",
        },
        {
            "title": "Build the drum and sample lanes",
            "category": "drums",
            "instruction": (
                "Create the core drum/sample lanes exactly as the blueprint calls for. Required lanes: "
                + "; ".join(
                    f"`{row['slot_id']}` on {row['lane']} for {row['purpose']}"
                    for row in required_slots
                )
                + ". Reserved lanes that should stay empty until the arrangement proves it needs them: "
                + ("; ".join(f"`{row['slot_id']}` for {row['purpose']}" for row in optional_slots) if optional_slots else "none")
                + "."
            ),
            "why": (
                f"{blueprint['drum_strategy']} "
                "This step freezes which lanes are essential and which ones are intentionally reserved for later texture, vocal, or transition work."
            ),
            "ableton_cheatsheet_id": "drum-rack",
            "splice_search": None,
            "tip": "A required lane needs a real sound source. A reserved lane should stay empty until the arrangement proves it needs it.",
        },
        {
            "title": "Set the drum processing and reserved spaces",
            "category": "drums",
            "instruction": (
                "Process the drum and sample lanes according to their chain families before writing extra material. "
                + "; ".join(
                    f"`{row['slot_id']}` uses `{row['processing_chain_id']}`: {_chain_text(row['processing_chain'])}"
                    for row in drum_slots
                )
                + f" Keep these spaces intentionally open while you build the core groove: {reserved_space_text}"
            ),
            "why": (
                "Production quality comes from layout discipline. "
                "If you assign the lane roles and processing logic now, later layers have somewhere intentional to sit."
            ),
            "ableton_cheatsheet_id": "drum-rack",
            "splice_search": None,
            "tip": "Do not spend all your energy filling reserved lanes. Make the required groove hit first.",
        },
    ]

    if synth_steps:
        static_steps.append(
            {
                "title": "Wire the returns before the arrangement grows",
                "category": "mix",
                "instruction": (
                    "Set up the return architecture before automating anything: "
                    + "; ".join(f"`{row['return_id']}` `{row['name']}` for {row['purpose']}" for row in blueprint["returns"])
                    + ". Keep the returns purposeful instead of washing every lane equally."
                ),
                "why": "Returns are part of the song design. They define depth, contrast, and the size changes between intro, break, and drop sections.",
                "ableton_cheatsheet_id": "return-tracks",
                "splice_search": None,
                "tip": "The cleanest drops usually happen when the big FX tail resets right at the re-entry.",
            }
        )

    static_steps.extend(
        [
            {
                "title": "Arrange the full song structure",
                "category": "ableton",
                "instruction": (
                    "Lay the arrangement out exactly to the blueprint before refining transitions: "
                    + _arrangement_text(blueprint)
                    + " Use the arrangement notes as guardrails: "
                    + " ".join(blueprint["arrangement_notes"])
                ),
                "why": "A release-shaped arrangement needs bar-count discipline. If the structure is fixed early, every later automation and layer choice has a clear job.",
                "ableton_cheatsheet_id": "arrangement-view",
                "splice_search": None,
                "tip": "Do not invent extra sections until the listed ones already feel intentional.",
            },
            {
                "title": "Automate transitions and space management",
                "category": "mix",
                "instruction": (
                    "Write the transition and space-management moves into the arrangement. Follow these rules directly: "
                    + automation_text
                    + " Keep the reserved spaces active as design constraints: "
                    + reserved_space_text
                ),
                "why": "Automation is part of composition in this style. It is what turns a static loop into sections with tension, release, and impact.",
                "ableton_cheatsheet_id": "arrangement-view",
                "splice_search": None,
                "tip": "One clean transition move at the right bar is better than constant motion everywhere.",
            },
            {
                "title": "Run the mix pass around role separation",
                "category": "mix",
                "instruction": (
                    "Do the first mix pass using the blueprint's role and space rules, not instinctive fader grabbing. "
                    + mix_text
                    + " Use the per-layer chains as the default starting point for each synth and sample lane."
                ),
                "why": "This keeps the mix tied to the song design. The point is to preserve the hook, the low-end ownership, and the open spaces the arrangement needs.",
                "ableton_cheatsheet_id": "eq-eight",
                "splice_search": None,
                "tip": "If a layer has no clear role after the first pass, mute it before you turn it up.",
            },
            {
                "title": "Export the finished blueprint version",
                "category": "mix",
                "instruction": (
                    f"Bounce the full arrangement as {blueprint['export_plan']['target_bounce']}. "
                    f"Keep this headroom rule in mind: {blueprint['export_plan']['headroom_note']} "
                    f"Before exporting, confirm these checks: {export_checks}"
                ),
                "why": "The export is part of the lesson because the song has to behave like a finished record, not just a playable session.",
                "ableton_cheatsheet_id": None,
                "splice_search": None,
                "tip": "Do the final check from the loudest section of the song, not the intro.",
            },
        ]
    )
    return static_steps


def _enrich_synth_step(step: dict, blueprint: dict) -> dict:
    source_part_id = step.get("source_part_id")
    layer = next((row for row in blueprint["synth_layers"] if row["part_id"] == source_part_id), None)
    if not layer:
        return step

    chain_note = _chain_text(layer.get("processing_chain"))
    instruction = re.sub(
        r"\s*If the base sound still feels weak, keep these alternates ready to audition next:.*?$",
        "",
        step["instruction"],
        flags=re.IGNORECASE,
    )
    title = re.sub(r"^Choose and shape", "Load and shape", step["title"])
    addition = (
        f" After shaping the preset, treat this lane with `{layer.get('processing_chain_id')}`: {chain_note}. "
        f"In the arrangement, this layer should {layer['arrangement_role']}."
    )
    tip = step["tip"]
    if layer.get("audio_status") != "rendered":
        tip = f"{tip} This lane is still param-driven until a render confirms it."
    return {
        **step,
        "title": title,
        "instruction": instruction + addition,
        "why": step["why"] + f" The song blueprint assigns this lane to {layer['job_in_track']}.",
        "tip": tip,
    }


def _find_vague_step_ids(lesson: dict) -> list[int]:
    vague_ids = []
    for step in lesson["steps"]:
        text = " ".join(
            str(step.get(field) or "")
            for field in ("title", "instruction", "tip")
        )
        if any(re.search(pattern, text, flags=re.IGNORECASE) for pattern in VAGUE_PATTERNS):
            vague_ids.append(step["id"])
    return vague_ids


def build_report(args: argparse.Namespace) -> dict:
    blueprint = build_full_song_blueprint_report(_full_song_namespace(args))
    synth_steps_report = build_synth_steps_report(_synth_steps_namespace(args, blueprint))
    static_steps = _make_static_steps(blueprint, synth_steps_report["steps"])
    enriched_synth_steps = [_enrich_synth_step(step, blueprint) for step in synth_steps_report["steps"]]
    all_steps = static_steps[:3] + enriched_synth_steps + static_steps[3:]
    steps = []
    for index, step in enumerate(all_steps, start=1):
        steps.append({
            **step,
            "id": index,
        })

    lesson = {
        "id": f"draft-{blueprint['brief_id']}",
        "title": _titleize(blueprint["brief_id"]),
        "build_type": "original",
        "difficulty": "beginner",
        "estimated_time_mins": _estimate_minutes(blueprint),
        "bpm": blueprint["bpm"],
        "key": blueprint["key"],
        "source_track_id": None,
        "spinoff_level": None,
        "description": blueprint["description"],
        "what_youll_learn": _learn_list(blueprint),
        "steps": steps,
    }

    compiler_warnings = []
    if blueprint["readiness"]["issues"]:
        compiler_warnings.extend(blueprint["readiness"]["issues"])
    vague_step_ids = _find_vague_step_ids(lesson)
    if vague_step_ids:
        compiler_warnings.append(
            f"Some compiled steps still contain draft-style wording and need hand-tightening: {', '.join(str(i) for i in vague_step_ids)}."
        )
    if any(layer["audio_status"] != "rendered" for layer in blueprint["synth_layers"]):
        compiler_warnings.append("At least one synth lane is still param-driven rather than audio-verified.")

    return {
        "brief_id": blueprint["brief_id"],
        "blueprint_readiness": blueprint["readiness"],
        "synth_step_count": synth_steps_report["step_count"],
        "vague_step_ids": vague_step_ids,
        "compiler_warnings": compiler_warnings,
        "lesson": lesson,
        "blueprint": blueprint,
    }


def render_text(report: dict) -> str:
    lesson = report["lesson"]
    lines = []
    lines.append("# Guided Build Lesson Draft")
    lines.append("")
    lines.append(f"- brief: `{report['brief_id']}`")
    lines.append(f"- lesson id: `{lesson['id']}`")
    lines.append(f"- blueprint readiness: `{report['blueprint_readiness']['label']}`")
    lines.append(f"- step count: {len(lesson['steps'])}")
    if report["compiler_warnings"]:
        lines.append("")
        lines.append("## Compiler Warnings")
        for row in report["compiler_warnings"]:
            lines.append(f"- {row}")
    lines.append("")
    lines.append("## Steps")
    for step in lesson["steps"]:
        lines.append(f"- {step['id']}. {step['title']} [{step['category']}]")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = make_parser()
    args = parser.parse_args()
    report = build_report(args)
    payload = report["lesson"] if args.lesson_only else report
    if args.format == "json":
        print(json.dumps(payload, indent=2))
        return
    if args.lesson_only:
        print(json.dumps(payload, indent=2))
        return
    print(render_text(report), end="")


if __name__ == "__main__":
    main()
