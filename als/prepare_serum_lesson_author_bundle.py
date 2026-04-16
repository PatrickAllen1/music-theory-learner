#!/usr/bin/env python3
"""
prepare_serum_lesson_author_bundle.py

Prepare a brief-specific authoring bundle: refined packet export, render
blockers for the chosen brief, real Garage bank candidates for weak parts, and
an explicit summary of what to do next before turning the stack into a lesson.

Examples:
    python3 als/prepare_serum_lesson_author_bundle.py --brief ukg-2step-dark-stab --out-dir als/lesson-author/ukg-2step-dark-stab
"""

from __future__ import annotations

import argparse
import json
from argparse import Namespace
from pathlib import Path

try:
    from generate_serum_guided_build_steps import build_report as build_synth_steps_report, render_text as render_synth_steps_text
    from export_serum_lesson_packet import export_packet
    from generate_serum_guided_build_synth_plan import build_report as build_synth_plan_report, render_text as render_synth_plan_text
    from report_serum_brief_bank_candidates import build_report as build_brief_bank_report
    from report_serum_lesson_author_queue import build_report as build_author_queue_report
    from report_serum_packet_readiness import build_report as build_packet_readiness_report
    from report_serum_render_backlog import build_report as build_render_backlog_report
except ModuleNotFoundError:
    from .generate_serum_guided_build_steps import build_report as build_synth_steps_report, render_text as render_synth_steps_text
    from .export_serum_lesson_packet import export_packet
    from .generate_serum_guided_build_synth_plan import build_report as build_synth_plan_report, render_text as render_synth_plan_text
    from .report_serum_brief_bank_candidates import build_report as build_brief_bank_report
    from .report_serum_lesson_author_queue import build_report as build_author_queue_report
    from .report_serum_packet_readiness import build_report as build_packet_readiness_report
    from .report_serum_render_backlog import build_report as build_render_backlog_report


DEFAULT_CATALOG_DIR = Path("als/catalog/profiles")
DEFAULT_BRIEFS_PATH = Path("als/serum-track-briefs.json")
DEFAULT_SPEC_PATH = Path("als/serum-audio-audition-spec.json")


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Prepare a brief-specific Serum lesson author bundle.")
    parser.add_argument("--brief", required=True, help="Brief id from the manifest.")
    parser.add_argument("--out-dir", required=True, help="Output directory for the author bundle.")
    parser.add_argument("--catalog-dir", default=str(DEFAULT_CATALOG_DIR), help="Directory of generated *-profiles.json files.")
    parser.add_argument("--briefs", default=str(DEFAULT_BRIEFS_PATH), help="Track brief manifest JSON.")
    parser.add_argument("--spec", default=str(DEFAULT_SPEC_PATH), help="Audio audition spec JSON.")
    parser.add_argument("--prefer-rendered", action="store_true", help="Prefer rendered profiles where available.")
    parser.add_argument("--limit-per-part", type=int, default=5, help="Max candidates to inspect per part. Default: 5")
    parser.add_argument("--mutation-limit", type=int, default=6, help="Max mutation suggestions per part. Default: 6")
    parser.add_argument("--max-swaps", type=int, default=2, help="Maximum refinement swaps to apply. Default: 2")
    parser.add_argument("--render-limit", type=int, default=6, help="Maximum render blockers to include. Default: 6")
    parser.add_argument("--bank-dir", action="append", default=[], help="Preset bank directory to scan. Pass multiple times.")
    parser.add_argument("--bank-top-per-part", type=int, default=5, help="Maximum bank candidates per part. Default: 5")
    parser.add_argument("--include-stable-bank-parts", action="store_true", help="Include stable parts in the bank-candidate report.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files.")
    return parser


def _write_text(path: Path, content: str, force: bool) -> None:
    if path.exists() and not force:
        raise FileExistsError(f"{path} already exists; rerun with --force to overwrite")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def _shared_namespace(args: argparse.Namespace) -> Namespace:
    return Namespace(
        catalog_dir=args.catalog_dir,
        briefs=args.briefs,
        prefer_rendered=args.prefer_rendered,
        limit_per_part=args.limit_per_part,
        mutation_limit=args.mutation_limit,
        max_swaps=args.max_swaps,
        format="json",
    )


def _packet_namespace(args: argparse.Namespace, packet_dir: Path) -> Namespace:
    return Namespace(
        out_dir=str(packet_dir),
        catalog_dir=args.catalog_dir,
        briefs=args.briefs,
        brief=args.brief,
        spec=args.spec,
        prefer_rendered=args.prefer_rendered,
        limit_per_part=args.limit_per_part,
        mutation_limit=args.mutation_limit,
        refine=True,
        max_swaps=args.max_swaps,
        force=args.force,
    )


def _bank_namespace(args: argparse.Namespace) -> Namespace:
    return Namespace(
        brief=args.brief,
        catalog_dir=args.catalog_dir,
        briefs=args.briefs,
        prefer_rendered=args.prefer_rendered,
        limit_per_part=args.limit_per_part,
        mutation_limit=args.mutation_limit,
        max_swaps=args.max_swaps,
        bank_dir=args.bank_dir,
        top_per_part=args.bank_top_per_part,
        include_stable=args.include_stable_bank_parts,
        format="json",
    )


def _synth_plan_namespace(args: argparse.Namespace) -> Namespace:
    return Namespace(
        brief=args.brief,
        catalog_dir=args.catalog_dir,
        briefs=args.briefs,
        prefer_rendered=args.prefer_rendered,
        limit_per_part=args.limit_per_part,
        mutation_limit=args.mutation_limit,
        max_swaps=args.max_swaps,
        bank_dir=args.bank_dir,
        bank_top_per_part=args.bank_top_per_part,
        render_limit=args.render_limit,
        format="json",
    )


def _synth_steps_namespace(args: argparse.Namespace) -> Namespace:
    return Namespace(
        brief=args.brief,
        catalog_dir=args.catalog_dir,
        briefs=args.briefs,
        prefer_rendered=args.prefer_rendered,
        limit_per_part=args.limit_per_part,
        mutation_limit=args.mutation_limit,
        max_swaps=args.max_swaps,
        bank_dir=args.bank_dir,
        bank_top_per_part=args.bank_top_per_part,
        render_limit=args.render_limit,
        format="json",
    )


def _find_row(rows: list[dict], brief_id: str) -> dict:
    for row in rows:
        if row["brief_id"] == brief_id:
            return row
    raise KeyError(f"brief not found in report: {brief_id}")


def _brief_render_blockers(backlog: dict, brief_id: str, limit: int) -> list[dict]:
    rows = []
    for row in backlog["backlog"]:
        links = [item for item in row["briefs"] if item["brief_id"] == brief_id]
        if not links:
            continue
        rows.append({
            "profile_id": row["profile_id"],
            "track": row.get("track"),
            "analysis_slug": row.get("analysis_slug"),
            "audio_status": row.get("audio_status"),
            "priority": row["priority"],
            "score": row["score"],
            "selection_count": row["selection_count"],
            "reasons": row["reasons"],
            "brief_links": links,
        })
    rows.sort(key=lambda row: (-row["score"], row["profile_id"]))
    return rows[:limit]


def _render_blockers_tsv(rows: list[dict]) -> str:
    header = [
        "profile_id",
        "track",
        "analysis_slug",
        "priority",
        "score",
        "part_id",
        "constraint_mode",
        "conflict_count",
        "mutation_suggestion_count",
        "reasons",
    ]
    lines = ["\t".join(header)]
    for row in rows:
        for link in row["brief_links"]:
            lines.append("\t".join([
                row["profile_id"],
                row.get("track") or "",
                row.get("analysis_slug") or "",
                row["priority"],
                str(row["score"]),
                link["part_id"],
                link["constraint_mode"],
                str(link["conflict_count"]),
                str(link["mutation_suggestion_count"]),
                " | ".join(row["reasons"]),
            ]))
    return "\n".join(lines) + "\n"


def _bank_candidates_tsv(report: dict) -> str:
    header = [
        "part_id",
        "attention_score",
        "attention_reasons",
        "current_profile_id",
        "current_constraint_mode",
        "preset_path",
        "track",
        "bank",
        "role",
        "tone_tags",
        "mix_tags",
        "score",
        "coverage_gain",
    ]
    lines = ["\t".join(header)]
    for part in report["parts"]:
        for row in part["candidates"]:
            gains = []
            if row["coverage_gain"]["tone"]:
                gains.append(f"tone={','.join(row['coverage_gain']['tone'])}")
            if row["coverage_gain"]["mix"]:
                gains.append(f"mix={','.join(row['coverage_gain']['mix'])}")
            lines.append("\t".join([
                part["part_id"],
                str(part["attention_score"]),
                " | ".join(part["attention_reasons"]),
                part.get("current_profile_id") or "",
                part.get("current_constraint_mode") or "",
                row["path"],
                row["track"],
                row.get("bank") or "",
                row["role"],
                ",".join(row["tone_tags"]),
                ",".join(row["mix_tags"]),
                str(row["score"]),
                " | ".join(gains),
            ]))
    return "\n".join(lines) + "\n"


def _author_summary(
    packet: dict,
    author_row: dict,
    readiness_row: dict,
    render_blockers: list[dict],
    bank_candidates: dict,
    synth_plan: dict,
    packet_dir: Path,
) -> str:
    lines = []
    lines.append("# Serum Lesson Author Bundle")
    lines.append("")
    lines.append(f"- brief: `{author_row['brief_id']}`")
    lines.append(f"- readiness: `{author_row['readiness']}`")
    lines.append(f"- author score: {author_row['author_score']}")
    lines.append(f"- refined profile count: {packet['profile_count']}")
    lines.append(f"- packet dir: `{packet_dir}`")
    lines.append("")
    lines.append("## Summary")
    lines.append(f"- {author_row['description']}")
    lines.append(f"- refined pairwise conflicts: {author_row['refined_pairwise_conflicts']}")
    lines.append(f"- fallback count: {author_row['fallback_count']}")
    if author_row["parts_without_mutations"]:
        lines.append(f"- parts without mutations: {', '.join(author_row['parts_without_mutations'])}")
    lines.append(f"- render blockers in bundle: {len(render_blockers)}")
    lines.append(f"- weak parts with bank candidates: {bank_candidates['parts_needing_attention']}")
    lines.append(f"- synth sections in scaffold: {len(synth_plan['synth_sections'])}")
    lines.append("")
    lines.append("## Next Actions")
    for step in readiness_row["next_actions"]:
        lines.append(f"1. {step}")
    if render_blockers:
        lines.append("1. Render the profiles listed in `render-blockers.tsv` before trusting final sound choices.")
    if bank_candidates["parts"]:
        lines.append("1. Review `bank-candidates.tsv` for parts that still need stronger bank options.")
    lines.append("1. Re-export or re-run the brief after renders or bank captures land.")
    lines.append("")
    if render_blockers:
        lines.append("## Top Render Blockers")
        for row in render_blockers:
            part_labels = ", ".join(f"{item['part_id']}({item['constraint_mode']})" for item in row["brief_links"])
            lines.append(f"- `{row['profile_id']}` :: score={row['score']} for {part_labels}")
        lines.append("")
    if bank_candidates["parts"]:
        lines.append("## Parts Needing Stronger Bank Options")
        for part in bank_candidates["parts"]:
            lines.append(
                f"- `{part['part_id']}` :: attention={part['attention_score']} "
                f"[mode: {part['current_constraint_mode']}; current: {part.get('current_profile_id') or '-'}]"
            )
            if part["attention_reasons"]:
                lines.append(f"  why: {' | '.join(part['attention_reasons'])}")
            if part["candidates"]:
                top = part["candidates"][0]
                lines.append(f"  top candidate: `{top['track']}` from `{top.get('bank') or '-'}`")
        lines.append("")
    lines.append("## Bundle Files")
    lines.append("- `packet/` contains the refined packet export.")
    lines.append("- `synth-plan.md` / `synth-plan.json` translate the chosen stack into per-part lesson-authoring steps.")
    lines.append("- `synth-steps.md` / `synth-steps.json` turn those synth sections into draft lesson `steps[]` objects.")
    lines.append("- `render-blockers.tsv` shows the exact profiles that still need audio truth.")
    lines.append("- `bank-candidates.tsv` shows real S1 bank presets worth trying when a part is weak or under-specified.")
    lines.append("")
    return "\n".join(lines) + "\n"


def prepare_bundle(args: argparse.Namespace) -> dict:
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    packet_dir = out_dir / "packet"

    packet = export_packet(_packet_namespace(args, packet_dir))
    namespace = _shared_namespace(args)
    author_queue = build_author_queue_report(namespace)
    packet_readiness = build_packet_readiness_report(namespace)
    render_backlog = build_render_backlog_report(namespace)
    bank_candidates = build_brief_bank_report(_bank_namespace(args))
    synth_plan = build_synth_plan_report(_synth_plan_namespace(args))
    synth_steps = build_synth_steps_report(_synth_steps_namespace(args))

    author_row = _find_row(author_queue["queue"], args.brief)
    readiness_row = _find_row(packet_readiness["briefs"], args.brief)
    render_blockers = _brief_render_blockers(render_backlog, args.brief, args.render_limit)

    _write_text(out_dir / "author-queue.json", json.dumps(author_row, indent=2) + "\n", args.force)
    _write_text(out_dir / "packet-readiness.json", json.dumps(readiness_row, indent=2) + "\n", args.force)
    _write_text(out_dir / "render-blockers.json", json.dumps(render_blockers, indent=2) + "\n", args.force)
    _write_text(out_dir / "render-blockers.tsv", _render_blockers_tsv(render_blockers), args.force)
    _write_text(out_dir / "bank-candidates.json", json.dumps(bank_candidates, indent=2) + "\n", args.force)
    _write_text(out_dir / "bank-candidates.tsv", _bank_candidates_tsv(bank_candidates), args.force)
    _write_text(out_dir / "synth-plan.json", json.dumps(synth_plan, indent=2) + "\n", args.force)
    _write_text(out_dir / "synth-plan.md", render_synth_plan_text(synth_plan) + "\n", args.force)
    _write_text(out_dir / "synth-steps.json", json.dumps(synth_steps, indent=2) + "\n", args.force)
    _write_text(out_dir / "synth-steps.md", render_synth_steps_text(synth_steps) + "\n", args.force)
    _write_text(out_dir / "README.md", _author_summary(packet, author_row, readiness_row, render_blockers, bank_candidates, synth_plan, packet_dir), args.force)

    manifest = {
        "brief_id": args.brief,
        "out_dir": str(out_dir),
        "packet_dir": str(packet_dir),
        "prefer_rendered": args.prefer_rendered,
        "files": {
            "readme": str(out_dir / "README.md"),
            "author_queue_json": str(out_dir / "author-queue.json"),
            "packet_readiness_json": str(out_dir / "packet-readiness.json"),
            "render_blockers_json": str(out_dir / "render-blockers.json"),
            "render_blockers_tsv": str(out_dir / "render-blockers.tsv"),
            "bank_candidates_json": str(out_dir / "bank-candidates.json"),
            "bank_candidates_tsv": str(out_dir / "bank-candidates.tsv"),
            "synth_plan_json": str(out_dir / "synth-plan.json"),
            "synth_plan_md": str(out_dir / "synth-plan.md"),
            "synth_steps_json": str(out_dir / "synth-steps.json"),
            "synth_steps_md": str(out_dir / "synth-steps.md"),
            "packet_manifest_json": str(packet_dir / "packet-manifest.json"),
        },
    }
    _write_text(out_dir / "bundle-manifest.json", json.dumps(manifest, indent=2) + "\n", args.force)

    return {
        "ok": True,
        "brief_id": args.brief,
        "out_dir": str(out_dir),
        "packet_dir": str(packet_dir),
        "author_score": author_row["author_score"],
        "readiness": author_row["readiness"],
        "render_blocker_count": len(render_blockers),
        "weak_part_count": bank_candidates["parts_needing_attention"],
        "files": manifest["files"],
    }


def main() -> None:
    parser = make_parser()
    args = parser.parse_args()
    print(json.dumps(prepare_bundle(args), indent=2))


if __name__ == "__main__":
    main()
