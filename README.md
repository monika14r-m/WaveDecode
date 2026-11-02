# WaveDecode

**WaveDecode** is a modular Python toolkit for generating, loading, analysing, and visualising complex-baseband IQ samples from software-defined radio (SDR) receivers.

This version focuses on a dependable receive-side signal-analysis foundation: it is **not** an arbitrary radio-protocol decoder and does not transmit RF.

## What works

- Reproducible synthetic IQ generation with multiple tones, amplitudes, phases, additive white Gaussian noise, and configurable SNR.
- Windowed, coherent-gain-corrected complex FFT with a shifted baseband frequency axis.
- Local-maximum peak detection with a noise-aware threshold, reported relative magnitude and estimated SNR.
- Signal summary: dominant peak, sample metadata, frequency resolution, relative noise floor, peak-to-average ratio, and 99% occupied-bandwidth estimate.
- Raw IQ file loading for complex64/complex128 and interleaved int8/uint8/float32 recordings.
- Time-frequency waterfall generation and plotting with actual time and frequency axes.
- Optional receive-only RTL-SDR capture adapter.
- JSON analysis export and a command-line interface.
- Automated tests for core DSP, file loading, waterfall generation, and export.

## Project structure

\`\`\`text
WaveDecode/
├── src/
│   ├── capture/
│   │   ├── file_capture.py
│   │   ├── rtl_sdr_capture.py
│   │   └── simulator.py
│   ├── detection/
│   │   ├── analyzer.py
│   │   └── peak_detector.py
│   ├── export/result_exporter.py
│   ├── processing/fft_processor.py
│   ├── visualization/
│   │   ├── spectrum_plot.py
│   │   └── waterfall_plot.py
│   └── main.py
├── tests/
├── requirements.txt
└── requirements-dev.txt
\`\`\`

## Install

Python 3.10+ is recommended.

### Windows PowerShell

\`\`\`powershell
git clone https://github.com/monika14r-m/WaveDecode.git
cd WaveDecode
python -m venv .venv
.venv\\Scripts\\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
\`\`\`

### macOS / Linux

\`\`\`bash
git clone https://github.com/monika14r-m/WaveDecode.git
cd WaveDecode
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
\`\`\`

## Quick start: simulated spectrum

From the repository root:

\`\`\`bash
python -m src.main
\`\`\`

The default demo creates two synthetic baseband tones with noise, prints an analysis report, and writes \`results/analysis.json\`.

Show the spectrum and waterfall:

\`\`\`bash
python -m src.main --plot --waterfall
\`\`\`

Choose simulation parameters and save a plot:

\`\`\`bash
python -m src.main --sample-rate 2400000 --duration 0.25 --frequencies 125000 430000 --snr-db 18 --plot-output results/spectrum.png
\`\`\`

## Analyse a raw IQ file

\`\`\`bash
python -m src.main --iq-file recordings/capture.iq --dtype complex64 --sample-rate 2400000 --output results/capture-analysis.json
\`\`\`

Supported raw formats:

| dtype | Expected layout |
|---|---|
| \`complex64\` | Native complex float samples |
| \`complex128\` | Native complex double samples |
| \`int8\` | Interleaved signed I, Q bytes |
| \`uint8\` | Interleaved unsigned I, Q bytes, centered at 127.5 |
| \`float32\` | Interleaved float32 I, Q values |

For RTL-SDR unsigned 8-bit recordings, use the \`uint8\` option. Always confirm the file's actual sample format and endianness; raw IQ files do not carry metadata.

## Optional RTL-SDR receive capture

Install the Python wrapper and the operating-system RTL-SDR driver:

\`\`\`bash
pip install pyrtlsdr
\`\`\`

Example:

\`\`\`python
from src.capture.rtl_sdr_capture import capture_samples
from src.detection.analyzer import analyze_signal

samples = capture_samples(
    center_frequency=433.92e6,
    sample_rate=2.4e6,
    num_samples=256_000,
    gain="auto",
)
report = analyze_signal(samples, sample_rate=2.4e6)
print(report)
\`\`\`

RTL-SDR hardware, drivers, frequency coverage, and gain availability vary. This adapter is receive-only. Monitor only signals and frequency bands you are legally permitted to receive. Do not use this project to intercept private communications or access-control signals.

## Python API

\`\`\`python
from src.capture.simulator import generate_signal
from src.detection.analyzer import analyze_signal

samples = generate_signal(
    frequencies=[1_000, 2_300],
    sample_rate=10_000,
    duration=1.0,
    amplitudes=[1.0, 0.5],
    snr_db=20,
    seed=7,
)
report = analyze_signal(samples, sample_rate=10_000, min_snr_db=8)
print(report["dominant_frequency"])
print(report["peaks"])
\`\`\`

## Tests

\`\`\`bash
pytest -q
\`\`\`

## Interpretation and limitations

- FFT magnitude is a relative spectrum estimate, not a calibrated dBm measurement. Correct RF power measurement requires device calibration, impedance knowledge, and gain-chain metadata.
- The peak detector is a configurable heuristic. Noise, interference, window choice, SNR, and nearby tones affect detections.
- Labels such as "single-tone candidate" and "multi-tone candidate" describe spectral shape only; they do not identify a modulation scheme or protocol.
- Occupied bandwidth is an approximate 99% power bandwidth of the analysed FFT frame.
- The RTL-SDR adapter only acquires IQ samples. It does not demodulate or decode protocol payloads.
- Raw IQ recordings can be large and may contain sensitive location or activity information. Store and share them carefully.

## Roadmap

1. Calibration-aware power measurements and detector benchmarks on labelled synthetic datasets.
2. AM/FM/FSK/PSK modulation feature extraction with clearly reported confidence and validation data.
3. Streaming SDR capture with buffer management and real-time waterfall.
4. Reproducible datasets and model evaluation before attempting ML-based modulation classification.

## License

MIT.
