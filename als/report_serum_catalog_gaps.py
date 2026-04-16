#!/usr/bin/env python3
"""
report_serum_catalog_gaps.py

Aggregate the weak spots exposed by refined briefs so it is clear which kinds
of Serum sounds the catalog needs more of.

Examples:
    python3 als/report_serum_catalog_gaps.py
    python3 als/report_serum_catalog_gaps.py --format json
"""

from __future__ import annotations

import argparse
import json
from argparse import Namespace
from pathlib import Path

try:
    from refine_serum_track_blueprint import build_report as build_refined_blueprint_report
    from suggest_serum_blueprint_mutations import build_report as build_mutation_plan_report
except ModuleNotFoundError:
    from .refine_serum_track_blueprint import build_report as build_refined_blueprint_report
    from .suggest_serum_blueprint_mutations import build_report as build_mutation_plan_report


DEFAULT_CATALOG_DIR = Path("als/catalog/profiles")
DEFAULT_BRIEFS_PATH = Path("als/serum-track-briefs.json")


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Report catalog gaps exposed by Serum brief refinement.")
    parser.add_argument("--catalog-dir", default=str(DEFAULT_CATALOG_DIR), help="Directory of generated *-profiles.json files.")
    parser.add_argument("--briefs", default=str(DEFAULT_BRIEFS_PATH), help="Track brief manifest JSON.")
    parser.add_argument("--prefer-rendered", action="store_true", help="Prefer rendered profiles where available.")
    parser.add_argument("--limit-per-part", type=int, default=5, help="Max candidates to inspect per part. Default: 5")
    parser.add_argument("--mutation-limit", type=int, default=6, help="Max mutation suggestions per part. Default: 6")
    parser.add_argument("--max-swaps", type=int, default=2, help="Maximum refinement swaps to apply. Default: 2")
    parser.add_argument("--format", choices=["json", "text"], default="text", help="Output format.")
    return parser


def _brief_ids(path: Path) -> list[str]:
    payload = json.loads(path.read_text())
    return sorted((payload.get("briefs") or {}).keys())


def _refine_namespace(args: argparse.Namespace, brief_id: str) -> Namespace:
    return Namespace(
        catalog_dir=args.catalog_dir,
        briefs=args.briefs,
        brief=brief_id,
        prefer_rendered=args.prefer_rendered,
        limit_per_part=args.limit_per_part,
        mutation_limit=args.mutation_limit,
        alternative_limit=max(args.limit_per_part, 5),
        max_swaps=args.max_swaps,
        format="json",
    )


def _mutation_namespace(args: argparse.Namespace, brief_id: str) -> Namespace:
    return Namespace(
        **vars(_refine_namespace(args, brief_id)),
        refine=True,
        suggestion_limit=8,
    )


def _gap_key(part: dict) -> tuple:
    return (
        part["role"],
        tuple(part.get("target_tone") or []),
        tuple(part.get("target_mix") or []),
    )


def _gap_label(key: tuple) -> str:
    role, tone, mix = key
    tone_text = ", ".join(tone) if tone else "-"
    mix_text = ", ".join(mix) if mix else "-"
    return f"{role} | tone={tone_text} | mix={mix_text}"


def build_report(args: argparse.Namespace) -> dict:
    gaps: dict[tuple, dict] = {}

    for brief_id in _brief_ids(Path(args.briefs)):
        refined = build_refined_blueprint_report(_refine_namespace(args, brief_id))
        mutations = build_mutation_plan_report(_mutation_namespace(args, brief_id))
        mutation_by_part = {part["part_id"]: part for part in mutations["parts"]}

        for part in refined["parts"]:
            mutation_part = mutation_by_part.get(part["part_id"], {})
            flags = []
            if not part.get("selection"):
                flags.append("unresolved")
            if part.get("constraint_mode") != "full":
                flags.append(f"fallback:{part['constraint_mode']}")
            if part.get("selection") and not (mutation_part.get("suggestions") or []):
                flags.append("no_mutations")

            if not flags:
                continue

            key = _gap_key(part)
            entry = gaps.setdefault(key, {
                "role": part["role"],
                "target_tone": part.get("target_tone") or [],
                "target_mix": part.get("target_mix") or [],
                "count": 0,
                "flags": {},
                "examples": [],
                "suggested_action": "",
            })
            entry["count"] += 1
            for flag in flags:
                entry["flags"][flag] = entry["flags"].get(flag, 0) + 1
            entry["examples"].append({
                "brief_id": brief_id,
                "part_id": part["part_id"],
                "constraint_mode": part.get("constraint_mode"),
                "selected_profile_id": part["selection"]["profile_id"] if part.get("selection") else None,
                "flags": flags,
            })

    rows = []
    for key, row in gaps.items():
        severity = row["count"] * 2
        severity += row["flags"].get("unresolved", 0) * 4
        severity += sum(count for flag, count in row["flags"].items() if flag.startswith("fallback:")) * 2
        severity += row["flags"].get("no_mutations", 0)

        actions = []
        if row["flags"].get("unresolved", 0):
            actions.append("ingest more presets that match this role/tone/mix target")
        if any(flag.startswith("fallback:") for flag in row["flags"]):
            actions.append("capture more alternatives that satisfy the full brief instead of a fallback")
        if row["flags"].get("no_mutations", 0):
            actions.append("prioritize renders here so the audio layer can clarify whether the preset is already right or needs replacing")
        row["suggested_action"] = " | ".join(actions) or "monitor"
        row["gap_label"] = _gap_label(key)
        row["severity"] = severity
        row["examples"].sort(key=lambda item: (item["brief_id"], item["part_id"]))
        rows.append(row)

    rows.sort(key=lambda item: (-item["severity"], -item["count"], item["gap_label"]))
    return {
        "gap_count": len(rows),
        "prefer_rendered": args.prefer_rendered,
        "gaps": rows,
    }


def render_text(report: dict) -> str:
    lines = []
    lines.append("# Serum Catalog Gaps")
    lines.append("")
    lines.append(f"- gaps: {report['gap_count']}")
    lines.append(f"- prefer rendered: {'yes' if report['prefer_rendered'] else 'no'}")
    lines.append("")
    for row in report["gaps"]:
        lines.append(
            f"- `{row['gap_label']}` :: severity={row['severity']}; count={row['count']}; "
            f"flags={json.dumps(row['flags'], sort_keys=True)}"
        )
        lines.append(f"  action: {row['suggested_action']}")
        example_text = " | ".join(
            f"{item['brief_id']}:{item['part_id']}({','.join(item['flags'])})"
            for item in row["examples"][:4]
        )
        if example_text:
            lines.append(f"  examples: {example_text}")
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
