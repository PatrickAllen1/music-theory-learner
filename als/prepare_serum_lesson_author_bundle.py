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
    from build_song_decision_tree import build_report as build_song_decision_tree_report, render_text as render_song_decision_tree_text
    from compile_guided_build_lesson import build_report as build_compiled_lesson_report, render_text as render_compiled_lesson_text
    from design_full_song_blueprint import build_report as build_full_song_blueprint_report, render_text as render_full_song_blueprint_text
    from generate_serum_guided_build_steps import build_report as build_synth_steps_report, render_text as render_synth_steps_text
    from export_serum_lesson_packet import export_packet
    from generate_serum_guided_build_synth_plan import build_report as build_synth_plan_report, render_text as render_synth_plan_text
    from report_full_song_blueprint_readiness import build_report as build_full_song_readiness_report
    from report_serum_brief_bank_candidates import build_report as build_brief_bank_report
    from report_serum_lesson_author_queue import build_report as build_author_queue_report
    from report_serum_packet_readiness import build_report as build_packet_readiness_report
    from report_serum_render_backlog import build_report as build_render_backlog_report
    from validate_guided_build_lesson import build_report as build_lesson_validation_report, render_text as render_lesson_validation_text
except ModuleNotFoundError:
    from .build_song_decision_tree import build_report as build_song_decision_tree_report, render_text as render_song_decision_tree_text
    from .compile_guided_build_lesson import build_report as build_compiled_lesson_report, render_text as render_compiled_lesson_text
    from .design_full_song_blueprint import build_report as build_full_song_blueprint_report, render_text as render_full_song_blueprint_text
    from .generate_serum_guided_build_steps import build_report as build_synth_steps_report, render_text as render_synth_steps_text
    from .export_serum_lesson_packet import export_packet
    from .generate_serum_guided_build_synth_plan import build_report as build_synth_plan_report, render_text as render_synth_plan_text
    from .report_full_song_blueprint_readiness import build_report as build_full_song_readiness_report
    from .report_serum_brief_bank_candidates import build_report as build_brief_bank_report
    from .report_serum_lesson_author_queue import build_report as build_author_queue_report
    from .report_serum_packet_readiness import build_report as build_packet_readiness_report
    from .report_serum_render_backlog import build_report as build_render_backlog_report
    from .validate_guided_build_lesson import build_report as build_lesson_validation_report, render_text as render_lesson_validation_text


DEFAULT_CATALOG_DIR = Path("als/catalog/profiles")
DEFAULT_BRIEFS_PATH = Path("als/serum-track-briefs.json")
DEFAULT_SONG_BRIEFS_PATH = Path("als/song-blueprint-briefs.json")
DEFAULT_TEMPLATES_PATH = Path("als/song-production-templates.json")
DEFAULT_SPEC_PATH = Path("als/serum-audio-audition-spec.json")


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Prepare a brief-specific Serum lesson author bundle.")
    parser.add_argument("--brief", required=True, help="Brief id from the manifest.")
    parser.add_argument("--out-dir", required=True, help="Output directory for the author bundle.")
    parser.add_argument("--catalog-dir", default=str(DEFAULT_CATALOG_DIR), help="Directory of generated *-profiles.json files.")
    parser.add_argument("--briefs", default=str(DEFAULT_BRIEFS_PATH), help="Underlying Serum brief manifest JSON.")
    parser.add_argument("--song-briefs", default=str(DEFAULT_SONG_BRIEFS_PATH), help="Song-level brief manifest JSON.")
    parser.add_argument("--templates", default=str(DEFAULT_TEMPLATES_PATH), help="Song production templates JSON.")
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
        brief=args.brief,
        catalog_dir=args.catalog_dir,
        briefs=args.briefs,
        song_briefs=args.song_briefs,
        templates=args.templates,
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


def _full_song_namespace(args: argparse.Namespace) -> Namespace:
    return Namespace(
        brief=args.brief,
        song_briefs=args.song_briefs,
        templates=args.templates,
        catalog_dir=args.catalog_dir,
        serum_briefs=args.briefs,
        prefer_rendered=args.prefer_rendered,
        limit_per_part=args.limit_per_part,
        mutation_limit=args.mutation_limit,
        max_swaps=args.max_swaps,
        format="json",
        lesson_only=False,
        lesson_json=None,
    )


def _decision_tree_namespace(args: argparse.Namespace) -> Namespace:
    return Namespace(
        brief=args.brief,
        song_briefs=args.song_briefs,
        templates=args.templates,
        catalog_dir=args.catalog_dir,
        serum_briefs=args.briefs,
        prefer_rendered=args.prefer_rendered,
        limit_per_part=args.limit_per_part,
        mutation_limit=args.mutation_limit,
        max_swaps=args.max_swaps,
        format="json",
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
    song_readiness_row: dict,
    render_blockers: list[dict],
    bank_candidates: dict,
    full_song_blueprint: dict,
    decision_tree: dict,
    compiled_lesson: dict,
    lesson_validation: dict,
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
    lines.append(
        f"- song readiness: blueprint={song_readiness_row['blueprint_readiness']}, "
        f"lesson={song_readiness_row['lesson_readiness']}, overall={song_readiness_row['readiness']}"
    )
    lines.append(f"- refined pairwise conflicts: {author_row['synth_conflicts']}")
    lines.append(f"- fallback count: {author_row['fallback_synth_parts']}")
    if author_row["vague_step_ids"]:
        lines.append(f"- vague lesson steps: {', '.join(str(i) for i in author_row['vague_step_ids'])}")
    lines.append(f"- render blockers in bundle: {len(render_blockers)}")
    lines.append(f"- weak parts with bank candidates: {bank_candidates['parts_needing_attention']}")
    lines.append(f"- synth sections in scaffold: {len(synth_plan['synth_sections'])}")
    lines.append(f"- full-song bars: {full_song_blueprint['readiness']['total_bars']}")
    lines.append(f"- compiled lesson steps: {compiled_lesson['lesson']['steps'] and len(compiled_lesson['lesson']['steps'])}")
    lines.append(f"- decision branches: {len(decision_tree['branches'])}")
    lines.append(f"- production techniques attached: {full_song_blueprint['production_techniques']['result_count']}")
    lines.append(
        f"- technique interactions: "
        f"{full_song_blueprint['production_techniques']['interaction_analysis']['reinforcement_count']} reinforcements / "
        f"{full_song_blueprint['production_techniques']['interaction_analysis']['watchout_count']} watchouts"
    )
    lines.append(
        f"- production commitments: "
        f"{full_song_blueprint['production_techniques']['interaction_analysis']['decision_commitments']['required_pairing_count']} pairings / "
        f"{full_song_blueprint['production_techniques']['interaction_analysis']['decision_commitments']['mandatory_constraint_count']} constraints"
    )
    lines.append("")
    lines.append("## Next Actions")
    for step in song_readiness_row["next_actions"]:
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
    if full_song_blueprint["production_techniques"]["recommendations"]:
        lines.append("## Top Production Techniques")
        for row in full_song_blueprint["production_techniques"]["recommendations"][:3]:
            lines.append(f"- `{row['name']}` [{row['source']}]")
            lines.append(f"  why now: {row['when_to_use']}")
        lines.append("")
    interaction = full_song_blueprint["production_techniques"]["interaction_analysis"]
    if interaction["watchouts"] or interaction["reinforcements"]:
        lines.append("## Technique Interactions")
        for row in interaction["reinforcements"][:3]:
            lines.append(f"- reinforcement :: `{row['left_id']}` <-> `{row['right_id']}`")
            lines.append(f"  evidence: {' | '.join(item['phrase'] for item in row['evidence'])}")
        for row in interaction["watchouts"][:3]:
            lines.append(f"- watchout :: `{row['left_id']}` <-> `{row['right_id']}`")
            lines.append(f"  evidence: {' | '.join(item['phrase'] for item in row['evidence'])}")
            if row["mitigations"]:
                lines.append(f"  mitigations: {' | '.join(row['mitigations'][:2])}")
        lines.append("")
    commitments = interaction["decision_commitments"]
    if commitments["required_pairings"] or commitments["mandatory_constraints"]:
        lines.append("## Production Commitments")
        for row in commitments["required_pairings"][:3]:
            lines.append(f"- pairing :: {row['rule']}")
            if row["why"]:
                lines.append(f"  why: {row['why']}")
        for row in commitments["mandatory_constraints"][:3]:
            lines.append(f"- constraint :: {row['rule']}")
            if row["why"]:
                lines.append(f"  why: {row['why']}")
            if row["required_moves"]:
                lines.append(f"  must do: {' | '.join(row['required_moves'][:2])}")
        lines.append("")
    lines.append("## Bundle Files")
    lines.append("- `packet/` contains the refined packet export.")
    lines.append("- `full-song-blueprint.json` / `full-song-blueprint.md` capture the actual production plan.")
    lines.append("- `decision-tree.json` / `decision-tree.md` prepare the model-led composition pass.")
    lines.append("- `production-techniques.json` / `production-techniques.md` show the transcript-derived moves that fit this brief.")
    lines.append("- `full-song-readiness.json` shows whether the song plan is release-shaped enough to proceed.")
    lines.append("- `compiled-lesson.json` is the draft lesson object generated from the full-song plan.")
    lines.append("- `lesson-validation.json` shows what still keeps the draft from being app-ready.")
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
    full_song_readiness = build_full_song_readiness_report(namespace)
    packet_readiness = build_packet_readiness_report(namespace)
    render_backlog = build_render_backlog_report(namespace)
    bank_candidates = build_brief_bank_report(_bank_namespace(args))
    full_song_blueprint = build_full_song_blueprint_report(_full_song_namespace(args))
    decision_tree = build_song_decision_tree_report(_decision_tree_namespace(args))
    compiled_lesson = build_compiled_lesson_report(_full_song_namespace(args))
    lesson_validation = build_lesson_validation_report(_full_song_namespace(args))
    synth_plan = build_synth_plan_report(_synth_plan_namespace(args))
    synth_steps = build_synth_steps_report(_synth_steps_namespace(args))

    author_row = _find_row(author_queue["queue"], args.brief)
    song_readiness_row = _find_row(full_song_readiness["briefs"], args.brief)
    readiness_row = _find_row(packet_readiness["briefs"], args.brief)
    render_blockers = _brief_render_blockers(render_backlog, args.brief, args.render_limit)

    _write_text(out_dir / "author-queue.json", json.dumps(author_row, indent=2) + "\n", args.force)
    _write_text(out_dir / "packet-readiness.json", json.dumps(readiness_row, indent=2) + "\n", args.force)
    _write_text(out_dir / "full-song-readiness.json", json.dumps(song_readiness_row, indent=2) + "\n", args.force)
    _write_text(out_dir / "render-blockers.json", json.dumps(render_blockers, indent=2) + "\n", args.force)
    _write_text(out_dir / "render-blockers.tsv", _render_blockers_tsv(render_blockers), args.force)
    _write_text(out_dir / "bank-candidates.json", json.dumps(bank_candidates, indent=2) + "\n", args.force)
    _write_text(out_dir / "bank-candidates.tsv", _bank_candidates_tsv(bank_candidates), args.force)
    _write_text(out_dir / "full-song-blueprint.json", json.dumps(full_song_blueprint, indent=2) + "\n", args.force)
    _write_text(out_dir / "full-song-blueprint.md", render_full_song_blueprint_text(full_song_blueprint) + "\n", args.force)
    _write_text(out_dir / "decision-tree.json", json.dumps(decision_tree, indent=2) + "\n", args.force)
    _write_text(out_dir / "decision-tree.md", render_song_decision_tree_text(decision_tree) + "\n", args.force)
    _write_text(
        out_dir / "production-techniques.json",
        json.dumps(full_song_blueprint["production_techniques"], indent=2) + "\n",
        args.force,
    )
    _write_text(
        out_dir / "production-techniques.md",
        "\n".join([
            "# Production Techniques",
            "",
            f"- brief: `{args.brief}`",
            f"- results: {full_song_blueprint['production_techniques']['result_count']}",
            "",
            *[
                "\n".join([
                    f"- `{row['id']}` :: {row['name']} [{row['source']}] score={row['score']}",
                    f"  when: {row['when_to_use']}",
                    f"  does: {row['what_it_does']}",
                    f"  matched: {', '.join(row['matched_keywords'])}" if row["matched_keywords"] else "",
                ]).rstrip()
                for row in full_song_blueprint["production_techniques"]["recommendations"]
            ],
            "",
            "## Technique Interactions",
            *(
                [
                    *[
                        "\n".join([
                            f"- reinforcement :: `{row['left_id']}` <-> `{row['right_id']}`",
                            f"  evidence: {' | '.join(item['phrase'] for item in row['evidence'])}",
                        ])
                        for row in full_song_blueprint["production_techniques"]["interaction_analysis"]["reinforcements"]
                    ],
                    *[
                        "\n".join([
                            f"- watchout :: `{row['left_id']}` <-> `{row['right_id']}`",
                            f"  evidence: {' | '.join(item['phrase'] for item in row['evidence'])}",
                            f"  mitigations: {' | '.join(row['mitigations'][:3])}" if row["mitigations"] else "",
                        ]).rstrip()
                        for row in full_song_blueprint["production_techniques"]["interaction_analysis"]["watchouts"]
                    ],
                ]
                if (
                    full_song_blueprint["production_techniques"]["interaction_analysis"]["reinforcements"]
                    or full_song_blueprint["production_techniques"]["interaction_analysis"]["watchouts"]
                )
                else ["- none detected"]
            ),
            "",
            "## Production Commitments",
            *(
                [
                    *[
                        "\n".join([
                            f"- pairing :: {row['rule']}",
                            f"  why: {row['why']}" if row["why"] else "",
                        ]).rstrip()
                        for row in full_song_blueprint["production_techniques"]["interaction_analysis"]["decision_commitments"]["required_pairings"]
                    ],
                    *[
                        "\n".join([
                            f"- constraint :: {row['rule']}",
                            f"  why: {row['why']}" if row["why"] else "",
                            f"  must do: {' | '.join(row['required_moves'][:3])}" if row["required_moves"] else "",
                        ]).rstrip()
                        for row in full_song_blueprint["production_techniques"]["interaction_analysis"]["decision_commitments"]["mandatory_constraints"]
                    ],
                ]
                if (
                    full_song_blueprint["production_techniques"]["interaction_analysis"]["decision_commitments"]["required_pairings"]
                    or full_song_blueprint["production_techniques"]["interaction_analysis"]["decision_commitments"]["mandatory_constraints"]
                )
                else ["- none detected"]
            ),
            "",
        ]),
        args.force,
    )
    _write_text(out_dir / "compiled-lesson.json", json.dumps(compiled_lesson["lesson"], indent=2) + "\n", args.force)
    _write_text(out_dir / "compiled-lesson-diagnostics.json", json.dumps(compiled_lesson, indent=2) + "\n", args.force)
    _write_text(out_dir / "compiled-lesson.md", render_compiled_lesson_text(compiled_lesson) + "\n", args.force)
    _write_text(out_dir / "lesson-validation.json", json.dumps(lesson_validation, indent=2) + "\n", args.force)
    _write_text(out_dir / "lesson-validation.md", render_lesson_validation_text(lesson_validation) + "\n", args.force)
    _write_text(out_dir / "synth-plan.json", json.dumps(synth_plan, indent=2) + "\n", args.force)
    _write_text(out_dir / "synth-plan.md", render_synth_plan_text(synth_plan) + "\n", args.force)
    _write_text(out_dir / "synth-steps.json", json.dumps(synth_steps, indent=2) + "\n", args.force)
    _write_text(out_dir / "synth-steps.md", render_synth_steps_text(synth_steps) + "\n", args.force)
    _write_text(
        out_dir / "README.md",
        _author_summary(
            packet,
            author_row,
            readiness_row,
            song_readiness_row,
            render_blockers,
            bank_candidates,
            full_song_blueprint,
            decision_tree,
            compiled_lesson,
            lesson_validation,
            synth_plan,
            packet_dir,
        ),
        args.force,
    )

    manifest = {
        "brief_id": args.brief,
        "out_dir": str(out_dir),
        "packet_dir": str(packet_dir),
        "prefer_rendered": args.prefer_rendered,
        "files": {
            "readme": str(out_dir / "README.md"),
            "author_queue_json": str(out_dir / "author-queue.json"),
            "packet_readiness_json": str(out_dir / "packet-readiness.json"),
            "full_song_readiness_json": str(out_dir / "full-song-readiness.json"),
            "render_blockers_json": str(out_dir / "render-blockers.json"),
            "render_blockers_tsv": str(out_dir / "render-blockers.tsv"),
            "bank_candidates_json": str(out_dir / "bank-candidates.json"),
            "bank_candidates_tsv": str(out_dir / "bank-candidates.tsv"),
            "full_song_blueprint_json": str(out_dir / "full-song-blueprint.json"),
            "full_song_blueprint_md": str(out_dir / "full-song-blueprint.md"),
            "decision_tree_json": str(out_dir / "decision-tree.json"),
            "decision_tree_md": str(out_dir / "decision-tree.md"),
            "production_techniques_json": str(out_dir / "production-techniques.json"),
            "production_techniques_md": str(out_dir / "production-techniques.md"),
            "compiled_lesson_json": str(out_dir / "compiled-lesson.json"),
            "compiled_lesson_diagnostics_json": str(out_dir / "compiled-lesson-diagnostics.json"),
            "compiled_lesson_md": str(out_dir / "compiled-lesson.md"),
            "lesson_validation_json": str(out_dir / "lesson-validation.json"),
            "lesson_validation_md": str(out_dir / "lesson-validation.md"),
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
        "song_readiness": song_readiness_row["readiness"],
        "lesson_readiness": song_readiness_row["lesson_readiness"],
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
