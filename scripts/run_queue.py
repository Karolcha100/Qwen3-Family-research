import argparse
import json
import os
import subprocess
import tempfile
import time
from pathlib import Path

from qwen_compression.progress import PROGRESS_ENVIRONMENT_VARIABLE, read_progress


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("queue", type=Path)
    parser.add_argument("--progress", type=Path, default=Path("AGENTS/postep-obliczen.json"))
    parser.add_argument("--update-seconds", type=float, default=10.0)
    return parser.parse_args()


def write_atomically(path: Path, data: dict) -> None:
    with tempfile.NamedTemporaryFile("w", dir=path.parent, delete=False, suffix=".tmp") as temporary:
        json.dump(data, temporary, ensure_ascii=False, indent=2)
    os.replace(temporary.name, path)


def main() -> None:
    arguments = parse_arguments()
    queue = json.loads(arguments.queue.read_text())
    state = {
        "title": queue["title"],
        "queue": str(arguments.queue),
        "pid": os.getpid(),
        "started_at": time.time(),
        "updated_at": time.time(),
        "finished_at": None,
        "steps": [
            {"name": step["name"], "estimate_seconds": 60 * step["estimate_minutes"], "status": "waiting"}
            for step in queue["steps"]
        ],
    }
    write_atomically(arguments.progress, state)
    fraction_path = arguments.progress.with_suffix(".fraction")
    for step, record in zip(queue["steps"], state["steps"], strict=True):
        fraction_path.unlink(missing_ok=True)
        record.update(status="running", started_at=time.time())
        log_path = Path(step["log"])
        log_path.parent.mkdir(parents=True, exist_ok=True)
        environment = {**os.environ, PROGRESS_ENVIRONMENT_VARIABLE: str(fraction_path.resolve())}
        with log_path.open("w") as log_file:
            process = subprocess.Popen(step["command"], stdout=log_file, stderr=subprocess.STDOUT, env=environment)
            while process.poll() is None:
                record["fraction"] = read_progress(fraction_path)
                state["updated_at"] = time.time()
                write_atomically(arguments.progress, state)
                time.sleep(arguments.update_seconds)
        record.update(
            status="done" if process.returncode == 0 else "failed",
            finished_at=time.time(),
            exit_code=process.returncode,
            fraction=1.0 if process.returncode == 0 else read_progress(fraction_path),
        )
        state["updated_at"] = time.time()
        write_atomically(arguments.progress, state)
    fraction_path.unlink(missing_ok=True)
    state["finished_at"] = state["updated_at"] = time.time()
    write_atomically(arguments.progress, state)


if __name__ == "__main__":
    main()
