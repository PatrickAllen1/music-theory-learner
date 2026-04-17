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
            "influence": "Soul Mass Transit System / Y U QT public proxy",
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


def _named_references() -> list[dict]:
    return [
        {
            "axis": "low_end_pressure",
            "track": "KETTAMA - It Gets Better",
            "local_source": "als/analysis/kettama-it-gets-better-notes.md",
            "listen_for": [
                "kick body weight",
                "low-end physicality without harsh drum clipping",
                "overall mix density before the top end gets bright",
            ],
            "why_this_track": "This is the pressure benchmark for the song. Use it to calibrate how large the record feels in the body before worrying about extra top-end polish.",
        },
        {
            "axis": "groove_pocket",
            "track": "Interplanetary Criminal - Slow Burner",
            "local_source": "als/analysis/interplanetary-criminal-slow-burner-notes.md",
            "listen_for": [
                "ghost-hat drag",
                "phrase-end groove movement",
                "how the 4x4 stays bouncy rather than rigid",
            ],
            "why_this_track": "This is the bounce and re-entry pocket reference. Judge hats, loop support, and phrase pressure against it.",
        },
        {
            "axis": "bass_roll_character",
            "track": "Y U QT - NRG",
            "local_source": "docs/transcripts/yuqt2_spans.json",
            "listen_for": [
                "rolling bass motion that is rhythmic first, tonal second",
                "sub staying stable underneath the motion",
                "how much internal movement the mid layer carries before sounding melodic",
            ],
            "why_this_track": "This is the current named public proxy for the repo's Y U QT rolling-bass lane while the internal knowledge still comes from the local transcript study.",
        },
        {
            "axis": "hook_and_harmonic_readability",
            "track": "Sammy Virji - I Guess We're Not the Same",
            "local_source": "docs/transcripts/sammyvirjiiguesswerenotthesame_spans.json",
            "listen_for": [
                "hook identity at low note count",
                "chord color reading emotionally without softening the groove",
                "how melodic clarity survives inside a club mix",
            ],
            "why_this_track": "This is the hook-readability and harmonic-intelligence reference for the current lane.",
        },
    ]


def _sound_design_spec() -> dict:
    return {
        "bass_sub": {
            "engine": "Serum 2",
            "recipe": [
                "Use the Sub oscillator on a sine wave as the main weight source.",
                "Mono on, legato off by default, with only a tiny glide if needed (`~5-20ms`).",
                "Amp envelope: instant attack, full sustain, short release (`~40-60ms`).",
                "Keep the sub mostly clean in-patch; do the extra grit on the bass bus or harmonic layer instead.",
            ],
            "role": "Stable floor and root authority.",
        },
        "bass_mid": {
            "engine": "Serum 2",
            "recipe": [
                "Osc A: square-leaning basic shape for body.",
                "Osc B: saw or harmonically richer shape for upper motion, low blend, slight detune only.",
                "Low-pass filter with gentle drive.",
                "Movement comes from note-length variation plus filter/saturation breathing, not a big melodic rewrite.",
                "Keep most of this layer above `~120-150 Hz` so the sub stays clean underneath.",
            ],
            "role": "Character and rolling motion without becoming a second hook.",
        },
        "hook_voice": {
            "engine": "Serum 2",
            "recipe": [
                "FM-organ / woody garage-stab family, not a supersaw or vocal placeholder.",
                "Short pluck envelope: fast attack, medium-short decay, low sustain, short release.",
                "Keep the sound mid-focused and readable; high-pass enough to stay out of the bass lane.",
                "Use light saturation and compression for identity; send to short plate / filtered delay rather than drowning it in long reverb.",
            ],
            "role": "Instrumental-first identity lane that can stand without a sample.",
        },
        "answer_voice": {
            "engine": "Serum 2",
            "recipe": [
                "Same family as the hook voice, but shorter envelope and slightly dirtier tone.",
                "Use more bite or saturation than the hook, but do not turn it abrasive.",
                "Keep it phrase-end only so it reads as punctuation, not a second topline.",
            ],
            "role": "Drop B punctuation by substitution, not stacking.",
        },
        "chord_bed": {
            "engine": "Serum 2",
            "recipe": [
                "Use a hybrid pad/stab approach: a sustained emotional bed plus pulsed articulation where sections need it.",
                "Favor a warm saw/triangle-style palette with restrained unison and controlled stereo spread.",
                "Filter and tuck the Drop A state; widen and brighten in the break and Drop B.",
                "Voice-lead smoothly and preserve common tones where possible so the loop feels hypnotic.",
            ],
            "role": "Emotional depth and hopeful bloom without taking over the center lane.",
        },
        "air_layer": {
            "engine": "Serum 2",
            "recipe": [
                "Use an atonal noise-based air bed as the constant ceiling so it stays harmonically safe.",
                "High-pass heavily and keep it quiet.",
                "Make it most audible in the break, then tuck it under the drops.",
            ],
            "role": "Height, ceiling, and openness above `8 kHz`.",
        },
        "sample_source_policy": {
            "drums": "Use a modern UKG / garage sample selection policy: 909/garage-compatible kick layers, crisp clap/snare hybrids, 909-style hats, and one shaker source that survives filtering.",
            "tutorial_note": "During the actual build capture, lock the exact sample names so the handheld tutorial can reference real files instead of archetypes.",
        },
    }


def _stereo_field_map() -> list[dict]:
    return [
        {"element": "kick", "placement": "mono / center", "why": "keeps the body focused and club-safe"},
        {"element": "sub bass", "placement": "mono / center", "why": "non-negotiable low-end stability"},
        {"element": "mid-bass", "placement": "mono to narrow stereo above crossover", "why": "keeps weight centered while allowing a little character width"},
        {"element": "hook", "placement": "mostly center with stereo send support only", "why": "the identity lane should read clearly on mono and small speakers"},
        {"element": "answer stab", "placement": "slightly wider than the hook via returns, not by panning the dry source away", "why": "keeps the dialogue related but distinct"},
        {"element": "chord bed", "placement": "wide stereo, widening further in break and Drop B", "why": "this is where emotional width lives"},
        {"element": "air bed", "placement": "widest layer in the track", "why": "creates ceiling and height without crowding the center"},
        {"element": "loops / tops", "placement": "stereo but controlled, with the most important transients still reading near center", "why": "preserves groove clarity while making the record feel open"},
    ]


def _mix_master_spec() -> dict:
    return {
        "gain_staging": {
            "track_peak_target": "Most individual tracks should peak roughly between `-12 dBFS` and `-8 dBFS` before heavy bus processing.",
            "bus_peak_target": "Drum, bass, and music buses should generally live around `-8 dBFS` to `-6 dBFS` peak before the premaster.",
            "premaster_headroom": "Leave roughly `-6 dBFS` peak headroom on the premaster before the final limiter stage.",
        },
        "bus_structure": [
            "Drum bus",
            "Bass bus",
            "Music bus (chords + hook + answer + air)",
            "FX bus / returns",
            "Premaster",
        ],
        "sidechain_network": [
            "Kick -> bass sub: deepest duck, short attack, release matched to kick tail.",
            "Kick -> bass mid layer: slightly lighter duck than the sub, but still clearly breathing.",
            "Kick -> chord bus: gentle duck so chords pump around the groove without disappearing.",
            "Kick -> air bed: very light duck, mostly to keep transients clean in the drops.",
        ],
        "parallel_strategy": [
            "Drum parallel for extra body and density, blended back lightly.",
            "Bass parallel saturation / compression only if the harmonic layer needs more constant attitude.",
            "Avoid letting parallel chains make the groove flatter than the dry buses.",
        ],
        "saturation_strategy": [
            "Kick: subtle body thickening, not obvious crunch.",
            "Bass mid layer: main saturation character lives here.",
            "Chord bed: mild warmth so it glues, not fuzz.",
            "Hook / answer: light color for identity and presence.",
        ],
        "reverb_plan": [
            "Short room or ambience for some drum cohesion if needed.",
            "Short plate for hook/answer family.",
            "Longer hall/plate for chords and air, with filtering so the low end stays clean.",
        ],
        "delay_plan": [
            "Use filtered delays mostly as throws or phrase-end space, not constant wash.",
            "Hook can take a short rhythmic delay if it helps identity, but keep the center readable.",
        ],
        "master_chain": [
            "Utility / gain trim",
            "Gentle glue compression if needed",
            "Subtle saturation or soft clip stage",
            "Limiter only after the mix is behaving",
        ],
        "target_loudness": {
            "build_stage": "Prioritize headroom and translation over loudness while writing.",
            "final_direction": "Aim for a club-ready modern UKG level only after the balances and transients are correct; do not chase loudness early.",
        },
        "monitoring_checks": [
            "mono compatibility",
            "small-speaker / phone readability",
            "car or everyday speaker translation",
            "club-oriented low-end sanity check if possible",
        ],
    }


def _automation_plan() -> list[dict]:
    return [
        {
            "lane": "drum_bus_high_pass",
            "sections": "Intro A -> Drop A and Break -> Transition B -> Drop B",
            "shape": "Open the drum bus body gradually into the drop, then use a lighter filtered state for transitions so the return feels earned.",
        },
        {
            "lane": "bass_mid_filter_breathing",
            "sections": "Intro B through Drop B Lift",
            "shape": "Use small cyclical movement tied to phrase energy; stronger at phrase ends, calmer in the middle of the bar.",
        },
        {
            "lane": "chord_width_and_brightness",
            "sections": "Drop A -> Break -> Drop B",
            "shape": "Keep Drop A tucked, widen upward in the break, and return with more obvious bloom in Drop B.",
        },
        {
            "lane": "hook_send_levels",
            "sections": "Drop A and Drop B",
            "shape": "Keep the hook mostly dry enough to stay readable, then automate throws or extra tail only at selected phrase ends.",
        },
        {
            "lane": "air_bed_level",
            "sections": "Whole track",
            "shape": "Always present, most audible in the break, then tucked back under the drops and left whispering in the outro.",
        },
        {
            "lane": "transition_fx",
            "sections": "Major section boundaries",
            "shape": "Use risers, filtered returns, and pre-drop cuts intentionally at named bar boundaries rather than sprinkling FX everywhere.",
        },
    ]


def _transition_inventory() -> list[dict]:
    return [
        {
            "boundary": "32 -> 33",
            "purpose": "Intro B into Drop A",
            "tools": ["drum_section_riser_1bar", "filtered bass teaser opens", "drum-bus HP clears off"],
        },
        {
            "boundary": "64 -> 65",
            "purpose": "Drop A Lift into Break",
            "tools": ["phrase-end fill", "drum thinning", "reverb and chord width open"],
        },
        {
            "boundary": "80 -> 81",
            "purpose": "Break into Transition B",
            "tools": ["re-entry drum switch", "tighter chord pulse", "filtered bass re-implication"],
        },
        {
            "boundary": "96 -> 97",
            "purpose": "Transition B into Drop B",
            "tools": ["drum_pre_drop_cut_1bar", "filtered hook pickup", "full drop body returns"],
        },
        {
            "boundary": "128 -> 129",
            "purpose": "Drop B Lift into Outro",
            "tools": ["strip top pressure first", "leave air whisper", "return to stable groove identity"],
        },
    ]


def _originality_checks() -> list[str]:
    return [
        "If you hummed the hook next to a source hook, a listener should hear a different contour or rhythmic identity within the first four notes.",
        "If a bass phrase starts feeling too source-like, keep the root function but change either gate lengths, phrase-end note choice, or register emphasis.",
        "If a transition feels too recognizable, keep the role but change the timing or the exact FX combination.",
    ]


def _build_order(composition: dict, midi_plan: dict) -> list[dict]:
    return [
        {
            "stage": 1,
            "name": "Kick, core groove, and air ceiling",
            "goal": "Lock the 4x4 body, swingy tops, and quiet air bed before melodic material starts competing for attention.",
            "do_now": [
                "Build the kick/clap/off-hat skeleton from the intro and drop drum variants.",
                "Commit to the kick spec early: tonic-tuned body, layered click, short tail, and no harsh clipped overhang.",
                "Program ghost hats and shakers with manual late-push timing instead of relying on one global swing preset.",
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
            "goal": "Turn the stance into a real 144-bar record by assigning the exact phrase variants section by section.",
            "do_now": [
                "Lay in the section assignments exactly as the MIDI plan specifies.",
                "Humanize within each variant family so the same 2-bar or 4-bar pattern does not repeat identically for an entire section.",
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
        "Resolve fallback-heavy synth choices and pairwise sound conflicts before the full Ableton build. Do not assume mix fixes will solve selection problems later.",
        "The bass roll must feel rhythmic-primary. If tonal motion is doing most of the work, simplify it.",
        "Drop A Lift must not reveal new harmonic information. If it does, move that idea to the break or Drop B.",
        "When the Drop B answer arrives, the hook must step back to half density.",
        "The break must widen upward, not just sustain longer.",
        "The drums need micro-architecture inside each 16-bar section: establish, deepen, lift, then push. If a section loops identically, it is not finished.",
        "Ghost hats should be intentionally late, not randomly loose, and the kick should stay tonic-tuned and short enough for the bass to breathe.",
        "Keep the top-end map intact: Intro B teases, Drop A opens, Break breathes, Drop B Lift releases hardest.",
        "If a phrase feels too close to a source track, keep the function and change the contour, register, or rhythm immediately.",
        composition["architectural_decisions"]["break_sample_lane_target"]["decision"],
    ]


def _later_handoff(composition: dict) -> list[str]:
    return [
        "When the track is built later, bounce each major section and compare it back to the section targets before changing the arrangement.",
        "Capture the final MIDI for bass, chord bed, hook, and answer so the guided lesson can point to exact note decisions instead of abstractions.",
        "Capture screenshots of every Serum 2 patch and every major Ableton device chain once they are stable enough to teach from.",
        "Bounce checkpoint audio after drums, after drums+bass, after chords, after Drop A, after Drop B, and after the premaster.",
        "Keep the composition pass and MIDI plan beside the Ableton session; they are the authority, not late-session instinct.",
        f"Sample/vocal future rule: {composition['sample_strategy']['version_strategy']}",
    ]


def _tutorial_capture_requirements() -> dict:
    return {
        "goal": "Make the later Serum 2 + Ableton 12 tutorial traceable to the real successful build instead of reconstructed from memory afterward.",
        "must_capture": [
            "Serum 2 screenshots for bass sub, bass mid, chord bed, hook, answer, and air patches.",
            "Ableton device-chain screenshots for drums, bass, chords, hook/answer, returns, and premaster.",
            "MIDI screenshots for drum groove, bass phrase, chord voicings, and hook/answer alternation.",
            "Checkpoint audio bounces after each major tutorial milestone.",
        ],
        "checkpoints": [
            "kick + air",
            "full drums",
            "drums + bass",
            "drums + bass + chords",
            "Drop A",
            "Drop B",
            "premaster",
        ],
        "teaching_notes_to_log": [
            "What changed and why at each checkpoint.",
            "Which reference axis drove the decision.",
            "Any tempting wrong turn that got rejected and why.",
            "Any setting that mattered more than expected so the tutorial can emphasize it later.",
        ],
    }


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
        "named_references": _named_references(),
        "sound_design_spec": _sound_design_spec(),
        "stereo_field_map": _stereo_field_map(),
        "mix_master_spec": _mix_master_spec(),
        "automation_plan": _automation_plan(),
        "transition_inventory": _transition_inventory(),
        "originality_checks": _originality_checks(),
        "build_order": _build_order(composition, midi_plan),
        "section_targets": _section_targets(composition, midi_plan),
        "critical_checks": _critical_checks(composition),
        "later_handoff": _later_handoff(composition),
        "tutorial_capture_requirements": _tutorial_capture_requirements(),
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
    lines.append("## Named References")
    for row in report["named_references"]:
        lines.append(f"- `{row['axis']}` :: {row['track']}")
        lines.append(f"  source: {row['local_source']}")
        lines.append(f"  listen for: {' | '.join(row['listen_for'])}")
        lines.append(f"  why: {row['why_this_track']}")
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
    lines.append("## Sound Design Spec")
    for key, value in report["sound_design_spec"].items():
        if isinstance(value, dict) and "recipe" in value:
            lines.append(f"- `{key}` :: {value['engine']}")
            lines.append(f"  role: {value['role']}")
            lines.append(f"  recipe: {' | '.join(value['recipe'])}")
        else:
            lines.append(f"- `{key}`")
            for inner_key, inner_value in value.items():
                lines.append(f"  {inner_key}: {inner_value}")
    lines.append("")
    lines.append("## Stereo Field Map")
    for row in report["stereo_field_map"]:
        lines.append(f"- `{row['element']}` :: {row['placement']}")
        lines.append(f"  why: {row['why']}")
    lines.append("")
    lines.append("## Mix / Master Spec")
    for key, value in report["mix_master_spec"].items():
        if isinstance(value, dict):
            lines.append(f"- {key.replace('_', ' ')}:")
            for inner_key, inner_value in value.items():
                lines.append(f"  - {inner_key}: {inner_value}")
        else:
            lines.append(f"- {key.replace('_', ' ')}:")
            for item in value:
                lines.append(f"  - {item}")
    lines.append("")
    lines.append("## Automation Plan")
    for row in report["automation_plan"]:
        lines.append(f"- `{row['lane']}` :: {row['sections']}")
        lines.append(f"  shape: {row['shape']}")
    lines.append("")
    lines.append("## Transition Inventory")
    for row in report["transition_inventory"]:
        lines.append(f"- `{row['boundary']}` :: {row['purpose']}")
        lines.append(f"  tools: {' | '.join(row['tools'])}")
    lines.append("")
    lines.append("## Critical Checks")
    for row in report["critical_checks"]:
        lines.append(f"- {row}")
    lines.append("")
    lines.append("## Originality Checks")
    for row in report["originality_checks"]:
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
    lines.append("")
    lines.append("## Tutorial Capture Requirements")
    lines.append(f"- goal: {report['tutorial_capture_requirements']['goal']}")
    lines.append("- must capture:")
    for row in report["tutorial_capture_requirements"]["must_capture"]:
        lines.append(f"  - {row}")
    lines.append("- checkpoints:")
    for row in report["tutorial_capture_requirements"]["checkpoints"]:
        lines.append(f"  - {row}")
    lines.append("- teaching notes to log:")
    for row in report["tutorial_capture_requirements"]["teaching_notes_to_log"]:
        lines.append(f"  - {row}")
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
