import argparse
import json
from pathlib import Path

from qwen_compression.plotting import PRIMARY_INK, SECONDARY_INK, SERIES_COLORS, new_figure, save_figure

REMOVED_FRACTIONS = (0.2, 0.4)
IMPORTANCE = "perturbation"
VARIANTS = ("sliced", "least_squares", "trained")
REDUCED_PRECISION = "original-bf16"
TESTED_LAYERS = (24, 20, 17, 10)
EARLIER_TESTED = (
    ("layer13-40-window", "w. 13", "layer-13-perturbation-40-trained"),
    ("layer13-40-code-only", "w. 13 (mapa 100% kod)", "layer-13-code-only-40-trained"),
    ("layer13-40-output", "w. 13 (cel na wyjściu)", "layer-13-perturbation-40-trained_output"),
    ("layer26-40-output", "w. 26 (cel na wyjściu)", "layer-26-perturbation-40-trained_output"),
)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--layers", type=Path, default=Path("results/phase2/code/layers"))
    parser.add_argument("--stage4", type=Path, default=Path("results/phase2/code/stage4"))
    parser.add_argument("--costs", type=Path, default=Path("results/phase2/code/map-layer-costs.json"))
    parser.add_argument("--code-evaluation", type=Path, default=Path("results/phase2/code-eval"))
    parser.add_argument("--figures", type=Path, default=Path("AGENTS/phases/phase-2/figures"))
    parser.add_argument("--output", type=Path, default=Path("results/phase2/code/layers/summary.json"))
    return parser.parse_args()


def layer_rows(directories: list[Path]) -> dict[int, dict[str, dict]]:
    rows: dict[int, dict[str, dict]] = {}
    for directory in directories:
        for path in sorted(directory.glob("layer-*/results.jsonl")):
            layer_index = int(path.parent.name.removeprefix("layer-"))
            for line in path.read_text().splitlines():
                row = json.loads(line)
                if row["variant"] == "original":
                    rows.setdefault(layer_index, {})["original"] = row
                elif row["importance"] == IMPORTANCE and row["variant"] in VARIANTS:
                    rows.setdefault(layer_index, {})[f"{row['variant']}-{row['removed_fraction']}"] = row
    return rows


def pooled_agreement(sets: dict, sources: tuple[str, ...], variant: str) -> float | None:
    if any(variant not in sets.get(source, {}) for source in sources):
        return None
    agreeing = sum(sets[source][variant]["top1_agreement"] * sets[source][variant]["tokens"] for source in sources)
    return agreeing / sum(sets[source][variant]["tokens"] for source in sources)


def solved_plus(code_evaluation: Path, name: str) -> int | None:
    solved = 0
    for dataset in ("humaneval", "mbpp"):
        path = code_evaluation / name / f"{dataset}-summary.json"
        if not path.exists():
            return None
        summary = json.loads(path.read_text())
        solved += sum(
            task["base_status"] == "pass" and task["plus_status"] == "pass" for task in summary["per_task"].values()
        )
    return solved


def kl_figure(rows: dict[int, dict[str, dict]], new_layers: set[int], figures: Path) -> None:
    figure, axes = new_figure(2, width_per_panel=6.0, height=4.2)
    layers = sorted(rows)
    bar_width = 0.8 / len(REMOVED_FRACTIONS)
    for axis, (metric, title) in zip(
        axes, (("kl_code", "KL na Pythonie po treningu"), ("kl_c4", "KL na tekście C4 po treningu")), strict=True
    ):
        for position, fraction in enumerate(REMOVED_FRACTIONS):
            centers, values = [], []
            for index, layer_index in enumerate(layers):
                row = rows[layer_index].get(f"trained-{fraction}")
                if row is not None:
                    centers.append(index + (position - (len(REMOVED_FRACTIONS) - 1) / 2) * bar_width)
                    values.append(row[metric])
            axis.bar(
                centers,
                values,
                width=bar_width - 0.03,
                color=SERIES_COLORS[position],
                label=f"usunięte {round(100 * fraction)}% neuronów",
            )
        axis.set_xticks(
            range(len(layers)), [f"{layer}" if layer in new_layers else f"{layer}*" for layer in layers], fontsize=8
        )
        axis.set_xlabel("warstwa (* = policzona wcześniej, etap 4b)")
        axis.set_ylabel("KL (mniej = bliżej oryginału)")
        axis.set_title(title, fontsize=10, loc="left")
    axes[0].legend(frameon=False, fontsize=8, labelcolor=PRIMARY_INK, loc="upper left")
    save_figure(
        figure, str(figures / "kod-warstwy-kl.png"), "Zmniejszenie jednej warstwy: KL po treningu w każdej warstwie"
    )


def map_figure(rows: dict[int, dict[str, dict]], costs: dict, figures: Path) -> dict[str, list]:
    figure, axes = new_figure(2, width_per_panel=6.0, height=4.2)
    points: dict[str, list] = {}
    for axis, fraction in zip(axes, REMOVED_FRACTIONS, strict=True):
        selected = [
            (costs[str(fraction)][layer_index], rows[layer_index][f"sliced-{fraction}"]["kl_code"], layer_index)
            for layer_index in sorted(rows)
            if f"sliced-{fraction}" in rows[layer_index]
        ]
        points[str(fraction)] = selected
        largest = max(max(point[0] for point in selected), max(point[1] for point in selected)) * 1.1
        axis.plot([0, largest], [0, largest], color=SECONDARY_INK, linewidth=0.8, linestyle="--")
        axis.scatter(
            [point[0] for point in selected],
            [point[1] for point in selected],
            c=[point[2] for point in selected],
            cmap="viridis",
            vmin=0,
            vmax=27,
            s=55,
            edgecolors="white",
            linewidths=1.5,
            zorder=3,
        )
        for predicted, measured, layer_index in selected:
            axis.annotate(
                f"{layer_index}",
                (predicted, measured),
                xytext=(5, 3),
                textcoords="offset points",
                fontsize=8,
                color=SECONDARY_INK,
            )
        axis.set_xlim(0, largest)
        axis.set_ylim(0, largest)
        axis.set_xlabel("przewidywany koszt z mapy")
        axis.set_ylabel("zmierzona KL na Pythonie po samym wycięciu")
        axis.set_title(
            f"usunięte {round(100 * fraction)}% (liczba = warstwa; linia: mapa trafia dokładnie)",
            fontsize=9,
            loc="left",
        )
    save_figure(figure, str(figures / "kod-warstwy-mapa.png"), "Czy mapa przewiduje skutek wycięcia w każdej warstwie?")
    return points


def agreement_figure(
    panels: list[tuple[str, list[tuple[str, float, int]], float]], original_solved: int, figures: Path
) -> None:
    figure, axes = new_figure(len(panels), width_per_panel=6.2, height=4.6)
    for axis, (title, agreement_points, noise_floor) in zip(axes, panels, strict=True):
        axis.axvline(100 * noise_floor, color=SECONDARY_INK, linewidth=1.0, linestyle="--")
        axis.axhline(original_solved, color=SECONDARY_INK, linewidth=0.8, linestyle=":")
        rightmost = max(agreement for _, agreement, _ in agreement_points)
        for position, (label, agreement, solved) in enumerate(agreement_points):
            axis.scatter(
                [100 * agreement],
                [solved],
                s=60,
                color=SERIES_COLORS[0] if "nowa" in label else SERIES_COLORS[1],
                edgecolors="white",
                linewidths=1.5,
                zorder=3,
            )
            axis.annotate(
                label.replace(" (nowa)", ""),
                (100 * agreement, solved),
                xytext=(-5 if agreement == rightmost else 5, 3 if position % 2 == 0 else -9),
                textcoords="offset points",
                ha="right" if agreement == rightmost else "left",
                fontsize=7,
                color=SECONDARY_INK,
            )
        bottom = axis.get_ylim()[0]
        axis.text(100 * noise_floor, bottom + 0.5, "oryginał w bf16 ", fontsize=7, color=SECONDARY_INK, ha="right")
        axis.text(
            axis.get_xlim()[0], original_solved + 0.5, f" oryginał ({original_solved})", fontsize=7, color=SECONDARY_INK
        )
        axis.set_xlabel("zgodność tokenu z oryginałem (%)")
        axis.set_ylabel("rozwiązane zadania HumanEval+ i MBPP+ (z 542)")
        axis.set_title(title, fontsize=10, loc="left")
        axis.text(
            0.02,
            0.97,
            "niebieskie: nowe warstwy (−40%)\npomarańczowe: wcześniejsze modele",
            transform=axis.transAxes,
            fontsize=7,
            color=SECONDARY_INK,
            va="top",
        )
    save_figure(
        figure,
        str(figures / "kod-warstwy-zgodnosc-testy.png"),
        "Czy zgodność tokenu przewiduje testy kodu nowych warstw?",
    )


def main() -> None:
    arguments = parse_arguments()
    new_rows = layer_rows([arguments.layers])
    rows = {**layer_rows([arguments.stage4]), **new_rows}
    costs = json.loads(arguments.costs.read_text())["costs"]
    agreement_path = arguments.code_evaluation / "token-agreement-layers.json"
    new_sets = json.loads(agreement_path.read_text())["sets"] if agreement_path.exists() else {}
    earlier_sets = json.loads((arguments.code_evaluation / "token-agreement-with-held-out.json").read_text())["sets"]
    table = []
    for layer_index in sorted(rows):
        for fraction in REMOVED_FRACTIONS:
            trained = rows[layer_index].get(f"trained-{fraction}")
            if trained is None:
                continue
            variant = f"layer-{layer_index:02d}-{IMPORTANCE}-{round(100 * fraction)}-trained"
            table.append(
                {
                    "layer": layer_index,
                    "removed_fraction": fraction,
                    "map_cost": costs[str(fraction)][layer_index],
                    **{
                        f"kl_code_{name}": rows[layer_index][f"{name}-{fraction}"]["kl_code"]
                        for name in VARIANTS
                        if f"{name}-{fraction}" in rows[layer_index]
                    },
                    "kl_c4_trained": trained["kl_c4"],
                    "wikitext2_perplexity": trained["wikitext2_perplexity"],
                    "original_perplexity": rows[layer_index]["original"]["wikitext2_perplexity"],
                    "agreement_code": pooled_agreement(new_sets, ("code",), variant),
                    "agreement_evalplus": pooled_agreement(new_sets, ("humaneval", "mbpp"), variant),
                    "agreement_held_out": pooled_agreement(new_sets, ("mbpp-held-out",), variant),
                    "solved_plus": solved_plus(arguments.code_evaluation, f"layer{layer_index}-40-window")
                    if fraction == 0.4 and layer_index in new_rows
                    else None,
                }
            )
    kl_figure(rows, set(new_rows), arguments.figures)
    map_points = map_figure(rows, costs, arguments.figures)
    original_solved = solved_plus(arguments.code_evaluation, "original")
    agreement_points: dict[str, list[tuple[str, float, int]]] = {}
    noise_floors: dict[str, float | None] = {}
    for key, sources, column in (
        ("evalplus", ("humaneval", "mbpp"), "agreement_evalplus"),
        ("held_out", ("mbpp-held-out",), "agreement_held_out"),
    ):
        points = []
        for name, label, variant in EARLIER_TESTED:
            solved = solved_plus(arguments.code_evaluation, name)
            agreement = pooled_agreement(earlier_sets, sources, variant)
            if solved is not None and agreement is not None:
                points.append((label, agreement, solved))
        for row in table:
            if row["solved_plus"] is not None and row[column] is not None:
                points.append((f"w. {row['layer']} (nowa)", row[column], row["solved_plus"]))
        agreement_points[key] = points
        noise_floors[key] = pooled_agreement(earlier_sets, sources, REDUCED_PRECISION)
    evalplus_floor, held_out_floor = noise_floors["evalplus"], noise_floors["held_out"]
    if original_solved is not None and evalplus_floor is not None and held_out_floor is not None:
        agreement_figure(
            [
                ("Zgodność na odpowiedziach na zadania testowe", agreement_points["evalplus"], evalplus_floor),
                ("Zgodność na 510 zadaniach spoza testów (K46 B)", agreement_points["held_out"], held_out_floor),
            ],
            original_solved,
            arguments.figures,
        )
    arguments.output.write_text(
        json.dumps({"table": table, "map_points": map_points, "agreement_points": agreement_points}, indent=2)
    )
    for row in table:
        print(json.dumps(row))


if __name__ == "__main__":
    main()
