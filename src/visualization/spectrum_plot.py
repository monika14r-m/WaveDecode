import matplotlib.pyplot as plt

from capture.simulator import generate_signal
from processing.fft_processor import compute_fft


SAMPLE_RATE = 10000


samples = generate_signal(
    frequency=1000,
    sample_rate=SAMPLE_RATE,
    duration=1
)

freqs, mags = compute_fft(
    samples,
    SAMPLE_RATE
)

plt.figure(figsize=(10, 5))
plt.plot(freqs, mags)

plt.title("WaveDecode Spectrum")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude")

plt.grid()

plt.show()
