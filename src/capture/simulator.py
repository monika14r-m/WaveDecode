"""Synthetic complex-baseband IQ signal generation for testing and demos."""
from __future__ import annotations

import math
from collections.abc import Iterable

import numpy as np


def generate_signal(
    frequencies: Iterable[float] | None = None,
    sample_rate: float = 10_000,
    duration: float = 1.0,
    amplitudes: Iterable[float] | None = None,
    phases: Iterable[float] | None = None,
    snr_db: float | None = None,
    seed: int | None = None,
    *,
    frequency: float | None = None,
) -> np.ndarray:
    """Generate complex IQ tones, optionally with additive white Gaussian noise.

    Frequencies are baseband offsets in Hz and must lie strictly inside
    (-sample_rate/2, sample_rate/2). The frequency keyword is retained as a
    backwards-compatible single-tone alias.
    """
    if not math.isfinite(sample_rate) or sample_rate <= 0:
        raise ValueError("sample_rate must be a positive finite number")
    if not math.isfinite(duration) or duration <= 0:
        raise ValueError("duration must be a positive finite number")

    if frequency is not None:
        if frequencies is not None:
            raise ValueError("Use either frequencies or frequency, not both")
        frequencies = [frequency]
    if frequencies is None:
        frequencies = [1_000.0]

    freq_list = [float(value) for value in frequencies]
    if not freq_list:
        raise ValueError("At least one tone frequency is required")
    if not all(math.isfinite(value) for value in freq_list):
        raise ValueError("Frequencies must be finite numbers")
    if any(abs(value) >= sample_rate / 2 for value in freq_list):
        raise ValueError("Every baseband frequency must be strictly inside the Nyquist interval")

    def expand(values: Iterable[float] | None, default: float, name: str) -> list[float]:
        result = [default] * len(freq_list) if values is None else [float(v) for v in values]
        if len(result) != len(freq_list):
            raise ValueError(f"{name} must contain one value per frequency")
        if not all(math.isfinite(v) for v in result):
            raise ValueError(f"{name} must contain finite values")
        return result

    amp_list = expand(amplitudes, 1.0, "amplitudes")
    phase_list = expand(phases, 0.0, "phases")
    if any(value < 0 for value in amp_list):
        raise ValueError("Amplitudes must be non-negative")

    count = max(1, int(round(sample_rate * duration)))
    time = np.arange(count, dtype=np.float64) / sample_rate
    samples = np.zeros(count, dtype=np.complex128)
    for freq, amp, phase in zip(freq_list, amp_list, phase_list):
        samples += amp * np.exp(1j * (2.0 * np.pi * freq * time + phase))

    if snr_db is not None:
        if not math.isfinite(snr_db):
            raise ValueError("snr_db must be finite")
        signal_power = float(np.mean(np.abs(samples) ** 2))
        if signal_power > 0:
            noise_power = signal_power / (10.0 ** (snr_db / 10.0))
            rng = np.random.default_rng(seed)
            noise = rng.normal(0.0, math.sqrt(noise_power / 2.0), count)
            noise = noise + 1j * rng.normal(0.0, math.sqrt(noise_power / 2.0), count)
            samples += noise

    return samples.astype(np.complex64)
