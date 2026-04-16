#!/usr/bin/env python3
"""
export_serum_lesson_packet.py

Export a full lesson packet for a Serum brief: blueprint JSON, lesson notes,
and the audio render session metadata for the selected stack.

Examples:
    python3 als/export_serum_lesson_packet.py --brief ukg-4x4-pluck-driver --out-dir als/lesson-packets/ukg-4x4-pluck-driver
"""

from __future__ import annotations

import argparse
import json
from argparse import Namespace
from pathlib import Path

try:
    from design_serum_track_blueprint import build_report as build_blueprint_report, render_text as render_blueprint_text
    from refine_serum_track_blueprint import build_report as build_refined_blueprint_report, render_text as render_refined_blueprint_text
    from generate_serum_lesson_notes import build_report as build_lesson_notes_report, render_text as render_lesson_notes_text
    from suggest_serum_blueprint_mutations import build_report as build_mutation_plan_report, render_text as render_mutation_plan_text
    from prepare_serum_audio_session import build_queue, render_readme, render_tsv
    from search_serum_profiles import load_profiles
except ModuleNotFoundError:
    from .design_serum_track_blueprint import build_report as build_blueprint_report, render_text as render_blueprint_text
    from .refine_serum_track_blueprint import build_report as build_refined_blueprint_report, render_text as render_refined_blueprint_text
    from .generate_serum_lesson_notes import build_report as build_lesson_notes_report, render_text as render_lesson_notes_text
    from .suggest_serum_blueprint_mutations import build_report as build_mutation_plan_report, render_text as render_mutation_plan_text
    from .prepare_serum_audio_session import build_queue, render_readme, render_tsv
    from .search_serum_profiles import load_profiles


DEFAULT_CATALOG_DIR = Path("als/catalog/profiles")
DEFAULT_BRIEFS_PATH = Path("als/serum-track-briefs.json")
DEFAULT_SPEC_PATH = Path("als/serum-audio-audition-spec.json")


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Export a Serum lesson packet from a track brief.")
    parser.add_argument("--out-dir", required=True, help="Output directory for the lesson packet.")
    parser.add_argument("--catalog-dir", default=str(DEFAULT_CATALOG_DIR), help="Directory of generated *-profiles.json files.")
    parser.add_argument("--briefs", default=str(DEFAULT_BRIEFS_PATH), help="Track brief manifest JSON.")
    parser.add_argument("--brief", required=True, help="Brief id from the manifest.")
    parser.add_argument("--spec", default=str(DEFAULT_SPEC_PATH), help="Audio audition spec JSON.")
    parser.add_argument("--prefer-rendered", action="store_true", help="Prefer rendered profiles where available.")
    parser.add_argument("--limit-per-part", type=int, default=5, help="Max candidates to inspect per blueprint part. Default: 5")
    parser.add_argument("--mutation-limit", type=int, default=6, help="Max mutation suggestions per part. Default: 6")
    parser.add_argument("--refine", action="store_true", help="Refine the blueprint before exporting the packet.")
    parser.add_argument("--max-swaps", type=int, default=2, help="Maximum refinement swaps to apply when --refine is set. Default: 2")
    parser.add_argument("--force", action="store_true", help="Overwrite existing metadata files.")
    return parser


def _write_text(path: Path, content: str, force: bool) -> None:
    if path.exists() and not force:
        raise FileExistsError(f"{path} already exists; rerun with --force to overwrite")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def _namespace(args: argparse.Namespace) -> Namespace:
    return Namespace(
        catalog_dir=args.catalog_dir,
        briefs=args.briefs,
        brief=args.brief,
        prefer_rendered=args.prefer_rendered,
        limit_per_part=args.limit_per_part,
        mutation_limit=args.mutation_limit,
        refine=args.refine,
        max_swaps=args.max_swaps,
        format="json",
    )


def _refine_namespace(args: argparse.Namespace) -> Namespace:
    return Namespace(
        **vars(_namespace(args)),
        alternative_limit=max(args.limit_per_part, 5),
    )


def export_packet(args: argparse.Namespace) -> dict:
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    report_args = _namespace(args)
    refine_args = _refine_namespace(args)
    blueprint = build_refined_blueprint_report(refine_args) if args.refine else build_blueprint_report(report_args)
    lesson_notes = build_lesson_notes_report(refine_args if args.refine else report_args)
    mutation_plan = build_mutation_plan_report(refine_args if args.refine else report_args)

    profiles = load_profiles(Path(args.catalog_dir))
    by_id = {profile["profile_id"]: profile for profile in profiles}
    selected_profiles = [by_id[profile_id] for profile_id in blueprint["selected_profile_ids"] if profile_id in by_id]

    spec_path = Path(args.spec)
    spec = json.loads(spec_path.read_text())
    queue = build_queue(selected_profiles, spec)

    _write_text(out_dir / "blueprint.json", json.dumps(blueprint, indent=2) + "\n", args.force)
    _write_text(out_dir / "blueprint.md", (render_refined_blueprint_text(blueprint) if args.refine else render_blueprint_text(blueprint)) + "\n", args.force)
    _write_text(out_dir / "lesson-notes.json", json.dumps(lesson_notes, indent=2) + "\n", args.force)
    _write_text(out_dir / "lesson-notes.md", render_lesson_notes_text(lesson_notes) + "\n", args.force)
    _write_text(out_dir / "mutation-plan.json", json.dumps(mutation_plan, indent=2) + "\n", args.force)
    _write_text(out_dir / "mutation-plan.md", render_mutation_plan_text(mutation_plan) + "\n", args.force)

    audio_dir = out_dir / "audio-session"
    renders_dir = audio_dir / "renders"
    renders_dir.mkdir(parents=True, exist_ok=True)
    _write_text(audio_dir / "README.md", render_readme(queue, audio_dir, spec_path), args.force)
    _write_text(audio_dir / "audio_queue.tsv", render_tsv(queue), args.force)
    _write_text(audio_dir / "audio_queue.json", json.dumps({
        "spec_version": spec["spec_version"],
        "profile_count": len(selected_profiles),
        "queue_count": len(queue),
        "queue": queue,
        "blueprint": blueprint,
    }, indent=2) + "\n", args.force)
    _write_text(audio_dir / "session_config.json", json.dumps({
        "brief_id": blueprint["brief_id"],
        "catalog_dir": str(Path(args.catalog_dir)),
        "spec_path": str(spec_path),
        "profile_ids": blueprint["selected_profile_ids"],
    }, indent=2) + "\n", args.force)
    _write_text(audio_dir / ".gitignore", "renders/*.wav\n", args.force)

    manifest = {
        "brief_id": blueprint["brief_id"],
        "prefer_rendered": blueprint["prefer_rendered"],
        "refined": args.refine,
        "selected_profile_ids": blueprint["selected_profile_ids"],
        "files": {
            "blueprint_json": str(out_dir / "blueprint.json"),
            "blueprint_md": str(out_dir / "blueprint.md"),
            "lesson_notes_json": str(out_dir / "lesson-notes.json"),
            "lesson_notes_md": str(out_dir / "lesson-notes.md"),
            "mutation_plan_json": str(out_dir / "mutation-plan.json"),
            "mutation_plan_md": str(out_dir / "mutation-plan.md"),
            "audio_session_dir": str(audio_dir),
        },
    }
    _write_text(out_dir / "packet-manifest.json", json.dumps(manifest, indent=2) + "\n", args.force)

    return {
        "ok": True,
        "out_dir": str(out_dir),
        "brief_id": blueprint["brief_id"],
        "profile_count": len(selected_profiles),
        "queue_count": len(queue),
        "blueprint": blueprint,
        "lesson_notes": lesson_notes,
        "mutation_plan": mutation_plan,
        "audio_queue": queue,
        "manifest": manifest,
        "files": manifest["files"],
    }


def main() -> None:
    parser = make_parser()
    args = parser.parse_args()
    result = export_packet(args)
    print(json.dumps({
        "ok": result["ok"],
        "out_dir": result["out_dir"],
        "brief_id": result["brief_id"],
        "profile_count": result["profile_count"],
        "queue_count": result["queue_count"],
        "files": result["files"],
    }, indent=2))


if __name__ == "__main__":
    main()
