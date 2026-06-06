from capture.simulator import generate_signal
from detection.analyzer import analyze_signal

SAMPLE_RATE = 10000

samples = generate_signal(
    frequency=1000,
    sample_rate=SAMPLE_RATE,
    duration=1
)

analysis = analyze_signal(
    samples,
    SAMPLE_RATE
)

print("\n=== WaveDecode Analysis ===")
print(f"Signal Type: {analysis['signal_type']}")
print(f"Peak Count: {analysis['peak_count']}")
print(f"Dominant Frequency: {analysis['dominant_frequency']} Hz")
