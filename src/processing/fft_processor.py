import numpy as np


def compute_fft(samples, sample_rate):
    fft_data = np.fft.fftshift(
        np.fft.fft(samples)
    )

    frequencies = np.fft.fftshift(
        np.fft.fftfreq(
            len(samples),
            d=1 / sample_rate
        )
    )

    magnitude = np.abs(fft_data)

    return frequencies, magnitude
