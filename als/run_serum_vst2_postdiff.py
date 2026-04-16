#!/usr/bin/env python3
"""
run_serum_vst2_postdiff.py

Run the full post-diff workflow for a folder of Serum VST2 manual probe pairs.
This writes the normalized ingest artifact plus a concise markdown summary.

Examples:
    python3 als/run_serum_vst2_postdiff.py --pairs-dir /tmp/serum-manual-session/pairs --out-dir /tmp/serum-postdiff
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    from ingest_serum_manual_diff import build_ingest_report
    from promote_serum_vst2_mapping import build_mapping
    from report_serum_vst2_postdiff_gaps import build_gap_report
    from render_serum_manual_bundle import DEFAULT_MANIFESTS, load_bundle
except ModuleNotFoundError:
    from .ingest_serum_manual_diff import build_ingest_report
    from .promote_serum_vst2_mapping import build_mapping
    from .report_serum_vst2_postdiff_gaps import build_gap_report
    from .render_serum_manual_bundle import DEFAULT_MANIFESTS, load_bundle


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the Serum VST2 post-diff workflow.")
    parser.add_argument("--pairs-dir", required=True, help="Directory containing <probe_id>.before/.after pairs.")
    parser.add_argument("--out-dir", required=True, help="Directory to receive ingest + summary artifacts.")
    parser.add_argument(
        "--manifest",
        action="append",
        default=[],
        help="Optional manifest override. Pass multiple times to replace the default A-H bundle.",
    )
    parser.add_argument("--checkpoint", action="append", default=[], help="Restrict the post-diff run to one or more checkpoint ids.")
    parser.add_argument("--probe", action="append", default=[], help="Restrict the post-diff run to one or more probe ids.")
    parser.add_argument(
        "--accept-status",
        action="append",
        default=["confirmed", "expected_hit"],
        help="Consensus outcome statuses to promote into mapping.json.",
    )
    parser.add_argument("--slots", type=int, default=180, help="How many float slots to diff")
    parser.add_argument("--threshold", type=float, default=0.01, help="Minimum delta threshold")
    return parser


def render_summary(report: dict) -> str:
    consensus = report["consensus"]
    lines = []
    lines.append("# Serum VST2 Post-Diff Summary")
    lines.append("")
    lines.append(f"- pairs dir: `{report['pairs_dir']}`")
    lines.append(f"- completed probes: {len(report['results'])}")
    lines.append(f"- missing probes: {len(report['missing'])}")
    lines.append(f"- status counts: {json.dumps(consensus['status_counts'], sort_keys=True)}")
    lines.append("")

    if consensus["follow_up_queue"]:
        lines.append("## Follow-Up Queue")
        for index, item in enumerate(consensus["follow_up_queue"], 1):
            windows = ", ".join(item["matched_windows"]) if item["matched_windows"] else "-"
            modules = ", ".join(item["matched_modules"]) if item["matched_modules"] else "-"
            lines.append(
                f"{index}. `{item['probe_id']}` — {item['status']} "
                f"(checkpoint {item['checkpoint']}; primary cluster: `{item['primary_cluster'] or '-'}`; "
                f"windows: {windows}; modules: {modules})"
            )
        lines.append("")

    if consensus["window_consensus"]:
        lines.append("## Window Consensus")
        for row in consensus["window_consensus"]:
            lines.append(
                f"- `{row['window']}` — probes: {row['probe_count']}; "
                f"statuses: {', '.join(row['statuses'])}; modules: {', '.join(row['modules'])}"
            )
        lines.append("")

    if consensus["cluster_consensus"]:
        lines.append("## Cluster Consensus")
        for row in consensus["cluster_consensus"][:20]:
            lines.append(
                f"- `{row['cluster']}` — probes: {row['probe_count']}; "
                f"statuses: {', '.join(row['statuses'])}; modules: {', '.join(row['modules'])}"
            )
        lines.append("")

    if report["missing"]:
        lines.append("## Missing Pairs")
        for item in report["missing"]:
            lines.append(f"- `{item['probe_id']}` — {item['reason']}")
        lines.append("")

    gaps = report.get("gaps")
    if gaps:
        lines.append("## Checkpoint Status")
        for checkpoint_id, row in gaps["checkpoint_status"].items():
            lines.append(
                f"- `{checkpoint_id}` — {row['status']} "
                f"(promoted: {row['promoted_count']}, follow-up: {row['follow_up_count']}, missing: {row['missing_count']})"
            )
        lines.append("")

    return "\n".join(lines)


def main() -> None:
    parser = make_parser()
    args = parser.parse_args()
    manifest_paths = [Path(path) for path in args.manifest] if args.manifest else DEFAULT_MANIFESTS
    checkpoint_filter = set(args.checkpoint)
    probe_filter = set(args.probe)
    selected_probe_ids = sorted({
        probe["id"]
        for manifest_path in manifest_paths
        for checkpoint in json.loads(manifest_path.read_text())["checkpoints"]
        if not checkpoint_filter or checkpoint["id"] in checkpoint_filter
        for probe in checkpoint["probes"]
        if not probe_filter or probe["id"] in probe_filter
    })
    report = build_ingest_report(
        pairs_dir=Path(args.pairs_dir),
        manifest_paths=manifest_paths,
        selected_probe_ids=selected_probe_ids,
        slots=args.slots,
        threshold=args.threshold,
    )
    mapping = build_mapping(report, set(args.accept_status))
    bundle = load_bundle(manifest_paths)
    report["gaps"] = build_gap_report(mapping, bundle)

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    ingest_path = out_dir / "ingest.json"
    mapping_path = out_dir / "mapping.json"
    gaps_path = out_dir / "gaps.json"
    summary_path = out_dir / "summary.md"
    ingest_path.write_text(json.dumps(report, indent=2) + "\n")
    mapping_path.write_text(json.dumps(mapping, indent=2) + "\n")
    gaps_path.write_text(json.dumps(report["gaps"], indent=2) + "\n")
    summary_path.write_text(render_summary(report))

    print(json.dumps({
        "ok": True,
        "out_dir": str(out_dir),
        "ingest_path": str(ingest_path),
        "mapping_path": str(mapping_path),
        "gaps_path": str(gaps_path),
        "summary_path": str(summary_path),
        "result_count": len(report["results"]),
        "missing_count": len(report["missing"]),
        "status_counts": report["consensus"]["status_counts"],
    }, indent=2))


if __name__ == "__main__":
    main()
