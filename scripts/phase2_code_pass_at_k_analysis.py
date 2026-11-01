import argparse
import json
import random
from pathlib import Path

from qwen_compression.code_metrics import pass_at_k
from qwen_compression.plotting import PRIMARY_INK, SECONDARY_INK, SERIES_COLORS, new_figure, save_figure

DATASETS = ("humaneval", "mbpp")
ATTEMPTS = (1, 2, 3)
REFERENCE = "original"
MODELS = (("original", "oryginał"), ("layer13-40-window", "w. 13 −40%, cel za warstwą"))
BOOTSTRAP_RESAMPLES = 10000


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--code-evaluation", type=Path, default=Path("results/phase2/code-eval"))
    parser.add_argument("--figures", type=Path, default=Path("AGENTS/phases/phase-2/figures"))
    parser.add_argument("--output", type=Path, default=Path("results/phase2/code-eval/pass-at-k-summary.json"))
    parser.add_argument("--seed", type=int, default=1)
    return parser.parse_args()


def task_counts(code_evaluation: Path, name: str) -> dict[str, dict[str, int]]:
    counts = {}
    for dataset in DATASETS:
        summary = json.loads((code_evaluation / f"{name}-sampled" / f"{dataset}-summary.json").read_text())
        counts.update(summary["per_task"])
    return counts


def greedy_solved(code_evaluation: Path, name: str, plus: bool) -> int:
    solved = 0
    for dataset in DATASETS:
        summary = json.loads((code_evaluation / name / f"{dataset}-summary.json").read_text())
        solved += sum(
            task["base_status"] == "pass" and (not plus or task["plus_status"] == "pass")
            for task in summary["per_task"].values()
        )
    return solved


def expected_solved(counts: dict[str, dict[str, int]], key: str, k: int, task_ids: list[str]) -> float:
    return sum(pass_at_k(counts[task_id]["samples"], counts[task_id][key], k) for task_id in task_ids)


def bootstrap_interval(differences: list[float], generator: random.Random) -> tuple[float, float]:
    totals = sorted(sum(generator.choices(differences, k=len(differences))) for _ in range(BOOTSTRAP_RESAMPLES))
    return totals[int(0.025 * BOOTSTRAP_RESAMPLES)], totals[int(0.975 * BOOTSTRAP_RESAMPLES) - 1]


def model_summary(counts: dict[str, dict[str, int]], key: str) -> dict[str, float | int]:
    task_ids = sorted(counts)
    summary: dict[str, float | int] = {
        f"expected_solved_{k}": expected_solved(counts, key, k, task_ids) for k in ATTEMPTS
    }
    summary["solved_at_least_once"] = sum(counts[task_id][key] > 0 for task_id in task_ids)
    summary["solved_every_time"] = sum(counts[task_id][key] == counts[task_id]["samples"] for task_id in task_ids)
    summary["tasks"] = len(task_ids)
    return summary


def paired_summary(
    reference: dict[str, dict[str, int]], compared: dict[str, dict[str, int]], key: str, generator: random.Random
) -> dict[str, object]:
    task_ids = sorted(reference)
    result: dict[str, object] = {
        "tasks_better": sum(compared[task_id][key] > reference[task_id][key] for task_id in task_ids),
        "tasks_worse": sum(compared[task_id][key] < reference[task_id][key] for task_id in task_ids),
    }
    for k in ATTEMPTS:
        differences = [
            pass_at_k(compared[task_id]["samples"], compared[task_id][key], k)
            - pass_at_k(reference[task_id]["samples"], reference[task_id][key], k)
            for task_id in task_ids
        ]
        low, high = bootstrap_interval(differences, generator)
        result[f"difference_{k}"] = {"value": sum(differences), "low": low, "high": high}
    return result


def figure(summaries: dict[str, dict], greedy: dict[str, int], paired: dict[str, dict], figures: Path) -> None:
    plot, axes = new_figure(2, width_per_panel=6.0, height=4.2)
    bar_width = 0.8 / len(MODELS)
    for position, (name, label) in enumerate(MODELS):
        centers = [index + (position - (len(MODELS) - 1) / 2) * bar_width for index in range(len(ATTEMPTS))]
        values = [summaries[name]["plus"][f"expected_solved_{k}"] for k in ATTEMPTS]
        axes[0].bar(centers, values, width=bar_width - 0.03, color=SERIES_COLORS[position], label=label)
        for center, value in zip(centers, values, strict=True):
            axes[0].text(center, value + 3, f"{value:.0f}", ha="center", fontsize=8, color=SECONDARY_INK)
        axes[0].scatter(
            [centers[0]],
            [greedy[name]],
            marker="_",
            s=300,
            color=PRIMARY_INK,
            zorder=3,
            label="jedna odpowiedź bez losowania" if position == 0 else None,
        )
    axes[0].set_xticks(range(len(ATTEMPTS)), [f"{k} {'próba' if k == 1 else 'próby'}" for k in ATTEMPTS])
    axes[0].set_ylabel("rozwiązane zadania HumanEval+ i MBPP+ (z 542)")
    axes[0].set_ylim(0, axes[0].get_ylim()[1] * 1.3)
    axes[0].set_title("Ile zadań model rozwiązuje w k próbach", fontsize=10, loc="left")
    axes[0].legend(frameon=False, fontsize=8, labelcolor=PRIMARY_INK, loc="upper left")
    compared_name = MODELS[1][0]
    for index, k in enumerate(ATTEMPTS):
        difference = paired[compared_name]["plus"][f"difference_{k}"]
        axes[1].errorbar(
            [index],
            [difference["value"]],
            yerr=[[difference["value"] - difference["low"]], [difference["high"] - difference["value"]]],
            fmt="o",
            color=SERIES_COLORS[1],
            ecolor=SERIES_COLORS[1],
            capsize=6,
            markersize=8,
        )
        axes[1].annotate(
            f"{difference['value']:+.1f}",
            (index, difference["value"]),
            xytext=(10, -3),
            textcoords="offset points",
            fontsize=8,
            color=SECONDARY_INK,
        )
    axes[1].axhline(0, color=SECONDARY_INK, linewidth=0.8)
    axes[1].set_xticks(range(len(ATTEMPTS)), [f"{k} {'próba' if k == 1 else 'próby'}" for k in ATTEMPTS])
    axes[1].set_xlim(-0.5, len(ATTEMPTS) - 0.5)
    axes[1].set_ylabel("różnica liczby zadań względem oryginału")
    axes[1].set_title("w. 13 −40% minus oryginał (95% przedział)", fontsize=10, loc="left")
    save_figure(plot, str(figures / "kod-k44-pass-at-k.png"), "pass@1–3 z 10 losowanych odpowiedzi na zadanie")


def main() -> None:
    arguments = parse_arguments()
    generator = random.Random(arguments.seed)
    counts = {name: task_counts(arguments.code_evaluation, name) for name, _ in MODELS}
    summaries = {
        name: {variant: model_summary(counts[name], f"correct_{variant}") for variant in ("base", "plus")}
        for name, _ in MODELS
    }
    greedy = {name: greedy_solved(arguments.code_evaluation, name, plus=True) for name, _ in MODELS}
    paired = {
        name: {
            variant: paired_summary(counts[REFERENCE], counts[name], f"correct_{variant}", generator)
            for variant in ("base", "plus")
        }
        for name, _ in MODELS
        if name != REFERENCE
    }
    figure(summaries, greedy, paired, arguments.figures)
    result = {"models": summaries, "greedy_plus_solved": greedy, "paired": paired}
    arguments.output.write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
