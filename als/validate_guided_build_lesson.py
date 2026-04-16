#!/usr/bin/env python3
"""
validate_guided_build_lesson.py

Validate a compiled guided-build lesson draft and report whether it is still a
compiler scaffold, a usable internal draft, or close to app-ready.
"""

from __future__ import annotations

import argparse
import json
import re
from argparse import Namespace
from pathlib import Path

try:
    from compile_guided_build_lesson import build_report as build_compiled_lesson_report, VAGUE_PATTERNS
except ModuleNotFoundError:
    from .compile_guided_build_lesson import build_report as build_compiled_lesson_report, VAGUE_PATTERNS


DEFAULT_CATALOG_DIR = Path("als/catalog/profiles")
DEFAULT_SERUM_BRIEFS_PATH = Path("als/serum-track-briefs.json")
DEFAULT_SONG_BRIEFS_PATH = Path("als/song-blueprint-briefs.json")
DEFAULT_TEMPLATES_PATH = Path("als/song-production-templates.json")

REQUIRED_CATEGORIES = {"ableton", "drums", "mix"}


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate a compiled guided-build lesson draft.")
    parser.add_argument("--brief", help="Song brief id from the manifest. If omitted, --lesson-json is required.")
    parser.add_argument("--lesson-json", help="Existing compiled lesson JSON to validate.")
    parser.add_argument("--song-briefs", default=str(DEFAULT_SONG_BRIEFS_PATH), help="Song-level brief manifest JSON.")
    parser.add_argument("--templates", default=str(DEFAULT_TEMPLATES_PATH), help="Song production templates JSON.")
    parser.add_argument("--catalog-dir", default=str(DEFAULT_CATALOG_DIR), help="Directory of generated *-profiles.json files.")
    parser.add_argument("--serum-briefs", default=str(DEFAULT_SERUM_BRIEFS_PATH), help="Serum brief manifest JSON.")
    parser.add_argument("--prefer-rendered", action="store_true", help="Prefer rendered profiles where available.")
    parser.add_argument("--limit-per-part", type=int, default=5, help="Max candidates to inspect per part. Default: 5")
    parser.add_argument("--mutation-limit", type=int, default=6, help="Max mutation suggestions per part. Default: 6")
    parser.add_argument("--max-swaps", type=int, default=2, help="Maximum refinement swaps to apply. Default: 2")
    parser.add_argument("--format", choices=["json", "text"], default="text", help="Output format.")
    return parser


def _compiler_namespace(args: argparse.Namespace) -> Namespace:
    return Namespace(
        brief=args.brief,
        song_briefs=args.song_briefs,
        templates=args.templates,
        catalog_dir=args.catalog_dir,
        serum_briefs=args.serum_briefs,
        prefer_rendered=args.prefer_rendered,
        limit_per_part=args.limit_per_part,
        mutation_limit=args.mutation_limit,
        max_swaps=args.max_swaps,
        format="json",
        lesson_only=False,
    )


def _category_counts(lesson: dict) -> dict:
    counts: dict[str, int] = {}
    for step in lesson.get("steps", []):
        category = step.get("category") or "unknown"
        counts[category] = counts.get(category, 0) + 1
    return counts


def _step_ids_matching(lesson: dict, pattern: str) -> list[int]:
    ids = []
    for step in lesson.get("steps", []):
        text = " ".join(str(step.get(field) or "") for field in ("title", "instruction", "why", "tip"))
        if re.search(pattern, text, flags=re.IGNORECASE):
            ids.append(step["id"])
    return ids


def build_report(args: argparse.Namespace) -> dict:
    if not args.brief and not args.lesson_json:
        raise ValueError("pass either --brief or --lesson-json")

    compiler_report = None
    if args.brief:
        compiler_report = build_compiled_lesson_report(_compiler_namespace(args))
        lesson = compiler_report["lesson"]
    else:
        lesson = json.loads(Path(args.lesson_json).read_text())

    issues = []
    warnings = []

    required_top_level = [
        "id",
        "title",
        "build_type",
        "difficulty",
        "estimated_time_mins",
        "bpm",
        "key",
        "description",
        "what_youll_learn",
        "steps",
    ]
    missing_top_level = [key for key in required_top_level if key not in lesson]
    if missing_top_level:
        issues.append(f"Missing top-level keys: {', '.join(missing_top_level)}")

    step_count = len(lesson.get("steps", []))
    if step_count < 8:
        issues.append("Lesson has too few steps to cover a full song.")
    elif step_count < 10 or step_count > 16:
        warnings.append("Lesson step count is outside the usual 10-16 step target window.")

    category_counts = _category_counts(lesson)
    missing_categories = sorted(REQUIRED_CATEGORIES - set(category_counts))
    if missing_categories:
        issues.append(f"Missing required categories: {', '.join(missing_categories)}")
    if not any(category in category_counts for category in ("bass", "chords", "melody")):
        issues.append("Lesson does not contain any music-writing categories beyond setup and mix.")

    arrangement_steps = _step_ids_matching(lesson, r"\barrange|\barrangement|\bbars?\b")
    export_steps = _step_ids_matching(lesson, r"\bexport|\bbounce|\bwav\b")
    return_steps = _step_ids_matching(lesson, r"\breturn\b|\breverb\b|\bdelay\b")
    if not arrangement_steps:
        issues.append("No arrangement-focused step was detected.")
    if not export_steps:
        issues.append("No export step was detected.")
    if not return_steps:
        warnings.append("No return/fx-routing step was detected.")

    vague_step_ids = []
    for pattern in VAGUE_PATTERNS:
        vague_step_ids.extend(_step_ids_matching(lesson, pattern))
    vague_step_ids = sorted(set(vague_step_ids))
    if vague_step_ids:
        warnings.append(f"Vague or draft-style wording appears in steps: {', '.join(str(i) for i in vague_step_ids)}")

    if compiler_report:
        if compiler_report["compiler_warnings"]:
            warnings.extend(compiler_report["compiler_warnings"])
        if compiler_report["blueprint_readiness"]["label"] == "blocked":
            issues.append("Underlying full-song blueprint is still blocked.")
        elif compiler_report["blueprint_readiness"]["label"] == "needs_work":
            warnings.append("Underlying full-song blueprint still needs work before lesson finalization.")

    warnings = list(dict.fromkeys(warnings))

    if issues:
        readiness = "blocked"
    elif warnings:
        readiness = "needs_work"
    else:
        readiness = "strong"

    return {
        "lesson_id": lesson.get("id"),
        "readiness": readiness,
        "step_count": step_count,
        "category_counts": category_counts,
        "arrangement_steps": arrangement_steps,
        "export_steps": export_steps,
        "return_steps": return_steps,
        "vague_step_ids": vague_step_ids,
        "issues": issues,
        "warnings": warnings,
    }


def render_text(report: dict) -> str:
    lines = []
    lines.append("# Guided Build Lesson Validation")
    lines.append("")
    lines.append(f"- lesson id: `{report['lesson_id']}`")
    lines.append(f"- readiness: `{report['readiness']}`")
    lines.append(f"- step count: {report['step_count']}")
    lines.append("")
    lines.append("## Categories")
    for category, count in sorted(report["category_counts"].items()):
        lines.append(f"- `{category}`: {count}")
    if report["issues"]:
        lines.append("")
        lines.append("## Issues")
        for row in report["issues"]:
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
    report = build_report(args)
    if args.format == "json":
        print(json.dumps(report, indent=2))
        return
    print(render_text(report), end="")


if __name__ == "__main__":
    main()
