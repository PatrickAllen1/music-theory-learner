#!/usr/bin/env python3
"""
extract_serum_audio_features.py

Extract comparable audio descriptors from rendered Serum audition WAV files.

Examples:
    python3 als/extract_serum_audio_features.py --session-dir als/audio-session
    python3 als/extract_serum_audio_features.py --wav some-render.wav --out-dir als/catalog/audio/descriptors
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np
from scipy.io import wavfile


DESCRIPTOR_VERSION = "0.1.0"


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Extract audio descriptors from rendered Serum audition WAV files.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--session-dir", help="Audio session directory created by prepare_serum_audio_session.py.")
    group.add_argument("--renders-dir", help="Directory of WAV files to analyze.")
    group.add_argument("--wav", action="append", default=[], help="Specific WAV file to analyze. Pass multiple times.")
    parser.add_argument("--out-dir", help="Directory for per-render descriptor JSON files.")
    parser.add_argument("--index-out", help="Output path for the descriptor index JSON.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing outputs.")
    return parser


def _write_json(path: Path, payload: dict, force: bool) -> None:
    if path.exists() and not force:
        raise FileExistsError(f"{path} already exists; rerun with --force to overwrite")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n")


def _linear_to_db(value: float | None) -> float | None:
    if value is None or value <= 0:
        return None
    return 20.0 * math.log10(value)


def _normalize_pcm(data: np.ndarray) -> np.ndarray:
    if data.dtype.kind == "u":
        info = np.iinfo(data.dtype)
        midpoint = (info.max + 1) / 2.0
        return (data.astype(np.float64) - midpoint) / midpoint
    if data.dtype.kind == "i":
        info = np.iinfo(data.dtype)
        scale = max(abs(info.min), abs(info.max))
        return data.astype(np.float64) / float(scale)
    if data.dtype.kind == "f":
        return np.asarray(data, dtype=np.float64)
    raise TypeError(f"unsupported audio dtype: {data.dtype}")


def _ensure_2d(data: np.ndarray) -> np.ndarray:
    if data.ndim == 1:
        return data[:, np.newaxis]
    return data


def _rms(signal: np.ndarray) -> float:
    if signal.size == 0:
        return 0.0
    return float(np.sqrt(np.mean(np.square(signal), dtype=np.float64)))


def _moving_rms(signal: np.ndarray, window_size: int) -> np.ndarray:
    if signal.size == 0:
        return signal
    window_size = max(1, min(window_size, signal.size))
    kernel = np.ones(window_size, dtype=np.float64) / float(window_size)
    return np.sqrt(np.convolve(np.square(signal), kernel, mode="same"))


def _attack_time_ms(signal: np.ndarray, sample_rate: int) -> float | None:
    if signal.size == 0:
        return None
    envelope = _moving_rms(signal, max(1, int(sample_rate * 0.005)))
    peak = float(np.max(envelope))
    if peak <= 1e-8:
        return None
    low = peak * 0.1
    high = peak * 0.9
    low_hits = np.flatnonzero(envelope >= low)
    high_hits = np.flatnonzero(envelope >= high)
    if low_hits.size == 0 or high_hits.size == 0:
        return None
    start = int(low_hits[0])
    end_candidates = high_hits[high_hits >= start]
    if end_candidates.size == 0:
        return None
    end = int(end_candidates[0])
    return round((end - start) * 1000.0 / float(sample_rate), 3)


def _spectral_descriptors(signal: np.ndarray, sample_rate: int) -> dict:
    if signal.size == 0:
        return {
            "centroid_hz": None,
            "rolloff_hz": None,
            "flatness": None,
            "sub_energy_ratio": 0.0,
            "low_mid_energy_ratio": 0.0,
            "presence_energy_ratio": 0.0,
            "air_energy_ratio": 0.0,
        }

    max_frames = min(signal.size, 131072)
    focus_index = int(np.argmax(np.abs(signal)))
    start = max(0, focus_index - max_frames // 2)
    windowed = signal[start : start + max_frames]
    if windowed.size < 16:
        windowed = signal[:max_frames]
    window = np.hanning(windowed.size)
    spectrum = np.fft.rfft(windowed * window)
    magnitudes = np.abs(spectrum)
    power = np.square(magnitudes)
    freqs = np.fft.rfftfreq(windowed.size, d=1.0 / float(sample_rate))
    power_sum = float(np.sum(power))
    mag_sum = float(np.sum(magnitudes))

    centroid_hz = None
    if mag_sum > 0:
        centroid_hz = round(float(np.sum(freqs * magnitudes) / mag_sum), 3)

    rolloff_hz = None
    if power_sum > 0:
        cumulative = np.cumsum(power)
        threshold = power_sum * 0.85
        rolloff_hz = round(float(freqs[int(np.searchsorted(cumulative, threshold, side="left"))]), 3)

    flatness = None
    positive = magnitudes[magnitudes > 1e-12]
    if positive.size > 0:
        flatness = round(float(np.exp(np.mean(np.log(positive))) / np.mean(positive)), 6)

    def band_ratio(low: float, high: float) -> float:
        if power_sum <= 0:
            return 0.0
        mask = (freqs >= low) & (freqs < high)
        if not np.any(mask):
            return 0.0
        return round(float(np.sum(power[mask]) / power_sum), 6)

    return {
        "centroid_hz": centroid_hz,
        "rolloff_hz": rolloff_hz,
        "flatness": flatness,
        "sub_energy_ratio": band_ratio(20.0, 120.0),
        "low_mid_energy_ratio": band_ratio(120.0, 1000.0),
        "presence_energy_ratio": band_ratio(1000.0, 5000.0),
        "air_energy_ratio": band_ratio(5000.0, 20000.0),
    }


def _stereo_descriptors(data: np.ndarray) -> dict:
    channels = data.shape[1]
    if channels < 2:
        return {
            "stereo_correlation": None,
            "side_ratio": None,
            "channel_balance": None,
        }

    left = data[:, 0]
    right = data[:, 1]
    left_std = float(np.std(left))
    right_std = float(np.std(right))
    if left_std <= 1e-8 or right_std <= 1e-8:
        correlation = None
    else:
        correlation = round(float(np.corrcoef(left, right)[0, 1]), 6)

    mid = (left + right) * 0.5
    side = (left - right) * 0.5
    mid_rms = _rms(mid)
    side_rms = _rms(side)
    side_ratio = None if mid_rms <= 1e-8 else round(float(side_rms / mid_rms), 6)

    left_rms = _rms(left)
    right_rms = _rms(right)
    channel_balance = None
    if max(left_rms, right_rms) > 1e-8:
        channel_balance = round(float((left_rms - right_rms) / max(left_rms, right_rms)), 6)

    return {
        "stereo_correlation": correlation,
        "side_ratio": side_ratio,
        "channel_balance": channel_balance,
    }


def _queue_map(session_dir: Path) -> dict[str, dict]:
    queue_path = session_dir / "audio_queue.json"
    if not queue_path.exists():
        return {}
    payload = json.loads(queue_path.read_text())
    return {row["render_filename"]: row for row in payload.get("queue", [])}


def _analyze_wav(path: Path, queue_row: dict | None) -> dict:
    sample_rate, data = wavfile.read(path)
    normalized = _ensure_2d(_normalize_pcm(np.asarray(data)))
    mono = np.mean(normalized, axis=1)

    peak = float(np.max(np.abs(normalized))) if normalized.size else 0.0
    rms = _rms(mono)
    tail_frames = max(1, min(len(mono), int(sample_rate * 0.25)))
    tail_rms = _rms(mono[-tail_frames:])
    onset_hits = np.flatnonzero(np.abs(mono) >= max(peak * 0.1, 1e-4))
    onset_s = None if onset_hits.size == 0 else round(float(onset_hits[0] / float(sample_rate)), 6)

    descriptor = {
        "descriptor_version": DESCRIPTOR_VERSION,
        "render_filename": path.name,
        "render_path": str(path),
        "profile_id": queue_row.get("profile_id") if queue_row else None,
        "analysis_slug": queue_row.get("analysis_slug") if queue_row else None,
        "track": queue_row.get("track") if queue_row else None,
        "primary_role": queue_row.get("primary_role") if queue_row else None,
        "audition_id": queue_row.get("audition_id") if queue_row else None,
        "audition_label": queue_row.get("audition_label") if queue_row else None,
        "sample_rate": int(sample_rate),
        "channels": int(normalized.shape[1]),
        "frame_count": int(normalized.shape[0]),
        "duration_s": round(float(normalized.shape[0] / float(sample_rate)), 6),
        "levels": {
            "peak_linear": round(peak, 8),
            "peak_dbfs": None if peak <= 0 else round(_linear_to_db(peak), 3),
            "rms_linear": round(rms, 8),
            "rms_dbfs": None if rms <= 0 else round(_linear_to_db(rms), 3),
            "crest_db": None if peak <= 0 or rms <= 0 else round(_linear_to_db(peak / rms), 3),
            "tail_rms_dbfs": None if tail_rms <= 0 else round(_linear_to_db(tail_rms), 3),
            "tail_vs_body_db": None if rms <= 0 or tail_rms <= 0 else round(_linear_to_db(tail_rms / rms), 3),
            "dc_offset": round(float(np.mean(mono)), 8),
        },
        "time": {
            "onset_s": onset_s,
            "attack_time_ms": _attack_time_ms(mono, int(sample_rate)),
            "zero_crossing_rate": round(float(np.mean(np.abs(np.diff(np.signbit(mono))))), 6) if mono.size > 1 else 0.0,
        },
        "spectral": _spectral_descriptors(mono, int(sample_rate)),
        "stereo": _stereo_descriptors(normalized),
    }
    return descriptor


def _mean(values: list[float | None]) -> float | None:
    valid = [value for value in values if isinstance(value, (int, float))]
    if not valid:
        return None
    return round(float(sum(valid) / len(valid)), 6)


def _profile_summaries(descriptors: list[dict]) -> list[dict]:
    grouped: dict[str, list[dict]] = {}
    for descriptor in descriptors:
        profile_id = descriptor.get("profile_id")
        if not profile_id:
            continue
        grouped.setdefault(profile_id, []).append(descriptor)

    summaries = []
    for profile_id, rows in sorted(grouped.items()):
        summaries.append({
            "profile_id": profile_id,
            "analysis_slug": rows[0].get("analysis_slug"),
            "track": rows[0].get("track"),
            "primary_role": rows[0].get("primary_role"),
            "render_count": len(rows),
            "audition_ids": sorted({row.get("audition_id") for row in rows if row.get("audition_id")}),
            "mean_peak_dbfs": _mean([row["levels"]["peak_dbfs"] for row in rows]),
            "mean_rms_dbfs": _mean([row["levels"]["rms_dbfs"] for row in rows]),
            "mean_centroid_hz": _mean([row["spectral"]["centroid_hz"] for row in rows]),
            "mean_rolloff_hz": _mean([row["spectral"]["rolloff_hz"] for row in rows]),
            "mean_side_ratio": _mean([row["stereo"]["side_ratio"] for row in rows]),
            "mean_attack_time_ms": _mean([row["time"]["attack_time_ms"] for row in rows]),
            "render_filenames": [row["render_filename"] for row in rows],
        })
    return summaries


def main() -> None:
    parser = make_parser()
    args = parser.parse_args()

    queue_map: dict[str, dict] = {}
    expected_rows: list[dict] = []
    mode = "explicit"

    if args.session_dir:
        session_dir = Path(args.session_dir)
        renders_dir = session_dir / "renders"
        descriptor_dir = Path(args.out_dir) if args.out_dir else session_dir / "descriptors"
        index_out = Path(args.index_out) if args.index_out else session_dir / "audio_descriptor_index.json"
        queue_map = _queue_map(session_dir)
        expected_rows = list(queue_map.values())
        wav_paths = [renders_dir / row["render_filename"] for row in expected_rows]
        mode = "session"
    elif args.renders_dir:
        renders_dir = Path(args.renders_dir)
        descriptor_dir = Path(args.out_dir) if args.out_dir else renders_dir.parent / "descriptors"
        index_out = Path(args.index_out) if args.index_out else renders_dir.parent / "audio_descriptor_index.json"
        wav_paths = sorted(renders_dir.glob("*.wav"))
        mode = "renders_dir"
    else:
        wav_paths = [Path(path) for path in args.wav]
        descriptor_dir = Path(args.out_dir) if args.out_dir else Path("als/catalog/audio/descriptors")
        index_out = Path(args.index_out) if args.index_out else Path("als/catalog/audio/index.json")

    descriptors = []
    missing = []
    for wav_path in wav_paths:
        queue_row = queue_map.get(wav_path.name)
        if not wav_path.exists():
            missing.append({
                "render_filename": wav_path.name,
                "expected_profile_id": queue_row.get("profile_id") if queue_row else None,
            })
            continue
        descriptor = _analyze_wav(wav_path, queue_row)
        descriptors.append(descriptor)
        descriptor_path = descriptor_dir / f"{wav_path.stem}.json"
        _write_json(descriptor_path, descriptor, args.force)

    index_payload = {
        "descriptor_version": DESCRIPTOR_VERSION,
        "mode": mode,
        "descriptor_count": len(descriptors),
        "missing_count": len(missing),
        "descriptor_dir": str(descriptor_dir),
        "descriptors": [
            {
                "profile_id": descriptor.get("profile_id"),
                "render_filename": descriptor["render_filename"],
                "audition_id": descriptor.get("audition_id"),
                "duration_s": descriptor["duration_s"],
                "peak_dbfs": descriptor["levels"]["peak_dbfs"],
                "centroid_hz": descriptor["spectral"]["centroid_hz"],
                "side_ratio": descriptor["stereo"]["side_ratio"],
            }
            for descriptor in descriptors
        ],
        "profile_summaries": _profile_summaries(descriptors),
        "missing_expected": missing,
    }
    _write_json(index_out, index_payload, args.force)
    print(json.dumps({
        "ok": True,
        "mode": mode,
        "descriptor_count": len(descriptors),
        "missing_count": len(missing),
        "descriptor_dir": str(descriptor_dir),
        "index_out": str(index_out),
    }, indent=2))


if __name__ == "__main__":
    main()
