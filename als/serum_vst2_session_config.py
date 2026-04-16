#!/usr/bin/env python3
"""
serum_vst2_session_config.py

Helpers for locking a Serum VST2 deferred-capture session to a specific
manifest/filter scope.
"""

from __future__ import annotations

import json
from pathlib import Path


SESSION_CONFIG_FILENAME = "session_config.json"


def session_dir_from_pairs_dir(pairs_dir: Path) -> Path:
    return pairs_dir.resolve().parent


def session_config_path(session_dir: Path) -> Path:
    return session_dir / SESSION_CONFIG_FILENAME


def build_session_config(
    *,
    session_dir: Path,
    pairs_dir: Path,
    manifest_paths: list[Path],
    checkpoint_ids: list[str],
    probe_ids: list[str],
) -> dict:
    return {
        "session_dir": str(session_dir.resolve()),
        "pairs_dir": str(pairs_dir.resolve()),
        "manifest_paths": [str(path) for path in manifest_paths],
        "checkpoint_ids": list(checkpoint_ids),
        "probe_ids": list(probe_ids),
    }


def write_session_config(
    *,
    session_dir: Path,
    pairs_dir: Path,
    manifest_paths: list[Path],
    checkpoint_ids: list[str],
    probe_ids: list[str],
) -> dict:
    config = build_session_config(
        session_dir=session_dir,
        pairs_dir=pairs_dir,
        manifest_paths=manifest_paths,
        checkpoint_ids=checkpoint_ids,
        probe_ids=probe_ids,
    )
    session_config_path(session_dir).write_text(json.dumps(config, indent=2) + "\n")
    return config


def load_session_config(session_dir: Path) -> dict | None:
    path = session_config_path(session_dir)
    if not path.exists():
        return None
    return json.loads(path.read_text())


def load_session_config_from_pairs_dir(pairs_dir: Path) -> dict | None:
    return load_session_config(session_dir_from_pairs_dir(pairs_dir))


def load_session_bundle(session_dir: Path) -> dict | None:
    queue_path = session_dir / "capture_queue.json"
    if not queue_path.exists():
        return None
    return json.loads(queue_path.read_text())
