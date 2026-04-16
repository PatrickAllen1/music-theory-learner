#!/usr/bin/env python3
"""
prepare_serum_manual_session.py

Create a capture-ready Serum VST2 manual-session folder with the merged probe
bundle, queue sheets, and expected-pair filenames.

Examples:
    python3 als/prepare_serum_manual_session.py --out-dir /tmp/serum-session
    python3 als/prepare_serum_manual_session.py --out-dir /tmp/serum-session --force
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    from render_serum_manual_bundle import (
        DEFAULT_MANIFESTS,
        filter_bundle,
        load_bundle,
        render_markdown,
        render_tsv,
    )
except ModuleNotFoundError:
    from .render_serum_manual_bundle import (
        DEFAULT_MANIFESTS,
        filter_bundle,
        load_bundle,
        render_markdown,
        render_tsv,
    )
try:
    from serum_vst2_manual_plan import build_probe_subgroups
except ModuleNotFoundError:
    from .serum_vst2_manual_plan import build_probe_subgroups
try:
    from report_serum_vst2_session_progress import build_session_progress
except ModuleNotFoundError:
    from .report_serum_vst2_session_progress import build_session_progress
try:
    from serum_vst2_session_config import build_session_config
except ModuleNotFoundError:
    from .serum_vst2_session_config import build_session_config


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Prepare a capture-ready Serum VST2 manual-session folder.")
    parser.add_argument("--out-dir", required=True, help="Output directory for the session bundle.")
    parser.add_argument(
        "--manifest",
        action="append",
        default=[],
        help="Optional manifest override. Pass multiple times to replace the default A-H bundle.",
    )
    parser.add_argument("--checkpoint", action="append", default=[], help="Restrict the prepared session to one or more checkpoint ids.")
    parser.add_argument("--probe", action="append", default=[], help="Restrict the prepared session to one or more probe ids.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing metadata files in the output directory.")
    return parser


def _write_text(path: Path, content: str, force: bool) -> None:
    if path.exists() and not force:
        raise FileExistsError(f"{path} already exists; rerun with --force to overwrite")
    path.write_text(content)


def _build_readme(bundle: dict, session_dir: Path, pairs_dir: Path) -> str:
    lines = []
    lines.append("# Serum VST2 Manual Session")
    lines.append("")
    lines.append(f"- pairs dir: `{pairs_dir}`")
    lines.append(f"- probes: {bundle['probe_count']}")
    lines.append(f"- checkpoints: {bundle['checkpoint_count']}")
    lines.append("")
    lines.append("## Workflow")
    lines.append("1. Open the recommended preset for the current queue item.")
    lines.append("2. Save the untouched state as the listed `before` filename inside `pairs/`.")
    lines.append("3. Change only the target control for that probe.")
    lines.append("4. Save the edited state as the listed `after` filename inside `pairs/`.")
    lines.append("5. Move to the next queue item only after both files exist.")
    lines.append("6. For oversized probes, use `subprobe_queue.tsv` to work through the label chunks in order.")
    lines.append("")
    lines.append("## Preflight")
    lines.append("```bash")
    lines.append(f"python3 als/validate_serum_manual_bundle.py --pairs-dir {pairs_dir}")
    lines.append("```")
    lines.append("")
    lines.append("## Ingest")
    lines.append("```bash")
    lines.append(
        "python3 als/run_serum_vst2_postdiff.py "
        f"--pairs-dir {pairs_dir} "
        f"--out-dir {session_dir / 'postdiff'}"
    )
    lines.append("```")
    lines.append("")
    lines.append(render_markdown(bundle).rstrip())
    lines.append("")
    return "\n".join(lines) + "\n"


def _render_subprobe_tsv(bundle: dict) -> str:
    rows = [[
        "probe_sequence",
        "checkpoint_id",
        "probe_id",
        "subprobe_index",
        "subprobe_title",
        "label_count",
        "labels",
    ]]
    for probe in bundle["probes"]:
        subgroups = probe.get("subgroups") or build_probe_subgroups(probe)
        for index, subgroup in enumerate(subgroups, 1):
            rows.append([
                str(probe["probe_sequence"]),
                probe["checkpoint_id"],
                probe["probe_id"],
                str(index),
                subgroup["title"],
                str(len(subgroup["labels"])),
                " | ".join(subgroup["labels"]),
            ])
    return "\n".join("\t".join(cell.replace("\t", " ").replace("\n", " ") for cell in row) for row in rows) + "\n"


def main() -> None:
    parser = make_parser()
    args = parser.parse_args()

    manifest_paths = [Path(path) for path in args.manifest] if args.manifest else DEFAULT_MANIFESTS
    bundle = load_bundle(manifest_paths)
    if args.checkpoint or args.probe:
        bundle = filter_bundle(bundle, checkpoint_ids=args.checkpoint, probe_ids=args.probe)

    out_dir = Path(args.out_dir)
    pairs_dir = out_dir / "pairs"
    out_dir.mkdir(parents=True, exist_ok=True)
    pairs_dir.mkdir(parents=True, exist_ok=True)

    _write_text(out_dir / "README.md", _build_readme(bundle, out_dir, pairs_dir), args.force)
    _write_text(out_dir / "capture_queue.tsv", render_tsv(bundle), args.force)
    _write_text(out_dir / "capture_queue.json", json.dumps(bundle, indent=2) + "\n", args.force)
    _write_text(out_dir / "subprobe_queue.tsv", _render_subprobe_tsv(bundle), args.force)
    _write_text(
        out_dir / "expected-files.txt",
        "".join(f"{probe['before_filename']}\n{probe['after_filename']}\n" for probe in bundle["probes"]),
        args.force,
    )
    _write_text(out_dir / ".gitignore", "pairs/*.fxp\n", args.force)
    _write_text(
        out_dir / "session_config.json",
        json.dumps(
            build_session_config(
                session_dir=out_dir,
                pairs_dir=pairs_dir,
                manifest_paths=manifest_paths,
                checkpoint_ids=args.checkpoint,
                probe_ids=args.probe,
            ),
            indent=2,
        ) + "\n",
        args.force,
    )
    _write_text(out_dir / "session_state.json", json.dumps(build_session_progress(out_dir), indent=2) + "\n", args.force)

    print(json.dumps({
        "ok": True,
        "out_dir": str(out_dir),
        "pairs_dir": str(pairs_dir),
        "probe_count": bundle["probe_count"],
        "checkpoint_count": bundle["checkpoint_count"],
        "files": [
            "README.md",
            "capture_queue.tsv",
            "capture_queue.json",
            "subprobe_queue.tsv",
            "expected-files.txt",
            "session_config.json",
            "session_state.json",
            ".gitignore",
        ],
    }, indent=2))


if __name__ == "__main__":
    main()
