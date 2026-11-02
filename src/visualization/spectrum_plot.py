"""Spectrum plotting functions with no import-time side effects."""
from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np


def plot_spectrum(frequencies, magnitudes, peaks=None, title="WaveDecode Spectrum", save_path=None, show=True):
    freq = np.asarray(frequencies, dtype=float)
    mag = np.asarray(magnitudes, dtype=float)
    if freq.ndim != 1 or mag.ndim != 1 or freq.size != mag.size or freq.size == 0:
        raise ValueError("frequencies and magnitudes must be non-empty 1D arrays of equal length")

    fig, ax = plt.subplots(figsize=(11, 5))
    ax.plot(freq / 1e6, 20.0 * np.log10(np.maximum(mag, np.finfo(float).tiny)), linewidth=1.0, label="Magnitude")
    for peak in peaks or []:
        ax.axvline(peak["frequency"] / 1e6, linestyle="--", alpha=0.7)
        ax.annotate(f'{peak["frequency"] / 1e6:.5f} MHz', (peak["frequency"] / 1e6, peak["magnitude_db"]), xytext=(4, 7), textcoords="offset points", fontsize=8)
    ax.set_title(title)
    ax.set_xlabel("Baseband frequency offset (MHz)")
    ax.set_ylabel("Magnitude (dB relative)")
    ax.grid(True, alpha=0.25)
    fig.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=160, bbox_inches="tight")
    if show:
        plt.show()
    return fig, ax
