#!/usr/bin/env python3
"""
suggest_serum_blueprint_alternatives.py

Suggest alternative profiles for a specific part inside a track blueprint,
ranking options that preserve the role while reducing likely clashes with the
rest of the selected stack.

Examples:
    python3 als/suggest_serum_blueprint_alternatives.py --brief ukg-2step-dark-stab --part-id secondary-reese
"""

from __future__ import annotations

import argparse
import json
from argparse import Namespace
from pathlib import Path

try:
    from compare_serum_profiles import build_report as build_profile_comparison
    from design_serum_track_blueprint import build_report as build_blueprint_report
    from recommend_serum_part import build_report as build_part_report
    from search_serum_profiles import load_profiles
except ModuleNotFoundError:
    from .compare_serum_profiles import build_report as build_profile_comparison
    from .design_serum_track_blueprint import build_report as build_blueprint_report
    from .recommend_serum_part import build_report as build_part_report
    from .search_serum_profiles import load_profiles


DEFAULT_CATALOG_DIR = Path("als/catalog/profiles")
DEFAULT_BRIEFS_PATH = Path("als/serum-track-briefs.json")
CONSTRAINT_MODES = ["full", "mix_only", "tone_only", "role_only"]


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Suggest alternative profiles for one part in a Serum blueprint.")
    parser.add_argument("--catalog-dir", default=str(DEFAULT_CATALOG_DIR), help="Directory of generated *-profiles.json files.")
    parser.add_argument("--briefs", default=str(DEFAULT_BRIEFS_PATH), help="Track brief manifest JSON.")
    parser.add_argument("--brief", required=True, help="Brief id from the manifest.")
    parser.add_argument("--part-id", required=True, help="Part id within the brief to replace.")
    parser.add_argument("--prefer-rendered", action="store_true", help="Prefer rendered profiles where available.")
    parser.add_argument("--limit-per-part", type=int, default=8, help="Max candidates to inspect for the target part. Default: 8")
    parser.add_argument("--mutation-limit", type=int, default=6, help="Max mutation suggestions per part. Default: 6")
    parser.add_argument("--limit", type=int, default=5, help="Maximum ranked alternatives to return. Default: 5")
    parser.add_argument("--format", choices=["json", "text"], default="text", help="Output format.")
    return parser


def _blueprint_namespace(args: argparse.Namespace) -> Namespace:
    return Namespace(
        catalog_dir=args.catalog_dir,
        briefs=args.briefs,
        brief=args.brief,
        prefer_rendered=args.prefer_rendered,
        limit_per_part=max(args.limit_per_part, 5),
        mutation_limit=args.mutation_limit,
        format="json",
    )


def _part_namespace(args: argparse.Namespace, part: dict) -> Namespace:
    return Namespace(
        catalog_dir=args.catalog_dir,
        role=part["role"],
        tone=part.get("target_tone", []),
        mix=part.get("target_mix", []),
        track=None,
        analysis=None,
        wavetable=[],
        dest_module=[],
        rendered_only=False,
        prefer_rendered=args.prefer_rendered,
        min_centroid_hz=None,
        max_centroid_hz=None,
        min_side_ratio=None,
        max_side_ratio=None,
        min_attack_ms=None,
        max_attack_ms=None,
        min_rms_dbfs=None,
        max_rms_dbfs=None,
        goal=part.get("goals", []),
        limit=args.limit_per_part,
        mutation_limit=args.mutation_limit,
    )


def _profile_map(catalog_dir: Path) -> dict[str, dict]:
    return {profile["profile_id"]: profile for profile in load_profiles(catalog_dir)}


def _load_brief_part(briefs_path: Path, brief_id: str, part_id: str) -> dict:
    payload = json.loads(briefs_path.read_text())
    briefs = payload.get("briefs", {})
    if brief_id not in briefs:
        raise KeyError(f"brief not found: {brief_id}")
    for part in briefs[brief_id].get("parts", []):
        if part["part_id"] == part_id:
            return part
    raise KeyError(f"part not found in brief: {part_id}")


def _constraint_variant(part: dict, mode: str) -> dict:
    if mode == "full":
        return {**part, "tone": part.get("tone", []), "mix": part.get("mix", [])}
    if mode == "mix_only":
        return {**part, "tone": [], "mix": part.get("mix", [])}
    if mode == "tone_only":
        return {**part, "tone": part.get("tone", []), "mix": []}
    if mode == "role_only":
        return {**part, "tone": [], "mix": []}
    raise ValueError(f"unsupported constraint mode: {mode}")


def _modes_to_try(current_mode: str) -> list[str]:
    if current_mode not in CONSTRAINT_MODES:
        return CONSTRAINT_MODES[:]
    index = CONSTRAINT_MODES.index(current_mode)
    return CONSTRAINT_MODES[index:] + CONSTRAINT_MODES[:index]


def _rank_candidate(candidate: dict, target_full_profile: dict, other_profiles: list[dict], profile_map: dict[str, dict], args: argparse.Namespace) -> dict:
    score = 0.0
    reasons = []
    candidate_full = profile_map.get(candidate["profile_id"])
    if not candidate_full:
        return {
            **candidate,
            "replacement_score": -9999.0,
            "reasons": ["missing full profile"],
            "conflict_count": 999,
            "comparison_notes": [],
        }

    if candidate["profile_id"] != target_full_profile["profile_id"]:
        score += 1.5
        reasons.append("provides a genuine alternative")
    else:
        score -= 2.5
        reasons.append("matches the current choice")
    if candidate.get("audio_status") == "rendered" and args.prefer_rendered:
        score += 1.0
        reasons.append("rendered audio available")

    target_roles = set(target_full_profile["classification"]["role_candidates"])
    candidate_roles = set(candidate_full["classification"]["role_candidates"])
    score += len(target_roles & candidate_roles) * 2.0
    if target_full_profile["profile_id"] != candidate["profile_id"]:
        target_tones = set(target_full_profile["classification"]["tone_tags"])
        candidate_tones = set(candidate_full["classification"]["tone_tags"])
        tone_overlap = len(target_tones & candidate_tones)
        if tone_overlap:
            score += tone_overlap * 1.5
            reasons.append("keeps some of the original tone identity")

    conflict_count = 0
    comparison_notes = []
    for other in other_profiles:
        comparison = build_profile_comparison(candidate_full, other, mutation_limit=2)
        if comparison["conflicts"]:
            conflict_count += len(comparison["conflicts"])
            score -= len(comparison["conflicts"]) * 2.0
        if comparison["complements"]:
            score += len(comparison["complements"]) * 0.75
        for note in comparison["conflicts"][:2]:
            comparison_notes.append(f"conflict with {other['profile_id']}: {note}")
        for note in comparison["complements"][:1]:
            comparison_notes.append(f"complement with {other['profile_id']}: {note}")

    return {
        **candidate,
        "replacement_score": round(score, 4),
        "reasons": sorted(dict.fromkeys(reasons)),
        "conflict_count": conflict_count,
        "comparison_notes": comparison_notes[:6],
        "candidate_mode": candidate.get("candidate_mode"),
    }


def build_report(args: argparse.Namespace) -> dict:
    blueprint = build_blueprint_report(_blueprint_namespace(args))
    target_part = next((part for part in blueprint["parts"] if part["part_id"] == args.part_id), None)
    if target_part is None:
        raise KeyError(f"part not found in brief: {args.part_id}")
    if not target_part.get("selection"):
        return {
            "brief_id": blueprint["brief_id"],
            "part_id": args.part_id,
            "current_profile_id": None,
            "alternatives": [],
            "note": "Target part is unresolved in the current blueprint.",
        }

    profile_map = _profile_map(Path(args.catalog_dir))
    target_full_profile = profile_map[target_part["selection"]["profile_id"]]
    brief_part = _load_brief_part(Path(args.briefs), blueprint["brief_id"], args.part_id)
    other_profiles = [
        profile_map[part["selection"]["profile_id"]]
        for part in blueprint["parts"]
        if part["part_id"] != args.part_id and part.get("selection") and part["selection"]["profile_id"] in profile_map
    ]

    raw_candidates = []
    seen_profile_ids = set()
    mode_counts = {}
    for mode in _modes_to_try(target_part["constraint_mode"]):
        part_variant = _constraint_variant(brief_part, mode)
        candidate_report = build_part_report(_part_namespace(args, part_variant))
        mode_counts[mode] = candidate_report["candidate_count"]
        for candidate in candidate_report["candidates"]:
            candidate_id = candidate["profile_id"]
            if candidate_id in seen_profile_ids:
                continue
            seen_profile_ids.add(candidate_id)
            raw_candidates.append({
                **candidate,
                "candidate_mode": mode,
            })

    ranked = [
        _rank_candidate(candidate, target_full_profile, other_profiles, profile_map, args)
        for candidate in raw_candidates
        if candidate["profile_id"] != target_full_profile["profile_id"]
    ]
    ranked.sort(key=lambda row: (-row["replacement_score"], row["conflict_count"], row["profile_id"]))

    note = None
    if not ranked:
        note = "No distinct alternatives were found in the current fallback ladder."

    return {
        "brief_id": blueprint["brief_id"],
        "part_id": args.part_id,
        "current_profile_id": target_part["selection"]["profile_id"],
        "current_track": target_part["selection"]["track"],
        "constraint_mode": target_part["constraint_mode"],
        "search_modes_considered": _modes_to_try(target_part["constraint_mode"]),
        "candidate_mode_counts": mode_counts,
        "alternatives": ranked[: args.limit],
        "note": note,
    }


def render_text(report: dict) -> str:
    lines = []
    lines.append("# Serum Blueprint Alternatives")
    lines.append("")
    lines.append(f"- brief: `{report['brief_id']}`")
    lines.append(f"- part: `{report['part_id']}`")
    lines.append(f"- current: `{report['current_profile_id']}` ({report.get('current_track') or '-'})")
    lines.append(f"- constraint mode: {report.get('constraint_mode') or '-'}")
    if report.get("search_modes_considered"):
        lines.append(f"- search modes: {', '.join(report['search_modes_considered'])}")
    if report.get("candidate_mode_counts"):
        counts = ", ".join(f"{mode}={count}" for mode, count in report["candidate_mode_counts"].items())
        lines.append(f"- candidate counts: {counts}")
    lines.append("")
    if report.get("note"):
        lines.append(f"- {report['note']}")
        lines.append("")
        return "\n".join(lines)
    for row in report["alternatives"]:
        lines.append(
            f"- `{row['profile_id']}` :: replacement_score={row['replacement_score']} "
            f"conflicts={row['conflict_count']} "
            f"(mode: {row.get('candidate_mode') or '-'}; {row['track'] or '-'}; tone: {', '.join(row['tone_tags'])}; mix: {', '.join(row['mix_tags'])}; audio: {row['audio_status']})"
        )
        if row["reasons"]:
            lines.append(f"  reasons: {' | '.join(row['reasons'])}")
        if row["comparison_notes"]:
            lines.append(f"  notes: {' | '.join(row['comparison_notes'])}")
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
