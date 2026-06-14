# WaveDecode

A Python-based signal analysis platform for capturing, processing, visualizing, and classifying radio frequency (RF) transmissions using Software Defined Radio (SDR).

---

## Overview

WaveDecode is an SDR-focused signal processing project that converts raw IQ samples into actionable signal intelligence through FFT analysis, signal detection, visualization, and classification workflows.

The project is designed to provide a modular pipeline that can be extended for RF research, spectrum monitoring, protocol analysis, and machine learning applications.

### Core Capabilities

| Capability              | Description                                   |
| ----------------------- | --------------------------------------------- |
| IQ Sample Processing    | Ingestion and preprocessing of SDR IQ samples |
| Spectrum Analysis       | FFT-based frequency-domain analysis           |
| Signal Detection        | Threshold-based signal identification         |
| Waterfall Visualization | Time-frequency spectrum visualization         |
| Signal Classification   | Rule-based classification framework           |
| SDR Integration         | Support for RTL-SDR devices                   |

---

## System Architecture

```text
SDR Device / IQ Simulator
        │
        ▼
   IQ Sample Ingestion
        │
        ▼
   FFT Processing
        │
        ▼
   Signal Detection
        │
        ▼
   Classification Engine
        │
        ▼
   Visualization Layer
```

---

## Project Structure

```text
WaveDecode/
├── src/
│   ├── iq_simulator.py
│   ├── fft_processor.py
│   ├── signal_detector.py
│   ├── spectrum_plot.py
│   └── classifier.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

### Components

| Module               | Responsibility                       |
| -------------------- | ------------------------------------ |
| `iq_simulator.py`    | Synthetic IQ sample generation       |
| `fft_processor.py`   | FFT computation and windowing        |
| `signal_detector.py` | Signal detection logic               |
| `spectrum_plot.py`   | Spectrum and waterfall visualization |
| `classifier.py`      | Signal classification framework      |

---

## Installation

### Requirements

* Python 3.8+
* NumPy
* SciPy
* Matplotlib
* PyRTLSDR (optional)

### Setup

```bash
git clone https://github.com/monika14r-m/WaveDecode.git

cd WaveDecode

pip install -r requirements.txt
```

### RTL-SDR Support

```bash
sudo apt install rtl-sdr

pip install pyrtlsdr
```

---

## Usage

### Spectrum Analysis with Simulated Signals

```bash
python src/spectrum_plot.py
```

### Processing SDR Samples

```python
from src.fft_processor import process_iq
from src.signal_detector import detect_signals

samples = capture_from_device(
    freq=433.92e6,
    sample_rate=2.4e6
)

fft_output = process_iq(samples)
signals = detect_signals(fft_output)
```

---

## Processing Pipeline

### 1. IQ Sample Acquisition

IQ samples are collected from either:

* RTL-SDR hardware
* Synthetic signal generators

### 2. Frequency Analysis

Fast Fourier Transform (FFT) is applied to convert time-domain samples into the frequency domain.

### 3. Signal Detection

Frequency peaks above configurable thresholds are identified as candidate transmissions.

### 4. Classification

Detected signals are passed through a rule-based classification engine that can later be extended with machine learning models.

### 5. Visualization

Results are displayed through spectrum plots and waterfall diagrams for interactive analysis.

---

## Development Roadmap

### Phase 1: Signal Processing Foundation

* [x] IQ sample simulator
* [x] FFT processing pipeline
* [x] Spectrum visualization

### Phase 2: SDR Integration

* [ ] RTL-SDR device support
* [ ] Signal detection engine
* [ ] Waterfall visualization

### Phase 3: Signal Intelligence

* [ ] Modulation classification
* [ ] Dataset generation tools
* [ ] Analysis dashboard

### Phase 4: Machine Learning

* [ ] Automated signal classification
* [ ] Model training pipeline
* [ ] Performance benchmarking

---

## Project Status

**Current Status:** Active Development

**Completed:** Signal simulation, FFT processing, spectrum visualization

**In Progress:** RTL-SDR integration and signal detection

---

## Future Extensions

* GNU Radio integration
* Additional SDR hardware support
* Real-time streaming pipeline
* Protocol fingerprinting
* Signal clustering and anomaly detection
* Machine learning–based modulation recognition

---

## Contributing

Contributions are welcome.

```bash
git checkout -b feature/new-feature

pytest tests/

git commit -m "Add feature"
```

Please open an issue before submitting major changes.

---

## License

Licensed under the MIT License.

See the LICENSE file for additional information.
