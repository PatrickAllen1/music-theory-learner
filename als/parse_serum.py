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


# ---------------------------------------------------------------------------
# VST2 parser (Serum_x64 / Serum)
# ---------------------------------------------------------------------------

def parse_vst2_buffer(hex_data: str) -> dict:
    """Parse a VST2 Serum/Serum_x64 Buffer hex string."""
    raw = bytes.fromhex(re.sub(r"\s+", "", hex_data))
    data = zlib.decompress(raw)

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
                    decoded[key] = {
                        "label": label,
                        "raw": round(val, 4),
                        "value": decode_param(val, hint),
                        "confidence": conf,
                    }
        result["params_raw"] = params_raw
        result["params"] = decoded

    result["format"] = "vst2"
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
