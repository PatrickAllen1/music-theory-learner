#!/usr/bin/env python3
"""
design_full_song_blueprint.py

Turn a song-level brief plus the refined Serum stack into a complete production
blueprint with arrangement, drum/sample lanes, processing plans, returns, and
export scaffolding.

Examples:
    python3 als/design_full_song_blueprint.py --brief ukg-2step-dark-stab
    python3 als/design_full_song_blueprint.py --brief ukg-4x4-pluck-driver --format json
"""

from __future__ import annotations

import argparse
import json
from argparse import Namespace
from copy import deepcopy
from pathlib import Path

try:
    from refine_serum_track_blueprint import build_report as build_refined_blueprint_report
    from technique_bank import DEFAULT_BANK_PATH, load_bank, recommend_for_blueprint
except ModuleNotFoundError:
    from .refine_serum_track_blueprint import build_report as build_refined_blueprint_report
    from .technique_bank import DEFAULT_BANK_PATH, load_bank, recommend_for_blueprint


DEFAULT_CATALOG_DIR = Path("als/catalog/profiles")
DEFAULT_SERUM_BRIEFS_PATH = Path("als/serum-track-briefs.json")
DEFAULT_SONG_BRIEFS_PATH = Path("als/song-blueprint-briefs.json")
DEFAULT_TEMPLATES_PATH = Path("als/song-production-templates.json")


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Design a complete full-song production blueprint from a song brief.")
    parser.add_argument("--brief", required=True, help="Song brief id from the manifest.")
    parser.add_argument("--song-briefs", default=str(DEFAULT_SONG_BRIEFS_PATH), help="Song-level brief manifest JSON.")
    parser.add_argument("--templates", default=str(DEFAULT_TEMPLATES_PATH), help="Song production templates JSON.")
    parser.add_argument("--catalog-dir", default=str(DEFAULT_CATALOG_DIR), help="Directory of generated *-profiles.json files.")
    parser.add_argument("--serum-briefs", default=str(DEFAULT_SERUM_BRIEFS_PATH), help="Serum brief manifest JSON.")
    parser.add_argument("--technique-bank", default=str(DEFAULT_BANK_PATH), help="Production technique bank JSON path.")
    parser.add_argument("--technique-limit", type=int, default=6, help="Maximum production techniques to attach. Default: 6")
    parser.add_argument("--prefer-rendered", action="store_true", help="Prefer rendered profiles where available.")
    parser.add_argument("--limit-per-part", type=int, default=5, help="Max candidates to inspect per part. Default: 5")
    parser.add_argument("--mutation-limit", type=int, default=6, help="Max mutation suggestions per part. Default: 6")
    parser.add_argument("--max-swaps", type=int, default=2, help="Maximum refinement swaps to apply. Default: 2")
    parser.add_argument("--format", choices=["json", "text"], default="text", help="Output format.")
    return parser


def _load_song_brief(path: Path, brief_id: str) -> dict:
    payload = json.loads(path.read_text())
    briefs = payload.get("briefs", {})
    if brief_id not in briefs:
        raise KeyError(f"song brief not found: {brief_id}")
    return {"brief_id": brief_id, **briefs[brief_id]}


def _load_template(path: Path, template_id: str) -> dict:
    payload = json.loads(path.read_text())
    templates = payload.get("templates", {})
    if template_id not in templates:
        raise KeyError(f"template not found: {template_id}")
    return {"template_id": template_id, **templates[template_id]}


def _serum_namespace(args: argparse.Namespace, serum_brief_id: str) -> Namespace:
    return Namespace(
        catalog_dir=args.catalog_dir,
        briefs=args.serum_briefs,
        brief=serum_brief_id,
        prefer_rendered=args.prefer_rendered,
        limit_per_part=args.limit_per_part,
        mutation_limit=args.mutation_limit,
        alternative_limit=max(args.limit_per_part, 5),
        max_swaps=args.max_swaps,
        format="json",
    )


def _build_arrangement(sections: list[dict]) -> list[dict]:
    cursor = 1
    arrangement = []
    for row in sections:
        length_bars = int(row["length_bars"])
        arrangement.append({
            **row,
            "start_bar": cursor,
            "end_bar": cursor + length_bars - 1,
        })
        cursor += length_bars
    return arrangement


def _merge_sample_slots(template_slots: list[dict], overrides: dict) -> list[dict]:
    merged = []
    overrides = overrides or {}
    for row in template_slots:
        merged.append({
            **deepcopy(row),
            **deepcopy(overrides.get(row["slot_id"], {})),
        })
    return merged


def _build_drum_and_sample_lanes(song_brief: dict, template: dict) -> list[dict]:
    slots = _merge_sample_slots(template["sample_slots"], song_brief.get("sample_slot_overrides") or {})
    chains = template["processing_chains"]
    lanes = []
    for row in slots:
        chain_id = row.get("processing_chain_id")
        lanes.append({
            "slot_id": row["slot_id"],
            "slot_type": row["slot_type"],
            "required": bool(row.get("required")),
            "lane": row["lane"],
            "purpose": row["purpose"],
            "processing_chain_id": chain_id,
            "processing_chain": deepcopy(chains.get(chain_id)),
        })
    return lanes


def _build_synth_layers(song_brief: dict, template: dict, synth_report: dict) -> list[dict]:
    chains = template["processing_chains"]
    chain_defaults = template["role_chain_defaults"]
    layer_meta = song_brief.get("synth_layers") or {}
    layers = []
    for part in synth_report["parts"]:
        meta = layer_meta.get(part["part_id"], {})
        chain_id = meta.get("chain_id") or chain_defaults.get(part["role"])
        selection = part.get("selection")
        layers.append({
            "part_id": part["part_id"],
            "role": part["role"],
            "job_in_track": meta.get("job_in_track") or f"cover the {part['role']} role cleanly in the song.",
            "arrangement_role": meta.get("arrangement_role") or "present where the arrangement needs it.",
            "target_tone": part.get("target_tone") or [],
            "target_mix": part.get("target_mix") or [],
            "goals": part.get("goals") or [],
            "constraint_mode": part.get("constraint_mode"),
            "profile_id": selection.get("profile_id") if selection else None,
            "track": selection.get("track") if selection else None,
            "analysis_slug": selection.get("analysis_slug") if selection else None,
            "tone_tags": selection.get("tone_tags") if selection else [],
            "mix_tags": selection.get("mix_tags") if selection else [],
            "audio_status": selection.get("audio_status") if selection else "missing",
            "selection_notes": selection.get("notes") if selection else [],
            "mutation_suggestions": selection.get("mutation_suggestions") if selection else [],
            "processing_chain_id": chain_id,
            "processing_chain": deepcopy(chains.get(chain_id)),
            "unresolved": selection is None,
        })
    return layers


def _readiness(song_brief: dict, synth_report: dict, arrangement: list[dict], sample_lanes: list[dict], synth_layers: list[dict]) -> dict:
    unresolved_synth_parts = sum(1 for layer in synth_layers if layer["unresolved"])
    fallback_synth_parts = sum(1 for layer in synth_layers if layer.get("constraint_mode") not in {None, "full"})
    pairwise_conflicts = synth_report["final"]["pairwise_conflict_count"]
    missing_processing = sum(
        1
        for row in [*sample_lanes, *synth_layers]
        if not row.get("processing_chain")
    )
    required_sample_slots = sum(1 for lane in sample_lanes if lane["required"])
    total_bars = arrangement[-1]["end_bar"] if arrangement else 0

    issues = []
    if unresolved_synth_parts:
        issues.append("One or more synth parts are unresolved.")
    if pairwise_conflicts:
        issues.append("Selected synth parts still have at least one pairwise conflict.")
    if fallback_synth_parts:
        issues.append("Some synth parts are still using fallback constraint matches.")
    if missing_processing:
        issues.append("One or more lanes lack an explicit processing chain.")
    if required_sample_slots == 0:
        issues.append("No required sample lanes were defined.")
    if total_bars < 56:
        issues.append("Arrangement is too short to feel release-shaped.")

    if unresolved_synth_parts or missing_processing or total_bars < 56:
        label = "blocked"
    elif pairwise_conflicts > 1 or fallback_synth_parts > 1:
        label = "needs_work"
    elif pairwise_conflicts == 0 and fallback_synth_parts == 0:
        label = "strong"
    else:
        label = "usable"

    return {
        "label": label,
        "unresolved_synth_parts": unresolved_synth_parts,
        "fallback_synth_parts": fallback_synth_parts,
        "pairwise_conflicts": pairwise_conflicts,
        "missing_processing_chains": missing_processing,
        "required_sample_slots": required_sample_slots,
        "total_bars": total_bars,
        "issues": issues,
    }


def build_report(args: argparse.Namespace) -> dict:
    song_brief = _load_song_brief(Path(args.song_briefs), args.brief)
    template = _load_template(Path(args.templates), song_brief["template_id"])
    synth_report = build_refined_blueprint_report(_serum_namespace(args, song_brief["serum_brief_id"]))
    arrangement = _build_arrangement(template["arrangement_sections"])
    sample_lanes = _build_drum_and_sample_lanes(song_brief, template)
    synth_layers = _build_synth_layers(song_brief, template, synth_report)
    readiness = _readiness(song_brief, synth_report, arrangement, sample_lanes, synth_layers)
    blueprint_core = {
        "brief_id": song_brief["brief_id"],
        "description": song_brief["description"],
        "template_id": template["template_id"],
        "serum_brief_id": song_brief["serum_brief_id"],
        "bpm": song_brief["bpm"],
        "key": song_brief["key"],
        "energy_profile": song_brief["energy_profile"],
        "harmonic_plan": song_brief["harmonic_plan"],
        "drum_strategy": song_brief["drum_strategy"],
        "melodic_strategy": song_brief["melodic_strategy"],
        "arrangement_notes": song_brief.get("arrangement_notes") or [],
        "reserved_spaces": song_brief.get("reserved_spaces") or [],
        "arrangement": arrangement,
        "sample_lanes": sample_lanes,
        "synth_layers": synth_layers,
        "returns": deepcopy(template["returns"]),
        "automation_rules": deepcopy(template["automation_rules"]),
        "mix_rules": deepcopy(template["mix_rules"]),
        "export_plan": deepcopy(template["export_plan"]),
        "synth_blueprint": {
            "selected_profile_ids": synth_report["selected_profile_ids"],
            "conflict_notes": synth_report["conflict_notes"],
            "pairwise_analysis": synth_report["pairwise_analysis"],
            "refinement_swaps": synth_report["refinement_swaps"],
        },
        "readiness": readiness,
    }
    technique_bank_path = Path(getattr(args, "technique_bank", DEFAULT_BANK_PATH))
    technique_limit = getattr(args, "technique_limit", 6)
    technique_report = recommend_for_blueprint(
        blueprint_core,
        load_bank(technique_bank_path),
        technique_limit,
    )

    return {
        **blueprint_core,
        "production_techniques": technique_report,
    }


def render_text(report: dict) -> str:
    lines = []
    lines.append("# Full Song Blueprint")
    lines.append("")
    lines.append(f"- brief: `{report['brief_id']}`")
    lines.append(f"- serum brief: `{report['serum_brief_id']}`")
    lines.append(f"- template: `{report['template_id']}`")
    lines.append(f"- bpm / key: {report['bpm']} / {report['key']}")
    lines.append(f"- readiness: `{report['readiness']['label']}`")
    lines.append(f"- energy profile: {report['energy_profile']}")
    lines.append("")
    lines.append("## Harmonic Plan")
    lines.append(f"- center: {report['harmonic_plan']['center']}")
    lines.append(f"- progression: {' -> '.join(report['harmonic_plan']['progression'])}")
    lines.append(f"- movement note: {report['harmonic_plan']['movement_note']}")
    lines.append(f"- bass strategy: {report['harmonic_plan']['bass_strategy']}")
    lines.append("")
    lines.append("## Arrangement")
    for row in report["arrangement"]:
        lines.append(
            f"- `{row['section_id']}` bars {row['start_bar']}-{row['end_bar']} :: {row['goal']} "
            f"[energy: {row['energy_level']}]"
        )
    lines.append("")
    lines.append("## Drum And Sample Lanes")
    for lane in report["sample_lanes"]:
        lines.append(
            f"- `{lane['slot_id']}` ({lane['slot_type']}) :: "
            f"{'required' if lane['required'] else 'optional'}; {lane['purpose']}"
        )
        if lane.get("processing_chain"):
            lines.append(
                f"  chain `{lane['processing_chain_id']}`: "
                + " | ".join(lane["processing_chain"]["devices"])
            )
    lines.append("")
    lines.append("## Synth Layers")
    for layer in report["synth_layers"]:
        selection = layer["profile_id"] or "unresolved"
        lines.append(
            f"- `{layer['part_id']}` ({layer['role']}) :: {selection}; "
            f"job: {layer['job_in_track']}"
        )
        lines.append(f"  arrangement role: {layer['arrangement_role']}")
        if layer.get("processing_chain"):
            lines.append(
                f"  chain `{layer['processing_chain_id']}`: "
                + " | ".join(layer["processing_chain"]["devices"])
            )
    lines.append("")
    lines.append("## Returns")
    for row in report["returns"]:
        lines.append(f"- `{row['return_id']}` {row['name']}: {row['purpose']}")
    lines.append("")
    lines.append("## Automation Rules")
    for row in report["automation_rules"]:
        lines.append(f"- {row}")
    lines.append("")
    lines.append("## Mix Rules")
    for row in report["mix_rules"]:
        lines.append(f"- {row}")
    lines.append("")
    lines.append("## Reserved Spaces")
    for row in report["reserved_spaces"]:
        lines.append(f"- {row}")
    if report["arrangement_notes"]:
        lines.append("")
        lines.append("## Arrangement Notes")
        for row in report["arrangement_notes"]:
            lines.append(f"- {row}")
    if report["production_techniques"]["recommendations"]:
        lines.append("")
        lines.append("## Production Techniques")
        for row in report["production_techniques"]["recommendations"]:
            lines.append(
                f"- `{row['id']}` :: {row['name']} [{row['source']}] score={row['score']}"
            )
            lines.append(f"  when: {row['when_to_use']}")
            if row["matched_keywords"]:
                lines.append(f"  matched: {', '.join(row['matched_keywords'])}")
    interaction = report["production_techniques"]["interaction_analysis"]
    if interaction["reinforcements"] or interaction["watchouts"]:
        lines.append("")
        lines.append("## Technique Interactions")
        for row in interaction["reinforcements"]:
            lines.append(f"- reinforcement :: `{row['left_id']}` <-> `{row['right_id']}`")
            lines.append(f"  evidence: {' | '.join(item['phrase'] for item in row['evidence'])}")
        for row in interaction["watchouts"]:
            lines.append(f"- watchout :: `{row['left_id']}` <-> `{row['right_id']}`")
            lines.append(f"  evidence: {' | '.join(item['phrase'] for item in row['evidence'])}")
            if row["mitigations"]:
                lines.append(f"  mitigations: {' | '.join(row['mitigations'][:3])}")
    if report["readiness"]["issues"]:
        lines.append("")
        lines.append("## Readiness Issues")
        for row in report["readiness"]["issues"]:
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
