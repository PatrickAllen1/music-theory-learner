#!/usr/bin/env python3
"""
design_serum_track_blueprint.py

Turn a reusable track brief into a coherent Serum part stack with selected
profiles, rationale, and mutation suggestions.

Examples:
    python3 als/design_serum_track_blueprint.py --brief ukg-4x4-pluck-driver
    python3 als/design_serum_track_blueprint.py --brief ukg-4x4-lead-driver --prefer-rendered --format json
"""

from __future__ import annotations

import argparse
import json
from argparse import Namespace
from pathlib import Path

try:
    from recommend_serum_part import build_report as build_part_report
except ModuleNotFoundError:
    from .recommend_serum_part import build_report as build_part_report


DEFAULT_CATALOG_DIR = Path("als/catalog/profiles")
DEFAULT_BRIEFS_PATH = Path("als/serum-track-briefs.json")


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Design a Serum track blueprint from a reusable part brief.")
    parser.add_argument("--catalog-dir", default=str(DEFAULT_CATALOG_DIR), help="Directory of generated *-profiles.json files.")
    parser.add_argument("--briefs", default=str(DEFAULT_BRIEFS_PATH), help="Track brief manifest JSON.")
    parser.add_argument("--brief", required=True, help="Brief id from the manifest.")
    parser.add_argument("--prefer-rendered", action="store_true", help="Prefer rendered profiles where available.")
    parser.add_argument("--limit-per-part", type=int, default=5, help="Max candidates to inspect per part. Default: 5")
    parser.add_argument("--mutation-limit", type=int, default=6, help="Max mutation suggestions per part. Default: 6")
    parser.add_argument("--format", choices=["json", "text"], default="text", help="Output format.")
    return parser


def _load_brief(path: Path, brief_id: str) -> dict:
    payload = json.loads(path.read_text())
    briefs = payload.get("briefs", {})
    if brief_id not in briefs:
        raise KeyError(f"brief not found: {brief_id}")
    brief = briefs[brief_id]
    return {
        "brief_id": brief_id,
        "description": brief.get("description", ""),
        "parts": brief.get("parts", []),
    }


def _part_namespace(args: argparse.Namespace, part: dict) -> Namespace:
    return Namespace(
        catalog_dir=args.catalog_dir,
        role=part["role"],
        tone=part.get("tone", []),
        mix=part.get("mix", []),
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


def _part_report_with_fallback(args: argparse.Namespace, part: dict) -> tuple[dict, str]:
    attempts = [
        ("full", {"tone": part.get("tone", []), "mix": part.get("mix", [])}),
        ("mix_only", {"tone": [], "mix": part.get("mix", [])}),
        ("tone_only", {"tone": part.get("tone", []), "mix": []}),
        ("role_only", {"tone": [], "mix": []}),
    ]
    for mode, overrides in attempts:
        namespace = _part_namespace(args, {
            **part,
            "tone": overrides["tone"],
            "mix": overrides["mix"],
        })
        report = build_part_report(namespace)
        if report["candidate_count"] > 0:
            return report, mode
    return build_part_report(_part_namespace(args, part)), "full"


def _choose_candidate(candidates: list[dict], used_profile_ids: set[str]) -> dict | None:
    for candidate in candidates:
        if candidate["profile_id"] not in used_profile_ids:
            return candidate
    return candidates[0] if candidates else None


def _conflict_notes(parts: list[dict]) -> list[str]:
    notes = []
    low_end = [part for part in parts if "low_end_anchor" in part["selection"]["mix_tags"]]
    side_heavy = [part for part in parts if "side_heavy" in part["selection"]["mix_tags"]]
    background = [part for part in parts if "background" in part["selection"]["mix_tags"]]
    mid_focus = [part for part in parts if "mid_focus" in part["selection"]["mix_tags"]]

    if len(low_end) >= 2:
        notes.append("Multiple selected parts carry low_end_anchor tags; low-end cleanup may be needed.")
    if len(side_heavy) >= 2:
        notes.append("Multiple selected parts read side_heavy; watch stereo crowding.")
    if not background:
        notes.append("No selected part is clearly background-oriented; the arrangement may feel too forward.")
    if not mid_focus:
        notes.append("No selected part is clearly mid-focused; the hook layer may need more presence.")

    rendered = [part for part in parts if part["selection"].get("audio_summary")]
    for i, left in enumerate(rendered):
        left_summary = left["selection"]["audio_summary"]
        left_centroid = left_summary.get("mean_centroid_hz")
        if left_centroid is None:
            continue
        for right in rendered[i + 1 :]:
            right_summary = right["selection"]["audio_summary"]
            right_centroid = right_summary.get("mean_centroid_hz")
            if right_centroid is None:
                continue
            if abs(left_centroid - right_centroid) <= 180:
                notes.append(
                    f"{left['part_id']} and {right['part_id']} have similar rendered centroids; they may compete in the same spectral band."
                )
    return notes


def build_report(args: argparse.Namespace) -> dict:
    brief = _load_brief(Path(args.briefs), args.brief)
    used_profile_ids: set[str] = set()
    parts = []
    for part in brief["parts"]:
        report, constraint_mode = _part_report_with_fallback(args, part)
        selected = _choose_candidate(report["candidates"], used_profile_ids)
        if selected:
            used_profile_ids.add(selected["profile_id"])
        parts.append({
            "part_id": part["part_id"],
            "role": part["role"],
            "target_tone": part.get("tone", []),
            "target_mix": part.get("mix", []),
            "goals": part.get("goals", []),
            "candidate_count": report["candidate_count"],
            "constraint_mode": constraint_mode,
            "selection": selected,
        })
    return {
        "brief_id": brief["brief_id"],
        "description": brief["description"],
        "prefer_rendered": args.prefer_rendered,
        "parts": parts,
        "conflict_notes": _conflict_notes([part for part in parts if part["selection"]]),
    }


def render_text(report: dict) -> str:
    lines = []
    lines.append("# Serum Track Blueprint")
    lines.append("")
    lines.append(f"- brief: `{report['brief_id']}`")
    lines.append(f"- prefer rendered: {'yes' if report['prefer_rendered'] else 'no'}")
    lines.append(f"- description: {report['description']}")
    lines.append("")
    for part in report["parts"]:
        lines.append(f"## {part['part_id']} ({part['role']})")
        lines.append(f"- target tone: {', '.join(part['target_tone']) or '-'}")
        lines.append(f"- target mix: {', '.join(part['target_mix']) or '-'}")
        lines.append(f"- goals: {', '.join(part['goals']) or '-'}")
        lines.append(f"- candidate count: {part['candidate_count']}")
        lines.append(f"- constraint mode: {part['constraint_mode']}")
        selection = part["selection"]
        if not selection:
            lines.append("- selection: none")
            lines.append("")
            continue
        lines.append(
            f"- selection: `{selection['profile_id']}` "
            f"({selection['track'] or '-'}; tone: {', '.join(selection['tone_tags'])}; "
            f"mix: {', '.join(selection['mix_tags'])}; audio: {selection['audio_status']})"
        )
        if selection.get("audio_summary"):
            summary = selection["audio_summary"]
            lines.append(
                f"- audio summary: centroid={summary.get('mean_centroid_hz')}, "
                f"attack_ms={summary.get('mean_attack_time_ms')}, "
                f"side_ratio={summary.get('mean_side_ratio')}, "
                f"rms_dbfs={summary.get('mean_rms_dbfs')}"
            )
        if selection.get("notes"):
            lines.append(f"- reasons: {' | '.join(selection['notes'])}")
        for suggestion in selection.get("mutation_suggestions", []):
            lines.append(
                f"- mutate `{suggestion['path']}` :: {suggestion['action']} "
                f"{suggestion['current_value']} -> {suggestion['suggested_value']} "
                f"[goal: {suggestion['goal']}]"
            )
        lines.append("")
    if report["conflict_notes"]:
        lines.append("## Conflict Notes")
        for note in report["conflict_notes"]:
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
