import matplotlib.pyplot as plt

from src.capture.simulator import generate_signal
from src.processing.fft_processor import compute_fft

SAMPLE_RATE = 10000

samples = generate_signal(
    frequencies=[1000],
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
plt.plot(freqs, mags, label="Spectrum")

plt.axvline(
    peak_freq,
    linestyle="--",
    label=f"Peak: {peak_freq:.2f} Hz"
)

plt.title("WaveDecode Spectrum")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude")
plt.grid(True)
plt.legend()

plt.show()
