#!/usr/bin/env python3
"""
refine_serum_track_blueprint.py

Refine a Serum track blueprint by swapping conflict-heavy or fallback-heavy
parts for better alternatives when the replacement improves the overall stack.

Examples:
    python3 als/refine_serum_track_blueprint.py --brief ukg-4x4-pluck-driver
    python3 als/refine_serum_track_blueprint.py --brief ukg-2step-dark-stab --prefer-rendered --format json
"""

from __future__ import annotations

import argparse
import json
from argparse import Namespace
from pathlib import Path

try:
    from design_serum_track_blueprint import build_report as build_blueprint_report
    from design_serum_track_blueprint import _conflict_notes, _pairwise_analysis
    from suggest_serum_blueprint_alternatives import build_report as build_alternative_report
except ModuleNotFoundError:
    from .design_serum_track_blueprint import build_report as build_blueprint_report
    from .design_serum_track_blueprint import _conflict_notes, _pairwise_analysis
    from .suggest_serum_blueprint_alternatives import build_report as build_alternative_report


DEFAULT_CATALOG_DIR = Path("als/catalog/profiles")
DEFAULT_BRIEFS_PATH = Path("als/serum-track-briefs.json")
MODE_RANK = {
    "full": 0,
    "mix_only": 1,
    "tone_only": 2,
    "role_only": 3,
}


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Refine a Serum blueprint by swapping weak parts for better alternatives.")
    parser.add_argument("--catalog-dir", default=str(DEFAULT_CATALOG_DIR), help="Directory of generated *-profiles.json files.")
    parser.add_argument("--briefs", default=str(DEFAULT_BRIEFS_PATH), help="Track brief manifest JSON.")
    parser.add_argument("--brief", required=True, help="Brief id from the manifest.")
    parser.add_argument("--prefer-rendered", action="store_true", help="Prefer rendered profiles where available.")
    parser.add_argument("--limit-per-part", type=int, default=5, help="Max candidates to inspect per part. Default: 5")
    parser.add_argument("--mutation-limit", type=int, default=6, help="Max mutation suggestions per part. Default: 6")
    parser.add_argument("--alternative-limit", type=int, default=5, help="Max alternatives to inspect per weak part. Default: 5")
    parser.add_argument("--max-swaps", type=int, default=2, help="Maximum number of part swaps to apply. Default: 2")
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


def _alternative_namespace(args: argparse.Namespace, part_id: str) -> Namespace:
    return Namespace(
        catalog_dir=args.catalog_dir,
        briefs=args.briefs,
        brief=args.brief,
        part_id=part_id,
        prefer_rendered=args.prefer_rendered,
        limit_per_part=max(args.limit_per_part, args.alternative_limit),
        mutation_limit=args.mutation_limit,
        limit=args.alternative_limit,
        format="json",
    )


def _pairwise_conflict_count(pairwise_analysis: list[dict]) -> int:
    return sum(len(row["conflicts"]) for row in pairwise_analysis)


def _part_pairwise_conflict_count(pairwise_analysis: list[dict], part_id: str) -> int:
    total = 0
    for row in pairwise_analysis:
        if row["left_part_id"] == part_id or row["right_part_id"] == part_id:
            total += len(row["conflicts"])
    return total


def _issue_report(parts: list[dict], pairwise_analysis: list[dict]) -> list[dict]:
    issues = []
    for part in parts:
        if not part.get("selection"):
            continue
        conflict_count = _part_pairwise_conflict_count(pairwise_analysis, part["part_id"])
        fallback_penalty = 1 if part.get("constraint_mode") != "full" else 0
        score = conflict_count * 2 + fallback_penalty
        issues.append({
            "part_id": part["part_id"],
            "profile_id": part["selection"]["profile_id"],
            "constraint_mode": part.get("constraint_mode"),
            "pairwise_conflicts": conflict_count,
            "issue_score": score,
            "swap_trigger": "fallback_and_conflicts" if conflict_count and fallback_penalty else ("conflicts" if conflict_count else ("fallback" if fallback_penalty else "stable")),
        })
    issues.sort(key=lambda row: (-row["issue_score"], row["part_id"]))
    return issues


def _evaluate_parts(parts: list[dict], args: argparse.Namespace) -> dict:
    pairwise = _pairwise_analysis(parts, args.mutation_limit, Path(args.catalog_dir))
    return {
        "conflict_notes": _conflict_notes([part for part in parts if part.get("selection")]),
        "pairwise_analysis": pairwise,
        "pairwise_conflict_count": _pairwise_conflict_count(pairwise),
        "issues": _issue_report(parts, pairwise),
        "selected_profile_ids": [part["selection"]["profile_id"] for part in parts if part.get("selection")],
    }


def _selection_from_alternative(candidate: dict) -> dict:
    return {
        "profile_id": candidate["profile_id"],
        "track": candidate.get("track"),
        "analysis_slug": candidate.get("analysis_slug"),
        "role_candidates": candidate.get("role_candidates", []),
        "tone_tags": candidate.get("tone_tags", []),
        "mix_tags": candidate.get("mix_tags", []),
        "notes": candidate.get("notes") or [],
        "audio_status": candidate.get("audio_status"),
        "audio_summary": candidate.get("audio_summary"),
        "mutation_suggestions": candidate.get("mutation_suggestions") or [],
    }


def _choose_swap(parts: list[dict], part_id: str, alternatives: list[dict], baseline: dict, args: argparse.Namespace) -> dict | None:
    used_profile_ids = {
        part["selection"]["profile_id"]
        for part in parts
        if part.get("selection") and part["part_id"] != part_id
    }
    current_part = next(part for part in parts if part["part_id"] == part_id)
    current_conflicts = _part_pairwise_conflict_count(baseline["pairwise_analysis"], part_id)
    current_mode_rank = MODE_RANK.get(current_part.get("constraint_mode"), 99)

    best = None
    for candidate in alternatives:
        if candidate["profile_id"] in used_profile_ids:
            continue
        simulated = []
        for part in parts:
            if part["part_id"] != part_id:
                simulated.append(part)
                continue
            simulated.append({
                **part,
                "constraint_mode": candidate.get("candidate_mode") or part.get("constraint_mode"),
                "selection": _selection_from_alternative(candidate),
            })
        evaluation = _evaluate_parts(simulated, args)
        new_conflicts = _part_pairwise_conflict_count(evaluation["pairwise_analysis"], part_id)
        total_delta = baseline["pairwise_conflict_count"] - evaluation["pairwise_conflict_count"]
        part_delta = current_conflicts - new_conflicts
        mode_rank = MODE_RANK.get(candidate.get("candidate_mode"), 99)
        mode_penalty = max(0, mode_rank - current_mode_rank)
        decision_score = total_delta * 4 + part_delta * 2 + candidate["replacement_score"] - mode_penalty
        if part_delta <= 0 and total_delta <= 0:
            continue
        row = {
            "part_id": part_id,
            "from_profile_id": current_part["selection"]["profile_id"],
            "to_profile_id": candidate["profile_id"],
            "from_constraint_mode": current_part.get("constraint_mode"),
            "to_constraint_mode": candidate.get("candidate_mode"),
            "replacement_score": candidate["replacement_score"],
            "current_part_conflicts": current_conflicts,
            "new_part_conflicts": new_conflicts,
            "pairwise_conflict_delta": part_delta,
            "total_pairwise_conflict_delta": total_delta,
            "decision_score": round(decision_score, 4),
            "reasons": candidate.get("reasons") or [],
            "comparison_notes": candidate.get("comparison_notes") or [],
            "evaluation": evaluation,
            "selection": _selection_from_alternative(candidate),
        }
        if best is None or row["decision_score"] > best["decision_score"]:
            best = row
    return best


def build_report(args: argparse.Namespace) -> dict:
    initial_blueprint = build_blueprint_report(_blueprint_namespace(args))
    parts = [dict(part) for part in initial_blueprint["parts"]]
    current = _evaluate_parts(parts, args)
    swaps = []

    for issue in current["issues"]:
        if len(swaps) >= args.max_swaps:
            break
        if issue["issue_score"] <= 0:
            break
        alternatives_report = build_alternative_report(_alternative_namespace(args, issue["part_id"]))
        swap = _choose_swap(parts, issue["part_id"], alternatives_report["alternatives"], current, args)
        if not swap:
            continue
        for index, part in enumerate(parts):
            if part["part_id"] != issue["part_id"]:
                continue
            parts[index] = {
                **part,
                "constraint_mode": swap["to_constraint_mode"] or part.get("constraint_mode"),
                "selection": swap["selection"],
            }
            break
        swaps.append({
            key: value
            for key, value in swap.items()
            if key not in {"evaluation", "selection"}
        })
        current = swap["evaluation"]

    return {
        "brief_id": initial_blueprint["brief_id"],
        "description": initial_blueprint["description"],
        "prefer_rendered": args.prefer_rendered,
        "max_swaps": args.max_swaps,
        "initial": {
            "selected_profile_ids": initial_blueprint["selected_profile_ids"],
            "conflict_notes": initial_blueprint["conflict_notes"],
            "pairwise_conflict_count": _pairwise_conflict_count(initial_blueprint["pairwise_analysis"]),
            "issues": _issue_report(initial_blueprint["parts"], initial_blueprint["pairwise_analysis"]),
        },
        "swaps": swaps,
        "final": {
            "selected_profile_ids": current["selected_profile_ids"],
            "conflict_notes": current["conflict_notes"],
            "pairwise_conflict_count": current["pairwise_conflict_count"],
            "issues": current["issues"],
            "pairwise_analysis": current["pairwise_analysis"],
            "parts": parts,
        },
        "parts": parts,
        "selected_profile_ids": current["selected_profile_ids"],
        "conflict_notes": current["conflict_notes"],
        "pairwise_analysis": current["pairwise_analysis"],
        "refinement_swaps": swaps,
    }


def render_text(report: dict) -> str:
    lines = []
    lines.append("# Refined Serum Track Blueprint")
    lines.append("")
    lines.append(f"- brief: `{report['brief_id']}`")
    lines.append(f"- prefer rendered: {'yes' if report['prefer_rendered'] else 'no'}")
    lines.append(f"- max swaps: {report['max_swaps']}")
    lines.append(f"- initial pairwise conflicts: {report['initial']['pairwise_conflict_count']}")
    lines.append(f"- final pairwise conflicts: {report['final']['pairwise_conflict_count']}")
    lines.append("")
    lines.append("## Swaps")
    if report["swaps"]:
        for row in report["swaps"]:
            lines.append(
                f"- `{row['part_id']}` :: `{row['from_profile_id']}` -> `{row['to_profile_id']}` "
                f"(mode {row['from_constraint_mode']} -> {row['to_constraint_mode']}; "
                f"part delta={row['pairwise_conflict_delta']}; total delta={row['total_pairwise_conflict_delta']}; "
                f"decision_score={row['decision_score']})"
            )
            if row["reasons"]:
                lines.append(f"  reasons: {' | '.join(row['reasons'])}")
            if row["comparison_notes"]:
                lines.append(f"  notes: {' | '.join(row['comparison_notes'])}")
    else:
        lines.append("- none")
    lines.append("")
    lines.append("## Final Parts")
    for part in report["final"]["parts"]:
        selection = part.get("selection")
        if not selection:
            lines.append(f"- `{part['part_id']}` :: unresolved")
            continue
        lines.append(
            f"- `{part['part_id']}` :: `{selection['profile_id']}` "
            f"(mode: {part.get('constraint_mode')}; tone: {', '.join(selection.get('tone_tags') or [])}; "
            f"mix: {', '.join(selection.get('mix_tags') or [])}; audio: {selection.get('audio_status')})"
        )
    lines.append("")
    if report["final"]["conflict_notes"]:
        lines.append("## Final Conflict Notes")
        for note in report["final"]["conflict_notes"]:
            lines.append(f"- {note}")
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
