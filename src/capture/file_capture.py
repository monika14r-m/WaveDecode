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

    max_samples limits the number of complex samples read from disk, not merely
    the returned array size. This bounds memory use for large recordings.
    Interleaved scalar formats must contain complete I/Q pairs across the whole
    file, including any tail beyond the requested sample limit.
    """
    file_path = Path(path).expanduser()
    if not file_path.is_file():
        raise FileNotFoundError(f"IQ file not found: {file_path}")
    if dtype not in _SUPPORTED:
        raise ValueError(f"Unsupported dtype '{dtype}'. Choose from: {', '.join(_SUPPORTED)}")
    if max_samples is not None and (not isinstance(max_samples, int) or isinstance(max_samples, bool) or max_samples <= 0):
        raise ValueError("max_samples must be a positive integer")

    item_dtype = _SUPPORTED[dtype]
    file_size = file_path.stat().st_size
    if file_size == 0:
        raise ValueError("IQ file is empty")
    if file_size % item_dtype.itemsize:
        raise ValueError(f"IQ file size is not aligned to the selected {dtype} format")

    # Interleaved formats store two scalar values for each complex sample.
    # Validate the entire file before applying max_samples so a malformed tail
    # cannot be silently hidden by a bounded read.
    values_per_sample = 1 if dtype in {"complex64", "complex128"} else 2
    if values_per_sample == 2 and (file_size // item_dtype.itemsize) % 2:
        raise ValueError("Interleaved IQ file must contain an even number of I/Q values")

    count = -1 if max_samples is None else max_samples * values_per_sample
    raw = np.fromfile(file_path, dtype=item_dtype, count=count)
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

    if samples.size == 0 or not np.all(np.isfinite(samples)):
        raise ValueError("IQ file contains no valid finite samples")
    return samples.astype(np.complex64, copy=False)
