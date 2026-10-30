import os
from pathlib import Path

PROGRESS_ENVIRONMENT_VARIABLE = "QWEN_PROGRESS_FILE"


def report_progress(fraction: float) -> None:
    path = os.environ.get(PROGRESS_ENVIRONMENT_VARIABLE)
    if path is not None:
        Path(path).write_text(f"{min(max(fraction, 0.0), 1.0):.4f}")


def read_progress(path: Path) -> float | None:
    try:
        return float(path.read_text())
    except FileNotFoundError, ValueError:
        return None
