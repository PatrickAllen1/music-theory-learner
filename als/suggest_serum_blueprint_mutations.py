#!/usr/bin/env python3
"""
suggest_serum_blueprint_mutations.py

Suggest blueprint-level Serum parameter moves for the selected stack, combining
the part's original goals with pairwise conflict-derived goals.

Examples:
    python3 als/suggest_serum_blueprint_mutations.py --brief ukg-2step-dark-stab
    python3 als/suggest_serum_blueprint_mutations.py --brief ukg-4x4-pluck-driver --refine --format json
"""

from __future__ import annotations

import argparse
import json
from argparse import Namespace
from pathlib import Path

try:
    from design_serum_track_blueprint import build_report as build_blueprint_report
    from refine_serum_track_blueprint import build_report as build_refined_blueprint_report
    from search_serum_profiles import load_profiles
    from serum_mutation_rules import suggest_for_goal
except ModuleNotFoundError:
    from .design_serum_track_blueprint import build_report as build_blueprint_report
    from .refine_serum_track_blueprint import build_report as build_refined_blueprint_report
    from .search_serum_profiles import load_profiles
    from .serum_mutation_rules import suggest_for_goal


DEFAULT_CATALOG_DIR = Path("als/catalog/profiles")
DEFAULT_BRIEFS_PATH = Path("als/serum-track-briefs.json")


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Suggest blueprint-level Serum edits for the selected stack.")
    parser.add_argument("--catalog-dir", default=str(DEFAULT_CATALOG_DIR), help="Directory of generated *-profiles.json files.")
    parser.add_argument("--briefs", default=str(DEFAULT_BRIEFS_PATH), help="Track brief manifest JSON.")
    parser.add_argument("--brief", required=True, help="Brief id from the manifest.")
    parser.add_argument("--prefer-rendered", action="store_true", help="Prefer rendered profiles where available.")
    parser.add_argument("--limit-per-part", type=int, default=5, help="Max candidates to inspect per blueprint part. Default: 5")
    parser.add_argument("--mutation-limit", type=int, default=6, help="Max mutation suggestions per part. Default: 6")
    parser.add_argument("--refine", action="store_true", help="Refine the blueprint before building the mutation plan.")
    parser.add_argument("--max-swaps", type=int, default=2, help="Maximum refinement swaps to apply when --refine is set. Default: 2")
    parser.add_argument("--suggestion-limit", type=int, default=8, help="Maximum suggestions to return per part. Default: 8")
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


def _profile_map(catalog_dir: Path) -> dict[str, dict]:
    return {profile["profile_id"]: profile for profile in load_profiles(catalog_dir)}


def _collect_pairwise_goals(blueprint: dict) -> dict[str, list[dict]]:
    goals_by_part: dict[str, list[dict]] = {}
    for row in blueprint["pairwise_analysis"]:
        for side_name, key in (("left", "left_suggested_goals"), ("right", "right_suggested_goals")):
            part_id = row[f"{side_name}_part_id"]
            other_part_id = row["right_part_id"] if side_name == "left" else row["left_part_id"]
            for goal in row[key]:
                goals_by_part.setdefault(part_id, []).append({
                    "goal": goal,
                    "source": "pairwise_conflict",
                    "other_part_id": other_part_id,
                    "conflicts": row["conflicts"],
                })
    return goals_by_part


def _merge_suggestions(profile: dict, brief_suggestions: list[dict], pairwise_goals: list[dict], suggestion_limit: int) -> list[dict]:
    merged: dict[tuple[str, str], dict] = {}

    for row in brief_suggestions:
        key = (row["goal"], row["path"])
        merged[key] = {
            **row,
            "sources": [{"source": "brief_goal"}],
        }

    for goal_row in pairwise_goals:
        suggestions = suggest_for_goal(profile, goal_row["goal"])
        for row in suggestions:
            key = (row["goal"], row["path"])
            source_payload = {
                "source": goal_row["source"],
                "other_part_id": goal_row["other_part_id"],
                "conflicts": goal_row["conflicts"],
            }
            if key in merged:
                merged[key]["sources"].append(source_payload)
                merged[key]["priority"] = max(merged[key]["priority"], row["priority"])
                continue
            merged[key] = {
                **row,
                "sources": [source_payload],
            }

    suggestions = list(merged.values())
    suggestions.sort(key=lambda row: (-row["priority"], row["goal"], row["path"]))
    return suggestions[:suggestion_limit]


def build_report(args: argparse.Namespace) -> dict:
    blueprint = build_refined_blueprint_report(_refine_namespace(args)) if args.refine else build_blueprint_report(_blueprint_namespace(args))
    profiles = _profile_map(Path(args.catalog_dir))
    pairwise_goals = _collect_pairwise_goals(blueprint)
    suggestion_limit = getattr(args, "suggestion_limit", 8)

    parts = []
    for part in blueprint["parts"]:
        selection = part.get("selection")
        if not selection:
            parts.append({
                "part_id": part["part_id"],
                "role": part["role"],
                "status": "unresolved",
                "brief_goals": part.get("goals", []),
                "pairwise_goals": [],
                "suggestions": [],
            })
            continue
        profile = profiles.get(selection["profile_id"])
        if not profile:
            parts.append({
                "part_id": part["part_id"],
                "role": part["role"],
                "status": "missing_profile",
                "profile_id": selection["profile_id"],
                "brief_goals": part.get("goals", []),
                "pairwise_goals": pairwise_goals.get(part["part_id"], []),
                "suggestions": [],
            })
            continue
        pairwise_rows = pairwise_goals.get(part["part_id"], [])
        suggestions = _merge_suggestions(
            profile,
            selection.get("mutation_suggestions") or [],
            pairwise_rows,
            suggestion_limit,
        )
        parts.append({
            "part_id": part["part_id"],
            "role": part["role"],
            "status": "selected",
            "profile_id": selection["profile_id"],
            "track": selection.get("track"),
            "constraint_mode": part.get("constraint_mode"),
            "brief_goals": part.get("goals", []),
            "pairwise_goals": sorted(dict.fromkeys(row["goal"] for row in pairwise_rows)),
            "pairwise_sources": pairwise_rows,
            "suggestions": suggestions,
        })

    return {
        "brief_id": blueprint["brief_id"],
        "description": blueprint["description"],
        "prefer_rendered": blueprint["prefer_rendered"],
        "refined": args.refine,
        "selected_profile_ids": blueprint["selected_profile_ids"],
        "conflict_notes": blueprint["conflict_notes"],
        "refinement_swaps": blueprint.get("refinement_swaps") or [],
        "parts": parts,
    }


def render_text(report: dict) -> str:
    lines = []
    lines.append("# Serum Blueprint Mutation Plan")
    lines.append("")
    lines.append(f"- brief: `{report['brief_id']}`")
    lines.append(f"- refined: {'yes' if report['refined'] else 'no'}")
    lines.append(f"- selected profiles: {len(report['selected_profile_ids'])}")
    lines.append("")
    if report["conflict_notes"]:
        lines.append("## Remaining Conflict Notes")
        for row in report["conflict_notes"]:
            lines.append(f"- {row}")
        lines.append("")
    for part in report["parts"]:
        lines.append(f"## {part['part_id']} ({part['role']})")
        lines.append(f"- status: {part['status']}")
        if part.get("profile_id"):
            lines.append(f"- profile: `{part['profile_id']}` ({part.get('track') or '-'})")
        lines.append(f"- brief goals: {', '.join(part['brief_goals']) or '-'}")
        lines.append(f"- pairwise goals: {', '.join(part['pairwise_goals']) or '-'}")
        for row in part["suggestions"]:
            sources = []
            for source in row.get("sources") or []:
                label = source["source"]
                if source.get("other_part_id"):
                    label += f":{source['other_part_id']}"
                sources.append(label)
            lines.append(
                f"- mutate `{row['path']}` :: {row['action']} "
                f"{row['current_value']} -> {row['suggested_value']} "
                f"[goal: {row['goal']}; sources: {', '.join(sources) or '-'}]"
            )
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
