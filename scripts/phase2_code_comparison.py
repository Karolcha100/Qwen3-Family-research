import argparse
import json
import math
from pathlib import Path

from qwen_compression.plotting import PRIMARY_INK, SECONDARY_INK, SERIES_COLORS, new_figure, save_figure

PASS = "pass"
DATASETS = (("humaneval", "HumanEval"), ("mbpp", "MBPP"))
MODELS = (
    ("original", "oryginał", None),
    ("layer13-40-window", "w. 13 −40%, cel za warstwą", ("k31", "13", "perturbation", 0.4, "trained")),
    ("layer13-40-output", "w. 13 −40%, cel na wyjściu", ("k37", "13", "perturbation", 0.4, "trained_output")),
    ("layer13-40-code-only", "w. 13 −40%, mapa 100% kod", ("stage4", "13", "code-only", 0.4, "trained")),
    ("layer26-40-output", "w. 26 −40%, cel na wyjściu", ("k37", "26", "perturbation", 0.4, "trained_output")),
)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--code-evaluation", type=Path, default=Path("results/phase2/code-eval"))
    parser.add_argument("--code-results", type=Path, default=Path("results/phase2/code"))
    parser.add_argument("--figures", type=Path, default=Path("AGENTS/phases/phase-2/figures"))
    parser.add_argument("--output", type=Path, default=Path("results/phase2/code-eval/comparison.json"))
    return parser.parse_args()


def exact_mcnemar_p_value(gained: int, lost: int) -> float:
    changed = gained + lost
    if changed == 0:
        return 1.0
    tail = sum(math.comb(changed, count) for count in range(min(gained, lost) + 1)) / 2**changed
    return min(1.0, 2 * tail)


def solved_tasks(summary: dict, plus: bool) -> set[str]:
    return {
        task_id
        for task_id, task in summary["per_task"].items()
        if task["base_status"] == PASS and (not plus or task["plus_status"] == PASS)
    }


def kl_row(code_results: Path, source: tuple[str, str, str, float, str] | None) -> dict:
    if source is None:
        return {"kl_code": 0.0, "kl_c4": 0.0, "wikitext2_perplexity": None}
    directory, layer, importance, removed_fraction, variant = source
    for line in (code_results / directory / f"layer-{layer}" / "results.jsonl").read_text().splitlines():
        row = json.loads(line)
        if (
            row["importance"] == importance
            and row["removed_fraction"] == removed_fraction
            and row["variant"] == variant
        ):
            return {key: row[key] for key in ("kl_code", "kl_c4", "wikitext2_perplexity")}
    raise ValueError(f"missing row {source}")


def model_rows(code_evaluation: Path, code_results: Path) -> list[dict]:
    rows = []
    original_summaries = {
        dataset: json.loads((code_evaluation / "original" / f"{dataset}-summary.json").read_text())
        for dataset, _ in DATASETS
    }
    original_wikitext = json.loads(
        (code_results / "k31" / "layer-13" / "results.jsonl").read_text().splitlines()[0]
    ).get("wikitext2_perplexity")
    for name, label, source in MODELS:
        summaries = {
            dataset: json.loads((code_evaluation / name / f"{dataset}-summary.json").read_text())
            for dataset, _ in DATASETS
        }
        efficiency = {
            dataset: json.loads((code_evaluation / name / f"{dataset}-efficiency.json").read_text())
            for dataset, _ in DATASETS
        }
        row = {"name": name, "model": label, **kl_row(code_results, source)}
        if source is None:
            row["wikitext2_perplexity"] = original_wikitext
        for dataset, _ in DATASETS:
            summary = summaries[dataset]
            for plus in (False, True):
                key = f"{dataset}{'_plus' if plus else ''}"
                solved = solved_tasks(summary, plus)
                reference = solved_tasks(original_summaries[dataset], plus)
                row[key] = {
                    "solved": len(solved),
                    "tasks": summary["tasks"],
                    "gained": len(solved - reference),
                    "lost": len(reference - solved),
                    "p_value": exact_mcnemar_p_value(len(solved - reference), len(reference - solved)),
                }
            row[f"{dataset}_static"] = {
                metric: summary[f"mean_{metric}"]
                for metric in ("ruff_findings", "pyright_errors", "max_cyclomatic_complexity", "lines")
            }
            row[f"{dataset}_efficiency"] = {
                key: efficiency[dataset][key]
                for key in ("parameters", "peak_memory_bytes", "generated_tokens", "seconds", "tokens_per_second")
            }
        rows.append(row)
    return rows


def counts_figure(rows: list[dict], figures: Path) -> None:
    benchmarks = (
        ("humaneval", "HumanEval"),
        ("humaneval_plus", "HumanEval+"),
        ("mbpp", "MBPP"),
        ("mbpp_plus", "MBPP+"),
    )
    figure, axes = new_figure(2, width_per_panel=6.0, height=4.4)
    for axis, selected in zip(axes, (benchmarks[:2], benchmarks[2:]), strict=True):
        bar_width = 0.8 / len(rows)
        for position, row in enumerate(rows):
            centers = [index + (position - (len(rows) - 1) / 2) * bar_width for index in range(len(selected))]
            values = [row[key]["solved"] for key, _ in selected]
            axis.bar(centers, values, width=bar_width - 0.02, color=SERIES_COLORS[position], label=row["model"])
            for center, value in zip(centers, values, strict=True):
                axis.text(center, value + 1, str(value), ha="center", fontsize=7, color=SECONDARY_INK)
        task_count = rows[0][selected[0][0]]["tasks"]
        axis.set_xticks(range(len(selected)), [label for _, label in selected])
        axis.set_ylabel(f"rozwiązane zadania (z {task_count})")
        axis.set_title(f"{selected[0][1]}: {task_count} zadań", fontsize=10, loc="left")
    for axis in axes:
        axis.set_ylim(0, axis.get_ylim()[1] * 1.4)
    axes[0].legend(frameon=False, fontsize=7, labelcolor=PRIMARY_INK, loc="upper left", ncol=2)
    save_figure(
        figure,
        str(figures / "porownanie-liczba-zadan.png"),
        "Liczba rozwiązanych zadań: oryginał i modele z jedną zmniejszoną warstwą",
    )


def changes_figure(rows: list[dict], figures: Path) -> None:
    compared = rows[1:]
    figure, axes = new_figure(2, width_per_panel=6.0, height=4.0)
    for axis, (key, label) in zip(axes, (("humaneval_plus", "HumanEval+"), ("mbpp_plus", "MBPP+")), strict=True):
        positions = range(len(compared))
        gained = [row[key]["gained"] for row in compared]
        lost = [-row[key]["lost"] for row in compared]
        axis.barh(positions, gained, color=SERIES_COLORS[2], height=0.6, label="zyskane względem oryginału")
        axis.barh(positions, lost, color=SERIES_COLORS[7], height=0.6, label="stracone względem oryginału")
        for position, row in zip(positions, compared, strict=True):
            axis.text(
                row[key]["gained"] + 0.3,
                position,
                f"+{row[key]['gained']}",
                va="center",
                fontsize=8,
                color=SECONDARY_INK,
            )
            axis.text(
                -row[key]["lost"] - 0.3,
                position,
                f"−{row[key]['lost']}",
                va="center",
                ha="right",
                fontsize=8,
                color=SECONDARY_INK,
            )
        axis.axvline(0, color=SECONDARY_INK, linewidth=0.8)
        axis.set_yticks(list(positions), [row["model"] for row in compared], fontsize=8)
        axis.set_ylim(len(compared) + 0.7, -0.6)
        limit = max(max(gained), -min(lost)) + 4
        axis.set_xlim(-limit, limit)
        axis.set_xlabel("liczba zadań")
        axis.set_title(label, fontsize=10, loc="left")
    axes[1].legend(frameon=False, fontsize=8, labelcolor=PRIMARY_INK, loc="lower center", ncol=2)
    save_figure(
        figure,
        str(figures / "porownanie-zyski-straty.png"),
        "Które zadania zmieniły wynik względem oryginału (testy „+”)",
    )


def main() -> None:
    arguments = parse_arguments()
    rows = model_rows(arguments.code_evaluation, arguments.code_results)
    counts_figure(rows, arguments.figures)
    changes_figure(rows, arguments.figures)
    arguments.output.write_text(json.dumps(rows, indent=2, ensure_ascii=False))
    for row in rows:
        print(json.dumps(row, ensure_ascii=False))


if __name__ == "__main__":
    main()
