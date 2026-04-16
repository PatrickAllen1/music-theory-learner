#!/usr/bin/env python3
"""
report_serum_vst2_alignment_progress.py

Report progress for a prepared Serum VST2 parser-alignment workpack.

Examples:
    python3 als/report_serum_vst2_alignment_progress.py --alignment-dir /tmp/serum-alignment
    python3 als/report_serum_vst2_alignment_progress.py --alignment-dir /tmp/serum-alignment --write-state
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Report progress for a Serum VST2 parser-alignment workpack.")
    parser.add_argument("--alignment-dir", required=True, help="Directory created by prepare_serum_vst2_alignment_session.py.")
    parser.add_argument("--done-target", action="append", default=[], help="Mark one or more implementation targets as done in the emitted state.")
    parser.add_argument("--reset", action="store_true", help="Ignore any existing alignment_state.json when computing progress.")
    parser.add_argument("--write-state", action="store_true", help="Write alignment_state.json in the alignment directory.")
    parser.add_argument("--summary-only", action="store_true", help="Only print counts and next target.")
    return parser


def _load_existing_done_targets(alignment_dir: Path) -> set[str]:
    state_path = alignment_dir / "alignment_state.json"
    if not state_path.exists():
        return set()
    try:
        state = json.loads(state_path.read_text())
    except Exception:
        return set()
    return {
        row["implementation_target"]
        for row in state.get("targets", [])
        if row.get("done") and row.get("implementation_target")
    }


def build_alignment_progress(
    alignment_dir: Path,
    done_targets: set[str] | None = None,
    *,
    include_existing: bool = True,
) -> dict:
    actions = json.loads((alignment_dir / "alignment_actions.json").read_text())
    done_targets = set(done_targets or set())
    if include_existing:
        done_targets.update(_load_existing_done_targets(alignment_dir))
    rows = []
    grouped = defaultdict(lambda: {"modules": [], "done": False})
    next_target = None

    for item in actions.get("implementation_targets", []):
        target = item["implementation_target"]
        done = target in done_targets
        grouped[target]["modules"] = item["modules"]
        grouped[target]["done"] = done
        rows.append({
            "implementation_target": target,
            "module_count": item["module_count"],
            "modules": item["modules"],
            "probe_ids": item["probe_ids"],
            "done": done,
        })
        if not done and next_target is None:
            next_target = {
                "implementation_target": target,
                "modules": item["modules"],
                "probe_ids": item["probe_ids"],
            }

    return {
        "state_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "alignment_dir": str(alignment_dir),
        "target_count": len(rows),
        "completed_target_count": sum(1 for row in rows if row["done"]),
        "pending_target_count": sum(1 for row in rows if not row["done"]),
        "next_target": next_target,
        "targets": rows,
    }


def main() -> None:
    parser = make_parser()
    args = parser.parse_args()
    alignment_dir = Path(args.alignment_dir)
    report = build_alignment_progress(
        alignment_dir,
        done_targets=set(args.done_target),
        include_existing=not args.reset,
    )
    if args.write_state:
        (alignment_dir / "alignment_state.json").write_text(json.dumps(report, indent=2) + "\n")
    if args.summary_only:
        report = {
            "target_count": report["target_count"],
            "completed_target_count": report["completed_target_count"],
            "pending_target_count": report["pending_target_count"],
            "next_target": report["next_target"],
        }
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
