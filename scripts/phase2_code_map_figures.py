import argparse
import json
from pathlib import Path

import torch
from matplotlib.colors import LinearSegmentedColormap

from qwen_compression.plotting import (
    PRIMARY_INK,
    SECONDARY_INK,
    SEQUENTIAL_BLUE,
    SERIES_COLORS,
    new_figure,
    save_figure,
)

REMOVED_FRACTIONS = (0.2, 0.4)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--map", type=Path, default=Path("results/phase2/code/stage2/fisher-map.pt"))
    parser.add_argument("--stage4", type=Path, default=Path("results/phase2/code/stage4"))
    parser.add_argument("--figures", type=Path, default=Path("AGENTS/phases/phase-2/figures"))
    parser.add_argument("--output", type=Path, default=Path("results/phase2/code/map-layer-costs.json"))
    return parser.parse_args()


def removal_costs(coefficients: torch.Tensor) -> dict[float, list[float]]:
    ascending = coefficients.sort(dim=1).values
    neuron_count = coefficients.shape[1]
    return {
        fraction: ascending[:, : round(neuron_count * fraction)].sum(dim=1).tolist() for fraction in REMOVED_FRACTIONS
    }


def measured_kl(stage4: Path) -> dict[tuple[int, float], float]:
    measured = {}
    for path in sorted(stage4.glob("layer-*/results.jsonl")):
        layer_index = int(path.parent.name.removeprefix("layer-"))
        for line in path.read_text().splitlines():
            row = json.loads(line)
            if row["importance"] == "perturbation" and row["variant"] == "sliced":
                measured[(layer_index, row["removed_fraction"])] = row["kl_code"]
    return measured


def heatmap_figure(coefficients: torch.Tensor, figures: Path) -> None:
    descending = coefficients.sort(dim=1, descending=True).values
    relative = torch.log10(descending / coefficients.mean()).clamp(min=-3, max=2)
    figure, axes = new_figure(1, width_per_panel=10.0, height=5.6)
    colormap = LinearSegmentedColormap.from_list("sequential_blue", ["#f7f9fc", *SEQUENTIAL_BLUE])
    image = axes[0].imshow(relative.numpy(), aspect="auto", cmap=colormap, interpolation="nearest", vmin=-2, vmax=1.5)
    axes[0].grid(False)
    neuron_count = coefficients.shape[1]
    for fraction in REMOVED_FRACTIONS:
        axes[0].axvline(neuron_count * (1 - fraction), color=SERIES_COLORS[1], linewidth=1.2, linestyle="--")
        axes[0].text(
            neuron_count * (1 - fraction) + 15,
            -0.9,
            f"usuwane {round(100 * fraction)}% →",
            color=SERIES_COLORS[1],
            fontsize=8,
        )
    axes[0].set_yticks(range(0, coefficients.shape[0], 2))
    axes[0].set_ylabel("warstwa")
    axes[0].set_xlabel("neurony warstwy uporządkowane od najważniejszego do najmniej ważnego")
    colorbar = figure.colorbar(image, ax=axes[0], fraction=0.03)
    colorbar.set_label(
        "ważność względem średniej (log10; 0 = średnia, −1 = 10× mniej)", color=SECONDARY_INK, fontsize=8
    )
    colorbar.ax.tick_params(labelsize=8, colors=SECONDARY_INK)
    save_figure(
        figure,
        str(figures / "kod-mapa-warstwy.png"),
        "Mapa kodu (75% Python / 25% tekst): ważność neuronów w każdej warstwie",
    )


def cost_figure(costs: dict[float, list[float]], measured: dict[tuple[int, float], float], figures: Path) -> None:
    layer_count = len(costs[REMOVED_FRACTIONS[0]])
    figure, axes = new_figure(2, width_per_panel=6.0, height=4.2)
    bar_width = 0.8 / len(REMOVED_FRACTIONS)
    for position, fraction in enumerate(REMOVED_FRACTIONS):
        axes[0].bar(
            [index + (position - (len(REMOVED_FRACTIONS) - 1) / 2) * bar_width for index in range(layer_count)],
            costs[fraction],
            width=bar_width - 0.03,
            color=SERIES_COLORS[position],
            label=f"usunięcie {round(100 * fraction)}% najmniej ważnych",
        )
    measured_layers = sorted({layer_index for layer_index, _ in measured})
    for layer_index in measured_layers:
        axes[0].annotate(
            "▼",
            (layer_index, costs[REMOVED_FRACTIONS[-1]][layer_index] * 1.04),
            ha="center",
            color=PRIMARY_INK,
            fontsize=8,
        )
    axes[0].set_xticks(range(0, layer_count, 2))
    axes[0].set_xlabel("warstwa (▼ = warstwy już zmniejszane w etapie 4b)")
    axes[0].set_ylabel("suma ważności usuwanych neuronów")
    axes[0].set_title("Przewidywany koszt zmniejszenia warstwy (mniej = taniej)", fontsize=10, loc="left")
    axes[0].legend(frameon=False, fontsize=8, labelcolor=PRIMARY_INK)
    for position, fraction in enumerate(REMOVED_FRACTIONS):
        points = [
            (costs[fraction][layer_index], measured[(layer_index, fraction)], layer_index)
            for layer_index in measured_layers
            if (layer_index, fraction) in measured
        ]
        axes[1].scatter(
            [point[0] for point in points],
            [point[1] for point in points],
            s=50,
            color=SERIES_COLORS[position],
            edgecolors="white",
            linewidths=1.5,
            label=f"usunięcie {round(100 * fraction)}%",
            zorder=3,
        )
        for predicted, observed, layer_index in points:
            axes[1].annotate(
                f"w. {layer_index}",
                (predicted, observed),
                xytext=(5, 3),
                textcoords="offset points",
                fontsize=8,
                color=SECONDARY_INK,
            )
    axes[1].set_xlabel("przewidywany koszt z mapy")
    axes[1].set_ylabel("zmierzona KL na Pythonie po samym wycięciu")
    axes[1].set_title("Czy mapa przewiduje zmierzoną KL?", fontsize=10, loc="left")
    axes[1].legend(frameon=False, fontsize=8, labelcolor=PRIMARY_INK)
    save_figure(
        figure, str(figures / "kod-mapa-koszt-warstw.png"), "Które warstwy mają najwięcej mało ważnych neuronów"
    )


def main() -> None:
    arguments = parse_arguments()
    coefficients = torch.load(arguments.map)["coefficients"].double()
    costs = removal_costs(coefficients)
    measured = measured_kl(arguments.stage4)
    heatmap_figure(coefficients, arguments.figures)
    cost_figure(costs, measured, arguments.figures)
    summary = {
        "costs": {str(fraction): values for fraction, values in costs.items()},
        "ranking_cheapest_first": {
            str(fraction): sorted(range(len(values)), key=values.__getitem__) for fraction, values in costs.items()
        },
        "measured_sliced_kl_code": {
            f"{layer_index}-{fraction}": value for (layer_index, fraction), value in measured.items()
        },
    }
    arguments.output.write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary["ranking_cheapest_first"]))


if __name__ == "__main__":
    main()
