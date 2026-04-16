#!/usr/bin/env python3
"""
prepare_serum_priority_render_session.py

Create a consolidated audio render session for the highest-priority selected
profiles across all configured Serum briefs.

Examples:
    python3 als/prepare_serum_priority_render_session.py --out-dir als/audio-session/priority-renders
"""

from __future__ import annotations

import argparse
import json
from argparse import Namespace
from pathlib import Path

try:
    from prepare_serum_audio_session import build_queue, render_readme, render_tsv
    from report_serum_brief_coverage import build_report as build_coverage_report
    from search_serum_profiles import load_profiles
except ModuleNotFoundError:
    from .prepare_serum_audio_session import build_queue, render_readme, render_tsv
    from .report_serum_brief_coverage import build_report as build_coverage_report
    from .search_serum_profiles import load_profiles


DEFAULT_CATALOG_DIR = Path("als/catalog/profiles")
DEFAULT_BRIEFS_PATH = Path("als/serum-track-briefs.json")
DEFAULT_SPEC_PATH = Path("als/serum-audio-audition-spec.json")


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Prepare a priority render session across all Serum briefs.")
    parser.add_argument("--out-dir", required=True, help="Output directory for the audio session bundle.")
    parser.add_argument("--catalog-dir", default=str(DEFAULT_CATALOG_DIR), help="Directory of generated *-profiles.json files.")
    parser.add_argument("--briefs", default=str(DEFAULT_BRIEFS_PATH), help="Track brief manifest JSON.")
    parser.add_argument("--spec", default=str(DEFAULT_SPEC_PATH), help="Audio audition spec JSON.")
    parser.add_argument("--prefer-rendered", action="store_true", help="Prefer rendered profiles where available when computing coverage.")
    parser.add_argument("--limit-per-part", type=int, default=5, help="Max candidates to inspect per blueprint part. Default: 5")
    parser.add_argument("--mutation-limit", type=int, default=6, help="Max mutation suggestions per part. Default: 6")
    parser.add_argument("--profile-limit", type=int, default=6, help="Maximum number of profiles to include. Default: 6")
    parser.add_argument("--include-medium", action="store_true", help="Include medium-priority profiles after high-priority ones.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing metadata files.")
    return parser


def _write_text(path: Path, content: str, force: bool) -> None:
    if path.exists() and not force:
        raise FileExistsError(f"{path} already exists; rerun with --force to overwrite")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def _coverage_namespace(args: argparse.Namespace) -> Namespace:
    return Namespace(
        catalog_dir=args.catalog_dir,
        briefs=args.briefs,
        prefer_rendered=args.prefer_rendered,
        limit_per_part=args.limit_per_part,
        mutation_limit=args.mutation_limit,
        format="json",
    )


def main() -> None:
    parser = make_parser()
    args = parser.parse_args()
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    renders_dir = out_dir / "renders"
    renders_dir.mkdir(parents=True, exist_ok=True)

    coverage = build_coverage_report(_coverage_namespace(args))
    priorities = coverage["render_priorities"]
    allowed = {"high"}
    if args.include_medium:
        allowed.add("medium")
    chosen_rows = [row for row in priorities if row["render_priority"] in allowed][: args.profile_limit]
    selected_profile_ids = [row["profile_id"] for row in chosen_rows]

    profiles = load_profiles(Path(args.catalog_dir))
    by_id = {profile["profile_id"]: profile for profile in profiles}
    selected_profiles = [by_id[profile_id] for profile_id in selected_profile_ids if profile_id in by_id]

    spec_path = Path(args.spec)
    spec = json.loads(spec_path.read_text())
    queue = build_queue(selected_profiles, spec)

    readme = render_readme(queue, out_dir, spec_path) + "\n## Priority Selection\n\n" + json.dumps({
        "selected_profile_ids": selected_profile_ids,
        "include_medium": args.include_medium,
        "profile_limit": args.profile_limit,
    }, indent=2) + "\n"

    _write_text(out_dir / "README.md", readme, args.force)
    _write_text(out_dir / "audio_queue.tsv", render_tsv(queue), args.force)
    _write_text(out_dir / "audio_queue.json", json.dumps({
        "spec_version": spec["spec_version"],
        "profile_count": len(selected_profiles),
        "queue_count": len(queue),
        "queue": queue,
        "coverage": coverage,
        "selected_profile_ids": selected_profile_ids,
    }, indent=2) + "\n", args.force)
    _write_text(out_dir / "coverage-report.json", json.dumps(coverage, indent=2) + "\n", args.force)
    _write_text(out_dir / "session_config.json", json.dumps({
        "catalog_dir": str(Path(args.catalog_dir)),
        "briefs_path": str(Path(args.briefs)),
        "spec_path": str(spec_path),
        "profile_ids": selected_profile_ids,
        "profile_limit": args.profile_limit,
        "include_medium": args.include_medium,
    }, indent=2) + "\n", args.force)
    _write_text(out_dir / ".gitignore", "renders/*.wav\n", args.force)

    print(json.dumps({
        "ok": True,
        "out_dir": str(out_dir),
        "profile_count": len(selected_profiles),
        "queue_count": len(queue),
        "selected_profile_ids": selected_profile_ids,
    }, indent=2))


if __name__ == "__main__":
    main()
