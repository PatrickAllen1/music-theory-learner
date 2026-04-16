#!/usr/bin/env python3
"""
prepare_serum_blueprint_audio_session.py

Prepare an audio render session for the selected profiles inside a designed
Serum track blueprint.

Examples:
    python3 als/prepare_serum_blueprint_audio_session.py --brief ukg-4x4-pluck-driver --out-dir als/audio-session/ukg-pluck
"""

from __future__ import annotations

import argparse
import json
from argparse import Namespace
from pathlib import Path

try:
    from design_serum_track_blueprint import build_report as build_blueprint_report
    from refine_serum_track_blueprint import build_report as build_refined_blueprint_report
    from prepare_serum_audio_session import build_queue, render_readme, render_tsv
    from search_serum_profiles import load_profiles
except ModuleNotFoundError:
    from .design_serum_track_blueprint import build_report as build_blueprint_report
    from .refine_serum_track_blueprint import build_report as build_refined_blueprint_report
    from .prepare_serum_audio_session import build_queue, render_readme, render_tsv
    from .search_serum_profiles import load_profiles


DEFAULT_CATALOG_DIR = Path("als/catalog/profiles")
DEFAULT_BRIEFS_PATH = Path("als/serum-track-briefs.json")
DEFAULT_SPEC_PATH = Path("als/serum-audio-audition-spec.json")


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Prepare a render session from a Serum track blueprint.")
    parser.add_argument("--out-dir", required=True, help="Output directory for the audio session bundle.")
    parser.add_argument("--catalog-dir", default=str(DEFAULT_CATALOG_DIR), help="Directory of generated *-profiles.json files.")
    parser.add_argument("--briefs", default=str(DEFAULT_BRIEFS_PATH), help="Track brief manifest JSON.")
    parser.add_argument("--brief", required=True, help="Brief id from the manifest.")
    parser.add_argument("--spec", default=str(DEFAULT_SPEC_PATH), help="Audio audition spec JSON.")
    parser.add_argument("--prefer-rendered", action="store_true", help="Prefer rendered profiles where available in the blueprint selection.")
    parser.add_argument("--limit-per-part", type=int, default=5, help="Max candidates to inspect per blueprint part. Default: 5")
    parser.add_argument("--mutation-limit", type=int, default=6, help="Max mutation suggestions per part. Default: 6")
    parser.add_argument("--refine", action="store_true", help="Refine the blueprint before preparing the render session.")
    parser.add_argument("--max-swaps", type=int, default=2, help="Maximum refinement swaps to apply when --refine is set. Default: 2")
    parser.add_argument("--force", action="store_true", help="Overwrite existing metadata files.")
    return parser


def _write_text(path: Path, content: str, force: bool) -> None:
    if path.exists() and not force:
        raise FileExistsError(f"{path} already exists; rerun with --force to overwrite")
    path.write_text(content)


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


def main() -> None:
    parser = make_parser()
    args = parser.parse_args()
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    renders_dir = out_dir / "renders"
    renders_dir.mkdir(parents=True, exist_ok=True)

    blueprint = build_refined_blueprint_report(_refine_namespace(args)) if args.refine else build_blueprint_report(_blueprint_namespace(args))
    selected_profile_ids = blueprint["selected_profile_ids"]

    profiles = load_profiles(Path(args.catalog_dir))
    by_id = {profile["profile_id"]: profile for profile in profiles}
    selected_profiles = [by_id[profile_id] for profile_id in selected_profile_ids if profile_id in by_id]

    spec_path = Path(args.spec)
    spec = json.loads(spec_path.read_text())
    queue = build_queue(selected_profiles, spec)
    session_config = {
        "brief_id": blueprint["brief_id"],
        "catalog_dir": str(Path(args.catalog_dir)),
        "spec_path": str(spec_path),
        "profile_ids": selected_profile_ids,
        "selected_parts": [
            {
                "part_id": part["part_id"],
                "role": part["role"],
                "profile_id": part["selection"]["profile_id"] if part["selection"] else None,
            }
            for part in blueprint["parts"]
        ],
        "refined": args.refine,
    }

    readme = render_readme(queue, out_dir, spec_path) + "\n## Blueprint\n\n" + json.dumps({
        "brief_id": blueprint["brief_id"],
        "description": blueprint["description"],
        "selected_profile_ids": selected_profile_ids,
    }, indent=2) + "\n"

    _write_text(out_dir / "README.md", readme, args.force)
    _write_text(out_dir / "audio_queue.tsv", render_tsv(queue), args.force)
    _write_text(out_dir / "audio_queue.json", json.dumps({
        "spec_version": spec["spec_version"],
        "profile_count": len(selected_profiles),
        "queue_count": len(queue),
        "queue": queue,
        "blueprint": blueprint,
    }, indent=2) + "\n", args.force)
    _write_text(out_dir / "blueprint.json", json.dumps(blueprint, indent=2) + "\n", args.force)
    _write_text(out_dir / "session_config.json", json.dumps(session_config, indent=2) + "\n", args.force)
    _write_text(out_dir / ".gitignore", "renders/*.wav\n", args.force)

    print(json.dumps({
        "ok": True,
        "out_dir": str(out_dir),
        "brief_id": blueprint["brief_id"],
        "profile_count": len(selected_profiles),
        "queue_count": len(queue),
        "selected_profile_ids": selected_profile_ids,
    }, indent=2))


if __name__ == "__main__":
    main()
