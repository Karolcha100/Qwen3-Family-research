import argparse
import json
from pathlib import Path

import torch

from qwen_compression.plotting import PRIMARY_INK, SERIES_COLORS, new_figure, save_figure

REMOVED_FRACTION = 0.4


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--map", type=Path, default=Path("results/phase2/code/stage2/fisher-map.pt"))
    parser.add_argument("--figures", type=Path, default=Path("AGENTS/phases/phase-2/figures"))
    parser.add_argument("--output", type=Path, default=Path("results/phase2/code/map-concentration.json"))
    return parser.parse_args()


def weakest_sum(coefficients: torch.Tensor) -> torch.Tensor:
    removed = round(coefficients.shape[1] * REMOVED_FRACTION)
    return coefficients.sort(dim=1).values[:, :removed].sum(dim=1)


def main() -> None:
    arguments = parse_arguments()
    stored = torch.load(arguments.map)
    combined, code, text = (stored[name].double() for name in ("coefficients", "code", "text"))
    layers = list(range(combined.shape[0]))
    summary = {
        "total_code": code.sum(dim=1).tolist(),
        "total_text": text.sum(dim=1).tolist(),
        "weakest_share_combined": (weakest_sum(combined) / combined.sum(dim=1)).tolist(),
        "weakest_cost_code": weakest_sum(code).tolist(),
        "weakest_cost_text": weakest_sum(text).tolist(),
    }
    figure, axes = new_figure(3, width_per_panel=4.8, height=4.0)
    axes[0].plot(layers, summary["total_code"], marker="o", markersize=4, linewidth=2, color=SERIES_COLORS[0])
    axes[0].set_yscale("log")
    axes[0].set_ylabel("suma ważności wszystkich neuronów (skala log.)")
    axes[0].set_title("1. Łączna ważność warstwy (Python)", fontsize=10, loc="left")
    axes[1].bar(layers, [100 * share for share in summary["weakest_share_combined"]], color=SERIES_COLORS[0])
    axes[1].set_ylabel("% ważności warstwy w najsłabszych 40% neuronów")
    axes[1].set_title("2. Ile ważności niesie najsłabsze 40%", fontsize=10, loc="left")
    for position, (key, label) in enumerate(
        (("weakest_cost_code", "mapa Pythona"), ("weakest_cost_text", "mapa tekstu"))
    ):
        axes[2].plot(
            layers, summary[key], marker="o", markersize=4, linewidth=2, color=SERIES_COLORS[position], label=label
        )
    axes[2].set_ylim(bottom=0)
    axes[2].set_ylabel("koszt usunięcia najsłabszych 40%")
    axes[2].set_title("3. Koszt −40%: Python a tekst", fontsize=10, loc="left")
    axes[2].legend(frameon=False, fontsize=8, labelcolor=PRIMARY_INK, loc="upper right")
    for axis in axes:
        axis.set_xlabel("warstwa")
        axis.set_xticks(range(0, len(layers), 3))
    save_figure(
        figure,
        str(arguments.figures / "kod-mapa-skupienie-waznosci.png"),
        "Dlaczego końcowe warstwy wychodzą tanie: ważność skupiona w kilku neuronach, głównie na Pythonie",
    )
    arguments.output.write_text(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
