import numpy as np
import matplotlib.pyplot as plt


class WaterfallPlot:
    def __init__(self, max_frames=100):
        self.max_frames = max_frames
        self.frames = []

    def update(self, fft_magnitudes):
        self.frames.append(fft_magnitudes)

        if len(self.frames) > self.max_frames:
            self.frames.pop(0)

    def show(self):
        plt.figure(figsize=(10, 6))

        plt.imshow(
            np.array(self.frames),
            aspect="auto",
            origin="lower",
            cmap="viridis"
        )

        plt.title("WaveDecode Waterfall")
        plt.xlabel("Frequency Bin")
        plt.ylabel("Time")

        plt.colorbar(label="Magnitude")
        plt.show()
