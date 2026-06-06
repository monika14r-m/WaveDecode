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

    if peaks:
        dominant_peak = max(
            peaks,
            key=lambda peak: peak["magnitude"]
        )

        dominant_frequency = dominant_peak["frequency"]
    else:
        dominant_frequency = None

    analysis = {
        "peak_count": len(peaks),
        "dominant_frequency": dominant_frequency,
        "peaks": peaks
    }

    return analysis
