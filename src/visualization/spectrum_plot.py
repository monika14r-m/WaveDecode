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

peak_index = mags.argmax()
peak_freq = freqs[peak_index]

print(f"Strongest frequency: {peak_freq:.2f} Hz")

plt.figure(figsize=(10, 5))
plt.plot(freqs, mags)

plt.axvline(peak_freq)

plt.title("WaveDecode Spectrum")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude")

plt.grid()

plt.show()
