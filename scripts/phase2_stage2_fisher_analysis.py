import argparse
import json
from pathlib import Path

import torch

from qwen_compression.analysis import spearman, top_overlap
from qwen_compression.plotting import PRIMARY_INK, SECONDARY_INK, SERIES_COLORS, new_figure, save_figure

PILOT_LAYERS = (2, 13, 25)
SEQUENCE_LENGTH = 2048


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--samples", type=int, default=64)
    parser.add_argument("--stage1", type=Path, default=Path("results/phase2/stage1"))
    parser.add_argument("--stage2", type=Path, default=Path("results/phase2/stage2"))
    parser.add_argument("--figures", type=Path, default=Path("AGENTS/phases/phase-2/figures"))
    parser.add_argument("--repeats", type=int, default=8)
    parser.add_argument("--seed", type=int, default=0)
    return parser.parse_args()


def mean_over(coefficients: torch.Tensor, sequences: list[int] | torch.Tensor) -> torch.Tensor:
    return coefficients[torch.as_tensor(sequences)].mean(dim=0)


def disjoint_set_agreement(
    coefficients: torch.Tensor, set_size: int, repeats: int, generator: torch.Generator
) -> list[float]:
    sequence_count, layer_count, _ = coefficients.shape
    per_layer = torch.zeros(layer_count, dtype=torch.float64)
    for _ in range(repeats):
        order = torch.randperm(sequence_count, generator=generator)
        first = mean_over(coefficients, order[:set_size])
        second = mean_over(coefficients, order[set_size : 2 * set_size])
        for layer_index in range(layer_count):
            per_layer[layer_index] += spearman(first[layer_index], second[layer_index])
    return (per_layer / repeats).tolist()


def main() -> None:
    arguments = parse_arguments()
    generator = torch.Generator().manual_seed(arguments.seed)
    stored = torch.load(arguments.stage2 / f"fisher-per-sequence-{arguments.samples}.pt")
    coefficients, sources = stored["coefficients"], stored["sources"]
    sequence_count, layer_count, _ = coefficients.shape
    full_map = coefficients.mean(dim=0)
    torch.save({"coefficients": full_map, "sequences": sequence_count}, arguments.stage2 / "fisher-map.pt")
    set_sizes = [size for size in (1, 2, 4, 8, 16, 32) if 2 * size <= sequence_count]
    agreement = {size: disjoint_set_agreement(coefficients, size, arguments.repeats, generator) for size in set_sizes}
    half = sequence_count // 2
    first_half, second_half = (
        mean_over(coefficients, list(range(half))),
        mean_over(coefficients, list(range(half, sequence_count))),
    )
    text_sequences = [index for index, source in enumerate(sources) if source == "c4"]
    code_sequences = [index for index, source in enumerate(sources) if source == "code"]
    text_map, code_map = mean_over(coefficients, text_sequences), mean_over(coefficients, code_sequences)
    text_halves = (
        mean_over(coefficients, text_sequences[: len(code_sequences)]),
        mean_over(coefficients, text_sequences[len(code_sequences) : 2 * len(code_sequences)]),
    )
    noise = torch.load(arguments.stage1 / "noise.pt")
    pilot: dict[str, dict[str, float]] = {}
    for layer_index in PILOT_LAYERS:
        exact = torch.load(arguments.stage1 / f"exact-layer-{layer_index:02d}.pt")["kl"][:, 0, :].mean(dim=1)
        noise_layer = noise[f"layer_{layer_index}"]
        noise_exact = noise_layer["kl"][:, 0, :].mean(dim=1)
        same_tokens = mean_over(coefficients, [0, 3])[layer_index]
        other_tokens = mean_over(coefficients, [4, 7])[layer_index]
        pilot[str(layer_index)] = {
            "fisher_vs_exact_same_tokens": spearman(same_tokens, exact),
            "fisher_vs_exact_same_tokens_top10_overlap": top_overlap(same_tokens, exact, 0.1),
            "fisher_vs_exact_same_tokens_sum_ratio": float(same_tokens.sum() / exact.sum()),
            "fisher_vs_exact_second_tokens": spearman(other_tokens[noise_layer["neurons"]], noise_exact),
            "exact_first_vs_second_tokens": spearman(exact[noise_layer["neurons"]], noise_exact),
            "fisher_first_vs_second_tokens": spearman(same_tokens, other_tokens),
            "fisher_full_map_vs_exact": spearman(full_map[layer_index], exact),
            "fisher_full_map_vs_exact_top10_overlap": top_overlap(full_map[layer_index], exact, 0.1),
        }
    summary = {
        "samples_per_sequence": arguments.samples,
        "sequences": sequence_count,
        "tokens": sequence_count * SEQUENCE_LENGTH,
        "pilot_layers": pilot,
        "disjoint_set_agreement_per_layer": {str(size): values for size, values in agreement.items()},
        "disjoint_set_agreement_mean": {str(size): sum(values) / len(values) for size, values in agreement.items()},
        "half_vs_half_spearman": [spearman(first_half[index], second_half[index]) for index in range(layer_count)],
        "half_vs_half_top10_overlap": [
            top_overlap(first_half[index], second_half[index], 0.1) for index in range(layer_count)
        ],
        "text_vs_code_spearman": [spearman(text_map[index], code_map[index]) for index in range(layer_count)],
        "text_vs_text_spearman_same_size": [
            spearman(text_halves[0][index], text_halves[1][index]) for index in range(layer_count)
        ],
        "kl_disabled_per_layer": {
            "median": full_map.median(dim=1).values.tolist(),
            "p10": full_map.quantile(0.1, dim=1).tolist(),
            "p90": full_map.quantile(0.9, dim=1).tolist(),
            "max": full_map.max(dim=1).values.tolist(),
            "sum": full_map.sum(dim=1).tolist(),
        },
    }
    (arguments.stage2 / "fisher-summary.json").write_text(json.dumps(summary, indent=2))
    figure, axes = new_figure(2, width_per_panel=5.0, height=3.6)
    axis = axes[0]
    tokens = [size * SEQUENCE_LENGTH for size in set_sizes]
    for position, layer_index in enumerate(PILOT_LAYERS):
        axis.plot(
            tokens,
            [agreement[size][layer_index] for size in set_sizes],
            color=SERIES_COLORS[position],
            linewidth=2,
            marker="o",
            markersize=4,
            label=f"przesiew, warstwa {layer_index}",
        )
    exact_agreement = [pilot[str(layer_index)]["exact_first_vs_second_tokens"] for layer_index in PILOT_LAYERS]
    axis.scatter(
        [2 * SEQUENCE_LENGTH] * len(PILOT_LAYERS),
        exact_agreement,
        color=PRIMARY_INK,
        marker="x",
        s=40,
        zorder=3,
        label="dokładnie (3 warstwy)",
    )
    axis.axhline(0.95, color=SECONDARY_INK, linewidth=1, linestyle="--")
    axis.set_xscale("log", base=2)
    axis.set_xlabel("tokenów w każdym z dwóch rozłącznych zbiorów")
    axis.set_ylabel("zgodność rankingów (Spearman)")
    axis.set_ylim(0, 1)
    axis.legend(frameon=False, fontsize=8, labelcolor=PRIMARY_INK)
    axis.set_title("Ile tokenów potrzeba do stabilnego rankingu", fontsize=10, loc="left")
    axis = axes[1]
    layers = list(range(layer_count))
    axis.fill_between(
        layers,
        summary["kl_disabled_per_layer"]["p10"],
        summary["kl_disabled_per_layer"]["p90"],
        color=SERIES_COLORS[0],
        alpha=0.18,
        linewidth=0,
    )
    axis.plot(layers, summary["kl_disabled_per_layer"]["median"], color=SERIES_COLORS[0], linewidth=2)
    axis.plot(layers, summary["kl_disabled_per_layer"]["max"], color=SERIES_COLORS[1], linewidth=1.5)
    axis.text(layers[-1], summary["kl_disabled_per_layer"]["median"][-1], " mediana", fontsize=8, va="center")
    axis.text(layers[-1], summary["kl_disabled_per_layer"]["max"][-1], " maks.", fontsize=8, va="center")
    axis.set_yscale("log")
    axis.set_xlabel("warstwa")
    axis.set_ylabel("przewidywana KL po wyłączeniu neuronu")
    axis.set_title("Mapa przesiewu: pasmo 10–90% neuronów warstwy", fontsize=10, loc="left")
    save_figure(
        figure,
        str(arguments.figures / "etap2-mapa-przesiewu.png"),
        f"Przesiew gradientem: {sequence_count} sekwencji × {SEQUENCE_LENGTH} tokenów",
    )
    print(json.dumps({key: summary[key] for key in ("pilot_layers", "disjoint_set_agreement_mean")}, indent=2))


if __name__ == "__main__":
    main()
