import numpy as np


def generate_signal(
    frequency=1000,
    sample_rate=10000,
    duration=1.0
):
    t = np.arange(
        0,
        duration,
        1 / sample_rate
    )

    signal = np.exp(
        2j * np.pi * frequency * t
    )

    return signal


if __name__ == "__main__":
    samples = generate_signal()

    print(
        f"Generated {len(samples)} IQ samples"
    )
