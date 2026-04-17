#!/usr/bin/env python3
"""
build_frozen_song_spec.py

Turn the full-song blueprint and decision tree into a tighter, model-facing
"frozen" song spec. This is the first artifact that should read like an actual
record stance rather than a template plus options.

Examples:
    python3 als/build_frozen_song_spec.py --brief ukg-140-og-bounce-driver
    python3 als/build_frozen_song_spec.py --brief ukg-2step-dark-stab --format json
"""

from __future__ import annotations

import argparse
import json
from argparse import Namespace
from pathlib import Path

try:
    from build_song_decision_tree import build_report as build_song_decision_tree_report
    from design_full_song_blueprint import build_report as build_full_song_blueprint_report
    from phrase_evidence import DEFAULT_ANALYSIS_DIR, DEFAULT_TRANSCRIPTS_DIR, build_phrase_library, recommend_for_blueprint
    from technique_bank import DEFAULT_BANK_PATH, load_bank
except ModuleNotFoundError:
    from .build_song_decision_tree import build_report as build_song_decision_tree_report
    from .design_full_song_blueprint import build_report as build_full_song_blueprint_report
    from .phrase_evidence import DEFAULT_ANALYSIS_DIR, DEFAULT_TRANSCRIPTS_DIR, build_phrase_library, recommend_for_blueprint
    from .technique_bank import DEFAULT_BANK_PATH, load_bank


DEFAULT_CATALOG_DIR = Path("als/catalog/profiles")
DEFAULT_SERUM_BRIEFS_PATH = Path("als/serum-track-briefs.json")
DEFAULT_SONG_BRIEFS_PATH = Path("als/song-blueprint-briefs.json")
DEFAULT_TEMPLATES_PATH = Path("als/song-production-templates.json")


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build a frozen full-song spec from a song brief.")
    parser.add_argument("--brief", required=True, help="Song brief id from the manifest.")
    parser.add_argument("--song-briefs", default=str(DEFAULT_SONG_BRIEFS_PATH), help="Song-level brief manifest JSON.")
    parser.add_argument("--templates", default=str(DEFAULT_TEMPLATES_PATH), help="Song production templates JSON.")
    parser.add_argument("--catalog-dir", default=str(DEFAULT_CATALOG_DIR), help="Directory of generated *-profiles.json files.")
    parser.add_argument("--serum-briefs", default=str(DEFAULT_SERUM_BRIEFS_PATH), help="Serum brief manifest JSON.")
    parser.add_argument("--analysis-dir", default=str(DEFAULT_ANALYSIS_DIR), help="ALS analysis JSON directory.")
    parser.add_argument("--transcripts-dir", default=str(DEFAULT_TRANSCRIPTS_DIR), help="Transcript spans directory.")
    parser.add_argument("--technique-bank", default=str(DEFAULT_BANK_PATH), help="Technique bank JSON path.")
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
        prefer_rendered=args.prefer_rendered,
        limit_per_part=args.limit_per_part,
        mutation_limit=args.mutation_limit,
        max_swaps=args.max_swaps,
        format="json",
    )


def _first_layer_by_role(blueprint: dict, roles: set[str]) -> dict | None:
    for layer in blueprint["synth_layers"]:
        if layer["role"] in roles:
            return layer
    return None


def _first_sample_slot(blueprint: dict, slot_ids: list[str]) -> dict | None:
    for slot_id in slot_ids:
        for lane in blueprint["sample_lanes"]:
            if lane["slot_id"] == slot_id:
                return lane
    return None


def _pick_bold_moves(tree: dict) -> list[dict]:
    branch_priority = ["groove", "low_end", "hook", "harmony", "width", "arrangement"]
    moves: list[dict] = []
    seen = set()
    for domain in branch_priority:
        branch = next((row for row in tree["branches"] if row["domain"] == domain), None)
        if not branch:
            continue
        for technique in branch["recommended_techniques"]:
            if technique["id"] in seen:
                continue
            moves.append({
                "domain": domain,
                "id": technique["id"],
                "name": technique["name"],
                "source": technique["source"],
                "why_now": technique["when_to_use"],
                "what_it_does": technique["what_it_does"],
            })
            seen.add(technique["id"])
            break
    return moves[:6]


def _pick_rejections(blueprint: dict, tree: dict) -> list[str]:
    rejections = [
        "Do not let the response hook behave like a constant topline; keep it punctuational so the future sample lane stays viable.",
        "Do not stack multiple width-heavy low-mid layers at full strength at the same time.",
        "Do not over-resolve the harmony with busy chord movement that makes the bassline feel secondary.",
    ]
    if blueprint["sample_lanes"]:
        rejections.append("Do not fill every reserved sample lane now; leave at least one real center-mid vacancy for future chops or spoken phrases.")
    if any(row["domain"] == "arrangement" for row in tree["branches"]):
        rejections.append("Do not spend the biggest transition move before Drop B; save the most obvious contrast for the later payoff.")
    return rejections


def _build_stabilizers(blueprint: dict) -> list[str]:
    interaction = blueprint["production_techniques"]["interaction_analysis"]
    stabilizers: list[str] = []
    for row in interaction["decision_commitments"]["required_pairings"][:4]:
        stabilizers.append(row["rule"])
    for row in interaction["decision_commitments"]["mandatory_constraints"][:4]:
        stabilizers.append(row["rule"])
        stabilizers.extend(row["required_moves"][:2])
    stabilizers.extend(blueprint["mix_rules"][:3])
    return list(dict.fromkeys(item for item in stabilizers if item))


def _section_focus(blueprint: dict, section: dict) -> dict:
    section_id = section["section_id"]
    bass = _first_layer_by_role(blueprint, {"bass", "sub"})
    reese = _first_layer_by_role(blueprint, {"reese"})
    harmony = _first_layer_by_role(blueprint, {"pad"})
    hook = _first_layer_by_role(blueprint, {"lead", "pluck", "stab"})
    kick = _first_sample_slot(blueprint, ["kick"])
    loop = _first_sample_slot(blueprint, ["drum_loop_layer"])
    vocal = _first_sample_slot(blueprint, ["vocal_space"])
    atmosphere = _first_sample_slot(blueprint, ["atmosphere"])
    transition = _first_sample_slot(blueprint, ["transition_fx"])

    primary: list[str] = []
    support: list[str] = []
    keep_open: list[str] = []

    if section_id.startswith("intro"):
        primary.extend(item["slot_id"] for item in [kick] if item)
        support.extend(item["part_id"] for item in [harmony] if item)
        support.extend(item["slot_id"] for item in [loop, atmosphere] if item)
        keep_open.extend(item["slot_id"] for item in [vocal] if item)
    elif "transition" in section_id:
        primary.extend(item["slot_id"] for item in [kick, loop, transition] if item)
        support.extend(item["part_id"] for item in [bass, harmony] if item)
        support.extend(item["slot_id"] for item in [atmosphere] if item)
        keep_open.extend(item["slot_id"] for item in [vocal] if item)
    elif "break" in section_id:
        primary.extend(item["part_id"] for item in [harmony] if item)
        support.extend(item["slot_id"] for item in [atmosphere, vocal, transition] if item)
        keep_open.extend(item["part_id"] for item in [bass] if item)
    elif "drop_b" in section_id:
        primary.extend(item["part_id"] for item in [bass, reese] if item)
        primary.extend(item["slot_id"] for item in [kick, loop] if item)
        support.extend(item["part_id"] for item in [hook] if item)
        support.extend(item["slot_id"] for item in [vocal, transition] if item)
    elif "drop" in section_id:
        primary.extend(item["part_id"] for item in [bass] if item)
        primary.extend(item["slot_id"] for item in [kick] if item)
        support.extend(item["part_id"] for item in [reese, hook] if item)
        support.extend(item["slot_id"] for item in [loop] if item)
        keep_open.extend(item["slot_id"] for item in [vocal] if item)
    else:
        primary.extend(item["slot_id"] for item in [kick] if item)
        support.extend(item["part_id"] for item in [bass, harmony] if item)
        support.extend(item["slot_id"] for item in [atmosphere] if item)

    return {
        "section_id": section_id,
        "bars": f"{section['start_bar']}-{section['end_bar']}",
        "goal": section["goal"],
        "primary_owners": primary,
        "supporting_layers": support,
        "must_remain_open": keep_open,
    }


def _layer_hierarchy(blueprint: dict) -> list[dict]:
    output = []
    priority_map = {
        "bass": 1,
        "sub": 1,
        "reese": 2,
        "pad": 3,
        "lead": 4,
        "pluck": 4,
        "stab": 4,
        "fx": 5,
    }
    for layer in blueprint["synth_layers"]:
        output.append({
            "layer_id": layer["part_id"],
            "kind": "synth",
            "priority": priority_map.get(layer["role"], 6),
            "role": layer["role"],
            "job": layer["job_in_track"],
            "arrangement_role": layer["arrangement_role"],
            "profile_id": layer.get("profile_id"),
            "audio_status": layer.get("audio_status"),
            "processing_chain_id": layer.get("processing_chain_id"),
            "als_anchor": {
                "track": layer.get("track"),
                "analysis_slug": layer.get("analysis_slug"),
            },
        })
    for lane in blueprint["sample_lanes"]:
        if not lane["required"]:
            continue
        output.append({
            "layer_id": lane["slot_id"],
            "kind": "sample_lane",
            "priority": 2 if lane["slot_type"] in {"kick", "clap_snare", "drum_loop"} else 5,
            "role": lane["slot_type"],
            "job": lane["purpose"],
            "arrangement_role": lane["lane"],
            "profile_id": None,
            "audio_status": "n/a",
            "processing_chain_id": lane.get("processing_chain_id"),
            "als_anchor": None,
        })
    output.sort(key=lambda row: (row["priority"], row["layer_id"]))
    return output


def build_report(args: argparse.Namespace) -> dict:
    blueprint = build_full_song_blueprint_report(_namespace(args))
    decision_tree = build_song_decision_tree_report(_namespace(args))
    bank = load_bank(Path(args.technique_bank))
    phrase_library = build_phrase_library(
        bank,
        analysis_dir=Path(args.analysis_dir),
        transcripts_dir=Path(args.transcripts_dir),
    )
    phrase_evidence = recommend_for_blueprint(blueprint, phrase_library, args.phrase_limit)
    bold_moves = _pick_bold_moves(decision_tree)
    rejected_moves = _pick_rejections(blueprint, decision_tree)
    stabilizers = _build_stabilizers(blueprint)
    section_intent = [_section_focus(blueprint, section) for section in blueprint["arrangement"]]
    layer_hierarchy = _layer_hierarchy(blueprint)

    harmonic = blueprint["harmonic_plan"]
    hook_layer = _first_layer_by_role(blueprint, {"lead", "pluck", "stab"})
    bass_layer = _first_layer_by_role(blueprint, {"bass", "sub"})
    thesis = (
        f"Build a {blueprint['bpm']} BPM {blueprint['key']} speed-garage record whose thesis is kick-led pressure plus "
        f"an OG low-end spine, while the harmony ({' -> '.join(harmonic['progression'])}) adds emotional depth without "
        f"taking over the center lane. The foreground hook should stay economical through `{hook_layer['part_id'] if hook_layer else 'hook lane'}`, "
        f"and the true sub ownership stays locked to `{bass_layer['part_id'] if bass_layer else 'bass foundation'}`."
    )

    return {
        "brief_id": blueprint["brief_id"],
        "description": blueprint["description"],
        "readiness": blueprint["readiness"],
        "bpm": blueprint["bpm"],
        "key": blueprint["key"],
        "harmonic_plan": blueprint["harmonic_plan"],
        "thesis": thesis,
        "bold_moves_to_keep": bold_moves,
        "tempting_moves_to_reject": rejected_moves,
        "required_stabilizers": stabilizers,
        "section_intent": section_intent,
        "layer_hierarchy": layer_hierarchy,
        "ableton_reference_points": {
            "returns": blueprint["returns"],
            "mix_rules": blueprint["mix_rules"],
            "automation_rules": blueprint["automation_rules"],
            "als_anchor_profiles": [
                {
                    "part_id": layer["part_id"],
                    "profile_id": layer.get("profile_id"),
                    "track": layer.get("track"),
                    "analysis_slug": layer.get("analysis_slug"),
                    "processing_chain_id": layer.get("processing_chain_id"),
                }
                for layer in blueprint["synth_layers"]
                if layer.get("profile_id")
            ],
        },
        "phrase_evidence": phrase_evidence,
        "decision_tree_summary": {
            "root_question": decision_tree["root_question"],
            "decision_order": decision_tree["decision_order"],
        },
    }


def render_text(report: dict) -> str:
    lines = []
    lines.append("# Frozen Song Spec")
    lines.append("")
    lines.append(f"- brief: `{report['brief_id']}`")
    lines.append(f"- readiness: `{report['readiness']['label']}`")
    lines.append(f"- runtime target: {report['readiness'].get('duration_minutes', 0)} minutes current draft")
    lines.append("")
    lines.append("## Thesis")
    lines.append(report["thesis"])
    lines.append("")
    lines.append("## Bold Moves To Keep")
    for row in report["bold_moves_to_keep"]:
        lines.append(f"- `{row['name']}` [{row['source']}]")
        lines.append(f"  why now: {row['why_now']}")
    lines.append("")
    lines.append("## Tempting Moves To Reject")
    for row in report["tempting_moves_to_reject"]:
        lines.append(f"- {row}")
    lines.append("")
    lines.append("## Required Stabilizers")
    for row in report["required_stabilizers"]:
        lines.append(f"- {row}")
    lines.append("")
    lines.append("## Section Intent")
    for row in report["section_intent"]:
        lines.append(f"- `{row['section_id']}` bars {row['bars']}: {row['goal']}")
        if row["primary_owners"]:
            lines.append(f"  primary: {', '.join(row['primary_owners'])}")
        if row["supporting_layers"]:
            lines.append(f"  support: {', '.join(row['supporting_layers'])}")
        if row["must_remain_open"]:
            lines.append(f"  keep open: {', '.join(row['must_remain_open'])}")
    lines.append("")
    lines.append("## Layer Hierarchy")
    for row in report["layer_hierarchy"]:
        lines.append(
            f"- `{row['layer_id']}` [{row['kind']}/{row['role']}] priority={row['priority']} chain={row['processing_chain_id'] or '-'}"
        )
        lines.append(f"  job: {row['job']}")
        if row["als_anchor"] and row["als_anchor"]["track"]:
            lines.append(
                f"  ALS anchor: {row['als_anchor']['track']} ({row['als_anchor']['analysis_slug']})"
            )
    lines.append("")
    lines.append("## Ableton Reference Points")
    lines.append("- returns:")
    for row in report["ableton_reference_points"]["returns"]:
        lines.append(f"  - `{row['return_id']}` {row['name']}: {row['purpose']}")
    lines.append("- mix rules:")
    for row in report["ableton_reference_points"]["mix_rules"]:
        lines.append(f"  - {row}")
    lines.append("- automation rules:")
    for row in report["ableton_reference_points"]["automation_rules"]:
        lines.append(f"  - {row}")
    if report["phrase_evidence"]["recommendations"]:
        lines.append("")
        lines.append("## Phrase Evidence")
        for row in report["phrase_evidence"]["recommendations"]:
            lines.append(f"- `{row['title']}` [{row['kind']}/{row['role']}] source={row['source']}")
            if row["matched_keywords"]:
                lines.append(f"  matched: {', '.join(row['matched_keywords'])}")
            if row["emotion_hints"]:
                lines.append(f"  emotion: {', '.join(row['emotion_hints'])}")
            lines.append(f"  {row['summary']}")
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
