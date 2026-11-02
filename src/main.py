"""WaveDecode command-line demo and IQ-file analysis entry point."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.capture.file_capture import load_iq_file
from src.capture.simulator import generate_signal
from src.detection.analyzer import analyze_signal
from src.export.result_exporter import export_analysis
from src.processing.fft_processor import compute_fft
from src.visualization.spectrum_plot import plot_spectrum
from src.visualization.waterfall_plot import compute_waterfall, plot_waterfall


def build_parser():
    parser = argparse.ArgumentParser(description="Analyze simulated or recorded complex IQ samples.")
    parser.add_argument("--iq-file", type=Path, help="Raw IQ file to analyze. If omitted, a synthetic example is generated.")
    parser.add_argument("--dtype", choices=["complex64", "complex128", "int8", "uint8", "float32"], default="complex64", help="IQ file data format")
    parser.add_argument("--sample-rate", type=float, default=10_000, help="Sample rate in samples/second")
    parser.add_argument("--duration", type=float, default=1.0, help="Demo duration in seconds")
    parser.add_argument("--frequencies", type=float, nargs="+", default=[1_000.0, 2_300.0], help="Demo baseband tone offsets in Hz")
    parser.add_argument("--snr-db", type=float, default=20.0, help="Demo signal-to-noise ratio in dB")
    parser.add_argument("--window", choices=["hann", "hamming", "blackman", "rectangular"], default="hann")
    parser.add_argument("--min-snr-db", type=float, default=8.0)
    parser.add_argument("--max-samples", type=int, default=2_000_000, help="Maximum IQ samples loaded from disk")
    parser.add_argument("--output", type=Path, default=Path("results/analysis.json"), help="JSON report destination")
    parser.add_argument("--plot", action="store_true", help="Display the spectrum plot")
    parser.add_argument("--waterfall", action="store_true", help="Display a time-frequency waterfall")
    parser.add_argument("--plot-output", type=Path, help="Optional spectrum PNG output path")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    if args.iq_file:
        samples = load_iq_file(args.iq_file, dtype=args.dtype, max_samples=args.max_samples)
    else:
        samples = generate_signal(
            frequencies=args.frequencies,
            sample_rate=args.sample_rate,
            duration=args.duration,
            snr_db=args.snr_db,
            seed=7,
        )

    analysis = analyze_signal(samples, args.sample_rate, window=args.window, min_snr_db=args.min_snr_db)
    output_path = export_analysis(analysis, args.output)
    print(json.dumps(analysis, indent=2))
    print(f"\nReport saved to: {output_path}")

    if args.plot or args.plot_output:
        frequencies, magnitudes = compute_fft(samples, args.sample_rate, window=args.window)
        plot_spectrum(frequencies, magnitudes, analysis["peaks"], save_path=args.plot_output, show=args.plot)
    if args.waterfall:
        frequencies, times, levels = compute_waterfall(samples, args.sample_rate)
        plot_waterfall(frequencies, times, levels)
    return analysis


if __name__ == "__main__":
    main()
