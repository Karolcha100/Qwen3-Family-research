import argparse
import json
import subprocess
import tempfile
from pathlib import Path

from qwen_compression.code_metrics import pass_at_k

SANDBOX_IMAGE = "qwen-code-sandbox"
PASS = "pass"
MAXIMUM_K = 3


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--samples", type=Path, required=True)
    parser.add_argument("--dataset", choices=["humaneval", "mbpp"], required=True)
    parser.add_argument("--parallel", type=int, default=8)
    return parser.parse_args()


def sandbox_command(work_directory: Path, command: list[str]) -> list[str]:
    return [
        "podman",
        "run",
        "--rm",
        "--network=none",
        "--read-only",
        "--tmpfs=/tmp:size=1g",
        "--memory=8g",
        "--cpus=8",
        "--pids-limit=1024",
        "--userns=keep-id",
        "--volume=qwen-evalplus-cache:/cache",
        f"--volume={work_directory.resolve()}:/work:Z",
        SANDBOX_IMAGE,
        *command,
    ]


def run_tests(samples: Path, dataset: str, parallel: int) -> dict[str, list[dict[str, str]]]:
    work_directory = samples.parent
    sanitized = samples.with_name(samples.name.replace(".jsonl", "-sanitized.jsonl"))
    results_path = sanitized.with_name(sanitized.name.replace(".jsonl", "_eval_results.json"))
    results_path.unlink(missing_ok=True)
    subprocess.run(
        sandbox_command(work_directory, ["evalplus.sanitize", "--samples", f"/work/{samples.name}"]), check=True
    )
    subprocess.run(
        sandbox_command(
            work_directory,
            [
                "evalplus.evaluate",
                "--dataset",
                dataset,
                "--samples",
                f"/work/{sanitized.name}",
                "--parallel",
                str(parallel),
            ],
        ),
        check=True,
    )
    evaluation = json.loads(results_path.read_text())["eval"]
    return {
        task_id: [
            {"solution": run["solution"], "base_status": run["base_status"], "plus_status": run["plus_status"]}
            for run in runs
        ]
        for task_id, runs in evaluation.items()
    }


def correct_counts(runs: list[dict[str, str]]) -> dict[str, int]:
    return {
        "samples": len(runs),
        "correct_base": sum(run["base_status"] == PASS for run in runs),
        "correct_plus": sum(run["base_status"] == run["plus_status"] == PASS for run in runs),
    }


def mean_pass_at_k(counts: dict[str, dict[str, int]], key: str, k: int) -> float:
    return sum(pass_at_k(task["samples"], task[key], k) for task in counts.values()) / len(counts)


def file_name(task_id: str) -> str:
    return task_id.replace("/", "_") + ".py"


def static_analysis(solutions: dict[str, str]) -> dict[str, dict[str, float]]:
    with tempfile.TemporaryDirectory() as directory_name:
        directory = Path(directory_name)
        for task_id, solution in solutions.items():
            (directory / file_name(task_id)).write_text(solution)
        ruff_output = subprocess.run(
            ["ruff", "check", "--isolated", "--no-cache", "--select", "E9,F,B", "--output-format", "json", "."],
            check=False,
            cwd=directory,
            capture_output=True,
            text=True,
        ).stdout
        pyright_output = subprocess.run(
            ["pyright", "--outputjson", "."], check=False, cwd=directory, capture_output=True, text=True
        ).stdout
        radon_output = subprocess.run(
            ["radon", "cc", "--json", "."], check=False, cwd=directory, capture_output=True, text=True
        ).stdout
    ruff_counts: dict[str, int] = {}
    for diagnostic in json.loads(ruff_output or "[]"):
        name = Path(diagnostic["filename"]).name
        ruff_counts[name] = ruff_counts.get(name, 0) + 1
    pyright_counts: dict[str, int] = {}
    for diagnostic in json.loads(pyright_output)["generalDiagnostics"]:
        if diagnostic["severity"] == "error":
            name = Path(diagnostic["file"]).name
            pyright_counts[name] = pyright_counts.get(name, 0) + 1
    complexity: dict[str, float] = {}
    for path, blocks in json.loads(radon_output).items():
        if isinstance(blocks, list) and blocks:
            complexity[Path(path).name] = max(block["complexity"] for block in blocks)
    return {
        task_id: {
            "ruff_findings": ruff_counts.get(file_name(task_id), 0),
            "pyright_errors": pyright_counts.get(file_name(task_id), 0),
            "max_cyclomatic_complexity": complexity.get(file_name(task_id), 0.0),
            "lines": sum(1 for line in solution.splitlines() if line.strip()),
        }
        for task_id, solution in solutions.items()
    }


def main() -> None:
    arguments = parse_arguments()
    tasks = run_tests(arguments.samples, arguments.dataset, arguments.parallel)
    analysis = static_analysis({task_id: runs[0]["solution"] for task_id, runs in tasks.items()})
    counts = {task_id: correct_counts(runs) for task_id, runs in tasks.items()}
    task_count = len(tasks)
    sample_count = min(task["samples"] for task in counts.values())
    summary = {
        "dataset": arguments.dataset,
        "samples": str(arguments.samples),
        "tasks": task_count,
        "samples_per_task": sample_count,
        "pass_at_1_base": mean_pass_at_k(counts, "correct_base", 1),
        "pass_at_1_plus": mean_pass_at_k(counts, "correct_plus", 1),
        "pass_at_k": {
            variant: {
                str(k): mean_pass_at_k(counts, f"correct_{variant}", k)
                for k in range(1, min(MAXIMUM_K, sample_count) + 1)
            }
            for variant in ("base", "plus")
        },
        **{
            f"mean_{metric}": sum(values[metric] for values in analysis.values()) / task_count
            for metric in ("ruff_findings", "pyright_errors", "max_cyclomatic_complexity", "lines")
        },
        "per_task": {
            task_id: {
                "base_status": runs[0]["base_status"],
                "plus_status": runs[0]["plus_status"],
                **counts[task_id],
                **analysis[task_id],
            }
            for task_id, runs in tasks.items()
        },
    }
    output = arguments.samples.with_name(arguments.samples.name.replace(".jsonl", "-summary.json"))
    output.write_text(json.dumps(summary, indent=2))
    print(json.dumps({key: value for key, value in summary.items() if key != "per_task"}, indent=2))


if __name__ == "__main__":
    main()
