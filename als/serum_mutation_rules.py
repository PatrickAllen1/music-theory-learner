#!/usr/bin/env python3
"""
serum_mutation_rules.py

Reusable heuristics for suggesting Serum parameter moves from normalized
profiles and high-level sound goals.
"""

from __future__ import annotations

from typing import Callable


MutationRule = dict


MUTATION_GOALS: dict[str, dict] = {
    "darker": {
        "description": "Reduce top-end brightness and move the sound backward.",
    },
    "brighter": {
        "description": "Open the sound up and increase top-end energy.",
    },
    "tighter": {
        "description": "Shorten the sound so it stays out of the way rhythmically.",
    },
    "longer_tail": {
        "description": "Increase sustain/release for a more lingering sound.",
    },
    "harder_attack": {
        "description": "Make the front edge hit faster and feel more immediate.",
    },
    "softer_attack": {
        "description": "Soften the front edge for gentler entries.",
    },
    "more_grit": {
        "description": "Add harmonic dirt or aggression.",
    },
    "cleaner": {
        "description": "Reduce harmonic dirt and harshness.",
    },
    "mono_safer": {
        "description": "Bias the sound toward center/mono stability.",
    },
    "wider": {
        "description": "Push the sound further into the sides.",
    },
    "more_motion": {
        "description": "Increase audible movement from modulation.",
    },
    "less_motion": {
        "description": "Reduce audible movement and make the sound steadier.",
    },
    "more_presence": {
        "description": "Help the sound read more clearly in the mix.",
    },
    "less_busy": {
        "description": "Reduce activity and density so other parts have room.",
    },
    "more_sub": {
        "description": "Increase low-end weight.",
    },
    "less_sub": {
        "description": "Reduce low-end weight.",
    },
}


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def find_first_filter(profile: dict) -> tuple[str, dict] | tuple[None, None]:
    filters = profile.get("synthesis", {}).get("filters", {}) or {}
    for name, row in filters.items():
        if isinstance(row, dict):
            return name, row
    return None, None


def find_env(profile: dict, env_name: str = "env_0") -> tuple[str, dict] | tuple[None, None]:
    envs = profile.get("synthesis", {}).get("envelopes", {}) or {}
    row = envs.get(env_name)
    if isinstance(row, dict):
        return env_name, row
    for name, row in envs.items():
        if isinstance(row, dict):
            return name, row
    return None, None


def find_global_param(profile: dict, key: str) -> tuple[str, float] | tuple[None, None]:
    global_row = profile.get("synthesis", {}).get("global", {}) or {}
    value = global_row.get(key)
    if isinstance(value, (int, float)):
        return key, float(value)
    return None, None


def iter_mod_routes(profile: dict):
    mod_matrix = profile.get("synthesis", {}).get("mod_matrix", {}) or {}
    for slot_name, row in mod_matrix.items():
        if isinstance(row, dict):
            yield slot_name, row


def find_mod_routes(profile: dict, *, dest_module_contains: str | None = None, dest_param_contains: str | None = None) -> list[tuple[str, dict]]:
    matches = []
    for slot_name, row in iter_mod_routes(profile):
        module = (row.get("dest_module") or "").lower()
        param = (row.get("dest_param") or "").lower()
        if dest_module_contains and dest_module_contains.lower() not in module:
            continue
        if dest_param_contains and dest_param_contains.lower() not in param:
            continue
        matches.append((slot_name, row))
    return matches


def find_low_octave_oscillators(profile: dict) -> list[tuple[str, dict]]:
    oscillators = profile.get("synthesis", {}).get("oscillators", {}) or {}
    matches = []
    for osc_name, row in oscillators.items():
        if not isinstance(row, dict):
            continue
        octave = row.get("kParamOctave")
        if isinstance(octave, (int, float)) and octave <= -1:
            matches.append((osc_name, row))
    return matches


def find_unison_keys(profile: dict) -> list[tuple[str, str, float]]:
    oscillators = profile.get("synthesis", {}).get("oscillators", {}) or {}
    hits = []
    for osc_name, row in oscillators.items():
        if not isinstance(row, dict):
            continue
        for key, value in row.items():
            if "unison" in key.lower() and isinstance(value, (int, float)):
                hits.append((osc_name, key, float(value)))
    return hits


def make_suggestion(
    *,
    goal: str,
    priority: int,
    path: str,
    action: str,
    current_value,
    suggested_value,
    rationale: str,
    section: str,
) -> dict:
    return {
        "goal": goal,
        "priority": priority,
        "section": section,
        "path": path,
        "action": action,
        "current_value": current_value,
        "suggested_value": suggested_value,
        "rationale": rationale,
    }


def suggest_for_goal(profile: dict, goal: str) -> list[dict]:
    suggestions: list[dict] = []

    filter_name, filter_row = find_first_filter(profile)
    env_name, env_row = find_env(profile)

    if goal in ("darker", "brighter") and filter_name and filter_row:
        freq = filter_row.get("kParamFreq")
        if isinstance(freq, (int, float)):
            delta = -0.08 if goal == "darker" else 0.08
            suggestions.append(make_suggestion(
                goal=goal,
                priority=100,
                section="filter",
                path=f"synthesis.filters.{filter_name}.kParamFreq",
                action="decrease" if delta < 0 else "increase",
                current_value=round(float(freq), 4),
                suggested_value=round(clamp(float(freq) + delta, 0.0, 1.0), 4),
                rationale="Main filter frequency is the fastest reliable lever for perceived brightness.",
            ))
        reso = filter_row.get("kParamReso")
        if isinstance(reso, (int, float)) and goal == "brighter":
            suggestions.append(make_suggestion(
                goal=goal,
                priority=70,
                section="filter",
                path=f"synthesis.filters.{filter_name}.kParamReso",
                action="increase",
                current_value=round(float(reso), 4),
                suggested_value=round(clamp(float(reso) + 5.0, 0.0, 100.0), 4),
                rationale="A small resonance lift can increase edge without fully changing the patch identity.",
            ))

    if goal in ("more_grit", "cleaner") and filter_name and filter_row:
        drive = filter_row.get("kParamDrive")
        if isinstance(drive, (int, float)):
            delta = 8.0 if goal == "more_grit" else -8.0
            suggestions.append(make_suggestion(
                goal=goal,
                priority=90,
                section="filter",
                path=f"synthesis.filters.{filter_name}.kParamDrive",
                action="increase" if delta > 0 else "decrease",
                current_value=round(float(drive), 4),
                suggested_value=round(clamp(float(drive) + delta, 0.0, 100.0), 4),
                rationale="Filter drive is the clearest currently-parsed harmonic dirt control in the existing profile data.",
            ))

    if goal in ("tighter", "longer_tail", "harder_attack", "softer_attack") and env_name and env_row:
        if goal == "tighter":
            for key, delta, priority in (("kParamRelease", -0.08, 100), ("kParamDecay", -0.06, 80)):
                value = env_row.get(key)
                if isinstance(value, (int, float)):
                    suggestions.append(make_suggestion(
                        goal=goal,
                        priority=priority,
                        section="envelope",
                        path=f"synthesis.envelopes.{env_name}.{key}",
                        action="decrease",
                        current_value=round(float(value), 4),
                        suggested_value=round(clamp(float(value) + delta, 0.0, 1.0), 4),
                        rationale="Shorter amp timing makes the sound occupy less rhythmic space.",
                    ))
        elif goal == "longer_tail":
            value = env_row.get("kParamRelease")
            if isinstance(value, (int, float)):
                suggestions.append(make_suggestion(
                    goal=goal,
                    priority=100,
                    section="envelope",
                    path=f"synthesis.envelopes.{env_name}.kParamRelease",
                    action="increase",
                    current_value=round(float(value), 4),
                    suggested_value=round(clamp(float(value) + 0.1, 0.0, 1.0), 4),
                    rationale="Release is the most direct tail-length control in the current profile data.",
                ))
        elif goal == "harder_attack":
            value = env_row.get("kParamAttack")
            if isinstance(value, (int, float)):
                suggestions.append(make_suggestion(
                    goal=goal,
                    priority=100,
                    section="envelope",
                    path=f"synthesis.envelopes.{env_name}.kParamAttack",
                    action="decrease",
                    current_value=round(float(value), 6),
                    suggested_value=round(clamp(float(value) - 0.02, 0.0, 1.0), 6),
                    rationale="Lower attack gives a more immediate transient and stronger perceived front edge.",
                ))
        elif goal == "softer_attack":
            value = env_row.get("kParamAttack")
            if isinstance(value, (int, float)):
                suggestions.append(make_suggestion(
                    goal=goal,
                    priority=100,
                    section="envelope",
                    path=f"synthesis.envelopes.{env_name}.kParamAttack",
                    action="increase",
                    current_value=round(float(value), 6),
                    suggested_value=round(clamp(float(value) + 0.03, 0.0, 1.0), 6),
                    rationale="Higher attack softens the leading edge and makes entries gentler.",
                ))

    if goal in ("mono_safer", "wider"):
        key, value = find_global_param(profile, "kParamMonoToggle")
        if key:
            suggestions.append(make_suggestion(
                goal=goal,
                priority=100,
                section="global",
                path=f"synthesis.global.{key}",
                action="set",
                current_value=round(value, 4),
                suggested_value=1.0 if goal == "mono_safer" else 0.0,
                rationale="Mono/poly state is the cleanest parsed global width/stability lever.",
            ))
        for osc_name, key, value in find_unison_keys(profile):
            if "blend" in key.lower() or "detune" in key.lower() or "unison" in key.lower():
                delta = -0.1 if goal == "mono_safer" else 0.1
                suggestions.append(make_suggestion(
                    goal=goal,
                    priority=60,
                    section="oscillator",
                    path=f"synthesis.oscillators.{osc_name}.{key}",
                    action="decrease" if delta < 0 else "increase",
                    current_value=round(value, 4),
                    suggested_value=round(clamp(value + delta, 0.0, 1.0 if value <= 1 else 16.0), 4),
                    rationale="Unison-style parameters often drive perceived width more than base waveform choice.",
                ))

    if goal in ("more_motion", "less_motion", "less_busy"):
        routes = find_mod_routes(profile, dest_module_contains="voicefilter") or list(iter_mod_routes(profile))
        direction = 1 if goal == "more_motion" else -1
        rationale = (
            "Increasing modulation amount should make movement more audible."
            if goal == "more_motion"
            else "Reducing modulation amount should steady the sound and free mix space."
        )
        for priority, (slot_name, row) in enumerate(routes[:3], start=1):
            amount = row.get("amount")
            if isinstance(amount, (int, float)):
                suggestions.append(make_suggestion(
                    goal=goal,
                    priority=100 - priority,
                    section="mod_matrix",
                    path=f"synthesis.mod_matrix.{slot_name}.amount",
                    action="increase" if direction > 0 else "decrease",
                    current_value=round(float(amount), 4),
                    suggested_value=round(clamp(float(amount) + direction * 12.0, -100.0, 100.0), 4),
                    rationale=rationale,
                ))
        if goal == "less_busy" and env_name and env_row:
            release = env_row.get("kParamRelease")
            if isinstance(release, (int, float)):
                suggestions.append(make_suggestion(
                    goal=goal,
                    priority=70,
                    section="envelope",
                    path=f"synthesis.envelopes.{env_name}.kParamRelease",
                    action="decrease",
                    current_value=round(float(release), 4),
                    suggested_value=round(clamp(float(release) - 0.08, 0.0, 1.0), 4),
                    rationale="Reducing release is a reliable way to reduce overlap and perceived complexity.",
                ))

    if goal in ("more_presence", "less_sub", "more_sub"):
        low_oscillators = find_low_octave_oscillators(profile)
        if goal == "more_presence" and filter_name and filter_row:
            freq = filter_row.get("kParamFreq")
            if isinstance(freq, (int, float)):
                suggestions.append(make_suggestion(
                    goal=goal,
                    priority=95,
                    section="filter",
                    path=f"synthesis.filters.{filter_name}.kParamFreq",
                    action="increase",
                    current_value=round(float(freq), 4),
                    suggested_value=round(clamp(float(freq) + 0.05, 0.0, 1.0), 4),
                    rationale="A modest filter opening is often the fastest way to improve presence without redesigning the patch.",
                ))
        for osc_name, row in low_oscillators[:2]:
            volume = row.get("kParamVolume")
            if isinstance(volume, (int, float)):
                delta = 0.08 if goal == "more_sub" else -0.08
                suggestions.append(make_suggestion(
                    goal=goal,
                    priority=85,
                    section="oscillator",
                    path=f"synthesis.oscillators.{osc_name}.kParamVolume",
                    action="increase" if delta > 0 else "decrease",
                    current_value=round(float(volume), 4),
                    suggested_value=round(clamp(float(volume) + delta, 0.0, 1.0), 4),
                    rationale="Low-octave oscillator levels are the safest currently-parsed proxy for sub weight.",
                ))
        if goal == "less_sub":
            key, value = find_global_param(profile, "kParamMasterVolume")
            if key and not suggestions:
                suggestions.append(make_suggestion(
                    goal=goal,
                    priority=40,
                    section="global",
                    path=f"synthesis.global.{key}",
                    action="decrease",
                    current_value=round(value, 4),
                    suggested_value=round(clamp(value - 0.05, 0.0, 1.0), 4),
                    rationale="Fallback gain reduction when low-frequency oscillator volume is not exposed in the current profile.",
                ))

    suggestions.sort(key=lambda row: (-row["priority"], row["path"]))
    return suggestions


def list_supported_goals() -> list[dict]:
    return [
        {"goal": goal, "description": row["description"]}
        for goal, row in sorted(MUTATION_GOALS.items())
    ]
