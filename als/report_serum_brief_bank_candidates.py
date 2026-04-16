#!/usr/bin/env python3
"""
report_serum_brief_bank_candidates.py

Recommend real Garage/Speed Garage Serum preset files for one lesson brief,
focusing on parts that still need author attention because they are fallback-
heavy, conflict-heavy, or lack actionable mutation moves.

Examples:
    python3 als/report_serum_brief_bank_candidates.py --brief ukg-4x4-pluck-driver
    python3 als/report_serum_brief_bank_candidates.py --brief ukg-2step-dark-stab --format json
"""

from __future__ import annotations

import argparse
import json
from argparse import Namespace
from pathlib import Path

try:
    from refine_serum_track_blueprint import build_report as build_refined_blueprint_report
    from report_serum_preset_capture_candidates import DEFAULT_BANK_DIRS, _scan_presets, _score_candidate
    from suggest_serum_blueprint_mutations import build_report as build_mutation_plan_report
except ModuleNotFoundError:
    from .refine_serum_track_blueprint import build_report as build_refined_blueprint_report
    from .report_serum_preset_capture_candidates import DEFAULT_BANK_DIRS, _scan_presets, _score_candidate
    from .suggest_serum_blueprint_mutations import build_report as build_mutation_plan_report


DEFAULT_CATALOG_DIR = Path("als/catalog/profiles")
DEFAULT_BRIEFS_PATH = Path("als/serum-track-briefs.json")


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Recommend actual Serum bank presets for a specific lesson brief.")
    parser.add_argument("--brief", required=True, help="Brief id from the manifest.")
    parser.add_argument("--catalog-dir", default=str(DEFAULT_CATALOG_DIR), help="Directory of generated *-profiles.json files.")
    parser.add_argument("--briefs", default=str(DEFAULT_BRIEFS_PATH), help="Track brief manifest JSON.")
    parser.add_argument("--prefer-rendered", action="store_true", help="Prefer rendered catalog profiles where available.")
    parser.add_argument("--limit-per-part", type=int, default=5, help="Max candidates to inspect per brief part. Default: 5")
    parser.add_argument("--mutation-limit", type=int, default=6, help="Max mutation suggestions per part. Default: 6")
    parser.add_argument("--max-swaps", type=int, default=2, help="Maximum refinement swaps to apply. Default: 2")
    parser.add_argument("--bank-dir", action="append", default=[], help="Preset bank directory to scan. Pass multiple times.")
    parser.add_argument("--top-per-part", type=int, default=5, help="Maximum bank candidates to return per brief part. Default: 5")
    parser.add_argument("--include-stable", action="store_true", help="Include stable full-match parts with no open attention items.")
    parser.add_argument("--format", choices=["json", "text"], default="text", help="Output format.")
    return parser


def _refine_namespace(args: argparse.Namespace) -> Namespace:
    return Namespace(
        catalog_dir=args.catalog_dir,
        briefs=args.briefs,
        brief=args.brief,
        prefer_rendered=args.prefer_rendered,
        limit_per_part=args.limit_per_part,
        mutation_limit=args.mutation_limit,
        alternative_limit=max(args.limit_per_part, 5),
        max_swaps=args.max_swaps,
        format="json",
    )


def _mutation_namespace(args: argparse.Namespace) -> Namespace:
    return Namespace(
        catalog_dir=args.catalog_dir,
        briefs=args.briefs,
        brief=args.brief,
        prefer_rendered=args.prefer_rendered,
        limit_per_part=args.limit_per_part,
        mutation_limit=args.mutation_limit,
        alternative_limit=max(args.limit_per_part, 5),
        max_swaps=args.max_swaps,
        refine=True,
        suggestion_limit=8,
        format="json",
    )


def _attention(issue: dict | None, part: dict, mutation_part: dict | None) -> tuple[int, list[str]]:
    score = 0
    reasons = []
    if not part.get("selection"):
        score += 8
        reasons.append("selection is unresolved")
    if part.get("constraint_mode") != "full":
        score += 4
        reasons.append(f"selected under {part.get('constraint_mode')} fallback")
    if issue and issue.get("pairwise_conflicts"):
        conflict_count = issue["pairwise_conflicts"]
        score += conflict_count * 2
        reasons.append(f"involved in {conflict_count} remaining pairwise conflicts")
    if mutation_part and part.get("selection") and not mutation_part.get("suggestions"):
        score += 2
        reasons.append("has no actionable mutation suggestions yet")
    return score, reasons


def _coverage_gain(part: dict, preset: dict) -> dict[str, list[str]]:
    current_tones = set((part.get("selection") or {}).get("tone_tags") or [])
    current_mixes = set((part.get("selection") or {}).get("mix_tags") or [])
    target_tones = set(part.get("target_tone") or [])
    target_mixes = set(part.get("target_mix") or [])
    return {
        "tone": sorted((target_tones - current_tones) & set(preset["tone_tags"])),
        "mix": sorted((target_mixes - current_mixes) & set(preset["mix_tags"])),
    }


def _goal_fit_bonus(goals: list[str], preset: dict) -> tuple[float, list[str]]:
    score = 0.0
    reasons = []
    tone_tags = set(preset["tone_tags"])
    mix_tags = set(preset["mix_tags"])
    params = preset.get("key_params") or {}
    uni = max(
        float(params.get("osc_a_uni_voices") or 0),
        float(params.get("osc_b_uni_voices") or 0),
    )
    attack = params.get("env1_attack")
    release = params.get("env1_release")
    cutoff = params.get("flt_cutoff")

    for goal in goals:
        if goal == "cleaner":
            if "gritty" not in tone_tags:
                score += 1.0
                reasons.append("fits cleaner goal")
            else:
                score -= 1.0
        elif goal == "more_grit":
            if "gritty" in tone_tags:
                score += 1.0
                reasons.append("fits more_grit goal")
        elif goal == "mono_safer":
            if "side_heavy" not in mix_tags and "wide" not in tone_tags and uni <= 2:
                score += 1.0
                reasons.append("fits mono_safer goal")
            elif "side_heavy" in mix_tags or "wide" in tone_tags or uni > 4:
                score -= 0.75
        elif goal == "tighter":
            if isinstance(release, (int, float)) and release <= 0.25:
                score += 1.0
                reasons.append("fits tighter goal")
            elif isinstance(release, (int, float)) and release >= 0.5:
                score -= 0.5
            if isinstance(attack, (int, float)) and attack > 0.2:
                score -= 0.25
        elif goal == "longer_tail":
            if (isinstance(release, (int, float)) and release >= 0.25) or "soft" in tone_tags:
                score += 1.0
                reasons.append("fits longer_tail goal")
        elif goal == "more_presence":
            if "bright" in tone_tags or "mid_focus" in mix_tags or (isinstance(cutoff, (int, float)) and cutoff >= 0.35):
                score += 1.0
                reasons.append("fits more_presence goal")
        elif goal == "harder_attack":
            if isinstance(attack, (int, float)) and attack <= 0.05:
                score += 1.0
                reasons.append("fits harder_attack goal")
        elif goal == "less_sub":
            if preset["role"] not in {"sub", "bass"} and "low_end_anchor" not in mix_tags:
                score += 1.0
                reasons.append("fits less_sub goal")
            elif preset["role"] in {"sub", "bass"} and "low_end_anchor" in mix_tags:
                score -= 0.5
        elif goal == "wider":
            if "wide" in tone_tags or "side_heavy" in mix_tags or uni > 2:
                score += 1.0
                reasons.append("fits wider goal")
        elif goal == "less_busy":
            if "modulated" not in tone_tags:
                score += 1.0
                reasons.append("fits less_busy goal")
        elif goal == "more_motion":
            if "modulated" in tone_tags:
                score += 1.0
                reasons.append("fits more_motion goal")
    return score, reasons


def _candidate_score(part: dict, preset: dict, attention_score: int, desired_goals: list[str]) -> tuple[float, list[str], dict[str, list[str]]]:
    gap = {
        "role": part["role"],
        "target_tone": part.get("target_tone", []),
        "target_mix": part.get("target_mix", []),
    }
    score, reasons = _score_candidate(gap, preset)
    gains = _coverage_gain(part, preset)
    if gains["tone"]:
        score += len(gains["tone"]) * 1.5
        reasons.append(f"covers missing tone targets: {', '.join(gains['tone'])}")
    if gains["mix"]:
        score += len(gains["mix"]) * 1.0
        reasons.append(f"covers missing mix targets: {', '.join(gains['mix'])}")

    target_tones = set(part.get("target_tone") or [])
    target_mixes = set(part.get("target_mix") or [])
    if target_tones.issubset(set(preset["tone_tags"])) and target_mixes.issubset(set(preset["mix_tags"])):
        score += 2.0
        reasons.append("satisfies the full brief target without fallback")
    if attention_score >= 4 and preset.get("macro_labels"):
        score += 0.5
        reasons.append("exposes macro labels for faster guided tweaking")
    goal_bonus, goal_reasons = _goal_fit_bonus(desired_goals, preset)
    score += goal_bonus
    reasons.extend(goal_reasons)
    return round(score, 4), reasons, gains


def build_report(args: argparse.Namespace) -> dict:
    refined = build_refined_blueprint_report(_refine_namespace(args))
    mutations = build_mutation_plan_report(_mutation_namespace(args))
    bank_dirs = [Path(path) for path in (args.bank_dir or [])] or DEFAULT_BANK_DIRS
    presets = _scan_presets(bank_dirs)

    issue_by_part = {row["part_id"]: row for row in refined["final"]["issues"]}
    mutation_by_part = {row["part_id"]: row for row in mutations["parts"]}

    part_rows = []
    for part in refined["parts"]:
        issue = issue_by_part.get(part["part_id"])
        mutation_part = mutation_by_part.get(part["part_id"])
        attention_score, attention_reasons = _attention(issue, part, mutation_part)
        if attention_score <= 0 and not args.include_stable:
            continue
        desired_goals = list(dict.fromkeys((part.get("goals") or []) + ((mutation_part or {}).get("pairwise_goals") or [])))

        candidates = []
        for preset in presets:
            score, reasons, gains = _candidate_score(part, preset, attention_score, desired_goals)
            if score <= 0:
                continue
            candidates.append({
                **preset,
                "score": score,
                "reasons": reasons,
                "coverage_gain": gains,
            })
        candidates.sort(key=lambda row: (-row["score"], row["path"]))

        selection = part.get("selection") or {}
        part_rows.append({
            "part_id": part["part_id"],
            "role": part["role"],
            "target_tone": part.get("target_tone", []),
            "target_mix": part.get("target_mix", []),
            "goals": part.get("goals", []),
            "desired_goals": desired_goals,
            "current_profile_id": selection.get("profile_id"),
            "current_track": selection.get("track"),
            "current_constraint_mode": part.get("constraint_mode"),
            "current_tone_tags": selection.get("tone_tags", []),
            "current_mix_tags": selection.get("mix_tags", []),
            "current_audio_status": selection.get("audio_status"),
            "pairwise_conflicts": (issue or {}).get("pairwise_conflicts", 0),
            "attention_score": attention_score,
            "attention_reasons": attention_reasons,
            "candidate_count": len(candidates),
            "candidates": candidates[: args.top_per_part],
        })

    part_rows.sort(key=lambda row: (-row["attention_score"], row["part_id"]))
    return {
        "brief_id": refined["brief_id"],
        "description": refined["description"],
        "bank_dirs": [str(path) for path in bank_dirs],
        "preset_count": len(presets),
        "part_count": len(refined["parts"]),
        "parts_needing_attention": len(part_rows),
        "parts": part_rows,
    }


def render_text(report: dict) -> str:
    lines = []
    lines.append("# Serum Brief Bank Candidates")
    lines.append("")
    lines.append(f"- brief: `{report['brief_id']}`")
    lines.append(f"- scanned presets: {report['preset_count']}")
    lines.append(f"- parts needing attention: {report['parts_needing_attention']}")
    lines.append("")
    for part in report["parts"]:
        lines.append(
            f"- `{part['part_id']}` :: attention={part['attention_score']} "
            f"[role: {part['role']}; mode: {part['current_constraint_mode']}; "
            f"current: {part['current_profile_id'] or '-'}]"
        )
        if part["attention_reasons"]:
            lines.append(f"  why: {' | '.join(part['attention_reasons'])}")
        if not part["candidates"]:
            lines.append("  no bank candidates scored above zero")
            continue
        for row in part["candidates"]:
            lines.append(
                f"  candidate: `{row['track']}` score={row['score']} "
                f"[role: {row['role']}; tone: {', '.join(row['tone_tags']) or '-'}; "
                f"mix: {', '.join(row['mix_tags']) or '-'}; bank: {row.get('bank') or '-'}]"
            )
            lines.append(f"  path: {row['path']}")
            if row["coverage_gain"]["tone"] or row["coverage_gain"]["mix"]:
                gains = []
                if row["coverage_gain"]["tone"]:
                    gains.append(f"tone={', '.join(row['coverage_gain']['tone'])}")
                if row["coverage_gain"]["mix"]:
                    gains.append(f"mix={', '.join(row['coverage_gain']['mix'])}")
                lines.append(f"  gains: {' | '.join(gains)}")
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
