from processing.fft_processor import compute_fft
from detection.peak_detector import detect_peaks


def analyze_signal(samples, sample_rate):
    frequencies, magnitudes = compute_fft(
        samples,
        sample_rate
    )

    peaks = detect_peaks(
        frequencies,
        magnitudes
    )

    return peaks
