#!/usr/bin/env python3
"""
build_song_composition_pass.py

Turn the frozen song spec into an actual composition-facing plan: harmonic
language, bass writing, hook writing, section development, and concrete note
choices that can later be transformed into lesson steps.
"""

from __future__ import annotations

import argparse
import json
import re
from argparse import Namespace
from pathlib import Path

try:
    from build_frozen_song_spec import build_report as build_frozen_song_spec_report
except ModuleNotFoundError:
    from .build_frozen_song_spec import build_report as build_frozen_song_spec_report


DEFAULT_CATALOG_DIR = Path("als/catalog/profiles")
DEFAULT_SERUM_BRIEFS_PATH = Path("als/serum-track-briefs.json")
DEFAULT_SONG_BRIEFS_PATH = Path("als/song-blueprint-briefs.json")
DEFAULT_TEMPLATES_PATH = Path("als/song-production-templates.json")

PITCH_CLASS = {
    "C": 0,
    "C#": 1,
    "Db": 1,
    "D": 2,
    "D#": 3,
    "Eb": 3,
    "E": 4,
    "F": 5,
    "F#": 6,
    "Gb": 6,
    "G": 7,
    "G#": 8,
    "Ab": 8,
    "A": 9,
    "A#": 10,
    "Bb": 10,
    "B": 11,
}
NOTE_NAMES_SHARP = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
NOTE_NAMES_FLAT = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build a composition-facing song pass from the frozen song spec.")
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


def _parse_chord_root(symbol: str) -> tuple[str, str]:
    match = re.match(r"^([A-G](?:#|b)?)(.*)$", symbol)
    if not match:
        raise ValueError(f"Unsupported chord symbol: {symbol}")
    return match.group(1), match.group(2)


def _note_name(pc: int, octave: int, prefer_flat: bool = False) -> str:
    names = NOTE_NAMES_FLAT if prefer_flat else NOTE_NAMES_SHARP
    return f"{names[pc % 12]}{octave}"


def _note_from(root: str, interval: int, octave: int) -> str:
    base_pc = PITCH_CLASS[root]
    base_midi = base_pc + 12 * (octave + 1)
    midi = base_midi + interval
    prefer_flat = "b" in root
    pc = midi % 12
    out_octave = (midi // 12) - 1
    return _note_name(pc, out_octave, prefer_flat=prefer_flat)


def _progression_voicing(chord: str, octave: int) -> list[str]:
    root, quality = _parse_chord_root(chord)
    if quality.startswith("m9"):
        intervals = [0, 7, 10, 14, 15]
    elif quality.startswith("maj7"):
        intervals = [0, 7, 11, 14]
    elif quality.startswith("add9"):
        intervals = [0, 7, 14, 16]
    else:
        intervals = [0, 4, 7]
    return [_note_from(root, interval, octave) for interval in intervals]


def _root_map(progression: list[str]) -> list[str]:
    out = []
    for chord in progression:
        root, _ = _parse_chord_root(chord)
        out.append(root)
    return out


def _bass_release_notes(chord: str, octave: int) -> list[str]:
    root, quality = _parse_chord_root(chord)
    if quality.startswith("maj7"):
        intervals = [0, 12, 7, 4]
    elif quality.startswith("m"):
        intervals = [0, 12, 7, 10]
    elif quality.startswith("add9"):
        intervals = [0, 12, 7, 14]
    else:
        intervals = [0, 12, 7, 4]
    return [_note_from(root, interval, octave) for interval in intervals]


def _hook_cells(key: str) -> dict:
    root, _ = _parse_chord_root(key)
    if root == "D":
        return {
            "drop_a": ["A4", "C5", "D5"],
            "drop_b": ["A4", "C5", "D5", "F5"],
            "answer_alt": ["G4", "A4", "C5"],
        }
    return {
        "drop_a": ["G4", "A4", "C5"],
        "drop_b": ["G4", "A4", "C5", "D5"],
        "answer_alt": ["E4", "G4", "A4"],
    }


def _chord_octaves(progression: list[str]) -> list[int]:
    mapping = []
    for chord in progression:
        root, _ = _parse_chord_root(chord)
        if root in {"Bb", "A#", "F"}:
            mapping.append(2)
        else:
            mapping.append(3)
    return mapping


def _section_composition(section: dict, progression: list[str], hook_cells: dict) -> dict:
    section_id = section["section_id"]
    if section_id.startswith("intro_a"):
        return {
            "section_id": section_id,
            "bars": section["bars"],
            "harmonic_behavior": "Hint only the first half of the 4-chord cycle and keep the chord bed filtered.",
            "bass_behavior": "No full bass line yet. Let the low-end identity be implied by occasional root pulses only.",
            "hook_behavior": "No full hook. Only one delayed or filtered pickup from the response lane at the end of bar 16.",
        }
    if section_id.startswith("intro_b"):
        return {
            "section_id": section_id,
            "bars": section["bars"],
            "harmonic_behavior": "Run the full progression once per 4 bars, but keep the top note emphasis subdued.",
            "bass_behavior": "Introduce the root path and one held-note-then-release gesture per 2 bars.",
            "hook_behavior": "Use only the first two notes of the drop-A response cell as a teaser.",
        }
    if section_id == "break":
        return {
            "section_id": section_id,
            "bars": section["bars"],
            "harmonic_behavior": "Stretch each chord to 2 bars and let the top voices linger on 9th / maj7 color tones.",
            "bass_behavior": "Mute the full release runs. Keep only occasional root reminders or a filtered tail.",
            "hook_behavior": "Either no hook or one sparse ghost response every 4 bars so the sample lane stays open.",
        }
    if section_id == "drop_a":
        return {
            "section_id": section_id,
            "bars": section["bars"],
            "harmonic_behavior": "Full 4-chord loop with the pad tucked behind the bass and loop energy.",
            "bass_behavior": "Held root through the first half of each bar, then short release notes on bars 2 and 4 only.",
            "hook_behavior": f"Use `{', '.join(hook_cells['drop_a'])}` as the offbeat response cell at phrase ends, not every bar.",
        }
    if section_id == "drop_a_lift":
        return {
            "section_id": section_id,
            "bars": section["bars"],
            "harmonic_behavior": "Same progression, slightly brighter upper chord tone on the Fadd9 and Cadd9 bars.",
            "bass_behavior": "Release notes every bar, but only one octave jump per 2-bar unit.",
            "hook_behavior": f"Alternate `{', '.join(hook_cells['drop_a'])}` with `{', '.join(hook_cells['answer_alt'])}`.",
        }
    if section_id == "drop_b":
        return {
            "section_id": section_id,
            "bars": section["bars"],
            "harmonic_behavior": "Reintroduce the full progression with more obvious hopeful color on Bbmaj7 and Cadd9.",
            "bass_behavior": "Same held-then-release shape, but let the release note on the C chord hit the 9th for lift.",
            "hook_behavior": f"Use `{', '.join(hook_cells['drop_b'])}` sparingly and leave a center gap for sample answers.",
        }
    if section_id == "drop_b_lift":
        return {
            "section_id": section_id,
            "bars": section["bars"],
            "harmonic_behavior": "Keep the progression stable; the change comes from phrase density, not reharmonisation.",
            "bass_behavior": "Strongest ornament bars of the track, but still only from progression tones and chord color notes.",
            "hook_behavior": "Sample lane or response lane takes the strongest phrase-end answer here; do not let both fight.",
        }
    return {
        "section_id": section_id,
        "bars": section["bars"],
        "harmonic_behavior": "Return to the most stable half of the progression for mix-out.",
        "bass_behavior": "Reduce back to root implication and kick-led closure.",
        "hook_behavior": "Strip to minimal phrase fragments or mute completely.",
    }


def build_report(args: argparse.Namespace) -> dict:
    frozen = build_frozen_song_spec_report(_namespace(args))
    progression = list(frozen["harmonic_plan"]["progression"])
    roots = _root_map(progression)
    chord_octaves = _chord_octaves(progression)
    hook_cells = _hook_cells(frozen["key"])

    harmonic_palette = []
    for chord, octave in zip(progression, chord_octaves):
        harmonic_palette.append({
            "chord": chord,
            "voicing": _progression_voicing(chord, octave),
            "emotional_job": (
                "dark center" if chord.startswith("Dm")
                else "hopeful lift" if "maj7" in chord
                else "open forward motion" if chord.startswith("F")
                else "suspended pre-return tension"
            ),
        })

    bass_language = []
    bass_octaves = {"D": 2, "Bb": 1, "A#": 1, "F": 2, "C": 2}
    for chord in progression:
        root, _ = _parse_chord_root(chord)
        bass_language.append({
            "chord": chord,
            "root_path_note": _note_from(root, 0, bass_octaves.get(root, 2)),
            "release_notes": _bass_release_notes(chord, bass_octaves.get(root, 2)),
        })

    composition_sections = [
        _section_composition(section, progression, hook_cells)
        for section in frozen["section_intent"]
    ]

    hook_plan = {
        "thesis": "Three-note economy in Drop A, four-note payoff only in Drop B, always offbeat enough to leave the kick and future sample lane clear.",
        "drop_a_cell": hook_cells["drop_a"],
        "drop_b_cell": hook_cells["drop_b"],
        "secondary_answer_cell": hook_cells["answer_alt"],
        "note_logic": "Keep the hook mostly inside the D-minor / chord-color vocabulary, with only one brighter lift note when the section needs hope rather than more darkness.",
    }

    sample_strategy = {
        "center_lane_rule": "The vocal/sample lane stays empty until the instrumental version already works; when it enters, it replaces hook density rather than stacking with it.",
        "drop_b_role": "Phrase-end answers or resequenced chops only, not a constant topline.",
        "transition_role": "Use one printed throw or delay-tail transition per major section boundary, not every 4 bars.",
    }

    return {
        "brief_id": frozen["brief_id"],
        "readiness": frozen["readiness"],
        "thesis": frozen["thesis"],
        "emotional_target": ["dark", "hopeful"],
        "harmonic_language": {
            "progression": progression,
            "root_path": roots,
            "palette": harmonic_palette,
            "rule": "Keep the song dark through the tonic and low-end center, but let maj7 / add9 color tones supply the hopeful feeling rather than brightening the whole track.",
        },
        "bass_plan": {
            "thesis": "OG speed-garage low end: held root authority first, then short eighth-note or octave release figures built only from progression notes.",
            "four_bar_root_path": [row["root_path_note"] for row in bass_language],
            "per_chord_release_language": bass_language,
            "rule": "No ornamental note is allowed if it implies a new chord. The bass gets busier only by reusing the progression's own notes.",
        },
        "hook_plan": hook_plan,
        "section_plan": composition_sections,
        "sample_strategy": sample_strategy,
        "stabilizers": frozen["required_stabilizers"],
        "phrase_evidence": frozen["phrase_evidence"],
        "als_reference_points": frozen["ableton_reference_points"]["als_anchor_profiles"],
    }


def render_text(report: dict) -> str:
    lines = []
    lines.append("# Song Composition Pass")
    lines.append("")
    lines.append(f"- brief: `{report['brief_id']}`")
    lines.append(f"- readiness: `{report['readiness']['label']}`")
    lines.append(f"- emotional target: {', '.join(report['emotional_target'])}")
    lines.append("")
    lines.append("## Thesis")
    lines.append(report["thesis"])
    lines.append("")
    lines.append("## Harmonic Language")
    lines.append(f"- progression: {' -> '.join(report['harmonic_language']['progression'])}")
    lines.append(f"- root path: {' -> '.join(report['harmonic_language']['root_path'])}")
    lines.append(f"- rule: {report['harmonic_language']['rule']}")
    for row in report["harmonic_language"]["palette"]:
        lines.append(f"- `{row['chord']}`: {' - '.join(row['voicing'])} :: {row['emotional_job']}")
    lines.append("")
    lines.append("## Bass Plan")
    lines.append(f"- thesis: {report['bass_plan']['thesis']}")
    lines.append(f"- four-bar roots: {' -> '.join(report['bass_plan']['four_bar_root_path'])}")
    lines.append(f"- rule: {report['bass_plan']['rule']}")
    for row in report["bass_plan"]["per_chord_release_language"]:
        lines.append(f"- `{row['chord']}` release notes: {' -> '.join(row['release_notes'])}")
    lines.append("")
    lines.append("## Hook Plan")
    lines.append(f"- thesis: {report['hook_plan']['thesis']}")
    lines.append(f"- Drop A cell: {' -> '.join(report['hook_plan']['drop_a_cell'])}")
    lines.append(f"- Drop B cell: {' -> '.join(report['hook_plan']['drop_b_cell'])}")
    lines.append(f"- Answer cell: {' -> '.join(report['hook_plan']['secondary_answer_cell'])}")
    lines.append(f"- rule: {report['hook_plan']['note_logic']}")
    lines.append("")
    lines.append("## Section Plan")
    for row in report["section_plan"]:
        lines.append(f"- `{row['section_id']}` bars {row['bars']}")
        lines.append(f"  harmony: {row['harmonic_behavior']}")
        lines.append(f"  bass: {row['bass_behavior']}")
        lines.append(f"  hook: {row['hook_behavior']}")
    lines.append("")
    lines.append("## Sample Strategy")
    for key, value in report["sample_strategy"].items():
        lines.append(f"- {key.replace('_', ' ')}: {value}")
    lines.append("")
    lines.append("## ALS Reference Points")
    for row in report["als_reference_points"]:
        lines.append(f"- `{row['part_id']}` -> {row['track']} ({row['analysis_slug']}) [{row['processing_chain_id']}]")
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
