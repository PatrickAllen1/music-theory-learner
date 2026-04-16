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


def _build_readme(bundle: dict, pairs_dir: Path) -> str:
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
    lines.append("")
    lines.append("## Preflight")
    lines.append("```bash")
    lines.append(f"python3 als/validate_serum_manual_bundle.py --pairs-dir {pairs_dir}")
    lines.append("```")
    lines.append("")
    lines.append("## Ingest")
    lines.append("```bash")
    lines.append(
        "python3 als/ingest_serum_manual_diff.py "
        f"--pairs-dir {pairs_dir} "
        "--manifest als/serum-vst2-manual-probes.json "
        "--manifest als/serum-vst2-expansion-probes.json "
        "--manifest als/serum-vst2-phase3-probes.json "
        "--manifest als/serum-vst2-phase4-probes.json"
    )
    lines.append("```")
    lines.append("")
    lines.append(render_markdown(bundle).rstrip())
    lines.append("")
    return "\n".join(lines) + "\n"


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

    _write_text(out_dir / "README.md", _build_readme(bundle, pairs_dir), args.force)
    _write_text(out_dir / "capture_queue.tsv", render_tsv(bundle), args.force)
    _write_text(out_dir / "capture_queue.json", json.dumps(bundle, indent=2) + "\n", args.force)
    _write_text(
        out_dir / "expected-files.txt",
        "".join(f"{probe['before_filename']}\n{probe['after_filename']}\n" for probe in bundle["probes"]),
        args.force,
    )
    _write_text(out_dir / ".gitignore", "pairs/*.fxp\n", args.force)

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
            "expected-files.txt",
            ".gitignore",
        ],
    }, indent=2))


if __name__ == "__main__":
    main()
