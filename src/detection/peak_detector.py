import numpy as np


def detect_peaks(frequencies, magnitudes, threshold_ratio=0.6):
    threshold = np.max(magnitudes) * threshold_ratio

    peaks = []

    for freq, mag in zip(frequencies, magnitudes):
        if mag >= threshold:
            peaks.append(
                {
                    "frequency": float(freq),
                    "magnitude": float(mag)
                }
            )

    return peaks
