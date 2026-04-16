#!/usr/bin/env python3
"""
prepare_serum_vst2_alignment_session.py

Prepare a parser-alignment workpack from a completed Serum VST2 postdiff run.

Examples:
    python3 als/prepare_serum_vst2_alignment_session.py --postdiff-dir /tmp/serum-postdiff --out-dir /tmp/serum-alignment
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    from report_serum_vst2_alignment_progress import build_alignment_progress
    from report_serum_vst2_alignment_actions import build_alignment_actions
    from report_serum_vst2_mapping_coverage import build_mapping_coverage_report
    from report_serum_vst2_postdiff_gaps import build_gap_report
    from render_serum_manual_bundle import DEFAULT_MANIFESTS, load_bundle
except ModuleNotFoundError:
    from .report_serum_vst2_alignment_progress import build_alignment_progress
    from .report_serum_vst2_alignment_actions import build_alignment_actions
    from .report_serum_vst2_mapping_coverage import build_mapping_coverage_report
    from .report_serum_vst2_postdiff_gaps import build_gap_report
    from .render_serum_manual_bundle import DEFAULT_MANIFESTS, load_bundle


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Prepare a Serum VST2 parser-alignment workpack.")
    parser.add_argument("--postdiff-dir", required=True, help="Directory created by run_serum_vst2_postdiff.py.")
    parser.add_argument("--out-dir", required=True, help="Output directory for the alignment workpack.")
    parser.add_argument(
        "--manifest",
        action="append",
        default=[],
        help="Optional manifest override. Pass multiple times to replace the default A-H bundle.",
    )
    parser.add_argument("--force", action="store_true", help="Overwrite existing files in the output directory.")
    return parser


def _write(path: Path, text: str, force: bool) -> None:
    if path.exists() and not force:
        raise FileExistsError(f"{path} already exists; rerun with --force to overwrite")
    path.write_text(text)


def _render_markdown(mapping: dict, gaps: dict, coverage: dict, actions: dict) -> str:
    lines = []
    lines.append("# Serum VST2 Alignment Session")
    lines.append("")
    lines.append(f"- promoted probes: {mapping.get('promoted_count', 0)}")
    lines.append(f"- parser work items: {len(mapping.get('parser_work_items', []))}")
    lines.append(f"- ready modules: {coverage.get('ready_module_count', 0)}")
    lines.append(f"- still-dark modules: {coverage.get('still_dark_module_count', 0)}")
    lines.append("")

    lines.append("## Parser Work Items")
    for item in mapping.get("parser_work_items", []):
        lines.append(
            f"- `{item['implementation_target']}` — probes: {', '.join(item['probe_ids']) or '-'}; "
            f"modules: {', '.join(item['modules']) or '-'}; "
            f"sections: {', '.join(item['manual_sections']) or '-'}"
        )
    lines.append("")

    lines.append("## Alignment Queue")
    for row in coverage.get("alignment_queue", []):
        lines.append(
            f"- `{row['module']}` — evidenced labels: {row['evidenced_uncovered_count']}; "
            f"dark labels: {row['dark_uncovered_count']}; "
            f"probes: {', '.join(row['probe_ids']) or '-'}"
        )
    lines.append("")

    lines.append("## Parser Actions")
    for item in actions.get("actions", [])[:40]:
        lines.append(
            f"- `{item['implementation_target']}` :: `{item['module']}` "
            f"(priority: {item['priority_score']}; probes: {', '.join(item['probe_ids']) or '-'})"
        )
    lines.append("")

    lines.append("## Remaining Probe Gaps")
    for item in gaps.get("unresolved", [])[:40]:
        lines.append(
            f"- `{item['probe_id']}` — {item['reason']} "
            f"(checkpoint {item['checkpoint_id']}; next action: {item.get('next_action', '-')})"
        )
    lines.append("")
    return "\n".join(lines)


def _render_alignment_queue_tsv(coverage: dict) -> str:
    rows = [[
        "module",
        "manual_section",
        "evidenced_uncovered_count",
        "dark_uncovered_count",
        "probe_ids",
        "clusters",
        "windows",
    ]]
    for row in coverage.get("alignment_queue", []):
        rows.append([
            row["module"],
            row["manual_section"],
            str(row["evidenced_uncovered_count"]),
            str(row["dark_uncovered_count"]),
            " | ".join(row["probe_ids"]),
            " | ".join(row["clusters"]),
            " | ".join(row["windows"]),
        ])
    return "\n".join("\t".join(cell.replace("\t", " ").replace("\n", " ") for cell in row) for row in rows) + "\n"


def _render_alignment_actions_tsv(actions: dict) -> str:
    rows = [[
        "implementation_target",
        "module",
        "priority_score",
        "manual_section",
        "evidenced_uncovered_count",
        "dark_uncovered_count",
        "probe_ids",
        "clusters",
        "windows",
    ]]
    for item in actions.get("actions", []):
        rows.append([
            item["implementation_target"],
            item["module"],
            str(item["priority_score"]),
            item["manual_section"],
            str(item["evidenced_uncovered_count"]),
            str(item["dark_uncovered_count"]),
            " | ".join(item["probe_ids"]),
            " | ".join(item["clusters"]),
            " | ".join(item["windows"]),
        ])
    return "\n".join("\t".join(cell.replace("\t", " ").replace("\n", " ") for cell in row) for row in rows) + "\n"


def main() -> None:
    parser = make_parser()
    args = parser.parse_args()
    postdiff_dir = Path(args.postdiff_dir)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    manifest_paths = [Path(path) for path in args.manifest] if args.manifest else DEFAULT_MANIFESTS
    bundle = load_bundle(manifest_paths)
    mapping = json.loads((postdiff_dir / "mapping.json").read_text())
    coverage_path = postdiff_dir / "mapping_coverage.json"
    if coverage_path.exists():
        coverage = json.loads(coverage_path.read_text())
    else:
        coverage = build_mapping_coverage_report(mapping)
    gaps_path = postdiff_dir / "gaps.json"
    if gaps_path.exists():
        gaps = json.loads(gaps_path.read_text())
    else:
        gaps = build_gap_report(mapping, bundle)
    actions = build_alignment_actions(mapping, coverage, gaps)

    _write(out_dir / "alignment_brief.md", _render_markdown(mapping, gaps, coverage, actions), args.force)
    _write(out_dir / "alignment_queue.tsv", _render_alignment_queue_tsv(coverage), args.force)
    _write(out_dir / "alignment_actions.tsv", _render_alignment_actions_tsv(actions), args.force)
    _write(out_dir / "mapping.json", json.dumps(mapping, indent=2) + "\n", args.force)
    _write(out_dir / "mapping_coverage.json", json.dumps(coverage, indent=2) + "\n", args.force)
    _write(out_dir / "gaps.json", json.dumps(gaps, indent=2) + "\n", args.force)
    _write(out_dir / "alignment_actions.json", json.dumps(actions, indent=2) + "\n", args.force)
    _write(out_dir / "alignment_state.json", json.dumps(build_alignment_progress(out_dir), indent=2) + "\n", args.force)

    print(json.dumps({
        "ok": True,
        "postdiff_dir": str(postdiff_dir),
        "out_dir": str(out_dir),
        "files": [
            "alignment_brief.md",
            "alignment_queue.tsv",
            "alignment_actions.tsv",
            "mapping.json",
            "mapping_coverage.json",
            "gaps.json",
            "alignment_actions.json",
            "alignment_state.json",
        ],
        "ready_module_count": coverage.get("ready_module_count", 0),
        "still_dark_module_count": coverage.get("still_dark_module_count", 0),
    }, indent=2))


if __name__ == "__main__":
    main()
