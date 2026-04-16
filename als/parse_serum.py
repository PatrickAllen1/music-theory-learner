#!/usr/bin/env python3
"""
parse_serum.py
Extracts Serum VST state from Ableton Live Set (.als) files.

Handles two Serum variants:
  - Serum_x64 / Serum (VST2): zlib-compressed binary chunk
    → Extracts wavetable names + parameter floats (approx. labels)
  - Serum 2 (VST3): XferJson + Zstandard + CBOR
    → Fully named parameters (Oscillator, Filter, Env, LFO, ModSlot, etc.)
    → Wavetable paths from WTOsc subsections
    → Full mod routing: source name + destination module/param

Usage:
    python3 parse_serum.py                          # all 5 ALS files
    python3 parse_serum.py kettama-it-gets-better   # one file

Output: prints JSON and writes als/analysis/<slug>-serum.json
"""

import gzip
import json
import re
import struct
import sys
import zlib
from pathlib import Path

try:
    import zstandard
except ImportError:
    zstandard = None

try:
    import cbor2
except ImportError:
    cbor2 = None

ALS_DIR = Path(__file__).parent
ANALYSIS_DIR = ALS_DIR / "analysis"

# ---------------------------------------------------------------------------
# Serum parameter map for VST2 binary format (Serum_x64 / Serum)
# Parameters start at byte 13408 in the decompressed chunk.
# Ordering derived from community documentation and binary comparison.
# Confidence: H=confirmed, M=inferred, L=guess
#
# Values are normalized 0.0–1.0 unless noted.
# For bipolar params (octave, semi, fine, pan): 0.5 = centre.
# ---------------------------------------------------------------------------
SERUM_V2_PARAM_OFFSET = 13408  # bytes into decompressed VST2 chunk

# Format: (index, key, label, confidence, decoder_hint)
# decoder_hint: None=raw, "bipolar3"=(-3 to +3), "bipolar12"=(-12 to +12),
#               "bipolar100"=(-100 to +100 cents), "voice_count"=(1-16)
SERUM_VST2_PARAMS = [
    # --- OSC A --- index 0 = first float at SERUM_V2_PARAM_OFFSET ---
    (0,  "osc_a_level",       "OSC A Level",          "M", None),
    (1,  "osc_a_detune",      "OSC A Unison Detune",  "M", None),
    (2,  "osc_a_pan",         "OSC A Pan",            "M", "bipolar1"),
    (3,  "osc_a_wtpos",       "OSC A WT Position",    "M", None),
    (4,  "osc_a_oct",         "OSC A Octave",         "M", "bipolar3"),
    (5,  "osc_a_semi",        "OSC A Semitone",       "M", "bipolar12"),
    (6,  "osc_a_uni_voices",  "OSC A Unison Voices",  "M", "voice_count"),
    (7,  "osc_a_uni_blend",   "OSC A Unison Blend",   "L", None),
    (8,  "osc_a_phase",       "OSC A Phase",          "L", None),
    # --- OSC B ---
    (9,  "osc_b_level",       "OSC B Level",          "M", None),
    (10, "osc_b_detune",      "OSC B Unison Detune",  "M", None),
    (11, "osc_b_pan",         "OSC B Pan",            "M", "bipolar1"),
    (12, "osc_b_wtpos",       "OSC B WT Position",    "M", None),
    (13, "osc_b_oct",         "OSC B Octave",         "M", "bipolar3"),
    (14, "osc_b_semi",        "OSC B Semitone",       "M", "bipolar12"),
    (15, "osc_b_uni_voices",  "OSC B Unison Voices",  "M", "voice_count"),
    (16, "osc_b_uni_blend",   "OSC B Unison Blend",   "L", None),
    # --- Sub + Noise ---
    (17, "sub_level",         "Sub Level",            "L", None),
    (18, "noise_level",       "Noise Level",          "L", None),
    # --- Filter ---
    (19, "flt_cutoff",        "Filter Cutoff",        "M", None),
    (20, "flt_res",           "Filter Resonance",     "M", None),
    (21, "flt_drive",         "Filter Drive",         "L", None),
    (22, "flt_pan",           "Filter Pan",           "L", "bipolar1"),
    (23, "flt_mix",           "Filter Mix",           "L", None),
    # --- Env 1 (Amp) ---
    (24, "env1_attack",       "Env1 Attack",          "M", None),
    (25, "env1_decay",        "Env1 Decay",           "M", None),
    (26, "env1_sustain",      "Env1 Sustain",         "M", None),
    (27, "env1_release",      "Env1 Release",         "M", None),
    # --- Env 2 ---
    (28, "env2_attack",       "Env2 Attack",          "M", None),
    (29, "env2_decay",        "Env2 Decay",           "M", None),
    (30, "env2_sustain",      "Env2 Sustain",         "M", None),
    (31, "env2_release",      "Env2 Release",         "M", None),
    # --- LFO 1 ---
    (32, "lfo1_rate",         "LFO1 Rate",            "L", None),
    (33, "lfo1_attack",       "LFO1 Attack",          "L", None),
]

SERUM_VST2_PARAM_BY_INDEX = {
    idx: {
        "key": key,
        "label": label,
        "confidence": conf,
        "decoder_hint": hint,
    }
    for idx, key, label, conf, hint in SERUM_VST2_PARAMS
}

# Safe host-label aliases for the currently-decoded VST2 preset fields.
# These describe which Serum host-facing controls we already cover, but do not
# imply a direct float-slot index match to the host automation parameter order.
SERUM_VST2_KEY_TO_HOST_LABEL = {
    "osc_a_level": "A Vol",
    "osc_a_detune": "A UniDet",
    "osc_a_pan": "A Pan",
    "osc_a_wtpos": "A WTPos",
    "osc_a_oct": "A Octave",
    "osc_a_semi": "A Semi",
    "osc_a_uni_voices": "A Unison",
    "osc_a_uni_blend": "A UniBlend",
    "osc_b_level": "B Vol",
    "osc_b_detune": "B UniDet",
    "osc_b_pan": "B Pan",
    "osc_b_wtpos": "B WTPos",
    "osc_b_oct": "B Octave",
    "osc_b_semi": "B Semi",
    "osc_b_uni_voices": "B Unison",
    "osc_b_uni_blend": "B UniBlend",
    "sub_level": "Sub Osc Level",
    "noise_level": "Noise Oscillator Level",
    "flt_cutoff": "Fil Cutoff",
    "flt_res": "Fil Reso",
    "flt_drive": "Fil Drive",
    "flt_mix": "Fil Mix",
    "env1_attack": "Amp Atk",
    "env1_decay": "Amp Dec",
    "env1_sustain": "Amp Sus",
    "env1_release": "Amp Rel",
    "env2_attack": "Env2 Atk",
    "env2_decay": "Env2 Dec",
    "env2_sustain": "Env2 Sus",
    "env2_release": "Env2 Rel",
    "lfo1_rate": "LFO1Rate",
}
SERUM_VST2_EMBEDDED_TEXT_TO_HOST_LABEL = {
    "macro_1": "Macro 1",
    "macro_2": "Macro 2",
    "macro_3": "Macro 3",
    "macro_4": "Macro 4",
}

SERUM_VST2_TEXT_PREFIXES = ("KJHEGICH",)
SERUM_VST2_TEXT_REGIONS = {
    "embedded_preset_name": (18784, 18848),
    "embedded_vendor": (18848, 18896),
    "embedded_bank": (18896, 18928),
    "macro_1": (19024, 19064),
    "macro_2": (19064, 19096),
    "macro_3": (19096, 19128),
    "macro_4": (19128, 19160),
}
SERUM_VST2_PLUGIN_BINARY_PATH = Path("/Library/Audio/Plug-Ins/VST/Serum.vst/Contents/MacOS/Serum")
SERUM_VST2_HOST_PARAM_CATALOG_START = "Master Volume"
SERUM_VST2_HOST_PARAM_CATALOG_STOP = "FFT Table Edit"

# ---------------------------------------------------------------------------
# Serum 2 mod source type ID → human-readable label
# Based on CBOR structure analysis. IDs 0-13 are confident (Env/LFO in order).
# IDs 14+ are inferred from observed routing patterns (labeled "?").
# ---------------------------------------------------------------------------
SERUM2_SOURCE_NAMES = {
    0: "Env1", 1: "Env2", 2: "Env3", 3: "Env4",
    4: "LFO1", 5: "LFO2", 6: "LFO3", 7: "LFO4",
    8: "LFO5", 9: "LFO6", 10: "LFO7", 11: "LFO8",
    12: "LFO9", 13: "LFO10",
    14: "Macro1?", 15: "Macro2?", 16: "Macro3?", 17: "Macro4?",
    18: "Macro5?", 19: "Macro6?", 20: "Macro7?", 21: "Macro8?",
    22: "Note?", 23: "Velocity?", 24: "Aftertouch?",
    25: "ModWheel?", 26: "PitchBend?",
    27: "Random?", 28: "KeyTrack?", 29: "Gate?",
}


def decode_param(raw_val, hint):
    """Convert normalized float to human-readable value."""
    if raw_val is None:
        return None
    if hint == "bipolar1":
        return round(raw_val * 2 - 1, 3)
    if hint == "bipolar3":
        return round((raw_val - 0.5) * 6, 2)
    if hint == "bipolar12":
        return round((raw_val - 0.5) * 24, 1)
    if hint == "bipolar100":
        return round((raw_val - 0.5) * 200, 1)
    if hint == "voice_count":
        return max(1, round(raw_val * 16))
    return round(raw_val, 4)


def _clean_vst2_text(text: str) -> str:
    """Normalize embedded printable text extracted from a VST2 chunk."""
    cleaned = text.strip().strip("\x00")
    for prefix in SERUM_VST2_TEXT_PREFIXES:
        if cleaned.startswith(prefix):
            cleaned = cleaned[len(prefix):].strip()
    return cleaned


def extract_printable_strings(data: bytes, min_length=4, start_offset=0, end_offset=None, max_results=None):
    """Extract printable ASCII strings with offsets from a byte buffer."""
    if min_length < 1:
        raise ValueError("min_length must be >= 1")

    if end_offset is None or end_offset > len(data):
        end_offset = len(data)
    if start_offset < 0 or start_offset > end_offset:
        raise ValueError("invalid printable string scan range")

    pattern = rb"[\x20-\x7e]{%d,}" % min_length
    matches = []
    for match in re.finditer(pattern, data[start_offset:end_offset]):
        text = match.group().decode("ascii", errors="replace")
        matches.append({
            "offset": start_offset + match.start(),
            "length": len(text),
            "text": text,
        })
        if max_results is not None and len(matches) >= max_results:
            break
    return matches


def _extract_best_printable_string(data: bytes, start: int, end: int) -> str:
    """Return the longest printable string inside a bounded region."""
    candidates = extract_printable_strings(
        data,
        min_length=1,
        start_offset=start,
        end_offset=end,
    )
    if not candidates:
        return ""

    cleaned_candidates = []
    for candidate in candidates:
        cleaned = _clean_vst2_text(candidate["text"])
        if cleaned:
            cleaned_candidates.append(cleaned)

    if not cleaned_candidates:
        return ""

    return max(cleaned_candidates, key=len)


def extract_vst2_embedded_text(data: bytes) -> dict:
    """Extract human-readable metadata fields embedded in a VST2 Serum chunk."""
    metadata = {}
    macro_labels = {}

    for field, (start, end) in SERUM_VST2_TEXT_REGIONS.items():
        if start >= len(data):
            continue
        value = _extract_best_printable_string(data, start, min(end, len(data)))
        if not value:
            continue

        if field.startswith("macro_"):
            macro_labels[field] = value
        else:
            metadata[field] = value

    if macro_labels:
        metadata["macro_labels"] = macro_labels

    return metadata


def _is_serum_host_param_label(text: str) -> bool:
    """Heuristic filter for host-facing parameter labels in the Serum VST2 binary."""
    text = text.strip()
    if not text or len(text) > 40 or text.endswith("."):
        return False

    disallowed_prefixes = (
        "Adjust",
        "Sets",
        "Routes",
        "Selects",
        "Boosts",
        "This",
        "Keep",
        "controls",
        "determines",
        "Creates",
        "Alter",
        "Pitch",
        "Stereo",
        "Enabling",
        "drag",
        "Drag",
        "Low ",
        "Hi ",
        "note:",
        "middle:",
        "positive",
        "negative",
        "Most",
        "a dry",
        "boosts",
        "sets ",
        "you want",
        "or automation",
        "(including",
        "choose ",
        "choose",
        "whether ",
        "if you ",
        "Enable ",
        "Enable or",
        "Wet/Dry ",
        "Threshold ",
        "Ratio ",
        "Attack Time ",
        "Release Time ",
        "Hold Time ",
        "Decay Time ",
        "Sustain Level ",
        "Center Frequency",
        "Bandwidth ",
        "Feedback",
        "Delay time",
        "Number of voices",
        "Restarts ",
        "Adds ",
        "Makes ",
        "Set the ",
        "Additioinal",
        "Select the ",
        "Choose ",
        "Scales ",
        "original ",
        "Hall was",
        "Click here",
        "Determines ",
        "Determines when",
        "Adjust ",
        "Adjusts ",
        "It is ",
        "Note the ",
        "Allows ",
        "Specify",
        "Specifies ",
        "makeup ",
        "Enables ",
        "This is ",
        "Lfo Depth ",
        "Also handy",
        "Bypass For",
        "Show / Hide ",
    )
    if any(text.startswith(prefix) for prefix in disallowed_prefixes):
        return False

    if text.startswith("--") or text.startswith("@"):
        return False
    if re.search(r"[{}\[\];]", text):
        return False
    if re.fullmatch(r"[0-9.]+", text):
        return False
    return True


def _split_inline_label_description(text: str) -> tuple[str, str] | None:
    """Split strings like 'Noise Oscillator Color - pitch...' into label/description."""
    text = text.strip()
    if " - " not in text:
        return None
    label, description = text.split(" - ", 1)
    label = label.strip()
    description = description.strip()
    if not label or not description:
        return None
    if not _is_serum_host_param_label(label):
        return None
    return label, description


def classify_serum_vst2_host_param_label(label: str) -> str:
    """Group host-facing Serum VST2 labels into broad functional categories."""
    label = label.strip()
    if not label:
        return "other"

    fx_prefixes = (
        "Dist_",
        "Flg_",
        "Phs_",
        "Cho_",
        "Dly_",
        "Cmp_",
        "Cmp",
        "Comp_",
        "EQ",
        "EQ_",
        "Rev_",
        "Hyp_",
        "FX Fil",
        "FX ",
        "Hyper ",
    )
    if label.startswith(fx_prefixes):
        return "fx"

    if label.startswith(("Mod Matrix", "Mod Source", "Mod Aux Source", "Mod Dest", "Matrix Curve")):
        return "matrix"

    if label.startswith("Macro "):
        return "macro"

    if label.startswith(("LFO", "Chaos ")) or "LFO" in label:
        return "modulation"

    if label.startswith(("A ", "Warp Menu OSC A", "Osc A", "Osc Enable (Osc A)")):
        return "osc_a"

    if label.startswith(("B ", "Osc B", "Osc Enable B")):
        return "osc_b"

    if label.startswith(("Noise ", "Osc Enable noise", "Noise Osc Direct")):
        return "noise"

    if label.startswith(("Sub ", "SubOsc", "Sub Osc", "Osc Enable sub", "SubOsc Direct")):
        return "sub"

    if label.startswith(("Fil ", "Filter ", "Filter Enable", "Filter KeyTrack", "OscA>Fil", "OscB>Fil", "OscN>Fil", "OscS>Fil")):
        return "filter"

    if label.startswith(("Amp ", "Env2 ", "Env3 ", "Env4 ", "Attack Curve", "Decay Curve", "Release Curve")):
        return "envelope"

    global_prefixes = (
        "Master ",
        "Porta",
        "Portamento",
        "Bend Range",
        "Monophonic",
        "Legato",
        "Polyphony",
        "Quality",
        "Lock ",
        "Note Latch",
        "GUI Size",
        "Reverb Type",
        "Osc A PitchTrack",
        "Osc B PitchTrack",
        "Unison ",
    )
    if label.startswith(global_prefixes):
        return "global"

    return "other"


def infer_serum_vst2_host_control_kind(label: str) -> str:
    """Infer the likely automation/control kind from a Serum host label."""
    label = label.strip()
    if not label:
        return "unknown"

    boolean_tokens = (
        "_On",
        "PitchTrack",
        "BPM_Sync",
        "Link",
        "Retrig",
        "Legato",
        "Note Latch",
    )
    if any(token in label for token in boolean_tokens) or " Enable" in label or label in {
        "Monophonic / Polyphonic switch",
        "Porta Scaled",
    }:
        return "boolean_or_toggle"

    enum_tokens = (
        " Type",
        "_Type",
        " Mode",
        "_Mode",
        " Shape",
        "_Shape",
        "Curve",
        "Output",
        "Source",
        " Dest",
        "_Dest",
        "Octave",
        "Menu",
        "Stack",
        "Detune Mode",
        "Quality",
        "Polyphony Count",
        "GUI Size",
        "Reverb Type",
    )
    if any(token in label for token in enum_tokens):
        return "discrete_or_enum"

    return "continuous"


def describe_serum_vst2_host_param(label: str, description: str = "") -> dict:
    """Attach higher-level structure using the Serum manual's section layout."""
    category = classify_serum_vst2_host_param_label(label)
    module = category
    manual_section = {
        "osc_a": "Oscillator A",
        "osc_b": "Oscillator B",
        "noise": "Noise Oscillator",
        "sub": "Sub Oscillator",
        "filter": "Filter",
        "envelope": "Envelopes",
        "modulation": "LFO / Chaos",
        "matrix": "Mod Matrix",
        "macro": "Macros",
        "global": "Voicing / Global",
        "fx": "FX",
        "other": "Other",
    }.get(category, "Other")

    if category == "fx":
        fx_modules = (
            ("Dist_", "fx_distortion", "FX > Distortion"),
            ("Flg_", "fx_flanger", "FX > Flanger"),
            ("Phs_", "fx_phaser", "FX > Phaser"),
            ("Cho_", "fx_chorus", "FX > Chorus"),
            ("Dly_", "fx_delay", "FX > Delay"),
            ("Cmp_", "fx_compressor", "FX > Compressor"),
            ("Comp_", "fx_compressor", "FX > Compressor"),
            ("Rev_", "fx_reverb", "FX > Reverb"),
            ("EQ", "fx_eq", "FX > EQ"),
            ("FX Fil", "fx_filter", "FX > Filter"),
            ("Hyp_", "fx_hyper_dimension", "FX > Hyper/Dimension"),
            ("Hyper ", "fx_hyper_dimension", "FX > Hyper/Dimension"),
        )
        for prefix, candidate_module, candidate_section in fx_modules:
            if label.startswith(prefix):
                module = candidate_module
                manual_section = candidate_section
                break
    elif category == "matrix":
        if label.startswith("Mod Matrix Depth"):
            module = "matrix_depth"
        elif label.startswith("Mod Matrix Output"):
            module = "matrix_output"
        elif label.startswith("Mod Source"):
            module = "matrix_source"
        elif label.startswith("Mod Aux Source"):
            module = "matrix_aux_source"
        elif label.startswith("Mod Dest"):
            module = "matrix_destination"
        elif label.startswith("Matrix Curve"):
            module = "matrix_curve"
        manual_section = "Mod Matrix"
    elif category == "modulation":
        if label.startswith("Chaos "):
            module = "chaos"
            manual_section = "Global > Chaos"
        else:
            module = "lfo"
            manual_section = "LFO Controls"
    elif category == "envelope":
        if label.startswith("Amp "):
            module = "env1_amp"
            manual_section = "Envelope 1 / Amp"
        elif label.startswith("Env2 "):
            module = "env2"
            manual_section = "Envelope 2"
        elif label.startswith("Env3 "):
            module = "env3"
            manual_section = "Envelope 3"
        elif label.startswith("Env4 "):
            module = "env4"
            manual_section = "Envelope 4"
        elif "Curve" in label:
            module = "envelope_curve"
            manual_section = "Envelope Curves"
    elif category == "filter":
        if label.startswith(("OscA>Fil", "OscB>Fil", "OscN>Fil", "OscS>Fil")):
            module = "filter_routing"
            manual_section = "Filter Routing"
        else:
            module = "filter_core"
            manual_section = "Filter"
    elif category == "global":
        if label == "Master Volume":
            module = "global_master"
            manual_section = "Master"
        elif label.startswith(("Porta", "Portamento")):
            module = "global_portamento"
            manual_section = "Voicing > Portamento"
        elif label.startswith(("Bend Range", "Osc A PitchTrack", "Osc B PitchTrack")):
            module = "global_pitch"
            manual_section = "Global > Pitch"
        elif label.startswith(("Monophonic", "Legato", "Polyphony", "Unison ", "Note Latch")):
            module = "global_voicing"
            manual_section = "Voicing"
        else:
            module = "global_misc"
            manual_section = "Global"

    return {
        "category": category,
        "module": module,
        "manual_section": manual_section,
        "control_kind_hint": infer_serum_vst2_host_control_kind(label),
        "description_present": bool(description.strip()),
    }


def extract_serum_vst2_host_param_catalog(binary_path=SERUM_VST2_PLUGIN_BINARY_PATH) -> dict:
    """Extract a host-side parameter catalog from the installed Serum VST2 binary.

    This does not map parameter labels to preset float-slot offsets. It only
    extracts the host-facing labels and nearby descriptions from the plugin
    binary, which is useful for later alignment work.
    """
    binary_path = Path(binary_path)
    data = binary_path.read_bytes()
    printable = extract_printable_strings(data, min_length=4)
    start_indexes = [
        i for i, row in enumerate(printable)
        if row["text"].strip() == SERUM_VST2_HOST_PARAM_CATALOG_START
    ]
    if not start_indexes:
        raise ValueError("could not find Serum VST2 host parameter catalog anchor")

    stop_text_prefixes = (
        "Click to edit this wavetable.",
        "Edit the current visible wavetable",
        "Closes wavetable editor.",
        "Closes this graph editor.",
    )

    best_catalog = None
    for start_idx in start_indexes:
        stop_idx = None
        for j in range(start_idx + 1, len(printable)):
            text = printable[j]["text"].strip()
            if text == SERUM_VST2_HOST_PARAM_CATALOG_STOP:
                stop_idx = j
                break
        if stop_idx is None:
            continue

        region = printable[start_idx:stop_idx]
        entries = []
        i = 0
        while i < len(region):
            label_text = region[i]["text"].strip()
            inline = _split_inline_label_description(label_text)
            if inline is not None:
                label, inline_description = inline
            else:
                label = label_text
                inline_description = ""

            if not _is_serum_host_param_label(label):
                i += 1
                continue

            description_parts = []
            if inline_description:
                description_parts.append(inline_description)
            j = i + 1
            while j < len(region):
                next_text = region[j]["text"].strip()
                next_inline = _split_inline_label_description(next_text)
                if next_inline is not None:
                    break
                if _is_serum_host_param_label(next_text):
                    break
                if any(next_text.startswith(prefix) for prefix in stop_text_prefixes):
                    break
                if next_text:
                    description_parts.append(next_text)
                j += 1

            entries.append({
                "label": label,
                "description": " ".join(description_parts).strip(),
                "offset": region[i]["offset"],
            })
            i = j

        # Keep the richest catalog copy when the binary contains multiple slices.
        if best_catalog is None or len(entries) > len(best_catalog["entries"]):
            best_catalog = {
                "binary_path": str(binary_path),
                "start_offset": region[0]["offset"],
                "end_offset": region[-1]["offset"],
                "entry_count": len(entries),
                "entries": entries,
            }

    if best_catalog is None:
        raise ValueError("could not isolate a Serum VST2 host parameter catalog region")

    occurrences = {}
    for entry in best_catalog["entries"]:
        label = entry["label"]
        occurrences[label] = occurrences.get(label, 0) + 1
        if occurrences[label] > 1:
            entry["occurrence"] = occurrences[label]
            entry["key"] = f"{label} #{occurrences[label]}"
        else:
            entry["key"] = label
        entry.update(describe_serum_vst2_host_param(entry["label"], entry.get("description", "")))

    return best_catalog


def build_serum_vst2_host_coverage_report(binary_path=SERUM_VST2_PLUGIN_BINARY_PATH) -> dict:
    """Summarize which Serum host labels are already covered by the current parser."""
    catalog = extract_serum_vst2_host_param_catalog(binary_path=binary_path)

    coverage_sources = {}
    for parser_key, host_label in SERUM_VST2_KEY_TO_HOST_LABEL.items():
        coverage_sources.setdefault(host_label, []).append({
            "source": "vst2_slot",
            "parser_key": parser_key,
        })

    for embedded_key, host_label in SERUM_VST2_EMBEDDED_TEXT_TO_HOST_LABEL.items():
        coverage_sources.setdefault(host_label, []).append({
            "source": "embedded_text",
            "field": embedded_key,
        })

    category_summaries = {}
    module_summaries = {}
    enriched_entries = []
    covered_count = 0

    for entry in catalog["entries"]:
        category = entry["category"]
        module = entry["module"]
        sources = coverage_sources.get(entry["label"], [])
        covered = bool(sources)
        if covered:
            covered_count += 1

        enriched = {
            **entry,
            "category": category,
            "covered": covered,
        }
        if sources:
            enriched["coverage_sources"] = sources
        enriched_entries.append(enriched)

        summary = category_summaries.setdefault(category, {
            "total": 0,
            "covered": 0,
            "uncovered": 0,
            "covered_labels": [],
            "uncovered_labels": [],
        })
        summary["total"] += 1
        if covered:
            summary["covered"] += 1
            summary["covered_labels"].append(entry["key"])
        else:
            summary["uncovered"] += 1
            summary["uncovered_labels"].append(entry["key"])

        module_summary = module_summaries.setdefault(module, {
            "manual_section": entry["manual_section"],
            "total": 0,
            "covered": 0,
            "uncovered": 0,
            "covered_labels": [],
            "uncovered_labels": [],
        })
        module_summary["total"] += 1
        if covered:
            module_summary["covered"] += 1
            module_summary["covered_labels"].append(entry["key"])
        else:
            module_summary["uncovered"] += 1
            module_summary["uncovered_labels"].append(entry["key"])

    for summary in category_summaries.values():
        total = summary["total"] or 1
        summary["covered_pct"] = round(summary["covered"] / total * 100, 1)
    for summary in module_summaries.values():
        total = summary["total"] or 1
        summary["covered_pct"] = round(summary["covered"] / total * 100, 1)

    return {
        "binary_path": catalog["binary_path"],
        "catalog_entry_count": catalog["entry_count"],
        "covered_entry_count": covered_count,
        "uncovered_entry_count": catalog["entry_count"] - covered_count,
        "covered_pct": round(covered_count / max(catalog["entry_count"], 1) * 100, 1),
        "coverage_sources": {
            "vst2_slot_aliases": SERUM_VST2_KEY_TO_HOST_LABEL,
            "embedded_text_aliases": SERUM_VST2_EMBEDDED_TEXT_TO_HOST_LABEL,
        },
        "categories": category_summaries,
        "modules": module_summaries,
        "entries": enriched_entries,
    }


# ---------------------------------------------------------------------------
# VST2 parser (Serum_x64 / Serum)
# ---------------------------------------------------------------------------

def _extract_vst2_decompressed_data(raw: bytes) -> bytes:
    """Extract and decompress a VST2 Serum chunk from raw bytes.

    ALS VST2 buffers are typically just the compressed zlib payload.
    Standalone .fxp files wrap the same payload in an FXP container header,
    so we scan for the first valid zlib stream when direct decompression fails.
    """
    try:
        return zlib.decompress(raw)
    except zlib.error:
        pass

    headers = (b"\x78\x01", b"\x78\x9c", b"\x78\xda")
    for i in range(max(0, len(raw) - 2)):
        if raw[i:i + 2] not in headers:
            continue
        try:
            return zlib.decompress(raw[i:])
        except zlib.error:
            continue

    raise ValueError("no zlib-compressed Serum VST2 chunk found")


def _parse_vst2_decompressed_data(data: bytes) -> dict:
    """Parse already-decompressed VST2 Serum/Serum_x64 state bytes."""

    result = {}

    # 1. Wavetable names (reliable — ASCII strings ending in .wav)
    wt_matches = re.findall(rb"[\x20-\x7e]{4,}\.wav", data)
    seen = set()
    wavetables = []
    for wt in wt_matches:
        name = wt.decode("ascii", errors="replace")
        name = name.replace("\\", "/").lstrip("/")
        if name not in seen:
            seen.add(name)
            wavetables.append(name)
    result["wavetables"] = wavetables

    text_metadata = extract_vst2_embedded_text(data)
    if text_metadata:
        result["text_metadata"] = text_metadata

    # 2. Parameter floats starting at SERUM_V2_PARAM_OFFSET
    if len(data) > SERUM_V2_PARAM_OFFSET + 44 * 4:
        params_raw = {}
        decoded = {}
        for idx, key, label, conf, hint in SERUM_VST2_PARAMS:
            byte_off = SERUM_V2_PARAM_OFFSET + idx * 4
            if byte_off + 4 <= len(data):
                val = struct.unpack_from("<f", data, byte_off)[0]
                if 0.0 <= val <= 1.0:
                    params_raw[key] = round(val, 4)
                    decoded_entry = {
                        "label": label,
                        "raw": round(val, 4),
                        "value": decode_param(val, hint),
                        "confidence": conf,
                    }
                    host_label = SERUM_VST2_KEY_TO_HOST_LABEL.get(key)
                    if host_label:
                        decoded_entry["host_label"] = host_label
                    decoded[key] = decoded_entry
        result["params_raw"] = params_raw
        result["params"] = decoded

    result["format"] = "vst2"
    return result


def extract_vst2_float_slots(data: bytes, start_offset=SERUM_V2_PARAM_OFFSET, count=256):
    """Extract a raw float slot view from decompressed VST2 Serum state bytes."""
    slots = []
    for idx in range(count):
        byte_off = start_offset + idx * 4
        if byte_off + 4 > len(data):
            break

        val = struct.unpack_from("<f", data, byte_off)[0]
        meta = SERUM_VST2_PARAM_BY_INDEX.get(idx)
        slot = {
            "index": idx,
            "offset": byte_off,
            "raw": val,
            "rounded": round(val, 6),
        }
        if meta:
            slot["known_param"] = meta["key"]
            slot["label"] = meta["label"]
            slot["confidence"] = meta["confidence"]
            slot["decoded"] = decode_param(val, meta["decoder_hint"])
        slots.append(slot)
    return slots


def diff_vst2_float_slots(data_a: bytes, data_b: bytes, start_offset=SERUM_V2_PARAM_OFFSET, count=256, threshold=0.001):
    """Diff raw VST2 float slots between two decompressed Serum state blobs."""
    slots_a = extract_vst2_float_slots(data_a, start_offset=start_offset, count=count)
    slots_b = extract_vst2_float_slots(data_b, start_offset=start_offset, count=count)
    changes = []

    for slot_a, slot_b in zip(slots_a, slots_b):
        delta = abs(slot_a["raw"] - slot_b["raw"])
        if delta < threshold:
            continue

        change = {
            "index": slot_a["index"],
            "offset": slot_a["offset"],
            "a": round(slot_a["raw"], 6),
            "b": round(slot_b["raw"], 6),
            "delta": round(slot_b["raw"] - slot_a["raw"], 6),
        }
        for key in ("known_param", "label", "confidence"):
            if key in slot_a:
                change[key] = slot_a[key]
        if "decoded" in slot_a or "decoded" in slot_b:
            change["decoded_a"] = slot_a.get("decoded")
            change["decoded_b"] = slot_b.get("decoded")
        changes.append(change)

    return changes


def cluster_vst2_slot_rows(rows: list[dict], max_index_gap=1) -> list[dict]:
    """Group nearby varying slot rows into contiguous clusters."""
    if max_index_gap < 0:
        raise ValueError("max_index_gap must be >= 0")
    if not rows:
        return []

    ordered = sorted(rows, key=lambda row: row["index"])
    groups = [[ordered[0]]]

    for row in ordered[1:]:
        if row["index"] - groups[-1][-1]["index"] <= max_index_gap + 1:
            groups[-1].append(row)
            continue
        groups.append([row])

    clusters = []
    for group in groups:
        cluster = {
            "start_index": group[0]["index"],
            "end_index": group[-1]["index"],
            "count": len(group),
            "indices": [row["index"] for row in group],
        }

        known_params = []
        for row in group:
            if "known_param" in row and row["known_param"] not in known_params:
                known_params.append(row["known_param"])
        if known_params:
            cluster["known_params"] = known_params

        if any("delta" in row for row in group):
            cluster["max_abs_delta"] = round(max(abs(row.get("delta", 0.0)) for row in group), 6)
        if any("spread" in row for row in group):
            cluster["max_spread"] = round(max(row.get("spread", 0.0) for row in group), 6)

        clusters.append(cluster)

    return clusters


def parse_vst2_buffer(hex_data: str) -> dict:
    """Parse a VST2 Serum/Serum_x64 Buffer hex string from an ALS file."""
    raw = bytes.fromhex(re.sub(r"\s+", "", hex_data))
    data = _extract_vst2_decompressed_data(raw)
    return _parse_vst2_decompressed_data(data)


def parse_fxp_file(path) -> dict:
    """Parse a standalone Serum VST2 .fxp preset file."""
    preset_path = Path(path)
    raw = preset_path.read_bytes()
    data = _extract_vst2_decompressed_data(raw)
    result = _parse_vst2_decompressed_data(data)

    header = {}
    if raw[:4] == b"CcnK" and len(raw) >= 60:
        fxp_type = raw[8:12].decode("ascii", errors="replace")
        version = struct.unpack_from(">I", raw, 12)[0]
        plugin_id = raw[16:20].decode("ascii", errors="replace")
        plugin_version = struct.unpack_from(">I", raw, 20)[0]
        param_count = struct.unpack_from(">I", raw, 24)[0]
        preset_name = raw[28:56].split(b"\x00", 1)[0].decode("utf-8", errors="replace")
        header = {
            "container": "fxp",
            "fxp_type": fxp_type,
            "version": version,
            "plugin_id": plugin_id,
            "plugin_version": plugin_version,
            "param_count": param_count,
            "preset_name": preset_name,
        }

    result["path"] = str(preset_path)
    result["_decompressed_data"] = data
    if header:
        result["header"] = header
    return result


# ---------------------------------------------------------------------------
# VST3 parser (Serum 2)
# ---------------------------------------------------------------------------

def _normalize_wt_path(path: str) -> str:
    """Normalize a wavetable path to a clean relative form."""
    if not path:
        return ""
    path = path.replace("\\", "/").lstrip("/")
    return path


def parse_vst3_processor_state(hex_data: str) -> dict:
    """Parse a VST3 Serum 2 ProcessorState hex string."""
    if zstandard is None or cbor2 is None:
        return {"error": "zstandard and cbor2 required: pip3 install zstandard cbor2"}

    raw = bytes.fromhex(re.sub(r"\s+", "", hex_data))

    if raw[:8] != b"XferJson":
        return {"error": "unexpected magic: %s" % raw[:8]}

    # Find JSON header end
    json_start = raw.find(b"{")
    depth, j = 0, json_start
    for j in range(json_start, min(json_start + 600, len(raw))):
        if raw[j] == ord("{"):
            depth += 1
        elif raw[j] == ord("}"):
            depth -= 1
            if depth == 0:
                break
    json_end = j + 1

    # Decompress ZSTD (skip 8-byte length/flag header after JSON)
    zstd_frame = raw[json_end + 8:]
    dctx = zstandard.ZstdDecompressor()
    cbor_data = dctx.decompress(zstd_frame, max_output_size=20_000_000)

    parsed = cbor2.loads(cbor_data)

    result = {"format": "vst3_serum2", "sections": {}}

    def get_params(section_key):
        sec = parsed.get(section_key, {})
        if isinstance(sec, dict):
            pp = sec.get("plainParams", {})
            return pp if isinstance(pp, dict) else {}
        return {}

    # --- Wavetables ---
    # Each Oscillator{N} section has a WTOsc{N} subsection with relativePathToWT
    osc_labels = [(0, "osc_a"), (1, "osc_b"), (2, "osc_c")]
    wavetables = {}
    for i, label in osc_labels:
        osc_sec = parsed.get("Oscillator%d" % i, {})
        wt_key = "WTOsc%d" % i
        if wt_key in osc_sec and isinstance(osc_sec[wt_key], dict):
            path = osc_sec[wt_key].get("relativePathToWT", "")
            if path:
                wavetables[label] = _normalize_wt_path(path)
    if wavetables:
        result["sections"]["wavetables"] = wavetables

    # --- Oscillators ---
    for i, label in osc_labels:
        params = get_params("Oscillator%d" % i)
        if params:
            result["sections"][label] = params

    # --- Filters ---
    for i in range(2):
        params = get_params("VoiceFilter%d" % i)
        if params:
            result["sections"]["filter_%d" % i] = params

    # --- Envelopes ---
    for i in range(4):
        params = get_params("Env%d" % i)
        if params:
            result["sections"]["env_%d" % i] = params

    # --- LFOs ---
    for i in range(10):
        params = get_params("LFO%d" % i)
        if params:
            result["sections"]["lfo_%d" % i] = params

    # --- Global ---
    params = get_params("Global0")
    if params:
        result["sections"]["global"] = params

    # --- Mod matrix ---
    # Each active ModSlot has: source (list), destModuleTypeString,
    # destModuleParamName, destModuleID, plainParams.kParamAmount
    mod_slots = {}
    for i in range(64):
        ms = parsed.get("ModSlot%d" % i, {})
        if not isinstance(ms, dict):
            continue

        src = ms.get("source")              # list [type_id, slot_or_bus]
        dest_type = ms.get("destModuleTypeString", "")
        dest_id = ms.get("destModuleID", 0)
        dest_param = ms.get("destModuleParamName", "")
        amt_dict = ms.get("plainParams", {})
        if not isinstance(amt_dict, dict):
            continue
        amt = amt_dict.get("kParamAmount")
        bypass = amt_dict.get("kParamBypass", 0)

        # Only include slots with routing info and a non-zero amount
        if src is None or amt is None:
            continue
        if amt == 0.0 and bypass:
            continue

        type_id = src[0] if isinstance(src, list) and src else None
        source_label = SERUM2_SOURCE_NAMES.get(type_id, "src%s" % type_id) if type_id is not None else "unknown"

        slot_info = {
            "source": source_label,
            "source_raw": src,
            "dest_module": dest_type,
            "dest_instance": dest_id,
            "dest_param": dest_param,
            "amount": round(amt, 2),
        }
        if bypass:
            slot_info["bypassed"] = True
        mod_slots["slot_%d" % i] = slot_info

    if mod_slots:
        result["sections"]["mod_matrix"] = mod_slots

    return result


# ---------------------------------------------------------------------------
# ALS file parser
# ---------------------------------------------------------------------------

def parse_als(slug: str) -> dict:
    als_path = ALS_DIR / ("%s.als" % slug)
    if not als_path.exists():
        print("  Not found: %s" % als_path)
        return {}

    with gzip.open(als_path, "rb") as f:
        xml = f.read().decode("utf-8", errors="replace")

    results = []

    # --- VST2: Serum_x64 or Serum ---
    for match in re.finditer(
        r'PlugName Value="(?P<plug>Serum[^"]*)".*?<Buffer>\s*(?P<buf>.*?)\s*</Buffer>',
        xml,
        re.DOTALL,
    ):
        plug_name = match.group("plug")
        buf = match.group("buf")
        start = match.start()
        track_name = _find_track_name(xml, start)

        try:
            params = parse_vst2_buffer(buf)
        except Exception as e:
            params = {"error": str(e)}

        results.append({
            "track": track_name,
            "plugin": plug_name,
            **params,
        })

    # --- VST3: Serum 2 ---
    for match in re.finditer(
        r'Serum%202.*?<ProcessorState>\s*(?P<buf>[0-9A-Fa-f\s]+?)\s*</ProcessorState>',
        xml,
        re.DOTALL,
    ):
        buf = match.group("buf")
        raw = bytes.fromhex(re.sub(r"\s+", "", buf))
        if raw[:8] != b"XferJson":
            continue

        start = match.start()
        track_name = _find_track_name(xml, start)

        try:
            params = parse_vst3_processor_state(buf)
        except Exception as e:
            params = {"error": str(e)}

        results.append({
            "track": track_name,
            "plugin": "Serum 2",
            **params,
        })

    return {"slug": slug, "serum_instances": results}


def _find_track_name(xml: str, position: int) -> str:
    """Find the user-visible name of the track enclosing the plugin at `position`."""
    prefix = xml[:position]
    track_starts = list(re.finditer(r'<(?:MidiTrack|AudioTrack)\b', prefix))
    if not track_starts:
        return "unknown"

    track_start = track_starts[-1].start()
    snippet = xml[track_start:position]

    m = re.search(r'<UserName\s+Value="([^"]{1,80})"', snippet)
    if m:
        return m.group(1)
    m = re.search(r'<Name\s+Value="([^"]{1,80})"', snippet)
    if m:
        return m.group(1)
    return "unknown"


# ---------------------------------------------------------------------------
# Output helpers
# ---------------------------------------------------------------------------

def summarise_instance(inst: dict) -> dict:
    """Produce a compact summary suitable for adding to analysis JSONs."""
    out = {
        "track": inst.get("track", "unknown"),
        "plugin": inst.get("plugin", "Serum"),
    }

    fmt = inst.get("format", "")

    if fmt == "vst2":
        out["wavetables"] = inst.get("wavetables", [])
        text_metadata = inst.get("text_metadata", {})
        if text_metadata.get("embedded_vendor"):
            out["vendor"] = text_metadata["embedded_vendor"]
        if text_metadata.get("embedded_bank"):
            out["bank"] = text_metadata["embedded_bank"]
        if text_metadata.get("macro_labels"):
            out["macro_labels"] = text_metadata["macro_labels"]
        params = inst.get("params", {})
        interesting = {}

        # OSC A — always include
        for key in ["osc_a_level", "osc_a_wtpos", "osc_a_uni_voices", "osc_a_detune"]:
            if key in params:
                interesting[key] = params[key]["value"]

        # OSC B — only include detail when B is actually active (level > 0)
        osc_b_level_val = params.get("osc_b_level", {}).get("value", 0.0) or 0.0
        interesting["osc_b_level"] = osc_b_level_val
        if osc_b_level_val > 0.01:
            for key in ["osc_b_wtpos", "osc_b_uni_voices", "osc_b_detune"]:
                if key in params:
                    interesting[key] = params[key]["value"]

        # Filter — include cutoff only if non-zero (zero means fully closed, rarely set)
        flt_cutoff = params.get("flt_cutoff", {}).get("value", 0.0) or 0.0
        if flt_cutoff > 0.0:
            interesting["flt_cutoff"] = flt_cutoff
        flt_res = params.get("flt_res", {}).get("value")
        if flt_res is not None:
            interesting["flt_res"] = flt_res

        # Envelopes
        for key in ["env1_attack", "env1_decay", "env1_sustain", "env1_release"]:
            if key in params and params[key]["confidence"] in ("H", "M"):
                val = params[key]["value"]
                if val is not None:
                    interesting[key] = val

        # LFO — only include if non-default (default: rate=0.0, attack=0.75)
        lfo_rate = params.get("lfo1_rate", {}).get("value", 0.0) or 0.0
        lfo_atk = params.get("lfo1_attack", {}).get("value", 0.75) or 0.75
        if lfo_rate != 0.0:
            interesting["lfo1_rate"] = lfo_rate
        if lfo_atk != 0.75:
            interesting["lfo1_attack"] = lfo_atk

        out["key_params"] = interesting

    elif fmt == "vst3_serum2":
        secs = inst.get("sections", {})
        # Wavetables (new field)
        wt = secs.get("wavetables", {})
        if wt:
            out["wavetables"] = wt
        # Oscillator params
        out["oscillators"] = {k: v for k, v in secs.items() if k.startswith("osc")}
        out["filters"] = {k: v for k, v in secs.items() if k.startswith("filter")}
        out["envelopes"] = {k: v for k, v in secs.items() if k.startswith("env")}
        out["global"] = secs.get("global", {})
        lfos = {k: v for k, v in secs.items() if k.startswith("lfo")}
        if lfos:
            out["lfos"] = lfos
        mod = secs.get("mod_matrix", {})
        if mod:
            out["mod_matrix"] = mod

    if "error" in inst:
        out["error"] = inst["error"]

    return out


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

SLUGS = [
    "kettama-it-gets-better",
    "mph-raw",
    "interplanetary-criminal-slow-burner",
    "bl3ss-camrinwatsin-kisses",
    "sammy-virji-cops-and-robbers",
]


def main():
    targets = sys.argv[1:] if len(sys.argv) > 1 else SLUGS

    for slug in targets:
        print("\n%s" % ("=" * 60))
        print("Parsing: %s" % slug)
        print("=" * 60)

        result = parse_als(slug)
        instances = result.get("serum_instances", [])
        print("Found %d Serum instance(s)" % len(instances))

        summaries = [summarise_instance(i) for i in instances]

        for s in summaries:
            print("\n  Track: %s  [%s]" % (s["track"], s["plugin"]))
            if "wavetables" in s:
                print("    Wavetables: %s" % s["wavetables"])
            if "key_params" in s:
                print("    Key params: %s" % s["key_params"])
            if "oscillators" in s:
                for osc, params in s["oscillators"].items():
                    print("    %s: %s" % (osc, params))
            if "filters" in s:
                for flt, params in s["filters"].items():
                    print("    %s: %s" % (flt, params))
            mod = s.get("mod_matrix", {})
            if mod:
                print("    mod_matrix: %d active slots" % len(mod))
                for slot_k, slot_v in list(mod.items())[:3]:
                    print("      %s: %s -> %s[%s].%s (%.1f)" % (
                        slot_k,
                        slot_v.get("source", "?"),
                        slot_v.get("dest_module", "?"),
                        slot_v.get("dest_instance", "?"),
                        slot_v.get("dest_param", "?"),
                        slot_v.get("amount", 0),
                    ))
                if len(mod) > 3:
                    print("      ... +%d more" % (len(mod) - 3))

        out_path = ANALYSIS_DIR / ("%s-serum.json" % slug)
        output = {
            "slug": slug,
            "serum_instances": summaries,
            "_raw_count": len(instances),
        }
        with open(out_path, "w") as f:
            json.dump(output, f, indent=2, default=str)
        print("\n  → Written: %s" % out_path)


if __name__ == "__main__":
    main()
