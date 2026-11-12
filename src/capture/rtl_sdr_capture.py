"""Optional receive-only RTL-SDR capture adapter.

Requires the optional pyrtlsdr package and supported RTL-SDR hardware.
No transmit functionality is provided.
"""
from __future__ import annotations

import math
from numbers import Integral, Real


def _is_finite_positive_number(value: object) -> bool:
    return (
        isinstance(value, Real)
        and not isinstance(value, bool)
        and math.isfinite(value)
        and value > 0
    )


def capture_samples(
    center_frequency: float,
    sample_rate: float = 2.4e6,
    num_samples: int = 256_000,
    gain: float | str = "auto",
    device_index: int = 0,
):
    """Capture complex IQ samples from an RTL-SDR device.

    Frequency and sample-rate values must be finite positive numbers.
    Sample count must be a positive integer, and device index a
    non-negative integer. The SDR is closed even if configuration or
    capture raises an exception.
    """
    if not _is_finite_positive_number(center_frequency):
        raise ValueError("center_frequency must be a finite positive number")
    if not _is_finite_positive_number(sample_rate):
        raise ValueError("sample_rate must be a finite positive number")
    if (
        isinstance(num_samples, bool)
        or not isinstance(num_samples, Integral)
        or num_samples <= 0
    ):
        raise ValueError("num_samples must be a positive integer")
    if (
        isinstance(device_index, bool)
        or not isinstance(device_index, Integral)
        or device_index < 0
    ):
        raise ValueError("device_index must be a non-negative integer")

    try:
        from rtlsdr import RtlSdr
    except ImportError as exc:
        raise RuntimeError(
            "RTL-SDR support is optional. Install pyrtlsdr and its system driver first."
        ) from exc

    sdr = RtlSdr(device_index=int(device_index))
    try:
        sdr.sample_rate = float(sample_rate)
        sdr.center_freq = float(center_frequency)
        sdr.gain = gain
        return sdr.read_samples(int(num_samples))
    finally:
        sdr.close()
