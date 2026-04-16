#!/usr/bin/env python3
"""
build_song_decision_tree.py

Build a model-facing decision tree from the full-song blueprint and production
technique layer. The tree is not the composer; it is the structured context the
model uses to make high-quality track decisions.

Examples:
    python3 als/build_song_decision_tree.py --brief ukg-2step-dark-stab
    python3 als/build_song_decision_tree.py --brief ukg-4x4-lead-driver --format json
"""

from __future__ import annotations

import argparse
import json
from argparse import Namespace
from pathlib import Path

try:
    from design_full_song_blueprint import build_report as build_full_song_blueprint_report
except ModuleNotFoundError:
    from .design_full_song_blueprint import build_report as build_full_song_blueprint_report


DEFAULT_CATALOG_DIR = Path("als/catalog/profiles")
DEFAULT_SERUM_BRIEFS_PATH = Path("als/serum-track-briefs.json")
DEFAULT_SONG_BRIEFS_PATH = Path("als/song-blueprint-briefs.json")
DEFAULT_TEMPLATES_PATH = Path("als/song-production-templates.json")

DOMAIN_KEYWORDS = {
    "groove": {"groove", "swing", "drum", "kick", "clap", "hat", "percussion", "shuffle"},
    "low_end": {"bass", "sub", "reese", "low", "mono", "anchor"},
    "harmony": {"pad", "chord", "voicing", "minor", "harmony", "sustained"},
    "hook": {"lead", "pluck", "stab", "vocal", "hook", "phrase", "response"},
    "width": {"wide", "stereo", "unison", "pan", "spread", "side"},
    "arrangement": {"arrangement", "bars", "drop", "break", "switch", "transition", "intro", "outro"},
}


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build a model-facing song decision tree from a brief.")
    parser.add_argument("--brief", required=True, help="Song brief id from the manifest.")
    parser.add_argument("--song-briefs", default=str(DEFAULT_SONG_BRIEFS_PATH), help="Song-level brief manifest JSON.")
    parser.add_argument("--templates", default=str(DEFAULT_TEMPLATES_PATH), help="Song production templates JSON.")
    parser.add_argument("--catalog-dir", default=str(DEFAULT_CATALOG_DIR), help="Directory of generated *-profiles.json files.")
    parser.add_argument("--serum-briefs", default=str(DEFAULT_SERUM_BRIEFS_PATH), help="Serum brief manifest JSON.")
    parser.add_argument("--prefer-rendered", action="store_true", help="Prefer rendered profiles where available.")
    parser.add_argument("--limit-per-part", type=int, default=5, help="Max candidates to inspect per part. Default: 5")
    parser.add_argument("--mutation-limit", type=int, default=6, help="Max mutation suggestions per part. Default: 6")
    parser.add_argument("--max-swaps", type=int, default=2, help="Maximum refinement swaps to apply. Default: 2")
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


def _technique_domain(row: dict) -> str:
    combined = " ".join([
        row.get("id", "").replace("-", " "),
        row.get("name", ""),
        " ".join(row.get("matched_keywords", [])),
        row.get("when_to_use", ""),
    ]).lower()
    best_domain = "arrangement"
    best_score = -1
    for domain, keywords in DOMAIN_KEYWORDS.items():
        score = sum(1 for keyword in keywords if keyword in combined)
        if score > best_score:
            best_score = score
            best_domain = domain
    return best_domain


def _branch_for_domain(blueprint: dict, techniques: list[dict], commitments: dict, domain: str) -> dict:
    selected = [row for row in techniques if _technique_domain(row) == domain]
    technique_ids = {row["id"] for row in selected}
    pairings = [
        row for row in commitments["required_pairings"]
        if row["primary_id"] in technique_ids or row["support_id"] in technique_ids
    ]
    constraints = [
        row for row in commitments["mandatory_constraints"]
        if row["left_id"] in technique_ids or row["right_id"] in technique_ids
    ]

    prompts = {
        "groove": "Which rhythmic decision actually owns the track, and what must stay simple so that groove reads immediately?",
        "low_end": "What is allowed to own the true sub, and what is only allowed to add low-mid size or aggression?",
        "harmony": "How much harmonic definition is the track allowed before it stops feeling open, tense, or genre-bending?",
        "hook": "What single element owns memorability, and which other element is only allowed to answer rather than compete?",
        "width": "Where is the stereo width budget spent, and what must stay narrow or filtered so the width still feels huge?",
        "arrangement": "What is the 2/4/8/16-bar escalation logic, and which contrast moments are structural rather than decorative?",
    }
    evidence = {
        "groove": [blueprint["drum_strategy"], blueprint["melodic_strategy"], *blueprint["arrangement_notes"]],
        "low_end": [blueprint["harmonic_plan"]["bass_strategy"], *[row["job_in_track"] for row in blueprint["synth_layers"] if row["role"] in {"bass", "reese", "sub"}]],
        "harmony": [blueprint["harmonic_plan"]["center"], " -> ".join(blueprint["harmonic_plan"]["progression"]), blueprint["harmonic_plan"]["movement_note"]],
        "hook": [* [row["job_in_track"] for row in blueprint["synth_layers"] if row["role"] in {"lead", "pluck", "stab", "pad"}], *blueprint["reserved_spaces"]],
        "width": [*blueprint["mix_rules"], *[row["arrangement_role"] for row in blueprint["synth_layers"]]],
        "arrangement": [* [f"{row['section_id']}: {row['goal']}" for row in blueprint["arrangement"]], *blueprint["automation_rules"]],
    }

    must_preserve = []
    if domain == "groove":
        must_preserve = ["kick timing clarity", "space between important hits", "consistent swing logic if swing is chosen"]
    elif domain == "low_end":
        must_preserve = ["mono-safe sub ownership", "clear low-mid delegation", "kick/bass separation"]
    elif domain == "harmony":
        must_preserve = ["intended ambiguity or tension", "pad not over-resolving the track", "bass not redefining the chord by accident"]
    elif domain == "hook":
        must_preserve = ["single memorable focal point", "response layers staying subordinate", "hook surviving sidechain and arrangement holes"]
    elif domain == "width":
        must_preserve = ["one obvious width hero at a time", "center staying stable", "low end staying narrow"]
    elif domain == "arrangement":
        must_preserve = ["clear contrast cadence", "one major change per structural moment", "development in drop B or switch-up"]

    return {
        "domain": domain,
        "decision_prompt": prompts[domain],
        "evidence": [item for item in evidence[domain] if item],
        "recommended_techniques": selected,
        "required_pairings": pairings,
        "mandatory_constraints": constraints,
        "must_preserve": must_preserve,
    }


def build_report(args: argparse.Namespace) -> dict:
    blueprint = build_full_song_blueprint_report(_namespace(args))
    techniques = blueprint["production_techniques"]["recommendations"]
    commitments = blueprint["production_techniques"]["interaction_analysis"]["decision_commitments"]

    branches = [
        _branch_for_domain(blueprint, techniques, commitments, domain)
        for domain in ("groove", "low_end", "harmony", "hook", "width", "arrangement")
    ]

    return {
        "brief_id": blueprint["brief_id"],
        "description": blueprint["description"],
        "root_question": "What is the bold thesis of this track, and what follow-through is required to make that thesis land as intentional rather than messy?",
        "decision_order": [
            "Lock groove ownership and low-end ownership first.",
            "Choose one or two bold harmonic, hook, or width moves that make the track feel distinctive.",
            "Apply every required pairing that those bold moves demand.",
            "Apply every mandatory constraint before adding decorative layers.",
            "Check section-by-section whether the contrast cadence still reads.",
        ],
        "branches": branches,
        "production_techniques": blueprint["production_techniques"],
        "readiness": blueprint["readiness"],
    }


def render_text(report: dict) -> str:
    lines = []
    lines.append("# Song Decision Tree")
    lines.append("")
    lines.append(f"- brief: `{report['brief_id']}`")
    lines.append(f"- root question: {report['root_question']}")
    lines.append("")
    lines.append("## Decision Order")
    for index, row in enumerate(report["decision_order"], start=1):
        lines.append(f"{index}. {row}")
    for branch in report["branches"]:
        lines.append("")
        lines.append(f"## {branch['domain'].replace('_', ' ').title()}")
        lines.append(f"- prompt: {branch['decision_prompt']}")
        if branch["evidence"]:
            lines.append("- evidence:")
            for row in branch["evidence"]:
                lines.append(f"  - {row}")
        if branch["must_preserve"]:
            lines.append("- must preserve:")
            for row in branch["must_preserve"]:
                lines.append(f"  - {row}")
        if branch["recommended_techniques"]:
            lines.append("- candidate moves:")
            for row in branch["recommended_techniques"]:
                lines.append(f"  - `{row['name']}` [{row['source']}]")
        if branch["required_pairings"]:
            lines.append("- required pairings:")
            for row in branch["required_pairings"]:
                lines.append(f"  - {row['rule']}")
        if branch["mandatory_constraints"]:
            lines.append("- mandatory constraints:")
            for row in branch["mandatory_constraints"]:
                lines.append(f"  - {row['rule']}")
                if row["required_moves"]:
                    lines.append(f"    must do: {' | '.join(row['required_moves'])}")
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
