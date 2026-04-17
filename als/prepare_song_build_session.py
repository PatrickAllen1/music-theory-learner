#!/usr/bin/env python3
"""
prepare_song_build_session.py

Prepare a studio-facing build-session plan from the frozen song spec,
composition pass, and MIDI plan. This is the artifact for the eventual Ableton
writing session: build order, reference axes, critical checkpoints, and
section-specific listening targets.
"""

from __future__ import annotations

import argparse
import json
from argparse import Namespace
from pathlib import Path

try:
    from build_frozen_song_spec import build_report as build_frozen_song_spec_report
    from build_song_composition_pass import build_report as build_song_composition_pass_report
    from build_song_midi_plan import build_report as build_song_midi_plan_report
except ModuleNotFoundError:
    from .build_frozen_song_spec import build_report as build_frozen_song_spec_report
    from .build_song_composition_pass import build_report as build_song_composition_pass_report
    from .build_song_midi_plan import build_report as build_song_midi_plan_report


DEFAULT_CATALOG_DIR = Path("als/catalog/profiles")
DEFAULT_SERUM_BRIEFS_PATH = Path("als/serum-track-briefs.json")
DEFAULT_SONG_BRIEFS_PATH = Path("als/song-blueprint-briefs.json")
DEFAULT_TEMPLATES_PATH = Path("als/song-production-templates.json")


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Prepare a studio-facing build session from the song plan.")
    parser.add_argument("--brief", required=True, help="Song brief id from the manifest.")
    parser.add_argument("--song-briefs", default=str(DEFAULT_SONG_BRIEFS_PATH), help="Song-level brief manifest JSON.")
    parser.add_argument("--templates", default=str(DEFAULT_TEMPLATES_PATH), help="Song production templates JSON.")
    parser.add_argument("--catalog-dir", default=str(DEFAULT_CATALOG_DIR), help="Directory of generated *-profiles.json files.")
    parser.add_argument("--serum-briefs", default=str(DEFAULT_SERUM_BRIEFS_PATH), help="Serum brief manifest JSON.")
    parser.add_argument("--analysis-dir", default="als/analysis", help="ALS analysis JSON directory.")
    parser.add_argument("--transcripts-dir", default="docs/transcripts", help="Transcript spans directory.")
    parser.add_argument("--technique-bank", default="docs/techniques/bank.json", help="Technique bank JSON path.")
    parser.add_argument("--prefer-rendered", action="store_true", help="Prefer rendered profiles where available.")
    parser.add_argument("--limit-per-part", type=int, default=5, help="Max candidates to inspect per part. Default: 5")
    parser.add_argument("--mutation-limit", type=int, default=6, help="Max mutation suggestions per part. Default: 6")
    parser.add_argument("--max-swaps", type=int, default=2, help="Maximum refinement swaps to apply. Default: 2")
    parser.add_argument("--phrase-limit", type=int, default=8, help="Maximum phrase evidence rows. Default: 8")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="Output format.")
    return parser


def _namespace(args: argparse.Namespace) -> Namespace:
    return Namespace(
        brief=args.brief,
        song_briefs=args.song_briefs,
        templates=args.templates,
        catalog_dir=args.catalog_dir,
        serum_briefs=args.serum_briefs,
        analysis_dir=args.analysis_dir,
        transcripts_dir=args.transcripts_dir,
        technique_bank=args.technique_bank,
        prefer_rendered=args.prefer_rendered,
        limit_per_part=args.limit_per_part,
        mutation_limit=args.mutation_limit,
        max_swaps=args.max_swaps,
        phrase_limit=args.phrase_limit,
        format="json",
    )


def _reference_axes() -> list[dict]:
    return [
        {
            "axis": "low_end_pressure",
            "influence": "Kettama",
            "local_source": "docs/transcripts/kettamapge_spans.json",
            "listen_for": "Kick weight, mix density, and how the low end feels physically large without the drums turning harsh.",
            "apply_to_this_track": "Keep the kick body-forward and let the bass-foundation feel heavy before you brighten anything else.",
        },
        {
            "axis": "groove_pocket",
            "influence": "Interplanetary Criminal",
            "local_source": "docs/transcripts/kettamainterplanetarycriminal_spans.json",
            "listen_for": "Ghost-hat swing, loop bounce, and phrase-end movement that makes the 4x4 feel like UKG instead of rigid house.",
            "apply_to_this_track": "Judge the drop pocket by the hats and phrase tails, not by adding more kick or more bass notes.",
        },
        {
            "axis": "bass_roll_character",
            "influence": "Soul Mass Transit System / Y U QT lane",
            "local_source": "docs/transcripts/yuqt2_spans.json",
            "listen_for": "Rolling bass motion that feels rhythmic first, tonal second, with the sub staying authoritative underneath.",
            "apply_to_this_track": "The moving harmonic layer should feel alive inside the phrase while the sub still reads as one confident floor.",
        },
        {
            "axis": "hook_and_chord_readability",
            "influence": "Sammy Virji / Y U QT",
            "local_source": "docs/transcripts/sammyvirjiiguesswerenotthesame_spans.json",
            "listen_for": "Whether the hook voice is memorable and whether the chord color reads emotionally without softening the club impact.",
            "apply_to_this_track": "Make the warm organ-stab hook readable at low note count and save the full harmonic bloom for the break and Drop B.",
        },
    ]


def _build_order(composition: dict, midi_plan: dict) -> list[dict]:
    return [
        {
            "stage": 1,
            "name": "Kick, core groove, and air ceiling",
            "goal": "Lock the 4x4 body, swingy tops, and quiet air bed before melodic material starts competing for attention.",
            "do_now": [
                "Build the kick/clap/off-hat skeleton from the intro and drop drum variants.",
                "Add the constant quiet air layer so the track already feels tall in Intro A.",
                "Tease the presence lane in Intro B without fully opening it.",
            ],
            "done_when": "Intro A already feels intentional and the first drop can open up without sounding like the ceiling suddenly appears from nowhere.",
        },
        {
            "stage": 2,
            "name": "Rolling bass floor",
            "goal": "Get the low end behaving like a modern rolling UKG floor before writing the hook.",
            "do_now": [
                composition["architectural_decisions"]["intro_b_bass_gesture"]["decision"],
                composition["architectural_decisions"]["rolling_bass_mechanism"]["decision"],
                composition["architectural_decisions"]["rolling_bass_proportion"]["decision"],
            ],
            "done_when": "The bass feels alive from rhythmic pulse alone and does not need hook notes or extra top-end to feel like the record's engine.",
        },
        {
            "stage": 3,
            "name": "Chord bed and break bloom",
            "goal": "Establish the emotional harmonic staircase without spending the bloom too early.",
            "do_now": [
                "Write Drop A with restrained Bb color and no exposed major-7 bloom.",
                composition["architectural_decisions"]["break_chord_widening"]["decision"],
                "Make the break feel complete instrumentally from chord spread, air, and arrangement discipline.",
            ],
            "done_when": "Drop A feels austere and strong, while the break clearly opens up before Drop B arrives.",
        },
        {
            "stage": 4,
            "name": "Hook identity and conversation logic",
            "goal": "Give the instrumental a real identity lane without crowding the center.",
            "do_now": [
                composition["architectural_decisions"]["hook_voice_identity"]["decision"],
                composition["architectural_decisions"]["drop_b_conversation_rule"]["decision"],
                "Keep the answer phrase-end only and let the hook step back in Drop B.",
            ],
            "done_when": "The hook is memorable in Drop A and the answer makes Drop B feel bigger by substitution, not by clutter.",
        },
        {
            "stage": 5,
            "name": "Section writing and variant placement",
            "goal": "Turn the stance into a real 128-bar record by assigning the exact phrase variants section by section.",
            "do_now": [
                "Lay in the section assignments exactly as the MIDI plan specifies.",
                "Check that Drop A Lift grows only by pocket/top-end density.",
                "Check that Drop B Lift grows through tops and widened chord spread rather than a new low-end lane.",
            ],
            "done_when": "Every section has its own growth mechanism and the whole track no longer feels like one loop with muting.",
        },
        {
            "stage": 6,
            "name": "Returns, automation, and reference A/B",
            "goal": "Finalise the club behavior of the song before lesson conversion or later track recreation.",
            "do_now": [
                "Build the return structure and automation from the frozen song spec.",
                "A/B each reference axis separately instead of listening for everything at once.",
                "Preserve the whisper of air in the outro so the record does not shut abruptly.",
            ],
            "done_when": "The song reads as one coherent club record on its own and every major decision still matches the brief after ear fatigue sets in.",
        },
    ]


def _section_targets(composition: dict, midi_plan: dict) -> list[dict]:
    assignments = {row["section_id"]: row for row in midi_plan["section_assignments"]}
    out = []
    for section in composition["section_plan"]:
        assignment = assignments.get(section["section_id"], {})
        part_variants = assignment.get("part_variants", {})
        out.append({
            "section_id": section["section_id"],
            "bars": section["bars"],
            "what_to_listen_for": section["harmonic_behavior"],
            "bass_focus": section["bass_behavior"],
            "hook_focus": section["hook_behavior"],
            "arrangement_assignment": {
                "drums": part_variants.get("drums"),
                "bass": part_variants.get("bass-foundation"),
                "chords": part_variants.get("chord-bed"),
                "hook": part_variants.get("hook-response"),
            },
        })
    return out


def _critical_checks(composition: dict) -> list[str]:
    return [
        "The bass roll must feel rhythmic-primary. If tonal motion is doing most of the work, simplify it.",
        "Drop A Lift must not reveal new harmonic information. If it does, move that idea to the break or Drop B.",
        "When the Drop B answer arrives, the hook must step back to half density.",
        "The break must widen upward, not just sustain longer.",
        "Keep the top-end map intact: Intro B teases, Drop A opens, Break breathes, Drop B Lift releases hardest.",
        "If a phrase feels too close to a source track, keep the function and change the contour, register, or rhythm immediately.",
        composition["architectural_decisions"]["break_sample_lane_target"]["decision"],
    ]


def _later_handoff(composition: dict) -> list[str]:
    return [
        "When the track is built later, bounce each major section and compare it back to the section targets before changing the arrangement.",
        "Capture the final MIDI for bass, chord bed, hook, and answer so the guided lesson can point to exact note decisions instead of abstractions.",
        "Keep the composition pass and MIDI plan beside the Ableton session; they are the authority, not late-session instinct.",
        f"Sample/vocal future rule: {composition['sample_strategy']['version_strategy']}",
    ]


def build_report(args: argparse.Namespace) -> dict:
    frozen = build_frozen_song_spec_report(_namespace(args))
    composition = build_song_composition_pass_report(_namespace(args))
    midi_plan = build_song_midi_plan_report(_namespace(args))
    return {
        "brief_id": composition["brief_id"],
        "bpm": frozen["bpm"],
        "key": frozen["key"],
        "duration_minutes": frozen["readiness"].get("duration_minutes"),
        "thesis": composition["thesis"],
        "reference_axes": _reference_axes(),
        "build_order": _build_order(composition, midi_plan),
        "section_targets": _section_targets(composition, midi_plan),
        "critical_checks": _critical_checks(composition),
        "later_handoff": _later_handoff(composition),
        "als_anchor_profiles": composition["als_reference_points"],
    }


def render_text(report: dict) -> str:
    lines = []
    lines.append("# Song Build Session")
    lines.append("")
    lines.append(f"- brief: `{report['brief_id']}`")
    lines.append(f"- target: {report['bpm']} BPM / {report['key']} / ~{report['duration_minutes']} minutes")
    lines.append("")
    lines.append("## Thesis")
    lines.append(report["thesis"])
    lines.append("")
    lines.append("## Reference Axes")
    for row in report["reference_axes"]:
        lines.append(f"- `{row['axis']}` :: {row['influence']}")
        lines.append(f"  source: {row['local_source']}")
        lines.append(f"  listen for: {row['listen_for']}")
        lines.append(f"  apply here: {row['apply_to_this_track']}")
    lines.append("")
    lines.append("## Build Order")
    for row in report["build_order"]:
        lines.append(f"- {row['stage']}. {row['name']}")
        lines.append(f"  goal: {row['goal']}")
        lines.append(f"  do now: {' | '.join(row['do_now'])}")
        lines.append(f"  done when: {row['done_when']}")
    lines.append("")
    lines.append("## Section Targets")
    for row in report["section_targets"]:
        lines.append(f"- `{row['section_id']}` bars {row['bars']}")
        lines.append(f"  listen for: {row['what_to_listen_for']}")
        lines.append(f"  bass: {row['bass_focus']}")
        lines.append(f"  hook: {row['hook_focus']}")
        lines.append(
            "  assignments: "
            f"drums={row['arrangement_assignment']['drums']} | "
            f"bass={row['arrangement_assignment']['bass']} | "
            f"chords={row['arrangement_assignment']['chords']} | "
            f"hook={row['arrangement_assignment']['hook']}"
        )
    lines.append("")
    lines.append("## Critical Checks")
    for row in report["critical_checks"]:
        lines.append(f"- {row}")
    if report["als_anchor_profiles"]:
        lines.append("")
        lines.append("## ALS Anchors")
        for row in report["als_anchor_profiles"]:
            lines.append(
                f"- `{row['part_id']}` -> `{row['track']}` ({row['analysis_slug']}) chain={row['processing_chain_id'] or '-'}"
            )
    lines.append("")
    lines.append("## Later Handoff")
    for row in report["later_handoff"]:
        lines.append(f"- {row}")
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
