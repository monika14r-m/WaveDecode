"""High-level spectrum and peak analysis for complex IQ recordings."""
from __future__ import annotations

import numpy as np

from src.detection.peak_detector import detect_peaks
from src.processing.fft_processor import compute_fft


def _occupied_bandwidth(frequencies: np.ndarray, magnitudes: np.ndarray, fraction: float = 0.99):
    power = np.asarray(magnitudes, dtype=float) ** 2
    total = float(np.sum(power))
    if total <= 0:
        return None
    order = np.argsort(frequencies)
    sorted_power = power[order]
    cumulative = np.cumsum(sorted_power) / total
    lower_pos = int(np.searchsorted(cumulative, (1.0 - fraction) / 2.0))
    upper_pos = int(np.searchsorted(cumulative, 1.0 - (1.0 - fraction) / 2.0))
    sorted_freq = frequencies[order]
    lower = float(sorted_freq[min(lower_pos, len(sorted_freq) - 1)])
    upper = float(sorted_freq[min(upper_pos, len(sorted_freq) - 1)])
    return {"lower_hz": lower, "upper_hz": upper, "bandwidth_hz": max(0.0, upper - lower)}


def analyze_signal(samples, sample_rate: float, window: str = "hann", min_snr_db: float = 8.0):
    data = np.asarray(samples)
    if data.ndim != 1 or data.size < 2:
        raise ValueError("samples must be a one-dimensional IQ array with at least two samples")
    frequencies, magnitudes = compute_fft(data, sample_rate, window=window)
    peaks = detect_peaks(frequencies, magnitudes, min_snr_db=min_snr_db)

    dominant_peak = peaks[0] if peaks else None
    if len(peaks) == 1:
        signal_type = "single-tone candidate"
    elif len(peaks) > 1:
        signal_type = "multi-tone candidate"
    else:
        signal_type = "noise-like / no prominent peaks"

    power = float(np.mean(np.abs(data) ** 2))
    peak_amplitude = float(np.max(np.abs(data)))
    rms_amplitude = float(np.sqrt(power))
    peak_to_average_db = (
        float(20.0 * np.log10(peak_amplitude / rms_amplitude))
        if rms_amplitude > 0 and peak_amplitude > 0 else None
    )

    return {
        "signal_type": signal_type,
        "sample_rate_hz": float(sample_rate),
        "sample_count": int(data.size),
        "duration_seconds": float(data.size / sample_rate),
        "frequency_resolution_hz": float(sample_rate / data.size),
        "peak_count": len(peaks),
        "dominant_frequency": dominant_peak["frequency"] if dominant_peak else None,
        "dominant_snr_db": dominant_peak["snr_db"] if dominant_peak else None,
        "mean_iq_power": power,
        "peak_to_average_db": peak_to_average_db,
        "occupied_bandwidth_99": _occupied_bandwidth(frequencies, magnitudes),
        "noise_floor_db": float(np.median(20.0 * np.log10(np.maximum(magnitudes, np.finfo(float).tiny)))),
        "window": window,
        "peaks": peaks,
    }
