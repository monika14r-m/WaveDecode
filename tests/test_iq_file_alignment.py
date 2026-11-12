import numpy as np
import pytest

from src.capture.file_capture import load_iq_file


@pytest.mark.parametrize(
    ("dtype", "values"),
    [
        ("int8", np.array([10, 20, 30], dtype=np.int8)),
        ("uint8", np.array([10, 20, 30], dtype=np.uint8)),
        ("float32", np.array([0.1, 0.2, 0.3], dtype=np.float32)),
    ],
)
def test_rejects_odd_interleaved_tail_even_when_max_samples_truncates_it(
    tmp_path, dtype, values
):
    path = tmp_path / "odd-tail.iq"
    values.tofile(path)

    with pytest.raises(ValueError, match="even number of I/Q values"):
        load_iq_file(path, dtype=dtype, max_samples=1)


def test_valid_bounded_interleaved_file_still_reads_requested_pairs(tmp_path):
    path = tmp_path / "valid.iq"
    np.array([10, 20, 30, 40, 50, 60], dtype=np.int8).tofile(path)

    samples = load_iq_file(path, dtype="int8", max_samples=2)

    assert samples.shape == (2,)
    assert samples[0].real == pytest.approx(10 / 128)
    assert samples[1].imag == pytest.approx(40 / 128)
