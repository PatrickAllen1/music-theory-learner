#!/usr/bin/env python3
"""
extract_serum_host_params.py
Extract a host-facing parameter catalog from the installed Serum VST2 binary.

This is complementary to .fxp preset parsing:
- .fxp parsing tells us what a preset chunk stores
- host catalog extraction tells us what Serum exposes to the DAW / automation layer

Examples:
    python3 als/extract_serum_host_params.py
    python3 als/extract_serum_host_params.py --limit 40
    python3 als/extract_serum_host_params.py --binary '/Library/Audio/Plug-Ins/VST/Serum.vst/Contents/MacOS/Serum'
"""

import argparse
import json
import sys

from parse_serum import SERUM_VST2_PLUGIN_BINARY_PATH, extract_serum_vst2_host_param_catalog


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Extract the Serum VST2 host parameter catalog from the plugin binary.")
    parser.add_argument(
        "--binary",
        default=str(SERUM_VST2_PLUGIN_BINARY_PATH),
        help="Path to the Serum VST2 plugin binary",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="Only print the first N catalog entries",
    )
    parser.add_argument(
        "--labels-only",
        action="store_true",
        help="Print a compact label list instead of the full catalog JSON",
    )
    parser.add_argument(
        "--category",
        help="Only include labels from one category (e.g. fx, matrix, global)",
    )
    parser.add_argument(
        "--module",
        help="Only include labels from one module (e.g. fx_delay, env1_amp, global_voicing)",
    )
    return parser


def main():
    parser = make_parser()
    args = parser.parse_args()

    try:
        catalog = extract_serum_vst2_host_param_catalog(args.binary)
    except Exception as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        sys.exit(1)

    if args.category:
        category = args.category.strip()
        catalog = {
            **catalog,
            "entries": [entry for entry in catalog["entries"] if entry["category"] == category],
            "entry_count": sum(1 for entry in catalog["entries"] if entry["category"] == category),
        }

    if args.module:
        module = args.module.strip()
        catalog = {
            **catalog,
            "entries": [entry for entry in catalog["entries"] if entry["module"] == module],
            "entry_count": sum(1 for entry in catalog["entries"] if entry["module"] == module),
        }

    if args.limit > 0:
        catalog = {
            **catalog,
            "entries": catalog["entries"][:args.limit],
            "entry_count": min(catalog["entry_count"], args.limit),
        }

    if args.labels_only:
        print(json.dumps([entry["label"] for entry in catalog["entries"]], indent=2))
        return

    print(json.dumps(catalog, indent=2))


if __name__ == "__main__":
    main()
