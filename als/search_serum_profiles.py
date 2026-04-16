#!/usr/bin/env python3
"""
search_serum_profiles.py

Search the generated Serum profile catalog by role, tone, mix tags, track text,
analysis slug, wavetable refs, and mod-matrix destination modules.

Examples:
    python3 als/search_serum_profiles.py --role bass
    python3 als/search_serum_profiles.py --role pad --tone dark --mix background
    python3 als/search_serum_profiles.py --wavetable Juno --limit 10
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


DEFAULT_CATALOG_DIR = Path("als/catalog/profiles")


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Search the generated Serum profile catalog.")
    parser.add_argument("--catalog-dir", default=str(DEFAULT_CATALOG_DIR), help="Directory of generated *-profiles.json files.")
    parser.add_argument("--role", action="append", default=[], help="Required role candidate. Pass multiple times.")
    parser.add_argument("--tone", action="append", default=[], help="Required tone tag. Pass multiple times.")
    parser.add_argument("--mix", action="append", default=[], help="Required mix tag. Pass multiple times.")
    parser.add_argument("--track", help="Case-insensitive substring match against track name.")
    parser.add_argument("--analysis", help="Case-insensitive substring match against analysis slug.")
    parser.add_argument("--wavetable", action="append", default=[], help="Case-insensitive substring match against wavetable refs. Pass multiple times.")
    parser.add_argument("--dest-module", action="append", default=[], help="Case-insensitive exact/substring match against mod-matrix destination modules.")
    parser.add_argument("--limit", type=int, default=20, help="Maximum number of results. Default: 20")
    parser.add_argument("--format", choices=["json", "text"], default="text", help="Output format.")
    parser.add_argument("--summary-only", action="store_true", help="Output only the top-level summary and minimal result rows.")
    return parser


def load_profiles(catalog_dir: Path) -> list[dict]:
    profiles = []
    for path in sorted(catalog_dir.glob("*-profiles.json")):
        profiles.extend(json.loads(path.read_text()))
    return profiles


def _lower_list(values: list[str]) -> set[str]:
    return {value.lower() for value in values}


def _dest_modules(profile: dict) -> set[str]:
    modules = set()
    mod_matrix = profile.get("synthesis", {}).get("mod_matrix", {}) or {}
    for row in mod_matrix.values():
        module = row.get("dest_module")
        if isinstance(module, str) and module:
            modules.add(module.lower())
    return modules


def profile_matches(profile: dict, args: argparse.Namespace) -> bool:
    roles = _lower_list(profile["classification"]["role_candidates"])
    tones = _lower_list(profile["classification"]["tone_tags"])
    mixes = _lower_list(profile["classification"]["mix_tags"])
    wavetables = [item.lower() for item in profile["summary"]["wavetable_refs"]]
    track = (profile["source"].get("track") or "").lower()
    analysis = (profile["source"].get("analysis_slug") or "").lower()
    dest_modules = _dest_modules(profile)

    if any(role.lower() not in roles for role in args.role):
        return False
    if any(tone.lower() not in tones for tone in args.tone):
        return False
    if any(mix.lower() not in mixes for mix in args.mix):
        return False
    if args.track and args.track.lower() not in track:
        return False
    if args.analysis and args.analysis.lower() not in analysis:
        return False
    for wavetable in args.wavetable:
        needle = wavetable.lower()
        if not any(needle in ref for ref in wavetables):
            return False
    for dest_module in args.dest_module:
        needle = dest_module.lower()
        if not any(needle in module for module in dest_modules):
            return False
    return True


def score_profile(profile: dict, args: argparse.Namespace) -> int:
    score = 0
    score += len(set(map(str.lower, args.role)) & _lower_list(profile["classification"]["role_candidates"])) * 5
    score += len(set(map(str.lower, args.tone)) & _lower_list(profile["classification"]["tone_tags"])) * 3
    score += len(set(map(str.lower, args.mix)) & _lower_list(profile["classification"]["mix_tags"])) * 3
    if args.track and args.track.lower() in (profile["source"].get("track") or "").lower():
        score += 2
    if args.analysis and args.analysis.lower() in (profile["source"].get("analysis_slug") or "").lower():
        score += 2
    for wavetable in args.wavetable:
        needle = wavetable.lower()
        score += sum(1 for ref in profile["summary"]["wavetable_refs"] if needle in ref.lower())
    for dest_module in args.dest_module:
        needle = dest_module.lower()
        score += sum(1 for module in _dest_modules(profile) if needle in module)
    return score


def build_report(profiles: list[dict], args: argparse.Namespace) -> dict:
    matches = [profile for profile in profiles if profile_matches(profile, args)]
    matches.sort(key=lambda profile: (-score_profile(profile, args), profile["profile_id"]))
    matches = matches[: args.limit]
    return {
        "catalog_dir": str(Path(args.catalog_dir)),
        "total_profiles": len(profiles),
        "match_count": len(matches),
        "filters": {
            "role": args.role,
            "tone": args.tone,
            "mix": args.mix,
            "track": args.track,
            "analysis": args.analysis,
            "wavetable": args.wavetable,
            "dest_module": args.dest_module,
        },
        "results": matches,
    }


def render_text(report: dict, summary_only: bool) -> str:
    lines = []
    lines.append("# Serum Profile Search")
    lines.append("")
    lines.append(f"- catalog dir: `{report['catalog_dir']}`")
    lines.append(f"- total profiles: {report['total_profiles']}")
    lines.append(f"- matched: {report['match_count']}")
    lines.append("")
    for profile in report["results"]:
        lines.append(
            f"- `{profile['profile_id']}` :: "
            f"{profile['source'].get('track') or '-'} "
            f"[roles: {', '.join(profile['classification']['role_candidates'])}; "
            f"tone: {', '.join(profile['classification']['tone_tags'])}; "
            f"mix: {', '.join(profile['classification']['mix_tags'])}]"
        )
        if not summary_only:
            if profile["summary"]["wavetable_refs"]:
                lines.append(f"  wavetables: {', '.join(profile['summary']['wavetable_refs'])}")
            mod_modules = sorted(_dest_modules(profile))
            if mod_modules:
                lines.append(f"  mod dests: {', '.join(mod_modules)}")
            notes = profile["classification"].get("notes") or []
            if notes:
                lines.append(f"  notes: {' | '.join(notes)}")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = make_parser()
    args = parser.parse_args()
    catalog_dir = Path(args.catalog_dir)
    profiles = load_profiles(catalog_dir)
    report = build_report(profiles, args)
    if args.summary_only:
        report = {
            **report,
            "results": [
                {
                    "profile_id": profile["profile_id"],
                    "track": profile["source"].get("track"),
                    "analysis_slug": profile["source"].get("analysis_slug"),
                    "role_candidates": profile["classification"]["role_candidates"],
                    "tone_tags": profile["classification"]["tone_tags"],
                    "mix_tags": profile["classification"]["mix_tags"],
                }
                for profile in report["results"]
            ],
        }
    if args.format == "json":
        print(json.dumps(report, indent=2))
        return
    print(render_text(report, summary_only=args.summary_only), end="")


if __name__ == "__main__":
    main()
