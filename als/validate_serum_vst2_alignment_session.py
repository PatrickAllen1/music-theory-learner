#!/usr/bin/env python3
"""
validate_serum_vst2_alignment_session.py

Validate a prepared Serum VST2 parser-alignment workpack.

Examples:
    python3 als/validate_serum_vst2_alignment_session.py --alignment-dir /tmp/serum-alignment
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


REQUIRED_FILES = [
    "alignment_brief.md",
    "alignment_queue.tsv",
    "alignment_actions.tsv",
    "alignment_actions.json",
    "mapping.json",
    "mapping_coverage.json",
    "gaps.json",
]


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate a Serum VST2 parser-alignment workpack.")
    parser.add_argument("--alignment-dir", required=True, help="Directory created by prepare_serum_vst2_alignment_session.py.")
    parser.add_argument("--write-state", action="store_true", help="If alignment_actions.json exists, emit alignment_state.json with all targets pending.")
    return parser


def main() -> None:
    parser = make_parser()
    args = parser.parse_args()
    alignment_dir = Path(args.alignment_dir)
    missing = [name for name in REQUIRED_FILES if not (alignment_dir / name).exists()]

    try:
        actions = json.loads((alignment_dir / "alignment_actions.json").read_text()) if not missing else {"implementation_targets": [], "actions": []}
    except Exception as exc:
        print(json.dumps({"ok": False, "error": str(exc)}), file=sys.stderr)
        sys.exit(1)

    state_path = None
    if args.write_state and not missing:
        try:
            from report_serum_vst2_alignment_progress import build_alignment_progress
        except ModuleNotFoundError:
            from .report_serum_vst2_alignment_progress import build_alignment_progress
        state_path = alignment_dir / "alignment_state.json"
        state_path.write_text(json.dumps(build_alignment_progress(alignment_dir), indent=2) + "\n")

    result = {
        "ok": not missing,
        "alignment_dir": str(alignment_dir),
        "missing_files": missing,
        "implementation_target_count": len(actions.get("implementation_targets", [])),
        "action_count": len(actions.get("actions", [])),
        "targets_dir_exists": (alignment_dir / "targets").exists(),
    }
    if state_path:
        result["alignment_state_path"] = str(state_path)
    print(json.dumps(result, indent=2))
    if not result["ok"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
