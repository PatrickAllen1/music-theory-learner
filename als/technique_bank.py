"""
technique_bank.py

Shared helpers for loading, querying, and recommending production techniques
from docs/techniques/bank.json.
"""

from __future__ import annotations

import json
import re
from pathlib import Path


DEFAULT_BANK_PATH = Path("docs/techniques/bank.json")
STOPWORDS = {
    "the", "and", "for", "with", "that", "this", "from", "into", "when", "where",
    "then", "than", "just", "over", "like", "have", "has", "too", "out", "any",
    "are", "its", "you", "your", "they", "their", "them", "not", "can", "only",
    "track", "song", "part", "layer", "lane", "use", "using",
}


def load_bank(bank_path: Path = DEFAULT_BANK_PATH) -> list[dict]:
    payload = json.loads(bank_path.read_text())
    if not isinstance(payload, list):
        raise ValueError("Technique bank root must be a list.")
    return payload


def tokens(text: str) -> set[str]:
    return {
        token
        for token in re.findall(r"[a-z0-9#\-\+]+", text.lower())
        if len(token) >= 3 and token not in STOPWORDS
    }


def entry_text(entry: dict) -> str:
    return " ".join([
        entry.get("id", ""),
        entry.get("name", ""),
        entry.get("source", ""),
        entry.get("what_it_does", ""),
        entry.get("when_to_use", ""),
        entry.get("why", ""),
        " ".join(entry.get("works_well_with", [])),
        " ".join(entry.get("likely_clashes_with", [])),
        " ".join(entry.get("mitigations", [])),
    ])


def blueprint_text(blueprint: dict) -> str:
    parts = [
        blueprint.get("description", ""),
        blueprint.get("energy_profile", ""),
        blueprint.get("drum_strategy", ""),
        blueprint.get("melodic_strategy", ""),
        " ".join(blueprint.get("arrangement_notes", [])),
        " ".join(blueprint.get("reserved_spaces", [])),
        blueprint["harmonic_plan"].get("center", ""),
        " ".join(blueprint["harmonic_plan"].get("progression", [])),
        blueprint["harmonic_plan"].get("movement_note", ""),
        blueprint["harmonic_plan"].get("bass_strategy", ""),
    ]
    for row in blueprint.get("arrangement", []):
        parts.append(row.get("section_id", ""))
        parts.append(row.get("goal", ""))
    for row in blueprint.get("sample_lanes", []):
        parts.append(row.get("slot_type", ""))
        parts.append(row.get("purpose", ""))
    for row in blueprint.get("synth_layers", []):
        parts.append(row.get("role", ""))
        parts.append(row.get("job_in_track", ""))
        parts.append(row.get("arrangement_role", ""))
        parts.extend(row.get("target_tone", []))
        parts.extend(row.get("target_mix", []))
    return " ".join(parts)


def query_report(bank: list[dict], query: str | None, source: str | None, limit: int) -> dict:
    source_query = (source or "").lower().strip()
    query_tokens = tokens(query or "")
    rows = []
    for entry in bank:
        entry_source = str(entry.get("source") or "")
        if source_query and source_query not in entry_source.lower():
            continue
        text_tokens = tokens(entry_text(entry))
        matches = sorted(query_tokens & text_tokens)
        score = len(matches)
        if query and score == 0:
            continue
        rows.append({
            "id": entry["id"],
            "name": entry["name"],
            "source": entry["source"],
            "score": score,
            "matches": matches,
            "what_it_does": entry["what_it_does"],
            "when_to_use": entry["when_to_use"],
        })
    rows.sort(key=lambda row: (-row["score"], row["name"]))
    return {
        "query": query,
        "source": source,
        "result_count": len(rows[:limit]),
        "results": rows[:limit],
    }


def recommend_for_blueprint(blueprint: dict, bank: list[dict], limit: int) -> dict:
    blueprint_tokens = tokens(blueprint_text(blueprint))
    has_low_end_roles = any(layer["role"] in {"bass", "reese", "sub"} for layer in blueprint.get("synth_layers", []))
    rows = []
    for entry in bank:
        entry_tokens = tokens(entry_text(entry))
        matches = sorted(blueprint_tokens & entry_tokens)
        score = len(matches)
        if score == 0:
            continue
        if "sound" in matches and "design" in matches:
            score += 1
        if "bass" in matches and has_low_end_roles:
            score += 1
        if "arrangement" in matches or "bars" in matches:
            score += 1
        rows.append({
            "id": entry["id"],
            "name": entry["name"],
            "source": entry["source"],
            "score": score,
            "matched_keywords": matches[:12],
            "what_it_does": entry["what_it_does"],
            "when_to_use": entry["when_to_use"],
            "works_well_with": entry["works_well_with"],
            "likely_clashes_with": entry["likely_clashes_with"],
            "mitigations": entry["mitigations"],
        })
    rows.sort(key=lambda row: (-row["score"], row["name"]))
    return {
        "brief_id": blueprint["brief_id"],
        "description": blueprint["description"],
        "result_count": len(rows[:limit]),
        "recommendations": rows[:limit],
    }
