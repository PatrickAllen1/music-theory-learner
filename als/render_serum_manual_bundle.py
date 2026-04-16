#!/usr/bin/env python3
"""
render_serum_manual_bundle.py

Render the deferred Serum VST2 manual probe manifests into one ordered bundle.

Examples:
    python3 als/render_serum_manual_bundle.py
    python3 als/render_serum_manual_bundle.py --format json
    python3 als/render_serum_manual_bundle.py --format tsv > /tmp/serum-manual-bundle.tsv
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


DEFAULT_MANIFESTS = [
    Path("als/serum-vst2-manual-probes.json"),
    Path("als/serum-vst2-expansion-probes.json"),
    Path("als/serum-vst2-phase3-probes.json"),
    Path("als/serum-vst2-phase4-probes.json"),
]


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Render the deferred Serum VST2 manual bundle.")
    parser.add_argument(
        "--manifest",
        action="append",
        default=[],
        help="Probe manifest JSON path. Pass multiple times to override the default A-H bundle.",
    )
    parser.add_argument(
        "--format",
        choices=["markdown", "json", "tsv"],
        default="markdown",
        help="Output format.",
    )
    return parser


def _basename(path: str) -> str:
    return Path(path).name if path else ""


def load_bundle(manifest_paths: list[Path]) -> dict:
    checkpoints = []
    probes = []
    for manifest_path in manifest_paths:
        manifest = json.loads(manifest_path.read_text())
        for checkpoint in manifest["checkpoints"]:
            checkpoints.append({
                "manifest_path": str(manifest_path),
                "checkpoint_id": checkpoint["id"],
                "checkpoint_title": checkpoint["title"],
                "objective": checkpoint["objective"],
            })
            for probe in checkpoint["probes"]:
                probes.append({
                    "manifest_path": str(manifest_path),
                    "checkpoint_id": checkpoint["id"],
                    "checkpoint_title": checkpoint["title"],
                    "probe_id": probe["id"],
                    "label": probe["label"],
                    "candidate_host_labels": probe.get("candidate_host_labels", []),
                    "candidate_slot_windows": probe.get("candidate_slot_windows", []),
                    "recommended_preset": probe.get("recommended_preset", ""),
                    "recommended_preset_name": _basename(probe.get("recommended_preset", "")),
                    "fallback_presets": probe.get("fallback_presets", []),
                    "fallback_preset_names": [_basename(item) for item in probe.get("fallback_presets", [])],
                    "notes": probe.get("notes", ""),
                })
    return {
        "manifest_paths": [str(path) for path in manifest_paths],
        "checkpoint_count": len(checkpoints),
        "probe_count": len(probes),
        "checkpoints": checkpoints,
        "probes": probes,
    }


def render_markdown(bundle: dict) -> str:
    lines = []
    lines.append("# Serum VST2 Manual Bundle")
    lines.append("")
    lines.append(f"- manifests: {', '.join(bundle['manifest_paths'])}")
    lines.append(f"- checkpoints: {bundle['checkpoint_count']}")
    lines.append(f"- probes: {bundle['probe_count']}")
    lines.append("")

    checkpoints = {}
    for checkpoint in bundle["checkpoints"]:
        checkpoints.setdefault(checkpoint["checkpoint_id"], checkpoint)

    probes_by_checkpoint = {}
    for probe in bundle["probes"]:
        probes_by_checkpoint.setdefault(probe["checkpoint_id"], []).append(probe)

    for checkpoint_id in sorted(probes_by_checkpoint):
        checkpoint = checkpoints[checkpoint_id]
        lines.append(f"## {checkpoint_id} — {checkpoint['checkpoint_title']}")
        lines.append(f"- objective: {checkpoint['objective']}")
        lines.append(f"- manifest: `{checkpoint['manifest_path']}`")
        for probe in probes_by_checkpoint[checkpoint_id]:
            lines.append(f"- `{probe['probe_id']}` — {probe['label']}")
            if probe["candidate_host_labels"]:
                lines.append(f"  labels: {', '.join(probe['candidate_host_labels'])}")
            if probe["candidate_slot_windows"]:
                lines.append(f"  windows: {', '.join(probe['candidate_slot_windows'])}")
            if probe["recommended_preset"]:
                lines.append(f"  recommended: `{probe['recommended_preset_name']}`")
            if probe["fallback_preset_names"]:
                lines.append(f"  fallbacks: {', '.join(f'`{name}`' for name in probe['fallback_preset_names'])}")
            if probe["notes"]:
                lines.append(f"  notes: {probe['notes']}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_tsv(bundle: dict) -> str:
    rows = [
        [
            "checkpoint_id",
            "checkpoint_title",
            "probe_id",
            "label",
            "candidate_host_labels",
            "candidate_slot_windows",
            "recommended_preset",
            "fallback_presets",
            "notes",
            "manifest_path",
        ]
    ]
    for probe in bundle["probes"]:
        rows.append([
            probe["checkpoint_id"],
            probe["checkpoint_title"],
            probe["probe_id"],
            probe["label"],
            " | ".join(probe["candidate_host_labels"]),
            " | ".join(probe["candidate_slot_windows"]),
            probe["recommended_preset"],
            " | ".join(probe["fallback_presets"]),
            probe["notes"],
            probe["manifest_path"],
        ])
    return "\n".join("\t".join(column.replace("\t", " ").replace("\n", " ") for column in row) for row in rows) + "\n"


def main() -> None:
    parser = make_parser()
    args = parser.parse_args()
    manifest_paths = [Path(path) for path in args.manifest] if args.manifest else DEFAULT_MANIFESTS
    bundle = load_bundle(manifest_paths)

    if args.format == "json":
        print(json.dumps(bundle, indent=2))
        return
    if args.format == "tsv":
        print(render_tsv(bundle), end="")
        return
    print(render_markdown(bundle), end="")


if __name__ == "__main__":
    main()
