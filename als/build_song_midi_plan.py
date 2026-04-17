#!/usr/bin/env python3
"""
build_song_midi_plan.py

Convert the composition-facing song pass into exact part-level MIDI plans:
drum patterns, bass figures, chord voicings, hook cells, and per-section
variant assignments. This is the first artifact that turns the song from a
stance into something directly writable inside Ableton.
"""

from __future__ import annotations

import argparse
import json
from argparse import Namespace
from pathlib import Path

try:
    from build_song_composition_pass import build_report as build_song_composition_pass_report
except ModuleNotFoundError:
    from .build_song_composition_pass import build_report as build_song_composition_pass_report


DEFAULT_CATALOG_DIR = Path("als/catalog/profiles")
DEFAULT_SERUM_BRIEFS_PATH = Path("als/serum-track-briefs.json")
DEFAULT_SONG_BRIEFS_PATH = Path("als/song-blueprint-briefs.json")
DEFAULT_TEMPLATES_PATH = Path("als/song-production-templates.json")


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build exact part-level MIDI plans from the composition pass.")
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


def _event(note: str, position: str, length_beats: float, velocity: int, purpose: str | None = None) -> dict:
    row = {
        "note": note,
        "position": position,
        "length_beats": length_beats,
        "velocity": velocity,
    }
    if purpose:
        row["purpose"] = purpose
    return row


def _variant(
    variant_id: str,
    bars: int,
    usage: str,
    events: list[dict],
    note: str,
) -> dict:
    return {
        "variant_id": variant_id,
        "bars": bars,
        "usage": usage,
        "events": events,
        "note": note,
    }


def _drum_variants() -> list[dict]:
    intro_core = [
        *_kicks("1", [96, 92, 95, 91]),
        *_kicks("2", [96, 93, 95, 92]),
        *_claps("1", [91, 89]),
        *_claps("2", [91, 89]),
        *_off_hat("1", [68, 66, 69, 65]),
        *_off_hat("2", [68, 66, 70, 64]),
    ]
    drop_core = intro_core + [
        _event("A#1", "1.2.4", 0.25, 42, "ghost hat"),
        _event("A#1", "1.4.4", 0.25, 44, "ghost hat"),
        _event("A#1", "2.2.4", 0.25, 42, "ghost hat"),
        _event("A#1", "2.4.4", 0.25, 45, "ghost hat"),
        _event("A1", "2.4.3", 0.5, 58, "open hat"),
    ]
    intro_b_tease = [
        *_kicks("1", [96, 93, 95, 92]),
        *_kicks("2", [96, 93, 95, 92]),
        *_claps("1", [91, 89]),
        *_claps("2", [91, 89]),
        *_off_hat("1", [68, 66, 69, 65]),
        *_off_hat("2", [68, 66, 70, 64]),
        _event("A#1", "1.4.4", 0.25, 40, "ghost hat"),
        _event("A#1", "2.4.4", 0.25, 41, "ghost hat"),
        _event("A1", "2.4.3", 0.5, 46, "filtered open hat tease"),
    ]
    drop_lift = drop_core + [
        _event("G#1", "1.2.3", 0.25, 49, "shaker"),
        _event("G#1", "1.4.3", 0.25, 47, "shaker"),
        _event("G#1", "2.2.3", 0.25, 50, "shaker"),
        _event("G#1", "2.4.3", 0.25, 48, "shaker"),
        _event("A#1", "1.3.4", 0.25, 40, "lift ghost"),
        _event("A#1", "2.3.4", 0.25, 41, "lift ghost"),
        _event("A1", "1.4.3", 0.5, 56, "open hat"),
    ]
    break_sparse = [
        *_kicks("1", [92, 0, 94, 0], include_zero=False),
        *_kicks("2", [92, 0, 94, 0], include_zero=False),
        _event("D1", "1.4.1", 0.25, 84, "late clap"),
        _event("D1", "2.4.1", 0.25, 84, "late clap"),
        _event("F#1", "1.4.3", 0.25, 60, "late offbeat hat"),
        _event("F#1", "2.4.3", 0.25, 60, "late offbeat hat"),
    ]
    transition_switch = [
        *_kicks("1", [95, 0, 94, 0], include_zero=False),
        *_kicks("2", [96, 92, 95, 90]),
        _event("D1", "1.4.1", 0.25, 88, "late clap"),
        _event("D1", "2.2.1", 0.25, 89, "clap return"),
        _event("D1", "2.4.1", 0.25, 92, "clap return"),
        *_off_hat("1", [58, 0, 63, 0]),
        *_off_hat("2", [68, 66, 70, 72]),
        _event("A#1", "1.3.4", 0.25, 43, "transition ghost"),
        _event("A#1", "2.2.4", 0.25, 44, "transition ghost"),
        _event("G#1", "2.4.3", 0.25, 54, "shaker lift"),
        _event("A1", "2.4.3", 0.75, 62, "open hat re-entry"),
    ]
    outro_strip = [
        *_kicks("1", [96, 92, 95, 90]),
        *_kicks("2", [96, 92, 95, 90]),
        *_off_hat("1", [62, 60, 62, 58]),
        *_off_hat("2", [62, 60, 62, 58]),
    ]
    phrase_end_fill = [
        _event("D1", "1.3.3", 0.25, 88, "snare fill"),
        _event("D1", "1.3.4", 0.25, 92, "snare fill"),
        _event("D1", "1.4.1", 0.25, 96, "snare fill"),
        _event("G#1", "1.4.2", 0.25, 70, "shaker lift"),
        _event("A1", "1.4.3", 0.5, 72, "open hat throw"),
    ]
    section_riser = [
        _event("G#1", "1.1.3", 0.25, 62, "shaker"),
        _event("G#1", "1.2.3", 0.25, 68, "shaker"),
        _event("G#1", "1.3.3", 0.25, 74, "shaker"),
        _event("G#1", "1.4.3", 0.25, 80, "shaker"),
        _event("A#1", "1.4.4", 0.25, 54, "ghost hat push"),
        _event("A1", "1.4.3", 0.75, 78, "open hat riser"),
    ]
    pre_drop_cut = [
        _event("D1", "1.4.1", 0.25, 90, "clap stab"),
        _event("D1", "1.4.3", 0.25, 98, "snare stab"),
        _event("A1", "1.4.3", 0.5, 76, "open hat throw"),
    ]
    return [
        _variant(
            "drum_intro_core_2bar",
            2,
            "Intro and low-density sections. 4x4 spine with only the essential garage offbeat.",
            intro_core,
            "Kick-led spine without over-selling the groove before the bass arrives.",
        ),
        _variant(
            "drum_intro_b_tease_2bar",
            2,
            "Intro B. Tease the eventual open-hat/presence lane without fully opening the top yet.",
            intro_b_tease,
            "This keeps the section breathing while saving the full hat shimmer for Drop A.",
        ),
        _variant(
            "drum_drop_core_2bar",
            2,
            "Main drop groove. Add ghost hats around the claps to create Interplanetary Criminal-style bounce.",
            drop_core,
            "The ghosts add swing pressure without breaking the 4x4 commitment.",
        ),
        _variant(
            "drum_drop_lift_2bar",
            2,
            "Second-drop and lift version. Shakers and extra ghosts create energy, not a new pattern.",
            drop_lift,
            "The groove gets bigger by density and brightness, not by rewriting the beat.",
        ),
        _variant(
            "drum_break_sparse_2bar",
            2,
            "Break sections. Strip the pattern down so the harmony and future sample lane can breathe.",
            break_sparse,
            "This is intentional negative space, not an unfinished beat.",
        ),
        _variant(
            "drum_transition_switch_2bar",
            2,
            "Re-entry transition. Different drums pull the section back toward the drop through sparse first-half kicks, returning claps, and a sharper open-hat release.",
            transition_switch,
            "This should feel like an active switch-up, not just the break lasting longer.",
        ),
        _variant(
            "drum_outro_strip_2bar",
            2,
            "Outro pattern. Remove the backbeat so the DJ-safe exit feels lighter.",
            outro_strip,
            "The mix-out should still groove without feeling like a second drop.",
        ),
        _variant(
            "drum_phrase_end_fill_1bar",
            1,
            "Overlay fill for bar 8 / 16 boundaries. Use it sparingly to mark phrase turns without sounding EDM-obvious.",
            phrase_end_fill,
            "These fills should create excitement at the boundary, not replace the groove.",
        ),
        _variant(
            "drum_section_riser_1bar",
            1,
            "Overlay riser for major section boundaries. Increase shaker and hat pressure into the downbeat of the next section.",
            section_riser,
            "This is the cleanest way to raise phrase pressure without changing the core kick pattern.",
        ),
        _variant(
            "drum_pre_drop_cut_1bar",
            1,
            "Overlay pre-drop cut. Remove the full groove and let one last clap/snare/open-hat gesture tee up the next downbeat.",
            pre_drop_cut,
            "Use this before the biggest returns so the next kick lands harder.",
        ),
    ]


def _kicks(bar: str, velocities: list[int], include_zero: bool = True) -> list[dict]:
    positions = [f"{bar}.1.1", f"{bar}.2.1", f"{bar}.3.1", f"{bar}.4.1"]
    rows = []
    for position, velocity in zip(positions, velocities):
        if velocity == 0 and not include_zero:
            continue
        rows.append(_event("C1", position, 0.25, velocity, "kick"))
    return rows


def _claps(bar: str, velocities: list[int]) -> list[dict]:
    return [
        _event("D1", f"{bar}.2.1", 0.25, velocities[0], "clap"),
        _event("D1", f"{bar}.4.1", 0.25, velocities[1], "clap"),
    ]


def _off_hat(bar: str, velocities: list[int]) -> list[dict]:
    return [
        _event("F#1", f"{bar}.1.3", 0.25, velocities[0], "offbeat hat"),
        _event("F#1", f"{bar}.2.3", 0.25, velocities[1], "offbeat hat"),
        _event("F#1", f"{bar}.3.3", 0.25, velocities[2], "offbeat hat"),
        _event("F#1", f"{bar}.4.3", 0.25, velocities[3], "offbeat hat"),
    ]


def _chord_variants() -> list[dict]:
    intro_hint = [
        *_stack("1.1.1", 7.5, [("D3", 72), ("A3", 68), ("C4", 66), ("E4", 64), ("F4", 62)]),
        *_stack("3.1.1", 7.5, [("Bb2", 72), ("F3", 68), ("C4", 64)]),
    ]
    intro_full = [
        *_stack("1.1.1", 3.5, [("D3", 72), ("A3", 68), ("C4", 66), ("E4", 64), ("F4", 62)]),
        *_stack("2.1.1", 3.5, [("Bb2", 72), ("F3", 68), ("C4", 66)]),
        *_stack("3.1.1", 3.5, [("F2", 71), ("C3", 67), ("G3", 65), ("A3", 63)]),
        *_stack("4.1.1", 3.5, [("C3", 71), ("G3", 67), ("D4", 65), ("E4", 63)]),
    ]
    drop_core = [
        *_stack("1.1.1", 3.5, [("D3", 74), ("A3", 70), ("C4", 68), ("E4", 66), ("F4", 64)]),
        *_stack("2.1.1", 3.5, [("Bb2", 74), ("F3", 70), ("C4", 68)]),
        *_stack("3.1.1", 3.5, [("F2", 73), ("C3", 69), ("G3", 67), ("A3", 65)]),
        *_stack("4.1.1", 3.5, [("C3", 73), ("G3", 69), ("D4", 67), ("E4", 65)]),
    ]
    drop_a_lift = [
        *_stack("1.1.1", 3.5, [("D3", 74), ("A3", 70), ("C4", 68), ("E4", 66), ("F4", 64)]),
        *_stack("2.1.1", 3.5, [("Bb2", 74), ("F3", 70), ("C4", 68)]),
        *_stack("3.1.1", 3.5, [("F2", 73), ("C3", 69), ("G3", 67), ("A3", 65), ("C4", 63)]),
        *_stack("4.1.1", 3.5, [("C3", 73), ("G3", 69), ("D4", 67), ("E4", 65), ("G4", 63)]),
    ]
    drop_b_bloom = [
        *_stack("1.1.1", 3.5, [("D3", 74), ("A3", 70), ("C4", 68), ("E4", 66), ("F4", 64)]),
        *_stack("2.1.1", 3.5, [("Bb2", 74), ("F3", 70), ("A3", 68), ("C4", 66), ("D4", 64)]),
        *_stack("3.1.1", 3.5, [("F2", 73), ("C3", 69), ("G3", 67), ("A3", 65), ("C4", 63)]),
        *_stack("4.1.1", 3.5, [("C3", 73), ("G3", 69), ("D4", 67), ("E4", 65), ("G4", 63)]),
    ]
    break_stretch = [
        *_stack("1.1.1", 7.5, [("D3", 70), ("A3", 66), ("C4", 64), ("E4", 62), ("F4", 60)]),
        *_stack("3.1.1", 7.5, [("Bb2", 70), ("F3", 66), ("A3", 64), ("C4", 62)]),
        *_stack("5.1.1", 7.5, [("F2", 69), ("C3", 65), ("G3", 63), ("A3", 61)]),
        *_stack("7.1.1", 7.5, [("C3", 69), ("G3", 65), ("D4", 63), ("E4", 61)]),
    ]
    transition_pulse = [
        *_stack("1.1.1", 3.0, [("D3", 71), ("A3", 67), ("C4", 65), ("E4", 63), ("F4", 61)]),
        *_stack("2.1.1", 3.0, [("Bb2", 71), ("F3", 67), ("C4", 63)]),
        *_stack("3.1.1", 3.0, [("F2", 70), ("C3", 66), ("G3", 64), ("A3", 62)]),
        *_stack("4.1.1", 3.0, [("C3", 70), ("G3", 66), ("D4", 64), ("E4", 62)]),
    ]
    return [
        _variant(
            "chord_intro_hint_4bar",
            4,
            "Intro A. Only hint the first half of the cycle so the drop still reveals something.",
            intro_hint,
            "Two 2-bar washes establish darkness first, hope second.",
        ),
        _variant(
            "chord_intro_full_4bar",
            4,
            "Intro B. Full progression appears, but the voicing stays tucked and subdued.",
            intro_full,
            "This proves the harmony without stealing the center lane from the future sample.",
        ),
        _variant(
            "chord_drop_core_4bar",
            4,
            "Drop A. One bar per chord, full harmonic identity, still behind bass and drums.",
            drop_core,
            "The track should feel emotionally robust even when the hook stays small.",
        ),
        _variant(
            "chord_drop_a_lift_4bar",
            4,
            "Drop A lift. Same harmonic content as Drop A, with only rhythmic and dynamic tightening in the upper voices.",
            drop_a_lift,
            "The first lift gets bigger by pulse and brightness, not by revealing new harmony.",
        ),
        _variant(
            "chord_drop_b_bloom_4bar",
            4,
            "Drop B and its lift. This is where the Bb major-7 color finally blooms.",
            drop_b_bloom,
            "The hopeful widening is saved for the back half of the record so Drop B grows by harmony, not just loudness.",
        ),
        _variant(
            "chord_break_stretch_8bar",
            8,
            "Break. Stretch each chord to two bars and let the color tones ring.",
            break_stretch,
            "This is where the track breathes emotionally without losing key center.",
        ),
        _variant(
            "chord_transition_b_pulse_4bar",
            4,
            "Re-entry transition. Pull the break voicings back into a tighter pulse at restrained Drop-A-level harmonic density so Drop B can hit as a fresh reopening.",
            transition_pulse,
            "The transition should re-engage rhythm without giving away the full bloom before Drop B.",
        ),
    ]


def _stack(position: str, length_beats: float, notes: list[tuple[str, int]]) -> list[dict]:
    return [_event(note, position, length_beats, velocity, "chord tone") for note, velocity in notes]


def _bass_variants() -> list[dict]:
    intro_b_tease = [
        _event("D1", "1.1.1", 1.5, 95, "root hold"),
        _event("D1", "1.3.3", 0.25, 80, "internal pulse"),
        _event("Bb0", "2.1.1", 1.5, 93, "root hold"),
        _event("Bb1", "2.4.3", 0.25, 78, "tease octave"),
        _event("F1", "3.1.1", 1.5, 94, "root hold"),
        _event("F1", "3.3.3", 0.25, 79, "internal pulse"),
        _event("C1", "4.1.1", 1.5, 92, "root hold"),
        _event("C2", "4.4.3", 0.25, 80, "tease octave"),
    ]
    drop_a_core = [
        _event("D1", "1.1.1", 1.25, 96, "root hold"),
        _event("D1", "1.3.1", 0.5, 82, "rolling pulse"),
        _event("A1", "1.4.1", 0.25, 76, "fifth flick"),
        _event("Bb0", "2.1.1", 1.25, 94, "root hold"),
        _event("Bb1", "2.3.1", 0.25, 80, "octave pulse"),
        _event("F1", "2.4.1", 0.25, 77, "fifth release"),
        _event("D1", "2.4.3", 0.25, 75, "third color"),
        _event("F1", "3.1.1", 1.25, 95, "root hold"),
        _event("F1", "3.3.1", 0.5, 81, "rolling pulse"),
        _event("C2", "3.4.1", 0.25, 77, "fifth flick"),
        _event("C1", "4.1.1", 1.25, 93, "root hold"),
        _event("C2", "4.3.1", 0.25, 81, "octave pulse"),
        _event("G1", "4.4.1", 0.25, 77, "fifth release"),
        _event("D2", "4.4.3", 0.25, 79, "ninth lift"),
    ]
    drop_a_lift = [
        _event("D1", "1.1.1", 1.25, 96, "root hold"),
        _event("D1", "1.3.1", 0.25, 82, "rolling pulse"),
        _event("A1", "1.3.3", 0.25, 79, "fifth release"),
        _event("D1", "1.4.1", 0.25, 76, "root rebound"),
        _event("Bb0", "2.1.1", 1.25, 94, "root hold"),
        _event("Bb1", "2.3.1", 0.25, 82, "octave release"),
        _event("F1", "2.4.1", 0.25, 78, "fifth release"),
        _event("Bb0", "2.4.3", 0.25, 76, "root rebound"),
        _event("F1", "3.1.1", 1.25, 95, "root hold"),
        _event("F1", "3.3.1", 0.25, 81, "rolling pulse"),
        _event("C2", "3.3.3", 0.25, 79, "fifth release"),
        _event("F1", "3.4.1", 0.25, 76, "root rebound"),
        _event("C1", "4.1.1", 1.25, 93, "root hold"),
        _event("C2", "4.3.1", 0.25, 82, "octave release"),
        _event("G1", "4.4.1", 0.25, 78, "fifth release"),
        _event("C1", "4.4.3", 0.25, 80, "root rebound"),
    ]
    break_sparse = [
        _event("D1", "1.1.1", 1.0, 84, "root reminder"),
        _event("Bb0", "2.1.1", 1.0, 82, "root reminder"),
        _event("F1", "3.1.1", 1.0, 83, "root reminder"),
        _event("C1", "4.1.1", 1.0, 81, "root reminder"),
    ]
    transition_tease = [
        _event("D1", "1.1.1", 1.5, 90, "filtered root hold"),
        _event("D1", "1.4.3", 0.25, 77, "urgent pulse"),
        _event("Bb0", "2.1.1", 1.25, 88, "filtered root hold"),
        _event("Bb1", "2.4.1", 0.25, 79, "octave peek"),
        _event("F1", "3.1.1", 1.25, 89, "filtered root hold"),
        _event("F1", "3.3.3", 0.25, 78, "urgent pulse"),
        _event("C1", "4.1.1", 1.0, 91, "filtered root hold"),
        _event("C2", "4.3.1", 0.25, 81, "octave rise"),
        _event("D2", "4.4.1", 0.25, 83, "drop pull"),
        _event("F2", "4.4.3", 0.25, 79, "drop lift"),
    ]
    drop_b_core = [
        _event("D1", "1.1.1", 1.25, 97, "root hold"),
        _event("D1", "1.3.1", 0.25, 83, "rolling pulse"),
        _event("A1", "1.4.1", 0.25, 78, "fifth release"),
        _event("Bb0", "2.1.1", 1.25, 95, "root hold"),
        _event("Bb1", "2.3.1", 0.25, 82, "octave release"),
        _event("F1", "2.4.1", 0.25, 79, "fifth release"),
        _event("A1", "2.4.3", 0.25, 77, "maj7 color"),
        _event("F1", "3.1.1", 1.25, 96, "root hold"),
        _event("F1", "3.3.1", 0.25, 82, "rolling pulse"),
        _event("A1", "3.4.1", 0.25, 78, "third color"),
        _event("C1", "4.1.1", 1.25, 94, "root hold"),
        _event("C2", "4.3.1", 0.25, 82, "octave release"),
        _event("G1", "4.4.1", 0.25, 79, "fifth release"),
        _event("D2", "4.4.3", 0.25, 82, "ninth lift"),
    ]
    drop_b_lift = [
        _event("D1", "1.1.1", 1.25, 98, "root hold"),
        _event("D1", "1.3.1", 0.25, 84, "rolling pulse"),
        _event("A1", "1.3.3", 0.25, 80, "fifth release"),
        _event("C2", "1.4.1", 0.25, 78, "minor seventh color"),
        _event("E2", "1.4.3", 0.25, 80, "ninth lift"),
        _event("Bb0", "2.1.1", 1.25, 96, "root hold"),
        _event("Bb1", "2.3.1", 0.25, 84, "octave release"),
        _event("F1", "2.4.1", 0.25, 80, "fifth release"),
        _event("A1", "2.4.3", 0.25, 79, "maj7 color"),
        _event("F1", "3.1.1", 1.25, 97, "root hold"),
        _event("F1", "3.3.1", 0.25, 83, "rolling pulse"),
        _event("C2", "3.3.3", 0.25, 81, "fifth release"),
        _event("G2", "3.4.1", 0.25, 79, "ninth release"),
        _event("A1", "3.4.3", 0.25, 77, "third color"),
        _event("C1", "4.1.1", 1.25, 95, "root hold"),
        _event("C2", "4.3.1", 0.25, 84, "octave release"),
        _event("G1", "4.4.1", 0.25, 80, "fifth release"),
        _event("D2", "4.4.3", 0.25, 83, "ninth lift"),
    ]
    return [
        _variant(
            "bass_intro_b_tease_4bar",
            4,
            "Intro B. Hold the root for the first two beats, then reveal only one short octave tease every second bar.",
            intro_b_tease,
            "This is a sub hold plus one envelope-opened octave tease. No pitch bend; the personality should feel OG and locked.",
        ),
        _variant(
            "bass_drop_a_core_4bar",
            4,
            "Drop A. Held root authority in bars 1 and 3, release language only in bars 2 and 4.",
            drop_a_core,
            "The core drop feels hard because half the bars refuse to over-explain themselves.",
        ),
        _variant(
            "bass_drop_a_lift_4bar",
            4,
            "Drop A lift. Same harmonic language as Drop A, but with slightly tighter pocket and tone opening.",
            drop_a_lift,
            "The lift comes from feel and density, not from new bass harmony.",
        ),
        _variant(
            "bass_break_sparse_4bar",
            4,
            "Break. Root reminders only, no full release runs.",
            break_sparse,
            "The break should imply weight while leaving the mid lane and sample lane open.",
        ),
        _variant(
            "bass_transition_b_tease_4bar",
            4,
            "Re-entry transition. Filtered root holds and octave peeks pull the section back toward Drop B without spending the full rolling phrase yet.",
            transition_tease,
            "This should feel like the bass returning with intent, not like a second intro pasted into the middle.",
        ),
        _variant(
            "bass_drop_b_core_4bar",
            4,
            "Drop B. Same held-then-release logic, but the hopeful bars get maj7 / 9th color at the tail.",
            drop_b_core,
            "The emotional lift comes from harmonic color, not from rewriting the bass architecture.",
        ),
        _variant(
            "bass_drop_b_lift_4bar",
            4,
            "Drop B lift. Strongest release language of the track, still restricted to progression tones and color tones only.",
            drop_b_lift,
            "The bass gets more expressive, but the sub still reads as one confident voice.",
        ),
    ]


def _answer_stab_variants() -> list[dict]:
    drop_a_tail = [
        _event("A4", "4.4.1", 0.25, 70, "stab tone"),
        _event("D5", "4.4.1", 0.25, 76, "stab tone"),
    ]
    drop_b_conversation = [
        _event("A4", "2.4.1", 0.25, 74, "phrase-end stab"),
        _event("D5", "2.4.1", 0.25, 80, "phrase-end stab"),
    ]
    drop_b_lift = [
        _event("G4", "4.4.1", 0.25, 76, "phrase-end stab"),
        _event("D5", "4.4.1", 0.25, 82, "phrase-end stab"),
        _event("A4", "4.4.3", 0.25, 74, "tail smear"),
    ]
    return [
        _variant(
            "answer_drop_a_tail_4bar",
            4,
            "Drop A. Tiny phrase-end stab only, never a constant layer.",
            drop_a_tail,
            "This should feel like a clipped punctuation mark, not another bassline.",
        ),
        _variant(
            "answer_drop_b_conversation_4bar",
            4,
            "Drop B. Phrase-end warm organ-family answer on the alternate phrase ending only.",
            drop_b_conversation,
            "This lets the hook own one phrase ending and the answer own the other.",
        ),
        _variant(
            "answer_drop_b_lift_4bar",
            4,
            "Drop B lift. Strongest warm answer, still only at the opposing phrase ending.",
            drop_b_lift,
            "Keep the answer lane short and warm so it alternates with the hook instead of talking over it.",
        ),
    ]


def _hook_variants() -> list[dict]:
    intro_pickup = [
        _event("D5", "4.4.3", 0.5, 72, "filtered pickup"),
    ]
    drop_a = [
        _event("A4", "2.3.3", 0.25, 78, "hook cell"),
        _event("C5", "2.4.1", 0.25, 82, "hook cell"),
        _event("D5", "2.4.3", 0.5, 86, "hook resolve"),
        _event("A4", "4.3.3", 0.25, 76, "hook cell"),
        _event("C5", "4.4.1", 0.25, 80, "hook cell"),
        _event("D5", "4.4.3", 0.5, 84, "hook resolve"),
    ]
    drop_a_lift = [
        _event("A4", "2.3.3", 0.25, 79, "hook cell"),
        _event("C5", "2.4.1", 0.25, 83, "hook cell"),
        _event("D5", "2.4.3", 0.5, 87, "hook resolve"),
        _event("A4", "4.3.4", 0.25, 78, "hook cell"),
        _event("C5", "4.4.1", 0.25, 82, "hook cell"),
        _event("D5", "4.4.2", 0.5, 86, "hook resolve"),
    ]
    break_ghost = [
        _event("A4", "4.4.1", 0.5, 60, "ghost texture"),
    ]
    transition_pickup = [
        _event("A4", "4.3.3", 0.25, 70, "filtered pickup"),
        _event("C5", "4.4.1", 0.25, 73, "filtered pickup"),
        _event("D5", "4.4.3", 0.5, 78, "drop cue"),
    ]
    drop_b = [
        _event("A4", "4.3.1", 0.25, 80, "drop-b cell"),
        _event("C5", "4.3.3", 0.25, 84, "drop-b cell"),
        _event("D5", "4.4.1", 0.25, 88, "drop-b cell"),
        _event("F5", "4.4.3", 0.5, 90, "hope lift"),
    ]
    drop_b_lift = [
        _event("A4", "2.3.1", 0.25, 81, "drop-b cell"),
        _event("C5", "2.3.3", 0.25, 85, "drop-b cell"),
        _event("D5", "2.4.1", 0.25, 89, "drop-b cell"),
        _event("F5", "2.4.3", 0.5, 91, "hope lift"),
    ]
    return [
        _variant(
            "hook_intro_pickup_4bar",
            4,
            "Intro A / B. Only one filtered pickup at the end of the phrase.",
            intro_pickup,
            "The hook should arrive like a memory before it becomes a lane.",
        ),
        _variant(
            "hook_drop_a_phrase_4bar",
            4,
            "Drop A. Three-note phrase-end cell only on bars 2 and 4.",
            drop_a,
            "This keeps the kick and future sample lane clear.",
        ),
        _variant(
            "hook_drop_a_lift_4bar",
            4,
            "Drop A lift. Keep the same three-note hook cell, but tighten the pocket on the second phrase-end.",
            [
                _event("A4", "2.3.3", 0.25, 79, "hook cell"),
                _event("C5", "2.4.1", 0.25, 83, "hook cell"),
                _event("D5", "2.4.3", 0.5, 87, "hook resolve"),
                _event("A4", "4.3.4", 0.25, 78, "hook cell"),
                _event("C5", "4.4.1", 0.25, 82, "hook cell"),
                _event("D5", "4.4.2", 0.5, 86, "hook resolve"),
            ],
            "The hook gets bigger by phrasing and pressure, not by adding new melodic information.",
        ),
        _variant(
            "hook_break_ghost_4bar",
            4,
            "Break. One filtered timbral ghost every four bars at most, not a real hook phrase.",
            break_ghost,
            "The break ghost should read like a memory of the hook voice in the air, not a melodic statement.",
        ),
        _variant(
            "hook_transition_b_pickup_4bar",
            4,
            "Re-entry transition. Keep the hook mostly absent, then give one filtered pickup before Drop B lands.",
            transition_pickup,
            "This should tease the re-entry without stealing the full Drop B payoff.",
        ),
        _variant(
            "hook_drop_b_phrase_4bar",
            4,
            "Drop B. Four-note payoff cell once per four bars.",
            drop_b,
            "The extra note is the hopeful payoff. Using it constantly would cheapen it.",
        ),
        _variant(
            "hook_drop_b_lift_4bar",
            4,
            "Drop B lift. One stronger statement in bar 2, then leave bar 4 available for sample answers.",
            drop_b_lift,
            "This keeps the center lane free for phrases without losing melodic identity.",
        ),
    ]


def _parts(composition: dict) -> list[dict]:
    phrase_rows = composition["phrase_evidence"]["recommendations"]
    return [
        {
            "part_id": "drums",
            "writing_role": "4x4 spine with garage offbeat bounce and only lift-level embellishment.",
            "register_focus": "transient / top-end groove",
            "playback_rule": "Never rewrite the kick pattern. Energy changes happen through hat density, shaker brightness, loop support, and phrase-end transitions. Kick and clap stay on-grid; ghost hats are intentionally late; do not use one global swing value to fake the pocket.",
            "variants": _drum_variants(),
            "inspiration": _top_inspiration(phrase_rows, {"drums", "arrangement"}),
        },
        {
            "part_id": "bass-foundation",
            "writing_role": "Mono-safe rolling UKG bass anchor that owns the root path and gets its character from motion inside the phrase, not from becoming a hook.",
            "register_focus": "Bb0-D2",
            "playback_rule": "No pitch-bend gimmicks. The intro teaser is a root hold plus one envelope-opened octave hint every second bar, then the full drop adds rolling pulses without losing sub authority.",
            "variants": _bass_variants(),
            "inspiration": _top_inspiration(phrase_rows, {"bass", "harmony"}),
        },
        {
            "part_id": "og-reese-answer",
            "writing_role": "Warm organ/piano phrase-end stab answer that adds bite without becoming a second bassline.",
            "register_focus": "G4-F5",
            "playback_rule": "Rewrite this slot away from a Reese. Keep it clipped, warm, and short so the bass-foundation stays the only true low-end voice. Use the same timbral family as the hook, but make the answer shorter and slightly dirtier.",
            "variants": _answer_stab_variants(),
            "inspiration": _top_inspiration(phrase_rows, {"bass", "hook"}),
        },
        {
            "part_id": "chord-bed",
            "writing_role": "Dark-but-hopeful harmonic wash that carries emotional depth without taking the center lane.",
            "register_focus": "Bb2-G4",
            "playback_rule": "Keep the full progression stable. Drop A stays triad/add9-led; the exposed Bb major-7 color is reserved for the break and Drop B.",
            "variants": _chord_variants(),
            "inspiration": _top_inspiration(phrase_rows, {"harmony", "arrangement"}),
        },
        {
            "part_id": "hook-response",
            "writing_role": "Instrumental-led phrase-end melodic identity with enough space for a future re-versioned sample, not a dependency on one.",
            "register_focus": "G4-F5",
            "playback_rule": "Stay off the kick, enter late on the offbeat, and let a warm organ/garage stab timbre carry as much identity as the notes do. The hook should be slightly cleaner and longer-tailed than the answer stab.",
            "variants": _hook_variants(),
            "inspiration": _top_inspiration(phrase_rows, {"hook", "melody"}),
        },
    ]


def _top_inspiration(rows: list[dict], tags: set[str]) -> list[dict]:
    picks = []
    for row in rows:
        combined = " ".join([
            row.get("kind", ""),
            row.get("role", ""),
            row.get("summary", ""),
            " ".join(row.get("matched_keywords", [])),
        ]).lower()
        if not any(tag in combined for tag in tags):
            continue
        picks.append({
            "title": row["title"],
            "source": row["source"],
            "summary": row["summary"],
        })
    return picks[:2]


def _section_assignments() -> list[dict]:
    return [
        {
            "section_id": "intro_a",
            "bars": "1-16",
            "part_variants": {
                "drums": "drum_intro_core_2bar",
                "bass-foundation": None,
                "og-reese-answer": None,
                "chord-bed": "chord_intro_hint_4bar",
                "hook-response": None,
            },
            "notes": "Keep the first 8 bars almost rhythm-only. Let the chord hint fade in from bar 9, and use the hook pickup only at the very end.",
        },
        {
            "section_id": "intro_b",
            "bars": "17-32",
            "part_variants": {
                "drums": "drum_intro_b_tease_2bar",
                "bass-foundation": "bass_intro_b_tease_4bar",
                "og-reese-answer": None,
                "chord-bed": "chord_intro_full_4bar",
                "hook-response": "hook_intro_pickup_4bar",
            },
            "notes": "The bass teaser is mechanical on purpose: root hold for two beats, then one short octave hint every second bar. The top end is only teased here, not fully opened. Use phrase-end hat density or a light fill in the final bar if the handoff to Drop A feels too flat.",
        },
        {
            "section_id": "drop_a",
            "bars": "33-48",
            "part_variants": {
                "drums": "drum_drop_core_2bar",
                "bass-foundation": "bass_drop_a_core_4bar",
                "og-reese-answer": "answer_drop_a_tail_4bar",
                "chord-bed": "chord_drop_core_4bar",
                "hook-response": "hook_drop_a_phrase_4bar",
            },
            "notes": "The bass owns the section. The hook and stab only answer at phrase tails, and the Bb chord still avoids exposing its maj7 color. Use phrase-end fills at bars 8 and 16 rather than changing the core kick pattern.",
        },
        {
            "section_id": "drop_a_lift",
            "bars": "49-64",
            "part_variants": {
                "drums": "drum_drop_lift_2bar",
                "bass-foundation": "bass_drop_a_lift_4bar",
                "og-reese-answer": "answer_drop_a_tail_4bar",
                "chord-bed": "chord_drop_a_lift_4bar",
                "hook-response": "hook_drop_a_lift_4bar",
            },
            "notes": "Bigger by top-end density and phrase pocket only. Still no exposed Bb maj7 yet, no new bass harmonic content, and the instrumental has to stand on its own. Any extra pressure should come from shakers, ghost hats, or fill overlays, not new harmonic moves.",
        },
        {
            "section_id": "break",
            "bars": "65-80",
            "part_variants": {
                "drums": "drum_break_sparse_2bar",
                "bass-foundation": "bass_break_sparse_4bar",
                "og-reese-answer": None,
                "chord-bed": "chord_break_stretch_8bar",
                "hook-response": "hook_break_ghost_4bar",
            },
            "notes": "Let the air bed and upward-widened stretched chords carry the break instrumentally. If a future sample ever appears, keep it narrow and phrase-end only in roughly A3-F5. The hook ghost here should feel textural, not like a secret extra phrase.",
        },
        {
            "section_id": "transition_b",
            "bars": "81-96",
            "part_variants": {
                "drums": "drum_transition_switch_2bar",
                "bass-foundation": "bass_transition_b_tease_4bar",
                "og-reese-answer": None,
                "chord-bed": "chord_transition_b_pulse_4bar",
                "hook-response": "hook_transition_b_pickup_4bar",
            },
            "notes": "Use fresh transition drums and a filtered bass return so the second drop feels actively pulled in. Keep the chords pulsing at restrained density here; this section should feel like a re-entry switch, not like the break continuing or Drop B arriving early. This is the best place for a dedicated riser and a pre-drop cut overlay.",
        },
        {
            "section_id": "drop_b",
            "bars": "97-112",
            "part_variants": {
                "drums": "drum_drop_core_2bar",
                "bass-foundation": "bass_drop_b_core_4bar",
                "og-reese-answer": "answer_drop_b_conversation_4bar",
                "chord-bed": "chord_drop_b_bloom_4bar",
                "hook-response": "hook_drop_b_phrase_4bar",
            },
            "notes": "This is where the harmonic bloom and phrase-end stab answer arrive. The hook is half-density here so the answer can own the alternate phrase ending. The bass stays the only true low-end voice. Let the transition land, then keep the first four bars of the drop slightly cleaner before more top pressure returns.",
        },
        {
            "section_id": "drop_b_lift",
            "bars": "113-128",
            "part_variants": {
                "drums": "drum_drop_lift_2bar",
                "bass-foundation": "bass_drop_b_lift_4bar",
                "og-reese-answer": "answer_drop_b_lift_4bar",
                "chord-bed": "chord_drop_b_bloom_4bar",
                "hook-response": "hook_drop_b_lift_4bar",
            },
            "notes": "Keep hook and answer alternating by phrase. The biggest lift should come from tops and widened chord spread, not another new lane.",
        },
        {
            "section_id": "outro",
            "bars": "129-144",
            "part_variants": {
                "drums": "drum_outro_strip_2bar",
                "bass-foundation": "bass_break_sparse_4bar",
                "og-reese-answer": None,
                "chord-bed": "chord_intro_hint_4bar",
                "hook-response": None,
            },
            "notes": "Strip back to the most stable ideas for a DJ-safe exit, but keep a whisper of the air bed alive so the outro does not seal shut.",
        },
    ]


def _support_layers() -> list[dict]:
    return [
        {
            "layer_id": "top_presence",
            "role": "2-6 kHz bite and forward motion",
            "owners": [
                "filtered open-hat tease inside drum_intro_b_tease_2bar",
                "offbeat open-hat accents inside drum_drop_core_2bar / drum_drop_lift_2bar",
                "the sharper re-entry hats and clap return inside drum_transition_switch_2bar",
                "the clipped attack on hook-response",
                "the phrase-end warm answer stab in Drop B",
            ],
            "rule": "If the drop feels closed-in, solve it here before widening the chords or brightening the whole mix. Tease it in Intro B, feature it in Drop A, reduce it in the break, use it to pull the re-entry forward in transition_b, and make it strongest in Drop B Lift.",
        },
        {
            "layer_id": "air_bed",
            "role": "8 kHz+ height and ceiling",
            "owners": [
                "constant quiet shimmer/noise bed from intro_a onward",
                "more audible air in the break",
                "tucked but present air return in the drops",
            ],
            "rule": "The air source should be constant enough that the record feels tall, but quiet enough that the hats still define the groove.",
        },
    ]


def _drum_spec() -> dict:
    return {
        "kick": {
            "tuning_target": "Tune the kick body to `D` (tonic), with the weight living around `D1/D2` rather than an untuned boom.",
            "layering": "Layer a sub/body kick with a shorter click/attack layer. One sample should own weight; the other should own definition.",
            "tail_length": "Keep the tail short, roughly `90-120ms`, so the rolling bass can breathe without extreme sidechain.",
            "role": "Body-forward and physical, not harsh or over-clipped.",
        },
        "top_elements": {
            "closed_hat_pattern": "Use offbeat hats as the stable garage scaffold, then let ghost hats create the real swing.",
            "ghost_hat_placement": "Ghost hats should live on the `e` and `a` spaces around the beat and be intentionally pushed late by roughly `5-15 ticks`, not randomized.",
            "open_hat_pattern": "Use restrained open hats in Intro B and full offbeat/open phrase-end hats in the drops. Let phrase-end open hats help mark the pocket rather than washing every offbeat equally.",
            "clap_layering": "Clap lands on `2` and `4`. Layer with a tighter snare/rim element only when more presence is needed, not by default.",
            "shaker_role": "Shaker sits in the `5-8 kHz` energy bed and is one of the main lift tools in drop lifts and transition bars.",
        },
        "midi_policy": {
            "swing": "No global swing preset. Keep kick and clap on-grid. Push ghost hats late manually so the groove feels deliberate rather than mechanically shuffled.",
            "velocity_ranges": {
                "kick": "120-127 equivalent authority",
                "clap": "110-127 with small variation",
                "closed_hat": "60-110 with real variation",
                "ghost_hat": "30-70, felt more than heard",
                "open_hat": "90-120",
                "shaker": "70-100 with phrase-end lift",
            },
            "humanization": "Kick and clap remain tight to grid. Closed hats and shakers can move slightly. Ghost hats should be consistently late, not randomly loose.",
            "phrase_curve": "In bars `13-16` of a 16-bar section, lift hat/shaker velocity slightly so the transition pressure rises before the boundary.",
        },
        "micro_architecture": {
            "bars_1_4": "Establish the core groove with kick/clap/offbeat hat and minimal extras.",
            "bars_5_8": "Add ghost-hat life and loop support so the pocket deepens without sounding like a new pattern.",
            "bars_9_12": "Increase shaker or open-hat energy slightly so the section feels alive rather than static.",
            "bars_13_16": "Use phrase-end fills, risers, filter moves, and/or short groove drops to push toward the next section.",
        },
        "transition_toolkit": [
            "Use `drum_phrase_end_fill_1bar` at selected 8-bar and 16-bar boundaries.",
            "Use `drum_section_riser_1bar` at major section changes where you need energy to rise without changing the kick pattern.",
            "Use `drum_pre_drop_cut_1bar` before the most important returns so the next downbeat lands harder.",
            "Automate a high-pass filter on the drum bus during intros and transitions so the body opens into the drop instead of appearing instantly.",
            "Increase ghost-hat density in the final four bars of big sections rather than waiting for the next section to do all the work.",
        ],
    }


def build_report(args: argparse.Namespace) -> dict:
    composition = build_song_composition_pass_report(_namespace(args))
    return {
        "brief_id": composition["brief_id"],
        "readiness": composition["readiness"],
        "emotional_target": composition["emotional_target"],
        "architectural_decisions": composition["architectural_decisions"],
        "frequency_strategy": composition["frequency_strategy"],
        "originality_guardrails": composition["originality_guardrails"],
        "drum_spec": _drum_spec(),
        "parts": _parts(composition),
        "support_layers": _support_layers(),
        "section_assignments": _section_assignments(),
    }


def render_text(report: dict) -> str:
    lines = []
    lines.append("# Song MIDI Plan")
    lines.append("")
    lines.append(f"- brief: `{report['brief_id']}`")
    lines.append(f"- readiness: `{report['readiness']['label']}`")
    lines.append(f"- emotional target: {', '.join(report['emotional_target'])}")
    lines.append("")
    lines.append("## Architectural Decisions")
    for key, value in report["architectural_decisions"].items():
        lines.append(f"- {key.replace('_', ' ')}: {value['decision']}")
        lines.append(f"  why: {value['why']}")
    lines.append("")
    lines.append("## Frequency Strategy")
    for key, value in report["frequency_strategy"].items():
        lines.append(f"- {key.replace('_', ' ')}: {value}")
    lines.append("")
    lines.append("## Drum Spec")
    lines.append(f"- kick tuning: {report['drum_spec']['kick']['tuning_target']}")
    lines.append(f"- kick layering: {report['drum_spec']['kick']['layering']}")
    lines.append(f"- kick tail: {report['drum_spec']['kick']['tail_length']}")
    lines.append(f"- top hats: {report['drum_spec']['top_elements']['closed_hat_pattern']}")
    lines.append(f"- ghost hats: {report['drum_spec']['top_elements']['ghost_hat_placement']}")
    lines.append(f"- open hats: {report['drum_spec']['top_elements']['open_hat_pattern']}")
    lines.append(f"- clap layering: {report['drum_spec']['top_elements']['clap_layering']}")
    lines.append(f"- shaker role: {report['drum_spec']['top_elements']['shaker_role']}")
    lines.append(f"- swing policy: {report['drum_spec']['midi_policy']['swing']}")
    lines.append(f"- humanization: {report['drum_spec']['midi_policy']['humanization']}")
    lines.append(f"- phrase curve: {report['drum_spec']['midi_policy']['phrase_curve']}")
    lines.append("- transition toolkit:")
    for row in report["drum_spec"]["transition_toolkit"]:
        lines.append(f"  - {row}")
    lines.append("")
    lines.append("## Originality Guardrails")
    for row in report["originality_guardrails"]:
        lines.append(f"- {row}")
    lines.append("")
    lines.append("## Parts")
    for part in report["parts"]:
        lines.append(f"- `{part['part_id']}` :: {part['writing_role']}")
        lines.append(f"  register: {part['register_focus']}")
        lines.append(f"  playback: {part['playback_rule']}")
        for variant in part["variants"]:
            lines.append(f"  - `{variant['variant_id']}` ({variant['bars']} bars)")
            lines.append(f"    use: {variant['usage']}")
            lines.append(f"    note: {variant['note']}")
            preview = ", ".join(
                f"{event['note']}@{event['position']} len {event['length_beats']}"
                for event in variant["events"][:6]
            )
            lines.append(f"    preview: {preview}")
    lines.append("")
    lines.append("## Support Layers")
    for row in report["support_layers"]:
        lines.append(f"- `{row['layer_id']}` :: {row['role']}")
        lines.append(f"  owners: {' | '.join(row['owners'])}")
        lines.append(f"  rule: {row['rule']}")
    lines.append("")
    lines.append("## Section Assignments")
    for row in report["section_assignments"]:
        lines.append(f"- `{row['section_id']}` bars {row['bars']}")
        for part_id, variant_id in row["part_variants"].items():
            lines.append(f"  {part_id}: {variant_id or 'mute / reserved'}")
        lines.append(f"  note: {row['notes']}")
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
