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

MANIFEST_PACK_LABELS = {
    "als/serum-vst2-manual-probes.json": "primary",
    "als/serum-vst2-expansion-probes.json": "phase2",
    "als/serum-vst2-phase3-probes.json": "phase3",
    "als/serum-vst2-phase4-probes.json": "phase4",
}


def _pack_label(path: Path) -> str:
    return MANIFEST_PACK_LABELS.get(str(path), path.stem)


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
    parser.add_argument("--checkpoint", action="append", default=[], help="Restrict output to one or more checkpoint ids.")
    parser.add_argument("--probe", action="append", default=[], help="Restrict output to one or more probe ids.")
    return parser


def _basename(path: str) -> str:
    return Path(path).name if path else ""


def load_bundle(manifest_paths: list[Path]) -> dict:
    checkpoints = []
    probes = []
    checkpoint_sequence = 0
    probe_sequence = 0
    for pack_order, manifest_path in enumerate(manifest_paths, 1):
        manifest = json.loads(manifest_path.read_text())
        for checkpoint_order, checkpoint in enumerate(manifest["checkpoints"], 1):
            checkpoint_sequence += 1
            checkpoints.append({
                "manifest_path": str(manifest_path),
                "pack_order": pack_order,
                "pack_label": _pack_label(manifest_path),
                "checkpoint_sequence": checkpoint_sequence,
                "checkpoint_order": checkpoint_order,
                "checkpoint_id": checkpoint["id"],
                "checkpoint_title": checkpoint["title"],
                "objective": checkpoint["objective"],
            })
            for probe_order, probe in enumerate(checkpoint["probes"], 1):
                probe_sequence += 1
                probe_id = probe["id"]
                probes.append({
                    "manifest_path": str(manifest_path),
                    "pack_order": pack_order,
                    "pack_label": _pack_label(manifest_path),
                    "checkpoint_sequence": checkpoint_sequence,
                    "checkpoint_order": checkpoint_order,
                    "probe_sequence": probe_sequence,
                    "probe_order": probe_order,
                    "checkpoint_id": checkpoint["id"],
                    "checkpoint_title": checkpoint["title"],
                    "probe_id": probe_id,
                    "label": probe["label"],
                    "candidate_host_labels": probe.get("candidate_host_labels", []),
                    "candidate_slot_windows": probe.get("candidate_slot_windows", []),
                    "recommended_preset": probe.get("recommended_preset", ""),
                    "recommended_preset_name": _basename(probe.get("recommended_preset", "")),
                    "fallback_presets": probe.get("fallback_presets", []),
                    "fallback_preset_names": [_basename(item) for item in probe.get("fallback_presets", [])],
                    "notes": probe.get("notes", ""),
                    "before_filename": f"{probe_id}.before.fxp",
                    "after_filename": f"{probe_id}.after.fxp",
                })
    return {
        "manifest_paths": [str(path) for path in manifest_paths],
        "checkpoint_count": len(checkpoints),
        "probe_count": len(probes),
        "checkpoints": checkpoints,
        "probes": probes,
    }


def filter_bundle(
    bundle: dict,
    checkpoint_ids: list[str] | None = None,
    probe_ids: list[str] | None = None,
) -> dict:
    checkpoint_filter = set(checkpoint_ids or [])
    probe_filter = set(probe_ids or [])

    probes = []
    for probe in bundle["probes"]:
        if checkpoint_filter and probe["checkpoint_id"] not in checkpoint_filter:
            continue
        if probe_filter and probe["probe_id"] not in probe_filter:
            continue
        probes.append(probe)

    kept_checkpoints = {probe["checkpoint_id"] for probe in probes}
    checkpoints = [item for item in bundle["checkpoints"] if item["checkpoint_id"] in kept_checkpoints]
    return {
        "manifest_paths": bundle["manifest_paths"],
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
    lines.append("## Capture Queue")
    for probe in sorted(bundle["probes"], key=lambda item: item["probe_sequence"]):
        lines.append(
            f"{probe['probe_sequence']}. "
            f"[{probe['checkpoint_id']}.{probe['probe_order']}] "
            f"`{probe['probe_id']}` — {probe['label']} "
            f"(preset: `{probe['recommended_preset_name']}`; "
            f"files: `{probe['before_filename']}` / `{probe['after_filename']}`)"
        )
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
        lines.append(f"- queue: checkpoint {checkpoint['checkpoint_sequence']} of {bundle['checkpoint_count']} ({checkpoint['pack_label']} pack, position {checkpoint['checkpoint_order']})")
        lines.append(f"- objective: {checkpoint['objective']}")
        lines.append(f"- manifest: `{checkpoint['manifest_path']}`")
        for probe in probes_by_checkpoint[checkpoint_id]:
            lines.append(
                f"- step {probe['probe_sequence']} (`{probe['probe_id']}`) — {probe['label']}"
            )
            lines.append(
                f"  files: `{probe['before_filename']}` then `{probe['after_filename']}`"
            )
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
            "pack_label",
            "checkpoint_sequence",
            "probe_sequence",
            "probe_order",
            "probe_id",
            "label",
            "before_filename",
            "after_filename",
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
            probe["pack_label"],
            str(probe["checkpoint_sequence"]),
            str(probe["probe_sequence"]),
            str(probe["probe_order"]),
            probe["probe_id"],
            probe["label"],
            probe["before_filename"],
            probe["after_filename"],
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
    if args.checkpoint or args.probe:
        bundle = filter_bundle(bundle, checkpoint_ids=args.checkpoint, probe_ids=args.probe)

    if args.format == "json":
        print(json.dumps(bundle, indent=2))
        return
    if args.format == "tsv":
        print(render_tsv(bundle), end="")
        return
    print(render_markdown(bundle), end="")


if __name__ == "__main__":
    main()
