#!/usr/bin/env python3
"""
attach_serum_audio_descriptors.py

Attach extracted audio descriptor summaries back onto the generated Serum
profile catalog and build a catalog-level audio index.

Examples:
    python3 als/attach_serum_audio_descriptors.py --session-dir als/audio-session
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


DEFAULT_CATALOG_DIR = Path("als/catalog/profiles")
DEFAULT_AUDIO_DIR = Path("als/catalog/audio")


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Attach extracted Serum audio descriptors to the profile catalog.")
    parser.add_argument("--session-dir", required=True, help="Audio session directory containing descriptors and audio_queue.json.")
    parser.add_argument("--catalog-dir", default=str(DEFAULT_CATALOG_DIR), help="Directory of generated *-profiles.json files.")
    parser.add_argument("--audio-dir", default=str(DEFAULT_AUDIO_DIR), help="Destination directory for catalog-level audio summaries.")
    parser.add_argument("--force", action="store_true", help="Overwrite generated audio summary files.")
    return parser


def _slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-") or "unknown"


def _write_json(path: Path, payload: dict, force: bool) -> None:
    if path.exists() and not force:
        raise FileExistsError(f"{path} already exists; rerun with --force to overwrite")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n")


def _load_profile_files(catalog_dir: Path) -> list[tuple[Path, list[dict]]]:
    bundles = []
    for path in sorted(catalog_dir.glob("*-profiles.json")):
        bundles.append((path, json.loads(path.read_text())))
    return bundles


def _load_descriptor_rows(session_dir: Path) -> tuple[dict, list[dict], Path]:
    index_path = session_dir / "audio_descriptor_index.json"
    if not index_path.exists():
        raise FileNotFoundError(f"{index_path} does not exist; run extract_serum_audio_features.py first")
    index_payload = json.loads(index_path.read_text())
    descriptor_dir = Path(index_payload["descriptor_dir"])
    descriptors = []
    for path in sorted(descriptor_dir.glob("*.json")):
        descriptors.append(json.loads(path.read_text()))
    return index_payload, descriptors, descriptor_dir


def _profile_summary_rows(descriptors: list[dict]) -> dict[str, list[dict]]:
    grouped: dict[str, list[dict]] = {}
    for descriptor in descriptors:
        profile_id = descriptor.get("profile_id")
        if not profile_id:
            continue
        grouped.setdefault(profile_id, []).append(descriptor)
    return grouped


def _queue_profile_ids(session_dir: Path) -> set[str]:
    queue_path = session_dir / "audio_queue.json"
    if not queue_path.exists():
        return set()
    payload = json.loads(queue_path.read_text())
    return {row["profile_id"] for row in payload.get("queue", []) if row.get("profile_id")}


def _build_profile_audio_summary(
    profile_id: str,
    descriptors: list[dict],
    session_dir: Path,
    descriptor_dir: Path,
    summary_path: Path,
    aggregate: dict,
) -> dict:
    first = descriptors[0]
    return {
        "profile_id": profile_id,
        "analysis_slug": first.get("analysis_slug"),
        "track": first.get("track"),
        "primary_role": first.get("primary_role"),
        "session_dir": str(session_dir),
        "descriptor_count": len(descriptors),
        "render_paths": [row["render_path"] for row in descriptors],
        "auditions": [
            {
                "audition_id": row.get("audition_id"),
                "audition_label": row.get("audition_label"),
                "render_filename": row["render_filename"],
                "render_path": row["render_path"],
                "descriptor_path": str(descriptor_dir / f"{Path(row['render_filename']).stem}.json"),
                "levels": row["levels"],
                "time": row["time"],
                "spectral": row["spectral"],
                "stereo": row["stereo"],
            }
            for row in descriptors
        ],
        "summary": {
            "rendered": True,
            "summary_path": str(summary_path),
            "mean_peak_dbfs": aggregate.get("mean_peak_dbfs"),
            "mean_rms_dbfs": aggregate.get("mean_rms_dbfs"),
            "mean_centroid_hz": aggregate.get("mean_centroid_hz"),
            "mean_rolloff_hz": aggregate.get("mean_rolloff_hz"),
            "mean_side_ratio": aggregate.get("mean_side_ratio"),
            "mean_attack_time_ms": aggregate.get("mean_attack_time_ms"),
        },
    }


def main() -> None:
    parser = make_parser()
    args = parser.parse_args()
    session_dir = Path(args.session_dir)
    catalog_dir = Path(args.catalog_dir)
    audio_dir = Path(args.audio_dir)
    audio_profiles_dir = audio_dir / "profiles"

    descriptor_index, descriptors, descriptor_dir = _load_descriptor_rows(session_dir)
    grouped = _profile_summary_rows(descriptors)
    queued_profile_ids = _queue_profile_ids(session_dir)

    aggregate_by_profile = {
        row["profile_id"]: row
        for row in descriptor_index.get("profile_summaries", [])
        if row.get("profile_id")
    }
    audio_index_profiles = []
    for profile_id, rows in sorted(grouped.items()):
        summary_path = audio_profiles_dir / f"{_slugify(profile_id)}.json"
        aggregate = aggregate_by_profile.get(profile_id, {})
        payload = _build_profile_audio_summary(profile_id, rows, session_dir, descriptor_dir, summary_path, aggregate)
        _write_json(summary_path, payload, args.force)
        audio_index_profiles.append({
            "profile_id": profile_id,
            "analysis_slug": payload["analysis_slug"],
            "track": payload["track"],
            "primary_role": payload["primary_role"],
            "descriptor_count": payload["descriptor_count"],
            "mean_peak_dbfs": payload["summary"]["mean_peak_dbfs"],
            "mean_rms_dbfs": payload["summary"]["mean_rms_dbfs"],
            "mean_centroid_hz": payload["summary"]["mean_centroid_hz"],
            "mean_rolloff_hz": payload["summary"]["mean_rolloff_hz"],
            "mean_side_ratio": payload["summary"]["mean_side_ratio"],
            "mean_attack_time_ms": payload["summary"]["mean_attack_time_ms"],
            "summary_path": str(summary_path),
        })

    updated_files = 0
    rendered_profiles = set(grouped)
    for path, profiles in _load_profile_files(catalog_dir):
        changed = False
        for profile in profiles:
            profile_id = profile["profile_id"]
            audio_ref = profile.setdefault("audio_reference", {})
            if profile_id in rendered_profiles:
                summary_path = audio_profiles_dir / f"{_slugify(profile_id)}.json"
                summary_payload = json.loads(summary_path.read_text())
                audio_ref["status"] = "rendered"
                audio_ref["render_paths"] = summary_payload["render_paths"]
                audio_ref["descriptor_path"] = str(summary_path)
                changed = True
            elif profile_id in queued_profile_ids:
                if audio_ref.get("status") != "rendered":
                    audio_ref["status"] = "render_pending"
                    audio_ref["render_paths"] = []
                    audio_ref["descriptor_path"] = None
                    changed = True
        if changed:
            path.write_text(json.dumps(profiles, indent=2) + "\n")
            updated_files += 1

    audio_index = {
        "descriptor_version": descriptor_index["descriptor_version"],
        "session_dir": str(session_dir),
        "descriptor_count": descriptor_index["descriptor_count"],
        "missing_count": descriptor_index["missing_count"],
        "profile_count": len(audio_index_profiles),
        "profiles": audio_index_profiles,
        "missing_expected": descriptor_index.get("missing_expected", []),
    }
    _write_json(audio_dir / "index.json", audio_index, args.force)
    print(json.dumps({
        "ok": True,
        "session_dir": str(session_dir),
        "descriptor_count": descriptor_index["descriptor_count"],
        "profile_count": len(audio_index_profiles),
        "updated_catalog_files": updated_files,
        "audio_index": str(audio_dir / "index.json"),
    }, indent=2))


if __name__ == "__main__":
    main()
