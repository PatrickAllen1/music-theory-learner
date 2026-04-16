#!/usr/bin/env python3
"""
prepare_serum_audio_session.py

Create a repeatable manual audio-render queue for normalized Serum profiles.

Examples:
    python3 als/prepare_serum_audio_session.py --out-dir als/audio-session
    python3 als/prepare_serum_audio_session.py --out-dir als/audio-session --role bass --limit 10
    python3 als/prepare_serum_audio_session.py --out-dir als/audio-session --profile-id mph-raw:bass:i1
"""

from __future__ import annotations

import argparse
import json
from argparse import Namespace
from pathlib import Path

try:
    from search_serum_profiles import load_profiles, profile_matches, score_profile
except ModuleNotFoundError:
    from .search_serum_profiles import load_profiles, profile_matches, score_profile


DEFAULT_CATALOG_DIR = Path("als/catalog/profiles")
DEFAULT_SPEC_PATH = Path("als/serum-audio-audition-spec.json")


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Prepare a manual Serum audio audition session.")
    parser.add_argument("--out-dir", required=True, help="Output directory for the audio session bundle.")
    parser.add_argument("--catalog-dir", default=str(DEFAULT_CATALOG_DIR), help="Directory of generated *-profiles.json files.")
    parser.add_argument("--spec", default=str(DEFAULT_SPEC_PATH), help="Audio audition spec JSON.")
    parser.add_argument("--profile-id", action="append", default=[], help="Specific profile id to include. Pass multiple times.")
    parser.add_argument("--role", action="append", default=[], help="Filter by role candidate.")
    parser.add_argument("--tone", action="append", default=[], help="Filter by tone tag.")
    parser.add_argument("--mix", action="append", default=[], help="Filter by mix tag.")
    parser.add_argument("--track", help="Case-insensitive substring match against track name.")
    parser.add_argument("--analysis", help="Case-insensitive substring match against analysis slug.")
    parser.add_argument("--limit", type=int, default=20, help="Maximum profiles to include. Default: 20")
    parser.add_argument("--force", action="store_true", help="Overwrite existing metadata files.")
    return parser


def _write_text(path: Path, content: str, force: bool) -> None:
    if path.exists() and not force:
        raise FileExistsError(f"{path} already exists; rerun with --force to overwrite")
    path.write_text(content)


def primary_role(profile: dict) -> str:
    for role in profile["classification"]["role_candidates"]:
        if role != "unknown":
            return role
    return "unknown"


def build_queue(profiles: list[dict], spec: dict) -> list[dict]:
    queue = []
    for profile in profiles:
        role = primary_role(profile)
        auditions = spec["role_sets"].get(role) or spec["role_sets"]["unknown"]
        for idx, audition in enumerate(auditions, 1):
            render_filename = f"{profile['profile_id'].replace(':', '__')}__{audition['audition_id']}.wav"
            queue.append({
                "profile_id": profile["profile_id"],
                "analysis_slug": profile["source"].get("analysis_slug"),
                "track": profile["source"].get("track"),
                "primary_role": role,
                "audition_index": idx,
                "audition_id": audition["audition_id"],
                "audition_label": audition["label"],
                "clip_bars": audition["clip_bars"],
                "notes": audition["notes"],
                "render_filename": render_filename,
            })
    return queue


def render_readme(queue: list[dict], out_dir: Path, spec_path: Path) -> str:
    lines = []
    lines.append("# Serum Audio Session")
    lines.append("")
    lines.append(f"- renders dir: `{out_dir / 'renders'}`")
    lines.append(f"- queue rows: {len(queue)}")
    lines.append(f"- spec: `{spec_path}`")
    lines.append("")
    lines.append("## Workflow")
    lines.append("1. Load the requested profile/preset in Serum.")
    lines.append("2. Create the exact MIDI clip described in `audio_queue.tsv`.")
    lines.append("3. Render or freeze/flatten the audio.")
    lines.append("4. Save the audio using the exact `render_filename` into `renders/`.")
    lines.append("5. Keep the clip clean: no extra mastering chain, no unrelated effects, no tempo-dependent rework unless the preset needs tempo sync.")
    lines.append("")
    lines.append("## Notes")
    lines.append("- This session prepares repeatable auditions only. It does not render audio itself.")
    lines.append("- The goal is to create comparable references across presets so later scripts can extract descriptors.")
    lines.append("")
    return "\n".join(lines) + "\n"


def render_tsv(queue: list[dict]) -> str:
    rows = [[
        "profile_id",
        "analysis_slug",
        "track",
        "primary_role",
        "audition_index",
        "audition_id",
        "audition_label",
        "clip_bars",
        "notes_json",
        "render_filename",
    ]]
    for row in queue:
        rows.append([
            row["profile_id"],
            row["analysis_slug"] or "",
            row["track"] or "",
            row["primary_role"],
            str(row["audition_index"]),
            row["audition_id"],
            row["audition_label"],
            str(row["clip_bars"]),
            json.dumps(row["notes"], separators=(",", ":")),
            row["render_filename"],
        ])
    return "\n".join("\t".join(cell.replace("\t", " ").replace("\n", " ") for cell in row) for row in rows) + "\n"


def main() -> None:
    parser = make_parser()
    args = parser.parse_args()
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    renders_dir = out_dir / "renders"
    renders_dir.mkdir(parents=True, exist_ok=True)

    profiles = load_profiles(Path(args.catalog_dir))
    if args.profile_id:
        wanted = set(args.profile_id)
        profiles = [profile for profile in profiles if profile["profile_id"] in wanted]
    else:
        search_args = Namespace(
            role=args.role,
            tone=args.tone,
            mix=args.mix,
            track=args.track,
            analysis=args.analysis,
            wavetable=[],
            dest_module=[],
        )
        profiles = [profile for profile in profiles if profile_matches(profile, search_args)]
        profiles.sort(key=lambda profile: (-score_profile(profile, search_args), profile["profile_id"]))
        profiles = profiles[: args.limit]

    spec_path = Path(args.spec)
    spec = json.loads(spec_path.read_text())
    queue = build_queue(profiles, spec)
    session_config = {
        "catalog_dir": str(Path(args.catalog_dir)),
        "spec_path": str(spec_path),
        "profile_ids": [profile["profile_id"] for profile in profiles],
        "filters": {
            "role": args.role,
            "tone": args.tone,
            "mix": args.mix,
            "track": args.track,
            "analysis": args.analysis,
        },
    }

    _write_text(out_dir / "README.md", render_readme(queue, out_dir, spec_path), args.force)
    _write_text(out_dir / "audio_queue.tsv", render_tsv(queue), args.force)
    _write_text(out_dir / "audio_queue.json", json.dumps({
        "spec_version": spec["spec_version"],
        "profile_count": len(profiles),
        "queue_count": len(queue),
        "queue": queue,
    }, indent=2) + "\n", args.force)
    _write_text(out_dir / "session_config.json", json.dumps(session_config, indent=2) + "\n", args.force)
    _write_text(out_dir / ".gitignore", "renders/*.wav\n", args.force)

    print(json.dumps({
        "ok": True,
        "out_dir": str(out_dir),
        "profile_count": len(profiles),
        "queue_count": len(queue),
        "files": [
            "README.md",
            "audio_queue.tsv",
            "audio_queue.json",
            "session_config.json",
            ".gitignore",
        ],
    }, indent=2))


if __name__ == "__main__":
    main()
