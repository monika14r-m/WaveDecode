"""JSON export for WaveDecode analysis results."""
from __future__ import annotations

import json
import os
from pathlib import Path
import tempfile

import numpy as np


def _json_default(value):
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, Path):
        return str(value)
    raise TypeError(f"Object of type {type(value).__name__} is not JSON serializable")


def export_analysis(analysis, filename="analysis.json") -> Path:
    """Write JSON atomically, creating parent directories when needed."""
    destination = Path(filename).expanduser()
    destination.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=f".{destination.name}.", suffix=".tmp", dir=str(destination.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(analysis, handle, indent=2, ensure_ascii=False, default=_json_default)
            handle.write("\n")
        os.replace(temporary, destination)
    except Exception:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise
    return destination
