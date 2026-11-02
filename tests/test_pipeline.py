import json

import numpy as np
import pytest

from src.capture.file_capture import load_iq_file
from src.capture.simulator import generate_signal
from src.detection.analyzer import analyze_signal
from src.export.result_exporter import export_analysis
from src.processing.fft_processor import compute_fft
from src.visualization.waterfall_plot import compute_waterfall


def test_simulator_generates_expected_sample_count_and_dtype():
    samples = generate_signal([1_000], sample_rate=8_000, duration=0.25, seed=1)
    assert samples.shape == (2_000,)
    assert samples.dtype == np.complex64


def test_simulator_is_reproducible_with_seed_and_noise():
    first = generate_signal([500], sample_rate=8_000, duration=0.1, snr_db=15, seed=42)
    second = generate_signal([500], sample_rate=8_000, duration=0.1, snr_db=15, seed=42)
    np.testing.assert_array_equal(first, second)


@pytest.mark.parametrize("kwargs", [
    {"sample_rate": 0},
    {"duration": 0},
    {"frequencies": [5_000], "sample_rate": 10_000},
    {"frequencies": [1_000], "amplitudes": [1, 2]},
])
def test_simulator_rejects_invalid_configuration(kwargs):
    with pytest.raises(ValueError):
        generate_signal(**kwargs)


def test_fft_finds_bin_centred_complex_tone():
    sample_rate = 8_000
    samples = generate_signal([1_000], sample_rate=sample_rate, duration=1.0)
    frequencies, magnitudes = compute_fft(samples, sample_rate)
    peak_frequency = frequencies[int(np.argmax(magnitudes))]
    assert peak_frequency == pytest.approx(1_000, abs=1.0)
    assert float(np.max(magnitudes)) == pytest.approx(1.0, rel=0.02)


def test_analyzer_returns_expected_metadata_and_tone_peaks():
    sample_rate = 16_000
    samples = generate_signal(
        [1_250, 3_000],
        sample_rate=sample_rate,
        duration=1.0,
        amplitudes=[1.0, 0.6],
        snr_db=25,
        seed=7,
    )
    result = analyze_signal(samples, sample_rate, min_snr_db=8)
    assert result["signal_type"] == "multi-tone candidate"
    assert result["sample_count"] == 16_000
    assert result["duration_seconds"] == pytest.approx(1.0)
    assert result["frequency_resolution_hz"] == pytest.approx(1.0)
    detected = [peak["frequency"] for peak in result["peaks"]]
    assert any(abs(freq - 1_250) <= 2 for freq in detected)
    assert any(abs(freq - 3_000) <= 2 for freq in detected)


def test_iq_file_loads_interleaved_int8(tmp_path):
    path = tmp_path / "recording.iq"
    np.array([127, -128, 64, 0], dtype=np.int8).tofile(path)
    samples = load_iq_file(path, dtype="int8")
    assert samples.shape == (2,)
    assert samples[0].real == pytest.approx(127 / 128)
    assert samples[0].imag == pytest.approx(-1.0)
    assert samples[1].real == pytest.approx(0.5)
    assert samples[1].imag == pytest.approx(0.0)


def test_iq_loader_rejects_odd_interleaved_value_count(tmp_path):
    path = tmp_path / "broken.iq"
    np.array([1, 2, 3], dtype=np.int8).tofile(path)
    with pytest.raises(ValueError, match="even number"):
        load_iq_file(path, dtype="int8")


def test_iq_loader_respects_sample_limit(tmp_path):
    path = tmp_path / "complex.iq"
    np.array([1 + 2j, 3 + 4j, 5 + 6j], dtype=np.complex64).tofile(path)
    samples = load_iq_file(path, max_samples=2)
    assert samples.shape == (2,)


def test_waterfall_returns_frequency_time_and_level_matrix():
    samples = generate_signal([800], sample_rate=8_000, duration=0.5, snr_db=18, seed=3)
    frequencies, times, levels = compute_waterfall(samples, 8_000, nperseg=256)
    assert frequencies.shape == (256,)
    assert times.size > 1
    assert levels.shape == (frequencies.size, times.size)


def test_exporter_creates_parent_directory_and_valid_json(tmp_path):
    destination = tmp_path / "nested" / "result.json"
    path = export_analysis({"frequency": np.float64(1_000.0)}, destination)
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["frequency"] == 1_000.0
