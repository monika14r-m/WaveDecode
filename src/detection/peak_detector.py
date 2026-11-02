"""Noise-aware spectral peak detection."""
from __future__ import annotations

import numpy as np
from scipy.signal import find_peaks


def detect_peaks(
    frequencies,
    magnitudes,
    min_snr_db: float = 8.0,
    min_distance_bins: int = 4,
    max_dynamic_range_db: float = 50.0,
):
    """Find local maxima above a robust background and dynamic-range threshold."""
    freq = np.asarray(frequencies, dtype=float)
    mag = np.asarray(magnitudes, dtype=float)
    if freq.ndim != 1 or mag.ndim != 1 or freq.size != mag.size:
        raise ValueError("frequencies and magnitudes must be 1D arrays of equal length")
    if freq.size < 3:
        return []
    if not np.all(np.isfinite(freq)) or not np.all(np.isfinite(mag)):
        raise ValueError("Spectrum contains NaN or infinite values")
    if np.any(mag < 0):
        raise ValueError("magnitudes must be non-negative")
    if min_snr_db < 0 or min_distance_bins < 1 or max_dynamic_range_db <= 0:
        raise ValueError("Detection thresholds must be positive (min_snr_db may be zero)")

    eps = np.finfo(float).tiny
    mag_db = 20.0 * np.log10(np.maximum(mag, eps))
    noise_floor_db = float(np.median(mag_db))
    upper_background_db = float(np.percentile(mag_db, 90))
    threshold_db = max(
        noise_floor_db + float(min_snr_db),
        upper_background_db + 6.0,
        float(np.max(mag_db)) - max_dynamic_range_db,
    )
    prominence_db = max(2.0, min_snr_db / 2.0)
    indices, _ = find_peaks(
        mag_db,
        height=threshold_db,
        prominence=prominence_db,
        distance=int(min_distance_bins),
    )

    peaks = []
    for index in indices:
        peak_db = float(mag_db[index])
        peaks.append({
            "frequency": float(freq[index]),
            "magnitude": float(mag[index]),
            "magnitude_db": peak_db,
            "snr_db": peak_db - noise_floor_db,
            "frequency_bin": int(index),
        })
    return sorted(peaks, key=lambda item: item["magnitude"], reverse=True)
