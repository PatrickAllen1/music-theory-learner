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
_AUDIO_SUMMARY_CACHE: dict[str, dict | None] = {}


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
    parser.add_argument("--rendered-only", action="store_true", help="Only return profiles with attached rendered audio summaries.")
    parser.add_argument("--min-centroid-hz", type=float, help="Minimum mean spectral centroid from attached audio summaries.")
    parser.add_argument("--max-centroid-hz", type=float, help="Maximum mean spectral centroid from attached audio summaries.")
    parser.add_argument("--min-side-ratio", type=float, help="Minimum mean stereo side ratio from attached audio summaries.")
    parser.add_argument("--max-side-ratio", type=float, help="Maximum mean stereo side ratio from attached audio summaries.")
    parser.add_argument("--min-attack-ms", type=float, help="Minimum mean attack time in milliseconds from attached audio summaries.")
    parser.add_argument("--max-attack-ms", type=float, help="Maximum mean attack time in milliseconds from attached audio summaries.")
    parser.add_argument("--min-rms-dbfs", type=float, help="Minimum mean RMS level in dBFS from attached audio summaries.")
    parser.add_argument("--max-rms-dbfs", type=float, help="Maximum mean RMS level in dBFS from attached audio summaries.")
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


def _audio_summary(profile: dict) -> dict | None:
    descriptor_path = profile.get("audio_reference", {}).get("descriptor_path")
    if not descriptor_path:
        return None
    if descriptor_path in _AUDIO_SUMMARY_CACHE:
        return _AUDIO_SUMMARY_CACHE[descriptor_path]
    path = Path(descriptor_path)
    if not path.exists():
        _AUDIO_SUMMARY_CACHE[descriptor_path] = None
        return None
    summary = json.loads(path.read_text())
    _AUDIO_SUMMARY_CACHE[descriptor_path] = summary
    return summary


def _audio_metric(profile: dict, key: str) -> float | None:
    summary = _audio_summary(profile)
    if not summary:
        return None
    value = summary.get("summary", {}).get(key)
    return value if isinstance(value, (int, float)) else None


def _within_bounds(value: float | None, lower: float | None, upper: float | None) -> bool:
    if lower is None and upper is None:
        return True
    if value is None:
        return False
    if lower is not None and value < lower:
        return False
    if upper is not None and value > upper:
        return False
    return True


def profile_matches(profile: dict, args: argparse.Namespace) -> bool:
    roles = _lower_list(profile["classification"]["role_candidates"])
    tones = _lower_list(profile["classification"]["tone_tags"])
    mixes = _lower_list(profile["classification"]["mix_tags"])
    wavetables = [item.lower() for item in profile["summary"]["wavetable_refs"]]
    track = (profile["source"].get("track") or "").lower()
    analysis = (profile["source"].get("analysis_slug") or "").lower()
    dest_modules = _dest_modules(profile)
    audio_status = profile.get("audio_reference", {}).get("status")

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
    if args.rendered_only and audio_status != "rendered":
        return False
    if not _within_bounds(_audio_metric(profile, "mean_centroid_hz"), args.min_centroid_hz, args.max_centroid_hz):
        return False
    if not _within_bounds(_audio_metric(profile, "mean_side_ratio"), args.min_side_ratio, args.max_side_ratio):
        return False
    if not _within_bounds(_audio_metric(profile, "mean_attack_time_ms"), args.min_attack_ms, args.max_attack_ms):
        return False
    if not _within_bounds(_audio_metric(profile, "mean_rms_dbfs"), args.min_rms_dbfs, args.max_rms_dbfs):
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
    if profile.get("audio_reference", {}).get("status") == "rendered":
        score += 1
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
            "rendered_only": args.rendered_only,
            "min_centroid_hz": args.min_centroid_hz,
            "max_centroid_hz": args.max_centroid_hz,
            "min_side_ratio": args.min_side_ratio,
            "max_side_ratio": args.max_side_ratio,
            "min_attack_ms": args.min_attack_ms,
            "max_attack_ms": args.max_attack_ms,
            "min_rms_dbfs": args.min_rms_dbfs,
            "max_rms_dbfs": args.max_rms_dbfs,
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
        audio_summary = _audio_summary(profile)
        if not summary_only:
            if profile["summary"]["wavetable_refs"]:
                lines.append(f"  wavetables: {', '.join(profile['summary']['wavetable_refs'])}")
            mod_modules = sorted(_dest_modules(profile))
            if mod_modules:
                lines.append(f"  mod dests: {', '.join(mod_modules)}")
            if audio_summary:
                summary = audio_summary.get("summary", {})
                lines.append(
                    "  audio: "
                    f"status={profile.get('audio_reference', {}).get('status')}; "
                    f"centroid={summary.get('mean_centroid_hz')}; "
                    f"attack_ms={summary.get('mean_attack_time_ms')}; "
                    f"side_ratio={summary.get('mean_side_ratio')}; "
                    f"rms_dbfs={summary.get('mean_rms_dbfs')}"
                )
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
                    "audio_status": profile.get("audio_reference", {}).get("status"),
                    "audio_summary": (_audio_summary(profile) or {}).get("summary"),
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
