import argparse
import json
from pathlib import Path

import torch
from matplotlib.ticker import MaxNLocator
from transformers import AutoModelForCausalLM

from qwen_compression.activations import collect_neuron_statistics
from qwen_compression.plotting import PRIMARY_INK, SECONDARY_INK, SERIES_COLORS, new_figure, save_figure

MODEL_NAME = "Qwen/Qwen3-0.6B-Base"
KINDS = ("martwy", "zbędny", "krytyczny", "masywny", "asymetryczny", "kodowy", "tekstowy")


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dead-relative", type=float, default=0.05)
    parser.add_argument("--redundant-relative", type=float, default=0.1)
    parser.add_argument("--critical-relative", type=float, default=100.0)
    parser.add_argument("--massive-ratio", type=float, default=300.0)
    parser.add_argument("--asymmetry", type=float, default=0.5)
    parser.add_argument("--source-ratio", type=float, default=2.0)
    parser.add_argument("--source-sequences", type=int, default=16)
    parser.add_argument("--data-path", type=Path, default=Path.home() / "qwen3-checkpoints/phase2/measurement-set.pt")
    parser.add_argument("--stage1", type=Path, default=Path("results/phase2/stage1"))
    parser.add_argument("--stage2", type=Path, default=Path("results/phase2/stage2"))
    parser.add_argument("--output", type=Path, default=Path("results/phase2/stage3"))
    parser.add_argument("--figures", type=Path, default=Path("AGENTS/phases/phase-pomysl/figures"))
    return parser.parse_args()


def per_source_mean_absolute(arguments: argparse.Namespace) -> dict[str, torch.Tensor]:
    path = arguments.output / "source-statistics.pt"
    if path.exists():
        return torch.load(path)
    stored = torch.load(arguments.data_path)
    token_ids, sources = (
        stored["token_ids"][: arguments.source_sequences],
        stored["sources"][: arguments.source_sequences],
    )
    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, dtype=torch.bfloat16, device_map="cuda").eval()
    result = {}
    for source in ("c4", "code"):
        rows = torch.tensor([index for index, name in enumerate(sources) if name == source])
        result[source] = collect_neuron_statistics(model, token_ids[rows], active_threshold=1e-2)["mean_absolute"]
    torch.save(result, path)
    del model
    torch.cuda.empty_cache()
    return result


def disabled_kl_map(arguments: argparse.Namespace) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    kl_disabled = torch.load(arguments.stage2 / "fisher-map.pt")["coefficients"].double()
    exact_disabled = torch.full_like(kl_disabled, float("nan"))
    exact_amplified = torch.full_like(kl_disabled, float("nan"))
    for layer_index in range(kl_disabled.shape[0]):
        exact_path = arguments.stage1 / f"exact-layer-{layer_index:02d}.pt"
        screened_path = arguments.stage2 / f"layer-{layer_index:02d}.pt"
        if exact_path.exists():
            kl = torch.load(exact_path)["kl"].mean(dim=2)
            exact_disabled[layer_index], exact_amplified[layer_index] = kl[:, 0], kl[:, 3]
        elif screened_path.exists():
            stored = torch.load(screened_path)
            kl = stored["kl"].mean(dim=2)
            deltas = list(stored["deltas"])
            exact_disabled[layer_index, stored["neurons"]] = kl[:, deltas.index(-1.0)]
            exact_amplified[layer_index, stored["neurons"]] = kl[:, deltas.index(1.0)]
    return kl_disabled, exact_disabled, exact_amplified


def main() -> None:
    arguments = parse_arguments()
    arguments.output.mkdir(parents=True, exist_ok=True)
    arguments.figures.mkdir(parents=True, exist_ok=True)
    statistics = torch.load(arguments.stage1 / "statistics.pt")
    sources = per_source_mean_absolute(arguments)
    kl_disabled, exact_disabled, exact_amplified = disabled_kl_map(arguments)
    measured = exact_disabled.isfinite()
    mean_absolute = statistics["mean_absolute"]
    median_kl = kl_disabled.median()
    layer_median_activation = mean_absolute.median(dim=1, keepdim=True).values
    code_to_text = sources["code"] / sources["c4"].clamp_min(1e-12)
    asymmetry = (exact_amplified - exact_disabled).abs() / torch.maximum(exact_amplified, exact_disabled)
    labels = {
        "martwy": mean_absolute < arguments.dead_relative * layer_median_activation,
        "zbędny": kl_disabled < arguments.redundant_relative * median_kl,
        "krytyczny": kl_disabled > arguments.critical_relative * median_kl,
        "masywny": statistics["max_absolute"] / mean_absolute.clamp_min(1e-12) > arguments.massive_ratio,
        "asymetryczny": measured & (asymmetry > arguments.asymmetry),
        "kodowy": code_to_text > arguments.source_ratio,
        "tekstowy": code_to_text < 1 / arguments.source_ratio,
    }
    torch.save({"labels": labels, "kl_disabled": kl_disabled, "measured": measured}, arguments.output / "labels.pt")
    flat_order = kl_disabled.flatten().argsort(descending=True)[:25]
    width = kl_disabled.shape[1]
    summary = {
        "thresholds": {key: value for key, value in vars(arguments).items() if isinstance(value, float)},
        "median_kl_disabled": float(median_kl),
        "measured_share": float(measured.double().mean()),
        "counts_total": {kind: int(mask.sum()) for kind, mask in labels.items()},
        "counts_per_layer": {kind: mask.sum(dim=1).tolist() for kind, mask in labels.items()},
        "kl_disabled_per_layer": {
            "median": kl_disabled.median(dim=1).values.tolist(),
            "p10": kl_disabled.quantile(0.1, dim=1).tolist(),
            "p90": kl_disabled.quantile(0.9, dim=1).tolist(),
            "sum": kl_disabled.sum(dim=1).tolist(),
        },
        "most_critical": [
            {
                "layer": int(index // width),
                "neuron": int(index % width),
                "kl_disabled": float(kl_disabled.flatten()[index]),
                "max_absolute": float(statistics["max_absolute"].flatten()[index]),
                "measured": bool(measured.flatten()[index]),
            }
            for index in flat_order
        ],
    }
    (arguments.output / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False))
    layers = list(range(kl_disabled.shape[0]))
    figure, axes = new_figure(4, rows=2, width_per_panel=3.6, height=2.8)
    for position, kind in enumerate(KINDS):
        axis = axes[position]
        axis.bar(layers, labels[kind].sum(dim=1).tolist(), color=SERIES_COLORS[position], width=0.8)
        axis.set_title(f"{kind} (razem {int(labels[kind].sum())})", fontsize=10, loc="left")
        axis.set_xlabel("warstwa")
        axis.set_ylabel("neurony")
        axis.set_ylim(bottom=0)
        axis.yaxis.set_major_locator(MaxNLocator(integer=True))
    axes[-1].axis("off")
    save_figure(
        figure, str(arguments.figures / "etap3-rodzaje-neuronow.png"), "Rodzaje neuronów w 28 warstwach Qwen3-0.6B"
    )
    figure, axes = new_figure(1, width_per_panel=7.5, height=3.6)
    axis = axes[0]
    axis.fill_between(
        layers,
        summary["kl_disabled_per_layer"]["p10"],
        summary["kl_disabled_per_layer"]["p90"],
        color=SERIES_COLORS[0],
        alpha=0.18,
        linewidth=0,
    )
    axis.plot(layers, summary["kl_disabled_per_layer"]["median"], color=SERIES_COLORS[0], linewidth=2)
    axis.set_yscale("log")
    axis.set_xlabel("warstwa")
    axis.set_ylabel("KL po wyłączeniu neuronu")
    axis.text(
        layers[-1],
        summary["kl_disabled_per_layer"]["median"][-1],
        "  mediana",
        color=PRIMARY_INK,
        fontsize=8,
        va="center",
    )
    axis.text(
        layers[0],
        summary["kl_disabled_per_layer"]["p90"][0],
        " pasmo 10–90% neuronów",
        color=SECONDARY_INK,
        fontsize=8,
        ha="left",
        va="bottom",
    )
    save_figure(
        figure, str(arguments.figures / "etap3-kl-w-warstwach.png"), "Skutek wyłączenia neuronu w kolejnych warstwach"
    )
    print(
        json.dumps(
            {key: summary[key] for key in ("median_kl_disabled", "measured_share", "counts_total")},
            indent=2,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
