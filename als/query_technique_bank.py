#!/usr/bin/env python3
"""
query_technique_bank.py

Search the production technique bank by free text or source so it can be used
as part of day-to-day authoring work.

Examples:
    python3 als/query_technique_bank.py --q "pitch bend lead"
    python3 als/query_technique_bank.py --source "Raw — MPH"
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    from technique_bank import DEFAULT_BANK_PATH, load_bank, query_report
except ModuleNotFoundError:
    from .technique_bank import DEFAULT_BANK_PATH, load_bank, query_report


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Search the production technique bank.")
    parser.add_argument("--bank", default=str(DEFAULT_BANK_PATH), help="Technique bank JSON path.")
    parser.add_argument("--q", help="Free-text query.")
    parser.add_argument("--source", help="Filter by source substring.")
    parser.add_argument("--limit", type=int, default=10, help="Maximum rows to return. Default: 10")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="Output format.")
    return parser

def build_report(bank_path: Path, query: str | None, source: str | None, limit: int) -> dict:
    return query_report(load_bank(bank_path), query, source, limit)


def render_text(report: dict) -> str:
    lines = []
    lines.append("# Technique Query")
    lines.append("")
    lines.append(f"- query: {report['query'] or '-'}")
    lines.append(f"- source: {report['source'] or '-'}")
    lines.append(f"- results: {report['result_count']}")
    lines.append("")
    for row in report["results"]:
        lines.append(f"- `{row['id']}` :: {row['name']} [{row['source']}] score={row['score']}")
        if row["matches"]:
            lines.append(f"  matches: {', '.join(row['matches'])}")
        lines.append(f"  does: {row['what_it_does']}")
        lines.append(f"  when: {row['when_to_use']}")
    return "\n".join(lines)


def main() -> None:
    parser = make_parser()
    args = parser.parse_args()
    report = build_report(Path(args.bank), args.q, args.source, args.limit)
    if args.format == "json":
        print(json.dumps(report, indent=2))
        return
    print(render_text(report), end="")


if __name__ == "__main__":
    main()
