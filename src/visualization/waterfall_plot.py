"""Time-frequency waterfall generation and plotting."""
from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import stft


def compute_waterfall(samples, sample_rate: float, nperseg: int = 1024, noverlap: int | None = None):
    data = np.asarray(samples)
    if data.ndim != 1 or data.size < 4:
        raise ValueError("samples must be a one-dimensional array with at least four IQ samples")
    if not np.isfinite(sample_rate) or sample_rate <= 0:
        raise ValueError("sample_rate must be positive and finite")
    if nperseg < 4:
        raise ValueError("nperseg must be at least 4")
    nperseg = min(int(nperseg), data.size)
    if noverlap is None:
        noverlap = nperseg // 2
    if noverlap < 0 or noverlap >= nperseg:
        raise ValueError("noverlap must be in [0, nperseg)")

    frequencies, times, values = stft(
        data, fs=sample_rate, window="hann", nperseg=nperseg,
        noverlap=noverlap, return_onesided=False, boundary=None,
    )
    frequencies = np.fft.fftshift(frequencies)
    values = np.fft.fftshift(values, axes=0)
    magnitude_db = 20.0 * np.log10(np.maximum(np.abs(values), np.finfo(float).tiny))
    return frequencies, times, magnitude_db


def plot_waterfall(frequencies, times, magnitude_db, title="WaveDecode Waterfall", save_path=None, show=True):
    freq = np.asarray(frequencies, dtype=float)
    time = np.asarray(times, dtype=float)
    levels = np.asarray(magnitude_db, dtype=float)
    if levels.shape != (freq.size, time.size) or freq.size == 0 or time.size == 0:
        raise ValueError("magnitude_db must have shape (frequency_bins, time_frames)")
    fig, ax = plt.subplots(figsize=(11, 6))
    image = ax.pcolormesh(time, freq / 1e6, levels, shading="auto", cmap="viridis")
    ax.set_title(title)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Baseband frequency offset (MHz)")
    fig.colorbar(image, ax=ax, label="Magnitude (dB relative)")
    fig.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=160, bbox_inches="tight")
    if show:
        plt.show()
    return fig, ax


class WaterfallPlot:
    """Small rolling waterfall buffer for streaming magnitude frames."""
    def __init__(self, max_frames: int = 100, frequencies=None):
        if max_frames < 1:
            raise ValueError("max_frames must be positive")
        self.max_frames = int(max_frames)
        self.frames: list[np.ndarray] = []
        self.frequencies = None if frequencies is None else np.asarray(frequencies, dtype=float)

    def update(self, fft_magnitudes, frequencies=None):
        frame = np.asarray(fft_magnitudes, dtype=float).copy()
        if frame.ndim != 1 or frame.size == 0:
            raise ValueError("fft_magnitudes must be a non-empty 1D array")
        if frequencies is not None:
            axis = np.asarray(frequencies, dtype=float)
            if axis.shape != frame.shape:
                raise ValueError("frequencies must match the frame shape")
            self.frequencies = axis
        if self.frames and frame.shape != self.frames[0].shape:
            raise ValueError("All waterfall frames must have the same number of bins")
        self.frames.append(frame)
        self.frames = self.frames[-self.max_frames:]

    def show(self):
        if not self.frames:
            raise ValueError("No waterfall frames have been added")
        data = np.asarray(self.frames)
        fig, ax = plt.subplots(figsize=(11, 6))
        if self.frequencies is not None:
            extent = [float(self.frequencies[0] / 1e6), float(self.frequencies[-1] / 1e6), 0, len(data)]
            ax.imshow(20*np.log10(np.maximum(data, np.finfo(float).tiny)), aspect="auto", origin="lower", extent=extent, cmap="viridis")
            ax.set_xlabel("Baseband frequency offset (MHz)")
        else:
            ax.imshow(data, aspect="auto", origin="lower", cmap="viridis")
            ax.set_xlabel("Frequency bin")
        ax.set_ylabel("Frame")
        ax.set_title("WaveDecode Rolling Waterfall")
        fig.tight_layout()
        plt.show()
        return fig, ax
