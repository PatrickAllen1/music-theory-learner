"""
phrase_evidence.py

Build and recommend composition phrase evidence from three sources:
- ALS analysis JSON note clips
- cleaned transcript spans
- the production technique bank

This gives the model real note/rhythm/voicing examples plus the stated intent
behind them.
"""

from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path


DEFAULT_ANALYSIS_DIR = Path("als/analysis")
DEFAULT_TRANSCRIPTS_DIR = Path("docs/transcripts")

NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
STOPWORDS = {
    "the", "and", "for", "with", "that", "this", "from", "into", "when", "where",
    "then", "than", "just", "have", "has", "your", "their", "they", "you", "use",
    "using", "song", "track", "part", "layer", "lane", "very", "more", "less",
}

SOURCE_CONFIG = {
    "mph-raw": {
        "transcript_stem": "raw_mph",
        "source_labels": {"Raw — MPH"},
    },
    "interplanetary-criminal-slow-burner": {
        "transcript_stem": "kettamainterplanetarycriminal",
        "source_labels": {"Kettama × Interplanetary Criminal"},
    },
    "sammy-virji-cops-and-robbers": {
        "transcript_stem": "sammyvirjiiguesswerenotthesame",
        "source_labels": {"I Guess We're Not the Same — Sammy Virji"},
    },
    "kettama-it-gets-better": {
        "transcript_stem": "kettamapge",
        "source_labels": {"Kettamapge"},
    },
    "subfocusjohnsummit": {
        "transcript_stem": "subfocusjohnsummit",
        "source_labels": {"Go Back — Sub Focus × John Summit"},
    },
    "bl3ss-camrinwatsin-kisses": {
        "transcript_stem": None,
        "source_labels": set(),
    },
}

ROLE_HINTS = {
    "bass": {"bass", "sub", "reese", "break bass", "mid bass", "guitar bass"},
    "hook": {"lead", "pluck", "stab", "rave lead", "trumpet", "hook", "vocal"},
    "harmony": {"pad", "string", "strings", "arp", "chord", "piano", "organ"},
    "groove": {"kick", "clap", "hat", "open hat", "snare", "tambourine", "tops", "perc", "crash"},
}

SPAN_ROLE_HINTS = {
    "bass": {"bass"},
    "hook": {"lead", "vocal"},
    "harmony": {"theory"},
    "groove": {"drums", "mix", "fx"},
    "arrangement": {"arrangement"},
}

COMPOSITION_TEXT_HINTS = {
    "note", "notes", "root", "third", "fifth", "seventh", "ninth", "interval",
    "melody", "phrase", "voicing", "progression", "rhythm", "bassline", "chord",
    "resolve", "tension", "release", "octave", "pitch", "cadence", "hook",
}

EMOTION_HINTS = {
    "dark": {"dark", "minor", "tension", "hollow", "atonal", "heavy", "grim", "phrygian"},
    "hopeful": {"hopeful", "lift", "release", "open", "add9", "maj7", "triumphant", "uplift", "resolution"},
}


def _tokens(text: str) -> set[str]:
    return {
        token
        for token in re.findall(r"[a-z0-9#\+\-]+", (text or "").lower())
        if len(token) >= 3 and token not in STOPWORDS
    }


def _note_name(pitch: int) -> str:
    octave = (pitch // 12) - 1
    return f"{NOTE_NAMES[pitch % 12]}{octave}"


def _friendly_source_label(source_slug: str) -> str:
    if source_slug in SOURCE_CONFIG and SOURCE_CONFIG[source_slug]["source_labels"]:
        return sorted(SOURCE_CONFIG[source_slug]["source_labels"])[0]
    for slug, config in SOURCE_CONFIG.items():
        if config.get("transcript_stem") == source_slug and config["source_labels"]:
            return sorted(config["source_labels"])[0]
    return source_slug.replace("-", " ").replace("_", " ")


def _group_onsets(notes: list[dict]) -> list[dict]:
    grouped: dict[float, list[dict]] = defaultdict(list)
    for note in notes:
        grouped[round(float(note["beat"]), 4)].append(note)
    out = []
    for beat in sorted(grouped):
        event_notes = sorted(grouped[beat], key=lambda row: (row["pitch"], row["dur"]))
        out.append({
            "beat": beat,
            "notes": event_notes,
            "lowest_pitch": event_notes[0]["pitch"],
            "highest_pitch": event_notes[-1]["pitch"],
            "duration": max(float(row["dur"]) for row in event_notes),
        })
    return out


def _interval_signature(onsets: list[dict], role: str) -> list[int]:
    if len(onsets) < 2:
        return []
    key = "lowest_pitch" if role in {"bass", "harmony"} else "highest_pitch"
    return [onsets[index][key] - onsets[index - 1][key] for index in range(1, min(len(onsets), 9))]


def _rhythm_signature(onsets: list[dict]) -> list[float]:
    if len(onsets) < 2:
        return []
    return [round(onsets[index]["beat"] - onsets[index - 1]["beat"], 3) for index in range(1, min(len(onsets), 9))]


def _harmony_signature(onsets: list[dict]) -> list[str]:
    signatures = []
    for onset in onsets[:4]:
        base = onset["lowest_pitch"]
        intervals = sorted({note["pitch"] - base for note in onset["notes"]})
        signatures.append("/".join(str(interval) for interval in intervals))
    return signatures


def _classify_track_role(track_name: str, polyphony_peak: int) -> str:
    lowered = (track_name or "").lower()
    for role, hints in ROLE_HINTS.items():
        if any(hint in lowered for hint in hints):
            if role == "hook" and polyphony_peak >= 3 and "piano" in lowered:
                return "harmony"
            return role
    return "harmony" if polyphony_peak >= 3 else "hook"


def _summarize_als_clip(slug: str, track_name: str, clip: dict, role: str) -> dict | None:
    notes = clip.get("notes") or []
    if len(notes) < 4:
        return None
    onsets = _group_onsets(notes)
    if len(onsets) < 2:
        return None
    note_names = [_note_name(onset["lowest_pitch"] if role in {"bass", "harmony"} else onset["highest_pitch"]) for onset in onsets[:8]]
    interval_signature = _interval_signature(onsets, role)
    rhythm_signature = _rhythm_signature(onsets)
    harmony_signature = _harmony_signature(onsets) if role == "harmony" else []
    if role == "harmony":
        summary = (
            f"{track_name} harmonic phrase in bars {clip.get('bar_start')}-{clip.get('bar_end')} with "
            f"{len(onsets)} chord onsets; first interval stacks {' | '.join(harmony_signature[:3]) or 'n/a'}."
        )
    elif role == "bass":
        summary = (
            f"{track_name} bass phrase in bars {clip.get('bar_start')}-{clip.get('bar_end')} with "
            f"note path {' -> '.join(note_names[:6])} and rhythm gaps {', '.join(str(x) for x in rhythm_signature[:5]) or 'n/a'}."
        )
    else:
        summary = (
            f"{track_name} phrase in bars {clip.get('bar_start')}-{clip.get('bar_end')} with "
            f"note path {' -> '.join(note_names[:6])} and interval moves {', '.join(str(x) for x in interval_signature[:5]) or 'n/a'}."
        )
    return {
        "kind": "als_clip",
        "source_slug": slug,
        "source": _friendly_source_label(slug),
        "role": role,
        "title": f"{track_name} :: {clip.get('name') or 'clip'}",
        "summary": summary,
        "details": {
            "track_name": track_name,
            "clip_name": clip.get("name"),
            "bar_start": clip.get("bar_start"),
            "bar_end": clip.get("bar_end"),
            "note_count": len(notes),
            "onset_count": len(onsets),
            "polyphony_peak": max(len(onset["notes"]) for onset in onsets),
            "note_path": note_names,
            "interval_signature": interval_signature,
            "rhythm_signature": rhythm_signature,
            "harmony_signature": harmony_signature,
        },
        "signals": sorted(_tokens(" ".join(note_names) + " " + track_name)),
        "emotion_hints": [],
    }


def _span_role(span: dict) -> str | None:
    tags = {tag.lower() for tag in span.get("tags", [])}
    text = (span.get("text") or "").lower()
    for role, hints in SPAN_ROLE_HINTS.items():
        if tags & hints:
            return role
    if any(keyword in text for keyword in ("bassline", "root note", "offbeat", "octave")):
        return "bass"
    if any(keyword in text for keyword in ("melody", "lead", "hook", "reply phrase", "call-and-response")):
        return "hook"
    if any(keyword in text for keyword in ("voicing", "chord", "progression", "minor 9", "maj7", "add9")):
        return "harmony"
    if any(keyword in text for keyword in ("kick", "hat", "clap", "swing", "loop", "breakbeat")):
        return "groove"
    if "bars" in text or "drop" in text or "break" in text:
        return "arrangement"
    return None


def _is_composition_span(span: dict) -> bool:
    text = span.get("text") or ""
    tokens = _tokens(text)
    return bool(tokens & COMPOSITION_TEXT_HINTS)


def _span_entries(transcripts_dir: Path) -> list[dict]:
    rows = []
    for path in sorted(transcripts_dir.glob("*_spans.json")):
        stem = path.name.replace("_spans.json", "")
        data = json.loads(path.read_text())
        for index, span in enumerate(data):
            if not _is_composition_span(span):
                continue
            role = _span_role(span)
            if role is None:
                continue
            text = span.get("text") or ""
            emotion_hints = [emotion for emotion, hints in EMOTION_HINTS.items() if _tokens(text) & hints]
            rows.append({
                "kind": "transcript_span",
                "source_slug": stem,
                "source": _friendly_source_label(stem),
                "role": role,
                "title": f"{stem} span {index + 1}",
                "summary": text,
                "details": {
                    "tags": span.get("tags", []),
                    "section": span.get("section"),
                    "id": span.get("id"),
                },
                "signals": sorted(_tokens(text)),
                "emotion_hints": emotion_hints,
            })
    return rows


def _technique_entries(bank: list[dict]) -> list[dict]:
    rows = []
    for entry in bank:
        text = " ".join([
            entry.get("name", ""),
            entry.get("what_it_does", ""),
            entry.get("when_to_use", ""),
            entry.get("why", ""),
        ])
        tokens = _tokens(text)
        if not (tokens & COMPOSITION_TEXT_HINTS):
            continue
        role = "harmony"
        if {"bass", "sub", "reese", "octave"} & tokens:
            role = "bass"
        elif {"lead", "hook", "melody", "vocal", "stab", "pluck"} & tokens:
            role = "hook"
        elif {"kick", "hat", "drum", "break", "loop", "swing"} & tokens:
            role = "groove"
        elif {"arrangement", "drop", "break", "section", "bars"} & tokens:
            role = "arrangement"
        emotion_hints = [emotion for emotion, hints in EMOTION_HINTS.items() if tokens & hints]
        rows.append({
            "kind": "technique",
            "source_slug": None,
            "source": entry.get("source", ""),
            "role": role,
            "title": entry.get("name", ""),
            "summary": entry.get("what_it_does", ""),
            "details": {
                "id": entry.get("id"),
                "when_to_use": entry.get("when_to_use"),
                "why": entry.get("why"),
            },
            "signals": sorted(tokens),
            "emotion_hints": emotion_hints,
        })
    return rows


def _als_entries(analysis_dir: Path) -> list[dict]:
    rows = []
    for path in sorted(analysis_dir.glob("*.json")):
        if path.name.endswith("-serum.json"):
            continue
        slug = path.stem
        data = json.loads(path.read_text())
        tracks = data.get("tracks") or {}
        for _, track in tracks.items():
            clips = track.get("clips") or []
            if not clips:
                continue
            track_name = track.get("name") or ""
            polyphony_peak = 1
            all_notes = []
            for clip in clips:
                all_notes.extend(clip.get("notes") or [])
            if all_notes:
                polyphony_peak = max(len(onset["notes"]) for onset in _group_onsets(all_notes))
            role = _classify_track_role(track_name, polyphony_peak)
            for clip in clips[:6]:
                entry = _summarize_als_clip(slug, track_name, clip, role)
                if entry:
                    rows.append(entry)
    return rows


def build_phrase_library(
    bank: list[dict],
    analysis_dir: Path = DEFAULT_ANALYSIS_DIR,
    transcripts_dir: Path = DEFAULT_TRANSCRIPTS_DIR,
) -> list[dict]:
    return [
        *_als_entries(analysis_dir),
        *_span_entries(transcripts_dir),
        *_technique_entries(bank),
    ]


def _blueprint_query_tokens(blueprint: dict) -> set[str]:
    parts = [
        blueprint.get("description", ""),
        blueprint.get("energy_profile", ""),
        blueprint.get("drum_strategy", ""),
        blueprint.get("melodic_strategy", ""),
        " ".join(blueprint.get("arrangement_notes", [])),
        " ".join(blueprint.get("reserved_spaces", [])),
        " ".join(blueprint.get("emotional_target", [])),
        blueprint["harmonic_plan"].get("center", ""),
        " ".join(blueprint["harmonic_plan"].get("progression", [])),
        blueprint["harmonic_plan"].get("movement_note", ""),
        blueprint["harmonic_plan"].get("bass_strategy", ""),
    ]
    for row in blueprint.get("synth_layers", []):
        parts.append(row.get("role", ""))
        parts.append(row.get("job_in_track", ""))
        parts.append(" ".join(row.get("target_tone", [])))
        parts.append(" ".join(row.get("goals", [])))
    return _tokens(" ".join(parts))


def recommend_for_blueprint(blueprint: dict, library: list[dict], limit: int = 10) -> dict:
    query_tokens = _blueprint_query_tokens(blueprint)
    emotional_target = set(blueprint.get("emotional_target", []))
    role_targets = {layer["role"] for layer in blueprint.get("synth_layers", [])}
    if any(role in role_targets for role in ("bass", "reese", "sub")):
        role_targets.add("bass")
    if any(role in role_targets for role in ("lead", "pluck", "stab")):
        role_targets.add("hook")
    if "pad" in role_targets:
        role_targets.add("harmony")

    rows = []
    for entry in library:
        signals = set(entry.get("signals", []))
        overlap = sorted(query_tokens & signals)
        score = len(overlap)
        if entry["role"] in role_targets:
            score += 2
        if entry["kind"] == "als_clip":
            score += 4
        elif entry["kind"] == "transcript_span":
            score += 3
        else:
            score -= 1
        if emotional_target and emotional_target & set(entry.get("emotion_hints", [])):
            score += 2
        if entry["role"] == "harmony" and emotional_target & {"dark", "hopeful"}:
            score += 1
        if score < 2:
            continue
        rows.append({
            "kind": entry["kind"],
            "source": entry["source"],
            "source_slug": entry.get("source_slug"),
            "role": entry["role"],
            "title": entry["title"],
            "score": score,
            "matched_keywords": overlap[:12],
            "summary": entry["summary"],
            "details": entry["details"],
            "emotion_hints": entry.get("emotion_hints", []),
        })
    rows.sort(key=lambda row: (-row["score"], row["role"], row["title"]))
    selected = []
    used_keys = set()
    kind_counts = defaultdict(int)

    def add_row(row: dict) -> None:
        key = (row["kind"], row["title"], row["source"])
        if key in used_keys:
            return
        selected.append(row)
        used_keys.add(key)
        kind_counts[row["kind"]] += 1

    preferred_roles = [role for role in ("bass", "harmony", "hook", "groove", "arrangement") if role in role_targets or role == "arrangement"]
    for role in preferred_roles:
        for kind in ("als_clip", "transcript_span", "technique"):
            candidate = next((row for row in rows if row["role"] == role and row["kind"] == kind and (row["kind"] != "technique" or kind_counts["technique"] < max(2, limit // 2))), None)
            if candidate:
                add_row(candidate)
            if len(selected) >= limit:
                break
        if len(selected) >= limit:
            break

    for row in rows:
        if len(selected) >= limit:
            break
        if row["kind"] == "technique" and kind_counts["technique"] >= max(3, limit // 2):
            continue
        add_row(row)

    selected = selected[:limit]

    grouped: dict[str, list[dict]] = defaultdict(list)
    for row in selected:
        grouped[row["role"]].append(row)

    return {
        "brief_id": blueprint["brief_id"],
        "description": blueprint["description"],
        "result_count": len(selected),
        "emotional_target": list(emotional_target),
        "recommendations": selected,
        "by_role": dict(grouped),
    }
