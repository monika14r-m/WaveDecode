"""Optional receive-only RTL-SDR capture adapter.

Requires the optional pyrtlsdr package and supported RTL-SDR hardware.
No transmit functionality is provided.
"""
from __future__ import annotations


def capture_samples(
    center_frequency: float,
    sample_rate: float = 2.4e6,
    num_samples: int = 256_000,
    gain: float | str = "auto",
    device_index: int = 0,
):
    if center_frequency <= 0 or sample_rate <= 0 or num_samples <= 0:
        raise ValueError("center_frequency, sample_rate, and num_samples must be positive")
    try:
        from rtlsdr import RtlSdr
    except ImportError as exc:
        raise RuntimeError("RTL-SDR support is optional. Install pyrtlsdr and its system driver first.") from exc

    sdr = RtlSdr(device_index=device_index)
    try:
        sdr.sample_rate = float(sample_rate)
        sdr.center_freq = float(center_frequency)
        sdr.gain = gain
        return sdr.read_samples(int(num_samples))
    finally:
        sdr.close()
