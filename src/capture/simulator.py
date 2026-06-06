import numpy as np


def generate_signal(
    frequencies=None,
    sample_rate=10000,
    duration=1.0
):
    if frequencies is None:
        frequencies = [1000]

    t = np.arange(
        0,
        duration,
        1 / sample_rate
    )

    signal = np.zeros(
        len(t),
        dtype=complex
    )

    for freq in frequencies:
        signal += np.exp(
            2j * np.pi * freq * t
        )

    return signal


if __name__ == "__main__":
    samples = generate_signal(
        frequencies=[1000, 2000]
    )

    print(
        f"Generated {len(samples)} IQ samples"
    )
