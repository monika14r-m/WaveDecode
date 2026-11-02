"""Load recorded IQ data from common raw interleaved formats."""
from __future__ import annotations

from pathlib import Path
import numpy as np

_SUPPORTED = {
    "complex64": np.dtype(np.complex64),
    "complex128": np.dtype(np.complex128),
    "int8": np.dtype(np.int8),
    "uint8": np.dtype(np.uint8),
    "float32": np.dtype(np.float32),
}


def load_iq_file(path, dtype: str = "complex64", max_samples: int | None = None) -> np.ndarray:
    """Load complex samples or interleaved I/Q pairs from a raw binary file.

    int8, uint8 and float32 inputs are interpreted as interleaved I,Q values.
    Integer formats are normalized approximately to [-1, 1].
    """
    file_path = Path(path).expanduser()
    if not file_path.is_file():
        raise FileNotFoundError(f"IQ file not found: {file_path}")
    if dtype not in _SUPPORTED:
        raise ValueError(f"Unsupported dtype '{dtype}'. Choose from: {', '.join(_SUPPORTED)}")
    if max_samples is not None and max_samples <= 0:
        raise ValueError("max_samples must be a positive integer")

    raw = np.fromfile(file_path, dtype=_SUPPORTED[dtype])
    if raw.size == 0:
        raise ValueError("IQ file is empty")

    if dtype in {"complex64", "complex128"}:
        samples = raw
    else:
        if raw.size % 2:
            raise ValueError("Interleaved IQ file must contain an even number of I/Q values")
        pairs = raw.reshape(-1, 2).astype(np.float32)
        if dtype == "int8":
            pairs /= 128.0
        elif dtype == "uint8":
            pairs = (pairs - 127.5) / 127.5
        samples = pairs[:, 0] + 1j * pairs[:, 1]

    if max_samples is not None:
        samples = samples[:max_samples]
    if samples.size == 0 or not np.all(np.isfinite(samples)):
        raise ValueError("IQ file contains no valid finite samples")
    return samples.astype(np.complex64, copy=False)
