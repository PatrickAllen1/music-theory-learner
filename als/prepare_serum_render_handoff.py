#!/usr/bin/env python3
"""
prepare_serum_render_handoff.py

Create a consolidated handoff bundle for the eventual Ableton/Serum render
pass, combining the smart render backlog, catalog gaps, readiness snapshot,
and a ready-to-use audio render session.

Examples:
    python3 als/prepare_serum_render_handoff.py --out-dir als/audio-session/render-handoff
    python3 als/prepare_serum_render_handoff.py --out-dir als/audio-session/render-handoff --include-medium
"""

from __future__ import annotations

import argparse
import json
from argparse import Namespace
from pathlib import Path

try:
    from prepare_serum_audio_session import build_queue, render_readme, render_tsv
    from report_serum_catalog_gaps import build_report as build_catalog_gaps_report
    from report_serum_packet_readiness import build_report as build_packet_readiness_report
    from report_serum_render_backlog import build_report as build_render_backlog_report
    from search_serum_profiles import load_profiles
except ModuleNotFoundError:
    from .prepare_serum_audio_session import build_queue, render_readme, render_tsv
    from .report_serum_catalog_gaps import build_report as build_catalog_gaps_report
    from .report_serum_packet_readiness import build_report as build_packet_readiness_report
    from .report_serum_render_backlog import build_report as build_render_backlog_report
    from .search_serum_profiles import load_profiles


DEFAULT_CATALOG_DIR = Path("als/catalog/profiles")
DEFAULT_BRIEFS_PATH = Path("als/serum-track-briefs.json")
DEFAULT_SPEC_PATH = Path("als/serum-audio-audition-spec.json")


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Prepare a consolidated Serum render handoff bundle.")
    parser.add_argument("--out-dir", required=True, help="Output directory for the handoff bundle.")
    parser.add_argument("--catalog-dir", default=str(DEFAULT_CATALOG_DIR), help="Directory of generated *-profiles.json files.")
    parser.add_argument("--briefs", default=str(DEFAULT_BRIEFS_PATH), help="Track brief manifest JSON.")
    parser.add_argument("--spec", default=str(DEFAULT_SPEC_PATH), help="Audio audition spec JSON.")
    parser.add_argument("--prefer-rendered", action="store_true", help="Prefer rendered profiles where available during ranking.")
    parser.add_argument("--limit-per-part", type=int, default=5, help="Max candidates to inspect per part. Default: 5")
    parser.add_argument("--mutation-limit", type=int, default=6, help="Max mutation suggestions per part. Default: 6")
    parser.add_argument("--max-swaps", type=int, default=2, help="Maximum refinement swaps to apply. Default: 2")
    parser.add_argument("--profile-limit", type=int, default=6, help="Maximum number of profiles to include in the handoff. Default: 6")
    parser.add_argument("--include-medium", action="store_true", help="Include medium-priority backlog entries after high-priority ones.")
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


def _render_targets(backlog: dict, include_medium: bool, profile_limit: int) -> list[dict]:
    allowed = {"high"}
    if include_medium:
        allowed.add("medium")
    return [row for row in backlog["backlog"] if row["priority"] in allowed][:profile_limit]


def _render_targets_tsv(rows: list[dict]) -> str:
    header = [
        "profile_id",
        "track",
        "analysis_slug",
        "priority",
        "score",
        "selection_count",
        "reasons",
        "briefs",
    ]
    lines = ["\t".join(header)]
    for row in rows:
        briefs = " | ".join(
            f"{item['brief_id']}:{item['part_id']}({item['constraint_mode']},conflicts={item['conflict_count']},mutations={item['mutation_suggestion_count']})"
            for item in row["briefs"]
        )
        lines.append("\t".join([
            row["profile_id"],
            row.get("track") or "",
            row.get("analysis_slug") or "",
            row["priority"],
            str(row["score"]),
            str(row["selection_count"]),
            " | ".join(row["reasons"]),
            briefs,
        ]))
    return "\n".join(lines) + "\n"


def _handoff_readme(out_dir: Path, targets: list[dict], backlog: dict, gaps: dict, readiness: dict, spec_path: Path) -> str:
    lines = []
    lines.append("# Serum Render Handoff")
    lines.append("")
    lines.append("This bundle is the prepared handoff for the future Ableton/Serum render pass.")
    lines.append("")
    lines.append("## What To Render First")
    lines.append(f"- selected profiles: {len(targets)}")
    lines.append(f"- spec: `{spec_path}`")
    lines.append(f"- renders dir: `{out_dir / 'audio-session' / 'renders'}`")
    lines.append("")
    lines.append("## Why These Profiles")
    lines.append(f"- backlog profiles tracked: {backlog['profile_count']}")
    lines.append(f"- catalog gaps tracked: {gaps['gap_count']}")
    lines.append(f"- packet readiness snapshot: {json.dumps(readiness['readiness_counts'], sort_keys=True)}")
    lines.append("")
    lines.append("## Workflow")
    lines.append("1. Open `render_targets.tsv` and work from the top row down.")
    lines.append("2. Use `audio-session/audio_queue.tsv` for the exact clips and filenames.")
    lines.append("3. Render the WAV files into `audio-session/renders/` with the exact filenames.")
    lines.append("4. Later, run the existing audio-feature attachment workflow on that session.")
    lines.append("")
    lines.append("## Files")
    lines.append("- `render_targets.tsv`: ranked profiles and why they matter")
    lines.append("- `render-backlog.json`: detailed backlog scoring")
    lines.append("- `catalog-gaps.json`: current underserved sound targets")
    lines.append("- `packet-readiness.json`: raw/refined packet readiness snapshot")
    lines.append("- `audio-session/`: ready-to-use render queue")
    lines.append("")
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = make_parser()
    args = parser.parse_args()
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    namespace = _shared_namespace(args)
    backlog = build_render_backlog_report(namespace)
    gaps = build_catalog_gaps_report(namespace)
    readiness = build_packet_readiness_report(namespace)
    targets = _render_targets(backlog, args.include_medium, args.profile_limit)
    selected_profile_ids = [row["profile_id"] for row in targets]

    profiles = load_profiles(Path(args.catalog_dir))
    by_id = {profile["profile_id"]: profile for profile in profiles}
    selected_profiles = [by_id[profile_id] for profile_id in selected_profile_ids if profile_id in by_id]

    spec_path = Path(args.spec)
    spec = json.loads(spec_path.read_text())
    queue = build_queue(selected_profiles, spec)

    audio_dir = out_dir / "audio-session"
    audio_dir.mkdir(parents=True, exist_ok=True)
    renders_dir = audio_dir / "renders"
    renders_dir.mkdir(parents=True, exist_ok=True)

    _write_text(out_dir / "README.md", _handoff_readme(out_dir, targets, backlog, gaps, readiness, spec_path), args.force)
    _write_text(out_dir / "render_targets.tsv", _render_targets_tsv(targets), args.force)
    _write_text(out_dir / "render-backlog.json", json.dumps(backlog, indent=2) + "\n", args.force)
    _write_text(out_dir / "catalog-gaps.json", json.dumps(gaps, indent=2) + "\n", args.force)
    _write_text(out_dir / "packet-readiness.json", json.dumps(readiness, indent=2) + "\n", args.force)

    _write_text(audio_dir / "README.md", render_readme(queue, audio_dir, spec_path), args.force)
    _write_text(audio_dir / "audio_queue.tsv", render_tsv(queue), args.force)
    _write_text(audio_dir / "audio_queue.json", json.dumps({
        "spec_version": spec["spec_version"],
        "profile_count": len(selected_profiles),
        "queue_count": len(queue),
        "queue": queue,
        "selected_profile_ids": selected_profile_ids,
    }, indent=2) + "\n", args.force)
    _write_text(audio_dir / "session_config.json", json.dumps({
        "catalog_dir": str(Path(args.catalog_dir)),
        "briefs_path": str(Path(args.briefs)),
        "spec_path": str(spec_path),
        "profile_ids": selected_profile_ids,
        "profile_limit": args.profile_limit,
        "include_medium": args.include_medium,
    }, indent=2) + "\n", args.force)
    _write_text(audio_dir / ".gitignore", "renders/*.wav\n", args.force)

    print(json.dumps({
        "ok": True,
        "out_dir": str(out_dir),
        "profile_count": len(selected_profiles),
        "queue_count": len(queue),
        "selected_profile_ids": selected_profile_ids,
        "files": [
            "README.md",
            "render_targets.tsv",
            "render-backlog.json",
            "catalog-gaps.json",
            "packet-readiness.json",
            "audio-session/",
        ],
    }, indent=2))


if __name__ == "__main__":
    main()
