"""Validated, windowed FFT helpers for complex IQ samples."""
from __future__ import annotations

import numpy as np

_WINDOWS = {
    "hann": np.hanning,
    "hamming": np.hamming,
    "blackman": np.blackman,
    "rectangular": lambda size: np.ones(size, dtype=np.float64),
    "boxcar": lambda size: np.ones(size, dtype=np.float64),
}


def compute_fft(samples, sample_rate: float, window: str = "hann"):
    """Return shifted baseband frequencies and coherent-gain-corrected magnitude.

    The magnitude is an approximate sinusoid amplitude for a bin-centred
    complex tone. This is a spectrum helper, not a calibrated RF power reading.
    """
    data = np.asarray(samples)
    if data.ndim != 1:
        raise ValueError("samples must be a one-dimensional array")
    if data.size < 2:
        raise ValueError("At least two IQ samples are required")
    if not np.isfinite(sample_rate) or sample_rate <= 0:
        raise ValueError("sample_rate must be positive and finite")
    if not np.all(np.isfinite(data)):
        raise ValueError("samples contain NaN or infinite values")
    if window not in _WINDOWS:
        raise ValueError(f"Unsupported window '{window}'. Choose from: {', '.join(_WINDOWS)}")

    weights = _WINDOWS[window](data.size)
    coherent_gain = float(np.mean(weights))
    if coherent_gain <= 0:
        raise ValueError("Window coherent gain must be positive")

    spectrum = np.fft.fftshift(np.fft.fft(data * weights))
    magnitude = np.abs(spectrum) / (data.size * coherent_gain)
    frequencies = np.fft.fftshift(np.fft.fftfreq(data.size, d=1.0 / sample_rate))
    return frequencies, magnitude.astype(np.float64)
