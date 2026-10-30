import argparse
import json
from pathlib import Path

import numpy
import torch

from qwen_compression.analysis import spearman, top_overlap
from qwen_compression.plotting import PRIMARY_INK, SECONDARY_INK, SERIES_COLORS, new_figure, save_figure

DELTAS = (-1.0, -0.5, 0.5, 1.0)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", type=Path, default=Path("results/phase2/stage1"))
    parser.add_argument("--figures", type=Path, default=Path("AGENTS/phases/phase-2/figures"))
    parser.add_argument("--layers", type=int, nargs="+", default=[2, 13, 25])
    return parser.parse_args()


def precision_summary(results: Path) -> dict[str, float]:
    precision = torch.load(results / "precision.pt")
    count = len(precision["neuron_indices"])
    summary: dict[str, float] = {}
    for dtype_name in ("bfloat16", "float32"):
        kl = precision[f"kl_{dtype_name}"][:, 0]
        summary[f"{dtype_name}_control_max_abs"] = float(kl[:count].abs().max())
        summary[f"{dtype_name}_disabled_median"] = float(kl[count : 2 * count].median())
    return summary


def main() -> None:
    arguments = parse_arguments()
    arguments.figures.mkdir(parents=True, exist_ok=True)
    fisher = torch.load(arguments.results / "fisher.pt")["coefficients"]
    noise = torch.load(arguments.results / "noise.pt")
    statistics = torch.load(arguments.results / "statistics.pt")
    layer_summaries: dict[str, dict[str, object]] = {}
    scatter_figure, scatter_axes = new_figure(len(arguments.layers))
    distribution_figure, distribution_axes = new_figure(1, width_per_panel=6.0)
    for position, layer_index in enumerate(arguments.layers):
        exact = torch.load(arguments.results / f"exact-layer-{layer_index:02d}.pt")
        kl = exact["kl"]
        mean_kl = kl.mean(dim=2)
        layer_summary: dict[str, object] = {}
        disabled_summary: dict[str, float] = {}
        for delta_index, delta in enumerate(DELTAS):
            values = mean_kl[:, delta_index]
            predicted = fisher[layer_index] * delta**2
            delta_summary = {
                "kl_median": float(values.median()),
                "kl_p90": float(values.quantile(0.9)),
                "kl_max": float(values.max()),
                "fisher_spearman": spearman(predicted, values),
                "fisher_top10_overlap": top_overlap(predicted, values, 0.1),
                "fisher_sum_ratio": float(predicted.sum() / values.sum()),
            }
            layer_summary[f"delta_{delta}"] = delta_summary
            if delta == -1.0:
                disabled_summary = delta_summary
        disabled = mean_kl[:, 0]
        layer_summary["text_vs_code_spearman_disabled"] = spearman(kl[:, 0, 0], kl[:, 0, 1])
        layer_summary["mean_absolute_activation_spearman_disabled"] = spearman(
            statistics["mean_absolute"][layer_index], disabled
        )
        layer_summary["asymmetry_median"] = float(
            ((mean_kl[:, 3] - mean_kl[:, 0]).abs() / torch.maximum(mean_kl[:, 3], mean_kl[:, 0])).median()
        )
        noise_layer = noise[f"layer_{layer_index}"]
        first_set = mean_kl[noise_layer["neurons"], 0]
        second_set = noise_layer["kl"][:, 0, :].mean(dim=1)
        layer_summary["second_token_set_spearman_disabled"] = spearman(first_set, second_set)
        layer_summary["second_token_set_median_relative_difference"] = float(
            ((first_set - second_set).abs() / first_set).median()
        )
        layer_summaries[str(layer_index)] = layer_summary
        color = SERIES_COLORS[position]
        axis = scatter_axes[position]
        predicted = fisher[layer_index].numpy()
        axis.scatter(predicted, disabled.numpy(), s=4, color=color, alpha=0.35, linewidths=0)
        limits = [min(predicted.min(), disabled.min().item()), max(predicted.max(), disabled.max().item())]
        axis.plot(limits, limits, color=SECONDARY_INK, linewidth=1, linestyle="--")
        axis.set_xscale("log")
        axis.set_yscale("log")
        axis.set_xlabel("KL z przesiewu gradientem")
        axis.set_ylabel("KL dokładna")
        axis.set_title(
            f"warstwa {layer_index}: Spearman {disabled_summary['fisher_spearman']:.2f}",
            fontsize=10,
            loc="left",
        )
        bins = list(numpy.logspace(-9, 0, 80))
        distribution_axes[0].hist(
            disabled.numpy(), bins=bins, histtype="step", linewidth=2, color=color, label=f"warstwa {layer_index}"
        )
    distribution_axes[0].set_xscale("log")
    distribution_axes[0].set_xlabel("KL po wyłączeniu neuronu (δ = −1)")
    distribution_axes[0].set_ylabel("liczba neuronów")
    distribution_axes[0].legend(frameon=False, fontsize=9, labelcolor=PRIMARY_INK)
    save_figure(
        scatter_figure,
        str(arguments.figures / "etap1-przesiew-vs-dokladnie.png"),
        "Przesiew gradientem a dokładna KL (δ = −1)",
    )
    save_figure(
        distribution_figure, str(arguments.figures / "etap1-rozklad-kl.png"), "Rozkład skutku wyłączenia neuronu"
    )
    summary = {"precision": precision_summary(arguments.results), "layers": layer_summaries}
    (arguments.results / "summary.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
