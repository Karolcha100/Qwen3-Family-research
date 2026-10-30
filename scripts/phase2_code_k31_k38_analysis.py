import argparse
import json
import math
from pathlib import Path

from matplotlib.axes import Axes

from qwen_compression.plotting import PRIMARY_INK, SERIES_COLORS, new_figure, save_figure

METRICS = (("kl_code", "KL na odłożonym Pythonie"), ("kl_c4", "KL na odłożonym tekście C4"))
STEPS = (("sliced", "samo wycięcie"), ("least_squares", "najmniejsze kwadraty"), ("trained", "trening"))
CODE_MODELS = (
    ("original", "oryginał"),
    ("layer13-40-window", "w. 13 −40%, cel za warstwą"),
    ("layer13-40-output", "w. 13 −40%, cel na wyjściu"),
    ("layer13-40-code-only", "w. 13 −40%, mapa 100% kod"),
    ("layer26-40-output", "w. 26 −40%, cel na wyjściu"),
)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--code-results", type=Path, default=Path("results/phase2/code"))
    parser.add_argument("--code-evaluation", type=Path, default=Path("results/phase2/code-eval"))
    parser.add_argument("--figures", type=Path, default=Path("AGENTS/phases/phase-2/figures"))
    return parser.parse_args()


def load_rows(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []


def find_row(rows: list[dict], importance: str, removed_fraction: float, variant: str) -> dict | None:
    return next(
        (
            row
            for row in rows
            if row["importance"] == importance
            and row["removed_fraction"] == removed_fraction
            and row["variant"] == variant
        ),
        None,
    )


def grouped_bars(axis: Axes, groups: list[str], series: list[tuple[str, list[float]]]) -> None:
    bar_width = 0.8 / len(series)
    for position, (label, values) in enumerate(series):
        axis.bar(
            [index + (position - (len(series) - 1) / 2) * bar_width for index in range(len(groups))],
            values,
            width=bar_width - 0.03,
            color=SERIES_COLORS[position],
            label=label,
        )
    axis.set_xticks(range(len(groups)), groups, fontsize=8)
    axis.legend(frameon=False, fontsize=8, labelcolor=PRIMARY_INK)


def starts_figure(rows: list[dict], figures: Path) -> list[dict]:
    starts = (
        ("perturbation", "mapa kodu 75/25"),
        ("activation-rms", "aktywacje (RMS)"),
        ("random", "losowo"),
        ("merged", "scalanie neuronów"),
    )
    table = []
    figure, axes = new_figure(2, width_per_panel=5.6, height=4.0)
    for axis, (metric, title) in zip(axes, METRICS, strict=True):
        series = []
        for step, step_label in STEPS:
            values = []
            for importance, _ in starts:
                row = find_row(rows, importance, 0.4, step)
                values.append(row[metric] if row else 0.0)
            series.append((step_label, values))
        grouped_bars(axis, [label for _, label in starts], series)
        axis.set_ylabel("KL do oryginału (nat / token)")
        axis.set_title(title, fontsize=10, loc="left")
    for importance, label in starts:
        for step, step_label in STEPS:
            row = find_row(rows, importance, 0.4, step)
            if row:
                table.append({"start": label, "step": step_label, "kl_code": row["kl_code"], "kl_c4": row["kl_c4"]})
    save_figure(
        figure, str(figures / "kod-k31-punkty-startu.png"), "K31: warstwa 13 −40%, cztery punkty startu, 16 epok"
    )
    return table


def map_weight_figure(rows: list[dict], figures: Path) -> list[dict]:
    maps = (
        ("code-only", "mapa 100% kod"),
        ("perturbation", "mapa 75% kod / 25% tekst"),
        ("previous-map", "mapa z tekstu"),
    )
    fractions = (0.2, 0.4)
    table = []
    figure, axes = new_figure(2, width_per_panel=5.2, height=4.0)
    for axis, (metric, title) in zip(axes, METRICS, strict=True):
        series = []
        for importance, label in maps:
            values = []
            for fraction in fractions:
                row = find_row(rows, importance, fraction, "trained")
                values.append(row[metric] if row else 0.0)
            series.append((label, values))
        grouped_bars(axis, [f"zmniejszenie o {round(100 * fraction)}%" for fraction in fractions], series)
        axis.set_ylabel("KL do oryginału (nat / token)")
        axis.set_title(f"{title}, po treningu", fontsize=10, loc="left")
    for importance, label in maps:
        for fraction in fractions:
            row = find_row(rows, importance, fraction, "trained")
            if row:
                table.append(
                    {"map": label, "removed_fraction": fraction, "kl_code": row["kl_code"], "kl_c4": row["kl_c4"]}
                )
    save_figure(figure, str(figures / "kod-k38-waga-kodu.png"), "K38: waga kodu w mapie (warstwa 13, 6 epok)")
    return table


def objective_figure(
    window_rows: dict[str, list[dict]], output_rows: dict[str, list[dict]], figures: Path
) -> list[dict]:
    cases = (("13", 0.4, "w. 13, −40%"), ("13", 0.2, "w. 13, −20%"), ("26", 0.4, "w. 26, −40%"))
    table = []
    figure, axes = new_figure(2, width_per_panel=5.2, height=4.0)
    for axis, (metric, title) in zip(axes, METRICS, strict=True):
        series: list[tuple[str, list[float]]] = [
            ("najmniejsze kwadraty", []),
            ("cel za warstwą", []),
            ("cel na wyjściu", []),
        ]
        for layer, fraction, _ in cases:
            least_squares = find_row(output_rows[layer], "perturbation", fraction, "least_squares")
            window = find_row(window_rows[layer], "perturbation", fraction, "trained")
            output = find_row(output_rows[layer], "perturbation", fraction, "trained_output")
            for (_, values), row in zip(series, (least_squares, window, output), strict=True):
                values.append(row[metric] if row else 0.0)
        grouped_bars(axis, [label for _, _, label in cases], series)
        axis.set_ylabel("KL do oryginału (nat / token)")
        axis.set_title(title, fontsize=10, loc="left")
    for layer, fraction, label in cases:
        for variant_label, rows, variant in (
            ("najmniejsze kwadraty", output_rows[layer], "least_squares"),
            ("cel za warstwą", window_rows[layer], "trained"),
            ("cel na wyjściu", output_rows[layer], "trained_output"),
        ):
            row = find_row(rows, "perturbation", fraction, variant)
            if row:
                table.append(
                    {"case": label, "variant": variant_label, "kl_code": row["kl_code"], "kl_c4": row["kl_c4"]}
                )
    save_figure(
        figure,
        str(figures / "kod-k37-cel-treningu.png"),
        "K37: cel treningu za następną warstwą czy na wyjściu modelu (6 epok)",
    )
    return table


def learning_rate_figure(
    window_rows: list[dict], output_rows: list[dict], small_step_rows: list[dict], figures: Path
) -> None:
    runs = (
        ("cel na wyjściu, krok 5e-5", find_row(output_rows, "perturbation", 0.2, "trained_output")),
        ("cel na wyjściu, krok 1e-5", find_row(small_step_rows, "perturbation", 0.2, "trained_output")),
    )
    figure, axes = new_figure(2, width_per_panel=5.2, height=4.0)
    for position, (label, row) in enumerate(runs):
        if row is None:
            continue
        losses = [row["output_kl_before"], *row["epoch_losses"]]
        axes[0].plot(
            range(len(losses)), losses, color=SERIES_COLORS[position + 1], linewidth=2, marker="o", label=label
        )
    axes[0].set_xlabel("epoka (0 = start po najmniejszych kwadratach)")
    axes[0].set_ylabel("KL na wyjściu, odłożona porcja treningowa")
    axes[0].set_title("Błąd walidacji w trakcie treningu", fontsize=10, loc="left")
    axes[0].legend(frameon=False, fontsize=8, labelcolor=PRIMARY_INK)
    variants = (
        ("najmniejsze\nkwadraty", find_row(small_step_rows, "perturbation", 0.2, "least_squares")),
        ("na wyjściu\nkrok 5e-5", runs[0][1]),
        ("na wyjściu\nkrok 1e-5", runs[1][1]),
        ("za warstwą\nkrok 5e-5", find_row(window_rows, "perturbation", 0.2, "trained")),
    )
    axes[1].bar(
        range(len(variants)),
        [row["kl_code"] if row else 0.0 for _, row in variants],
        color=[SERIES_COLORS[0], SERIES_COLORS[1], SERIES_COLORS[2], SERIES_COLORS[3]],
        width=0.6,
    )
    axes[1].set_xticks(range(len(variants)), [label for label, _ in variants], fontsize=8)
    axes[1].set_ylabel("KL do oryginału (nat / token)")
    axes[1].set_title("KL na odłożonym Pythonie po treningu", fontsize=10, loc="left")
    save_figure(
        figure, str(figures / "kod-k37-krok-uczenia.png"), "K37: mniejszy krok uczenia, warstwa 13, zmniejszenie o 20%"
    )


def code_summary(code_evaluation: Path) -> list[dict]:
    table = []
    for name, label in CODE_MODELS:
        summaries = {
            dataset: json.loads(path.read_text())
            for dataset in ("humaneval", "mbpp")
            if (path := code_evaluation / name / f"{dataset}-summary.json").exists()
        }
        efficiency = {
            dataset: json.loads(path.read_text())
            for dataset in ("humaneval", "mbpp")
            if (path := code_evaluation / name / f"{dataset}-efficiency.json").exists()
        }
        if len(summaries) < 2:
            continue
        table.append(
            {
                "model": label,
                "humaneval": summaries["humaneval"]["pass_at_1_base"],
                "humaneval_plus": summaries["humaneval"]["pass_at_1_plus"],
                "mbpp": summaries["mbpp"]["pass_at_1_base"],
                "mbpp_plus": summaries["mbpp"]["pass_at_1_plus"],
                "solved_tasks": {
                    dataset: sorted(
                        task_id
                        for task_id, task in summary["per_task"].items()
                        if task["base_status"] == task["plus_status"] == "pass"
                    )
                    for dataset, summary in summaries.items()
                },
                "mean_ruff_findings": {
                    dataset: summary["mean_ruff_findings"] for dataset, summary in summaries.items()
                },
                "mean_pyright_errors": {
                    dataset: summary["mean_pyright_errors"] for dataset, summary in summaries.items()
                },
                "mean_lines": {dataset: summary["mean_lines"] for dataset, summary in summaries.items()},
                "parameters": efficiency["humaneval"]["parameters"],
                "tokens_per_second": {dataset: values["tokens_per_second"] for dataset, values in efficiency.items()},
                "peak_memory_bytes": max(values["peak_memory_bytes"] for values in efficiency.values()),
            }
        )
    return table


def exact_mcnemar_p_value(gained: int, lost: int) -> float:
    changed = gained + lost
    if changed == 0:
        return 1.0
    tail = sum(math.comb(changed, count) for count in range(min(gained, lost) + 1)) / 2**changed
    return min(1.0, 2 * tail)


def paired_with_original(table: list[dict]) -> list[dict]:
    original = table[0]["solved_tasks"]
    comparison = []
    for row in table[1:]:
        for dataset in ("humaneval", "mbpp"):
            solved = set(row["solved_tasks"][dataset])
            reference = set(original[dataset])
            gained = len(solved - reference)
            lost = len(reference - solved)
            comparison.append(
                {
                    "model": row["model"],
                    "dataset": dataset,
                    "gained": gained,
                    "lost": lost,
                    "p_value": exact_mcnemar_p_value(gained, lost),
                }
            )
    return comparison


def code_figure(table: list[dict], figures: Path) -> None:
    benchmarks = (
        ("humaneval", "HumanEval"),
        ("humaneval_plus", "HumanEval+"),
        ("mbpp", "MBPP"),
        ("mbpp_plus", "MBPP+"),
    )
    figure, axes = new_figure(1, width_per_panel=10.0, height=4.2)
    grouped_bars(
        axes[0],
        [label for _, label in benchmarks],
        [(row["model"], [100 * row[key] for key, _ in benchmarks]) for row in table],
    )
    axes[0].set_ylabel("pass@1 (%)")
    save_figure(
        figure,
        str(figures / "kod-testy-pass1.png"),
        "Testy kodu EvalPlus: oryginał i modele z jedną zmniejszoną warstwą",
    )


def main() -> None:
    arguments = parse_arguments()
    code_results = arguments.code_results
    stage4_rows = {
        layer: load_rows(code_results / "stage4" / f"layer-{layer}" / "results.jsonl") for layer in ("13", "26")
    }
    output_rows = {
        layer: load_rows(code_results / "k37" / f"layer-{layer}" / "results.jsonl") for layer in ("13", "26")
    }
    summary = {
        "k31": starts_figure(load_rows(code_results / "k31" / "layer-13" / "results.jsonl"), arguments.figures),
        "k38": map_weight_figure(stage4_rows["13"], arguments.figures),
        "k37": objective_figure(stage4_rows, output_rows, arguments.figures),
        "k37_learning_rate": load_rows(code_results / "k37-lr1e-5" / "layer-13" / "results.jsonl"),
        "code": code_summary(arguments.code_evaluation),
    }
    learning_rate_figure(stage4_rows["13"], output_rows["13"], summary["k37_learning_rate"], arguments.figures)
    summary["code_paired"] = paired_with_original(summary["code"])
    code_figure(summary["code"], arguments.figures)
    (code_results / "k31-k38-summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False))
    for key in ("k31", "k38", "k37"):
        for row in summary[key]:
            print(key, json.dumps(row, ensure_ascii=False))
    for row in summary["code"]:
        print(
            "code", json.dumps({key: value for key, value in row.items() if key != "solved_tasks"}, ensure_ascii=False)
        )
    for row in summary["code_paired"]:
        print("paired", json.dumps(row, ensure_ascii=False))


if __name__ == "__main__":
    main()
