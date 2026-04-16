#!/usr/bin/env python3
"""
find_similar_serum_profiles.py

Find similar profiles in the Serum catalog using roles, semantic tags,
wavetable overlap, and audio descriptors when present.

Examples:
    python3 als/find_similar_serum_profiles.py --profile-id mph-raw:bass:i1
    python3 als/find_similar_serum_profiles.py --profile-id mph-raw:bass:i1 --prefer-rendered --format json
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    from search_serum_profiles import load_profiles, _audio_summary
except ModuleNotFoundError:
    from .search_serum_profiles import load_profiles, _audio_summary


DEFAULT_CATALOG_DIR = Path("als/catalog/profiles")


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Find similar Serum profiles in the generated catalog.")
    parser.add_argument("--catalog-dir", default=str(DEFAULT_CATALOG_DIR), help="Directory of generated *-profiles.json files.")
    parser.add_argument("--profile-id", required=True, help="Reference profile id.")
    parser.add_argument("--limit", type=int, default=8, help="Maximum number of similar profiles to return. Default: 8")
    parser.add_argument("--prefer-rendered", action="store_true", help="Slightly prefer profiles with rendered audio summaries.")
    parser.add_argument("--format", choices=["json", "text"], default="text", help="Output format.")
    return parser


def _audio_metric(profile: dict, key: str) -> float | None:
    summary = _audio_summary(profile)
    if not summary:
        return None
    value = summary.get("summary", {}).get(key)
    return value if isinstance(value, (int, float)) else None


def _wavetable_overlap(left: dict, right: dict) -> int:
    left_refs = {row.lower() for row in left["summary"]["wavetable_refs"]}
    right_refs = {row.lower() for row in right["summary"]["wavetable_refs"]}
    return len(left_refs & right_refs)


def _metric_similarity(left: float | None, right: float | None, tolerance: float) -> float:
    if left is None or right is None:
        return 0.0
    delta = abs(left - right)
    if delta >= tolerance:
        return 0.0
    return 1.0 - (delta / tolerance)


def _score_similarity(reference: dict, candidate: dict, prefer_rendered: bool) -> tuple[float, list[str]]:
    score = 0.0
    reasons = []

    reference_roles = set(reference["classification"]["role_candidates"])
    candidate_roles = set(candidate["classification"]["role_candidates"])
    reference_tone = set(reference["classification"]["tone_tags"])
    candidate_tone = set(candidate["classification"]["tone_tags"])
    reference_mix = set(reference["classification"]["mix_tags"])
    candidate_mix = set(candidate["classification"]["mix_tags"])

    role_overlap = len(reference_roles & candidate_roles)
    if role_overlap:
        score += role_overlap * 5.0
        reasons.append("shares role tags")

    tone_overlap = len(reference_tone & candidate_tone)
    if tone_overlap:
        score += tone_overlap * 3.0
        reasons.append("shares tone tags")

    mix_overlap = len(reference_mix & candidate_mix)
    if mix_overlap:
        score += mix_overlap * 3.0
        reasons.append("shares mix tags")

    wavetable_overlap = _wavetable_overlap(reference, candidate)
    if wavetable_overlap:
        score += wavetable_overlap * 2.0
        reasons.append("shares wavetable sources")

    centroid_similarity = _metric_similarity(
        _audio_metric(reference, "mean_centroid_hz"),
        _audio_metric(candidate, "mean_centroid_hz"),
        tolerance=500.0,
    )
    if centroid_similarity > 0:
        score += centroid_similarity * 3.0
        reasons.append("close rendered centroid")

    side_similarity = _metric_similarity(
        _audio_metric(reference, "mean_side_ratio"),
        _audio_metric(candidate, "mean_side_ratio"),
        tolerance=0.4,
    )
    if side_similarity > 0:
        score += side_similarity * 2.0
        reasons.append("similar stereo spread")

    attack_similarity = _metric_similarity(
        _audio_metric(reference, "mean_attack_time_ms"),
        _audio_metric(candidate, "mean_attack_time_ms"),
        tolerance=120.0,
    )
    if attack_similarity > 0:
        score += attack_similarity * 2.0
        reasons.append("similar attack profile")

    if prefer_rendered and candidate.get("audio_reference", {}).get("status") == "rendered":
        score += 1.0
        reasons.append("rendered audio available")

    return score, reasons


def build_report(catalog_dir: Path, profile_id: str, limit: int, prefer_rendered: bool) -> dict:
    profiles = load_profiles(catalog_dir)
    by_id = {profile["profile_id"]: profile for profile in profiles}
    if profile_id not in by_id:
        raise KeyError(f"profile not found: {profile_id}")
    reference = by_id[profile_id]

    matches = []
    for candidate in profiles:
        if candidate["profile_id"] == profile_id:
            continue
        score, reasons = _score_similarity(reference, candidate, prefer_rendered)
        matches.append({
            "profile_id": candidate["profile_id"],
            "track": candidate["source"].get("track"),
            "analysis_slug": candidate["source"].get("analysis_slug"),
            "role_candidates": candidate["classification"]["role_candidates"],
            "tone_tags": candidate["classification"]["tone_tags"],
            "mix_tags": candidate["classification"]["mix_tags"],
            "audio_status": candidate.get("audio_reference", {}).get("status"),
            "audio_summary": (_audio_summary(candidate) or {}).get("summary"),
            "similarity_score": round(score, 4),
            "reasons": sorted(dict.fromkeys(reasons)),
        })
    matches.sort(key=lambda row: (-row["similarity_score"], row["profile_id"]))
    return {
        "reference": {
            "profile_id": reference["profile_id"],
            "track": reference["source"].get("track"),
            "analysis_slug": reference["source"].get("analysis_slug"),
            "role_candidates": reference["classification"]["role_candidates"],
            "tone_tags": reference["classification"]["tone_tags"],
            "mix_tags": reference["classification"]["mix_tags"],
            "audio_status": reference.get("audio_reference", {}).get("status"),
            "audio_summary": (_audio_summary(reference) or {}).get("summary"),
        },
        "prefer_rendered": prefer_rendered,
        "matches": matches[:limit],
    }


def render_text(report: dict) -> str:
    lines = []
    ref = report["reference"]
    lines.append("# Similar Serum Profiles")
    lines.append("")
    lines.append(
        f"- reference: `{ref['profile_id']}` "
        f"({ref['track'] or '-'}; roles: {', '.join(ref['role_candidates'])}; "
        f"tone: {', '.join(ref['tone_tags'])}; mix: {', '.join(ref['mix_tags'])}; "
        f"audio: {ref['audio_status']})"
    )
    lines.append(f"- prefer rendered: {'yes' if report['prefer_rendered'] else 'no'}")
    lines.append("")
    for row in report["matches"]:
        lines.append(
            f"- `{row['profile_id']}` :: score={row['similarity_score']} "
            f"({row['track'] or '-'}; roles: {', '.join(row['role_candidates'])}; "
            f"tone: {', '.join(row['tone_tags'])}; mix: {', '.join(row['mix_tags'])}; "
            f"audio: {row['audio_status']})"
        )
        if row["reasons"]:
            lines.append(f"  reasons: {' | '.join(row['reasons'])}")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = make_parser()
    args = parser.parse_args()
    report = build_report(Path(args.catalog_dir), args.profile_id, args.limit, args.prefer_rendered)
    if args.format == "json":
        print(json.dumps(report, indent=2))
        return
    print(render_text(report), end="")


if __name__ == "__main__":
    main()
