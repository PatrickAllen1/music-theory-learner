#!/usr/bin/env python3
"""
validate_technique_bank.py

Validate docs/techniques/bank.json so the production-technique layer stays
consistent before other tooling depends on it.

Examples:
    python3 als/validate_technique_bank.py
    python3 als/validate_technique_bank.py --format json
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

DEFAULT_BANK_PATH = Path("docs/techniques/bank.json")
REQUIRED_STRING_FIELDS = [
    "id",
    "name",
    "source",
    "what_it_does",
    "when_to_use",
    "why",
]
REQUIRED_LIST_FIELDS = [
    "works_well_with",
    "likely_clashes_with",
    "mitigations",
]


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate the production technique bank.")
    parser.add_argument("--bank", default=str(DEFAULT_BANK_PATH), help="Technique bank JSON path.")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="Output format.")
    return parser


def build_report(bank_path: Path) -> dict:
    payload = json.loads(bank_path.read_text())
    errors: list[str] = []
    warnings: list[str] = []
    if not isinstance(payload, list):
        return {
            "ok": False,
            "entry_count": 0,
            "errors": ["Technique bank root must be a list."],
            "warnings": [],
            "sources": {},
        }

    ids: list[str] = []
    sources: Counter[str] = Counter()
    for index, entry in enumerate(payload, start=1):
        prefix = f"entry {index}"
        if not isinstance(entry, dict):
            errors.append(f"{prefix} must be an object.")
            continue
        for field in REQUIRED_STRING_FIELDS:
            value = entry.get(field)
            if not isinstance(value, str) or not value.strip():
                errors.append(f"{prefix} missing non-empty string field `{field}`.")
        for field in REQUIRED_LIST_FIELDS:
            value = entry.get(field)
            if not isinstance(value, list) or not value:
                errors.append(f"{prefix} missing non-empty list field `{field}`.")
                continue
            if any(not isinstance(item, str) or not item.strip() for item in value):
                errors.append(f"{prefix}`{field}` must contain only non-empty strings.")
        entry_id = entry.get("id")
        if isinstance(entry_id, str) and entry_id.strip():
            ids.append(entry_id)
        source = entry.get("source")
        if isinstance(source, str) and source.strip():
            sources[source.strip()] += 1

        works = set(item.strip().lower() for item in entry.get("works_well_with", []) if isinstance(item, str))
        clashes = set(item.strip().lower() for item in entry.get("likely_clashes_with", []) if isinstance(item, str))
        overlap = sorted(works & clashes)
        if overlap:
            warnings.append(
                f"{prefix} (`{entry.get('id', '?')}`) has items in both works_well_with and likely_clashes_with: {', '.join(overlap)}"
            )

    duplicate_ids = sorted(item for item, count in Counter(ids).items() if count > 1)
    if duplicate_ids:
        errors.append(f"Duplicate technique ids: {', '.join(duplicate_ids)}")

    return {
        "ok": not errors,
        "entry_count": len(payload),
        "errors": errors,
        "warnings": warnings,
        "sources": dict(sorted(sources.items())),
    }


def render_text(report: dict) -> str:
    lines = []
    lines.append("# Technique Bank Validation")
    lines.append("")
    lines.append(f"- ok: {'yes' if report['ok'] else 'no'}")
    lines.append(f"- entries: {report['entry_count']}")
    if report["sources"]:
        lines.append("- sources:")
        for source, count in report["sources"].items():
            lines.append(f"  - {source}: {count}")
    if report["errors"]:
        lines.append("")
        lines.append("## Errors")
        for row in report["errors"]:
            lines.append(f"- {row}")
    if report["warnings"]:
        lines.append("")
        lines.append("## Warnings")
        for row in report["warnings"]:
            lines.append(f"- {row}")
    return "\n".join(lines)


def main() -> None:
    parser = make_parser()
    args = parser.parse_args()
    report = build_report(Path(args.bank))
    if args.format == "json":
        print(json.dumps(report, indent=2))
        return
    print(render_text(report), end="")


if __name__ == "__main__":
    main()
