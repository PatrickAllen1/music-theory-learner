#!/usr/bin/env python3
"""
report_serum_vst2_session_progress.py

Report progress for a prepared Serum VST2 manual capture session and optionally
write/update a session_state.json file.

Examples:
    python3 als/report_serum_vst2_session_progress.py --session-dir /tmp/serum-manual-session
    python3 als/report_serum_vst2_session_progress.py --session-dir /tmp/serum-manual-session --write-state
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Report progress for a prepared Serum VST2 manual capture session.")
    parser.add_argument("--session-dir", required=True, help="Directory created by prepare_serum_manual_session.py.")
    parser.add_argument("--write-state", action="store_true", help="Write or update session_state.json in the session directory.")
    parser.add_argument("--summary-only", action="store_true", help="Only print counts and next probe.")
    return parser


def _file_meta(path: Path) -> dict:
    stat = path.stat()
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    return {
        "size": stat.st_size,
        "mtime": datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat(),
        "sha256": digest,
    }


def build_session_progress(session_dir: Path) -> dict:
    bundle = json.loads((session_dir / "capture_queue.json").read_text())
    pairs_dir = session_dir / "pairs"

    probes = []
    by_checkpoint = defaultdict(lambda: {
        "probe_count": 0,
        "completed_count": 0,
        "pending_count": 0,
        "completed": [],
        "pending": [],
    })

    next_probe = None
    completed_probe_ids = []

    for probe in bundle["probes"]:
        before_exists = (pairs_dir / probe["before_filename"]).exists()
        after_exists = (pairs_dir / probe["after_filename"]).exists()
        before_meta = _file_meta(pairs_dir / probe["before_filename"]) if before_exists else None
        after_meta = _file_meta(pairs_dir / probe["after_filename"]) if after_exists else None
        integrity_warnings = []
        if before_meta and before_meta["size"] == 0:
            integrity_warnings.append("before_empty")
        if after_meta and after_meta["size"] == 0:
            integrity_warnings.append("after_empty")
        if before_meta and after_meta and before_meta["sha256"] == after_meta["sha256"]:
            integrity_warnings.append("identical_hash")
        captured = before_exists and after_exists
        complete = captured and not integrity_warnings
        state = {
            "probe_id": probe["probe_id"],
            "checkpoint_id": probe["checkpoint_id"],
            "label": probe["label"],
            "probe_sequence": probe["probe_sequence"],
            "before_filename": probe["before_filename"],
            "after_filename": probe["after_filename"],
            "before_exists": before_exists,
            "after_exists": after_exists,
            "before_meta": before_meta,
            "after_meta": after_meta,
            "captured": captured,
            "complete": complete,
            "integrity_warnings": integrity_warnings,
        }
        probes.append(state)
        row = by_checkpoint[probe["checkpoint_id"]]
        row["probe_count"] += 1
        if complete:
            row["completed_count"] += 1
            row["completed"].append(probe["probe_id"])
            completed_probe_ids.append(probe["probe_id"])
        else:
            row["pending_count"] += 1
            row["pending"].append(probe["probe_id"])
            if next_probe is None:
                next_probe = {
                    "probe_id": probe["probe_id"],
                    "checkpoint_id": probe["checkpoint_id"],
                    "label": probe["label"],
                    "probe_sequence": probe["probe_sequence"],
                }

    checkpoint_progress = {}
    for checkpoint_id, row in sorted(by_checkpoint.items()):
        checkpoint_progress[checkpoint_id] = {
            **row,
            "status": "complete" if row["pending_count"] == 0 else "in_progress" if row["completed_count"] else "not_started",
        }

    integrity_warning_count = sum(len(item["integrity_warnings"]) for item in probes)
    return {
        "state_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "session_dir": str(session_dir),
        "pairs_dir": str(pairs_dir),
        "probe_count": len(bundle["probes"]),
        "completed_probe_count": len(completed_probe_ids),
        "pending_probe_count": len(bundle["probes"]) - len(completed_probe_ids),
        "integrity_warning_count": integrity_warning_count,
        "completed_probe_ids": completed_probe_ids,
        "next_probe": next_probe,
        "checkpoint_progress": checkpoint_progress,
        "probes": probes,
    }


def main() -> None:
    parser = make_parser()
    args = parser.parse_args()
    session_dir = Path(args.session_dir)
    report = build_session_progress(session_dir)
    if args.write_state:
        (session_dir / "session_state.json").write_text(json.dumps(report, indent=2) + "\n")
    if args.summary_only:
        report = {
            "probe_count": report["probe_count"],
            "completed_probe_count": report["completed_probe_count"],
            "pending_probe_count": report["pending_probe_count"],
            "integrity_warning_count": report["integrity_warning_count"],
            "next_probe": report["next_probe"],
            "checkpoint_progress": report["checkpoint_progress"],
        }
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
