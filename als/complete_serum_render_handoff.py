#!/usr/bin/env python3
"""
complete_serum_render_handoff.py

Ingest completed renders from a Serum handoff bundle, attach audio descriptors
back to the catalog, and recompute the readiness/backlog/gap reports so the
impact of the render pass is visible immediately.

Examples:
    python3 als/complete_serum_render_handoff.py --handoff-dir als/audio-session/render-handoff
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from argparse import Namespace
from pathlib import Path

try:
    from report_serum_catalog_gaps import build_report as build_catalog_gaps_report
    from report_serum_packet_readiness import build_report as build_packet_readiness_report
    from report_serum_render_backlog import build_report as build_render_backlog_report
except ModuleNotFoundError:
    from .report_serum_catalog_gaps import build_report as build_catalog_gaps_report
    from .report_serum_packet_readiness import build_report as build_packet_readiness_report
    from .report_serum_render_backlog import build_report as build_render_backlog_report


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Complete a Serum render handoff by ingesting finished renders.")
    parser.add_argument("--handoff-dir", required=True, help="Directory created by prepare_serum_render_handoff.py.")
    parser.add_argument("--catalog-dir", help="Optional override for the catalog dir.")
    parser.add_argument("--briefs", help="Optional override for the briefs path.")
    parser.add_argument("--audio-dir", help="Optional override for catalog audio output dir.")
    parser.add_argument("--force", action="store_true", help="Overwrite generated outputs.")
    return parser


def _write_json(path: Path, payload: dict, force: bool) -> None:
    if path.exists() and not force:
        raise FileExistsError(f"{path} already exists; rerun with --force to overwrite")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n")


def _write_text(path: Path, content: str, force: bool) -> None:
    if path.exists() and not force:
        raise FileExistsError(f"{path} already exists; rerun with --force to overwrite")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def _config(handoff_dir: Path, args: argparse.Namespace) -> dict:
    config_path = handoff_dir / "handoff_config.json"
    payload = _load_json(config_path) if config_path.exists() else {}
    return {
        "catalog_dir": args.catalog_dir or payload.get("catalog_dir", "als/catalog/profiles"),
        "briefs_path": args.briefs or payload.get("briefs_path", "als/serum-track-briefs.json"),
        "prefer_rendered": payload.get("prefer_rendered", False),
        "limit_per_part": payload.get("limit_per_part", 5),
        "mutation_limit": payload.get("mutation_limit", 6),
        "max_swaps": payload.get("max_swaps", 2),
        "audio_dir": args.audio_dir or str(Path(args.catalog_dir or payload.get("catalog_dir", "als/catalog/profiles")).parent / "audio"),
    }


def _shared_namespace(config: dict) -> Namespace:
    return Namespace(
        catalog_dir=config["catalog_dir"],
        briefs=config["briefs_path"],
        prefer_rendered=config["prefer_rendered"],
        limit_per_part=config["limit_per_part"],
        mutation_limit=config["mutation_limit"],
        max_swaps=config["max_swaps"],
        format="json",
    )


def _run_python(script_name: str, *extra_args: str) -> dict:
    script_path = Path(__file__).with_name(script_name)
    command = [sys.executable, str(script_path), *extra_args]
    completed = subprocess.run(command, check=True, capture_output=True, text=True)
    return json.loads(completed.stdout)


def _compare_counts(before: dict, after: dict) -> dict:
    keys = sorted(set(before) | set(after))
    return {
        key: {
            "before": before.get(key, 0),
            "after": after.get(key, 0),
            "delta": after.get(key, 0) - before.get(key, 0),
        }
        for key in keys
    }


def _readiness_delta(before: dict, after: dict) -> dict:
    before_by_brief = {row["brief_id"]: row for row in before.get("briefs", [])}
    after_by_brief = {row["brief_id"]: row for row in after.get("briefs", [])}
    rows = []
    for brief_id in sorted(set(before_by_brief) | set(after_by_brief)):
        left = before_by_brief.get(brief_id, {})
        right = after_by_brief.get(brief_id, {})
        rows.append({
            "brief_id": brief_id,
            "readiness_before": left.get("readiness"),
            "readiness_after": right.get("readiness"),
            "refined_pairwise_conflicts_before": left.get("refined_pairwise_conflicts"),
            "refined_pairwise_conflicts_after": right.get("refined_pairwise_conflicts"),
            "fallback_count_before": left.get("fallback_count"),
            "fallback_count_after": right.get("fallback_count"),
            "parts_without_mutations_before": left.get("parts_without_mutations", []),
            "parts_without_mutations_after": right.get("parts_without_mutations", []),
        })
    return {
        "readiness_counts": _compare_counts(before.get("readiness_counts", {}), after.get("readiness_counts", {})),
        "briefs": rows,
    }


def _rendered_profiles_from_index(audio_attach: dict) -> int:
    return int(audio_attach.get("profile_count", 0))


def _summary_text(summary: dict) -> str:
    lines = []
    lines.append("# Completed Serum Render Handoff")
    lines.append("")
    lines.append(f"- descriptor count: {summary['audio_extract']['descriptor_count']}")
    lines.append(f"- missing expected renders: {summary['audio_extract']['missing_count']}")
    lines.append(f"- rendered profiles attached: {_rendered_profiles_from_index(summary['audio_attach'])}")
    lines.append("")
    lines.append("## Readiness Delta")
    for key, row in summary["readiness_delta"]["readiness_counts"].items():
        lines.append(f"- `{key}`: {row['before']} -> {row['after']} (delta {row['delta']})")
    lines.append("")
    lines.append("## Briefs")
    for row in summary["readiness_delta"]["briefs"]:
        lines.append(
            f"- `{row['brief_id']}` :: readiness {row['readiness_before']} -> {row['readiness_after']}; "
            f"conflicts {row['refined_pairwise_conflicts_before']} -> {row['refined_pairwise_conflicts_after']}"
        )
    lines.append("")
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = make_parser()
    args = parser.parse_args()
    handoff_dir = Path(args.handoff_dir)
    audio_session_dir = handoff_dir / "audio-session"
    config = _config(handoff_dir, args)

    before_readiness = _load_json(handoff_dir / "packet-readiness.json") if (handoff_dir / "packet-readiness.json").exists() else build_packet_readiness_report(_shared_namespace(config))
    before_backlog = _load_json(handoff_dir / "render-backlog.json") if (handoff_dir / "render-backlog.json").exists() else build_render_backlog_report(_shared_namespace(config))
    before_gaps = _load_json(handoff_dir / "catalog-gaps.json") if (handoff_dir / "catalog-gaps.json").exists() else build_catalog_gaps_report(_shared_namespace(config))

    audio_extract = _run_python(
        "extract_serum_audio_features.py",
        "--session-dir", str(audio_session_dir),
        "--force",
    )
    audio_attach = _run_python(
        "attach_serum_audio_descriptors.py",
        "--session-dir", str(audio_session_dir),
        "--catalog-dir", config["catalog_dir"],
        "--audio-dir", config["audio_dir"],
        "--force",
    )

    namespace = _shared_namespace(config)
    after_readiness = build_packet_readiness_report(namespace)
    after_backlog = build_render_backlog_report(namespace)
    after_gaps = build_catalog_gaps_report(namespace)
    readiness_delta = _readiness_delta(before_readiness, after_readiness)

    _write_json(handoff_dir / "post-render-packet-readiness.json", after_readiness, args.force)
    _write_json(handoff_dir / "post-render-render-backlog.json", after_backlog, args.force)
    _write_json(handoff_dir / "post-render-catalog-gaps.json", after_gaps, args.force)
    _write_json(handoff_dir / "post-render-audio-extract.json", audio_extract, args.force)
    _write_json(handoff_dir / "post-render-audio-attach.json", audio_attach, args.force)
    _write_json(handoff_dir / "readiness-delta.json", readiness_delta, args.force)

    summary = {
        "handoff_dir": str(handoff_dir),
        "audio_extract": audio_extract,
        "audio_attach": audio_attach,
        "readiness_delta": readiness_delta,
        "before_files": {
            "packet_readiness": str(handoff_dir / "packet-readiness.json"),
            "render_backlog": str(handoff_dir / "render-backlog.json"),
            "catalog_gaps": str(handoff_dir / "catalog-gaps.json"),
        },
        "after_files": {
            "packet_readiness": str(handoff_dir / "post-render-packet-readiness.json"),
            "render_backlog": str(handoff_dir / "post-render-render-backlog.json"),
            "catalog_gaps": str(handoff_dir / "post-render-catalog-gaps.json"),
            "readiness_delta": str(handoff_dir / "readiness-delta.json"),
        },
    }
    _write_json(handoff_dir / "post-render-summary.json", summary, args.force)
    _write_text(handoff_dir / "post-render-summary.md", _summary_text(summary), args.force)

    print(json.dumps({
        "ok": True,
        "handoff_dir": str(handoff_dir),
        "descriptor_count": audio_extract["descriptor_count"],
        "missing_count": audio_extract["missing_count"],
        "rendered_profiles": _rendered_profiles_from_index(audio_attach),
        "files": [
            "post-render-packet-readiness.json",
            "post-render-render-backlog.json",
            "post-render-catalog-gaps.json",
            "post-render-audio-extract.json",
            "post-render-audio-attach.json",
            "readiness-delta.json",
            "post-render-summary.json",
            "post-render-summary.md",
        ],
    }, indent=2))


if __name__ == "__main__":
    main()
