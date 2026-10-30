import argparse
import json
from pathlib import Path

import torch
from matplotlib.axes import Axes
from matplotlib.ticker import NullFormatter

from qwen_compression.analysis import spearman
from qwen_compression.plotting import PRIMARY_INK, SECONDARY_INK, SERIES_COLORS, new_figure, save_figure

PILOT_LAYERS = (2, 13, 25)
PILOT_SEQUENCES = [0, 3]
LAYER_COUNT = 28
TOP_FRACTION = 0.10
ASYMMETRY_THRESHOLD = 0.5


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage1", type=Path, default=Path("results/phase2/stage1"))
    parser.add_argument("--stage2", type=Path, default=Path("results/phase2/stage2"))
    parser.add_argument("--stage4", type=Path, default=Path("results/phase2/stage4"))
    parser.add_argument("--figures", type=Path, default=Path("AGENTS/phases/phase-pomysl/figures"))
    parser.add_argument("--layer", type=int, default=13)
    parser.add_argument("--removed-fraction", type=float, default=0.2)
    return parser.parse_args()


def diagonal(axis: Axes, low: float, high: float, scale: float = 1.0, label: str = "") -> None:
    axis.plot([low, high], [scale * low, scale * high], color=SECONDARY_INK, linewidth=1, linestyle="--", label=label)


def log_scatter(axis: Axes, horizontal: torch.Tensor, vertical: torch.Tensor, color: str, label: str) -> None:
    axis.scatter(horizontal, vertical, s=6, color=color, alpha=0.45, linewidths=0, label=label)
    axis.set_xscale("log")
    axis.set_yscale("log")


def exact_pilot_kl(stage1: Path, layer_index: int) -> torch.Tensor:
    return torch.load(stage1 / f"exact-layer-{layer_index:02d}.pt")["kl"].mean(dim=2).double()


def delta_squared_figure(arguments: argparse.Namespace) -> None:
    figure, axes = new_figure(2, width_per_panel=4.6, height=4.0)
    for position, layer_index in enumerate(PILOT_LAYERS):
        kl = exact_pilot_kl(arguments.stage1, layer_index)
        log_scatter(axes[0], kl[:, 0], kl[:, 1], SERIES_COLORS[position], f"warstwa {layer_index}")
        log_scatter(axes[1], kl[:, 0], kl[:, 3], SERIES_COLORS[position], f"warstwa {layer_index}")
    diagonal(axes[0], 1e-6, 2e-2, 0.25, "¼ × wyłączenie")
    diagonal(axes[1], 1e-6, 2e-2, 1.0, "tyle samo co wyłączenie")
    axes[0].set_title("Osłabienie o połowę (δ = −0,5)", fontsize=10, loc="left")
    axes[1].set_title("Podwojenie (δ = +1)", fontsize=10, loc="left")
    for axis in axes:
        axis.set_xlabel("KL po wyłączeniu neuronu (δ = −1)")
        axis.legend(frameon=False, fontsize=8, labelcolor=PRIMARY_INK, markerscale=2.5)
    axes[0].set_ylabel("KL po zaburzeniu")
    save_figure(
        figure,
        str(arguments.figures / "etap1-delta-kwadrat.png"),
        "Etap 1: skutek rośnie jak δ² (każdy punkt to jeden neuron, 3 × 3072 neuronów)",
    )


def two_texts_figure(arguments: argparse.Namespace) -> None:
    noise = torch.load(arguments.stage1 / "noise.pt")
    coefficients = torch.load(arguments.stage2 / "fisher-per-sequence-64.pt")["coefficients"].double()
    screening_same_tokens = coefficients[PILOT_SEQUENCES].mean(dim=0)
    figure, axes = new_figure(2, width_per_panel=4.6, height=4.0)
    for position, layer_index in enumerate(PILOT_LAYERS):
        stored = noise[f"layer_{layer_index}"]
        first_tokens = exact_pilot_kl(arguments.stage1, layer_index)[stored["neurons"], 0]
        second_tokens = stored["kl"][:, 0, :].mean(dim=1).double()
        screening = screening_same_tokens[layer_index, stored["neurons"]]
        log_scatter(
            axes[0],
            first_tokens,
            second_tokens,
            SERIES_COLORS[position],
            f"warstwa {layer_index} (Spearman {spearman(first_tokens, second_tokens):.2f})",
        )
        log_scatter(
            axes[1],
            first_tokens,
            screening,
            SERIES_COLORS[position],
            f"warstwa {layer_index} (Spearman {spearman(first_tokens, screening):.2f})",
        )
    for axis in axes:
        diagonal(axis, 1e-6, 1e-2)
        axis.set_xlabel("KL dokładnie, tekst A (4096 tokenów)")
        axis.legend(frameon=False, fontsize=8, labelcolor=PRIMARY_INK, markerscale=2.5)
    axes[0].set_ylabel("KL dokładnie, inny tekst B (4096 tokenów)")
    axes[1].set_ylabel("KL z przesiewu, ten sam tekst A")
    axes[0].set_title("Ten sam pomiar, inny tekst: duży rozrzut", fontsize=10, loc="left")
    axes[1].set_title("Przesiew vs dokładnie, ten sam tekst: zgodne", fontsize=10, loc="left")
    save_figure(
        figure,
        str(arguments.figures / "etap1-dwa-teksty.png"),
        "Etap 1: ranking zależy od tekstu, nie od metody (166 losowych neuronów na warstwę)",
    )


def text_code_figure(arguments: argparse.Namespace) -> None:
    summary = json.loads((arguments.stage2 / "fisher-summary.json").read_text())
    layers = list(range(LAYER_COUNT))
    figure, axes = new_figure(1, width_per_panel=8.0, height=3.8)
    axis = axes[0]
    for position, (key, label) in enumerate(
        (
            ("half_vs_half_spearman", "dwie połowy mapy (po 32 sekwencje, mieszanka)"),
            ("text_vs_text_spearman_same_size", "dwie porcje tekstu C4 (po 16 sekwencji)"),
            ("text_vs_code_spearman", "tekst C4 (48 sekwencji) vs kod (16 sekwencji)"),
        )
    ):
        axis.plot(
            layers, summary[key], color=SERIES_COLORS[position], linewidth=2, marker="o", markersize=4, label=label
        )
    axis.axhline(0, color=SECONDARY_INK, linewidth=0.8)
    axis.set_xlabel("warstwa")
    axis.set_ylabel("zgodność rankingów neuronów (Spearman)")
    axis.set_ylim(-0.3, 1.0)
    axis.legend(frameon=False, fontsize=8, labelcolor=PRIMARY_INK, loc="center right")
    save_figure(
        figure,
        str(arguments.figures / "etap2-tekst-kod.png"),
        "Etap 2: tekst i kod mają inne ważne neurony (porcje tekstu zgadzają się, tekst z kodem prawie wcale)",
    )


def screened_layers(arguments: argparse.Namespace) -> dict[int, dict[str, torch.Tensor]]:
    full_map = torch.load(arguments.stage2 / "fisher-map.pt")["coefficients"].double()
    coefficients = torch.load(arguments.stage2 / "fisher-per-sequence-64.pt")["coefficients"].double()
    screening_same_tokens = coefficients[PILOT_SEQUENCES].mean(dim=0)
    width = full_map.shape[1]
    layers = {}
    for layer_index in range(LAYER_COUNT):
        path = arguments.stage2 / f"layer-{layer_index:02d}.pt"
        if not path.exists():
            continue
        stored = torch.load(path)
        deltas = list(stored["deltas"])
        kl = stored["kl"].mean(dim=2).double()
        neurons = stored["neurons"]
        top = torch.zeros(width, dtype=torch.bool)
        top[full_map[layer_index].topk(int(TOP_FRACTION * width)).indices] = True
        layers[layer_index] = {
            "disabled": kl[:, deltas.index(-1.0)],
            "amplified": kl[:, deltas.index(1.0)],
            "screening": screening_same_tokens[layer_index, neurons],
            "top": top[neurons],
        }
    return layers


def screening_check_figure(arguments: argparse.Namespace, layers: dict[int, dict[str, torch.Tensor]]) -> None:
    figure, axes = new_figure(2, width_per_panel=4.8, height=4.0)
    disabled = torch.cat([values["disabled"] for values in layers.values()])
    screening = torch.cat([values["screening"] for values in layers.values()])
    top = torch.cat([values["top"] for values in layers.values()])
    log_scatter(axes[0], disabled[~top], screening[~top], SERIES_COLORS[0], "5% losowych")
    log_scatter(axes[0], disabled[top], screening[top], SERIES_COLORS[1], "10% najważniejszych")
    diagonal(axes[0], 1e-6, 6e-2)
    axes[0].set_xlabel("KL dokładnie (wyłączenie neuronu)")
    axes[0].set_ylabel("KL z przesiewu (te same tokeny)")
    axes[0].set_title("25 warstw, 11 500 neuronów", fontsize=10, loc="left")
    axes[0].legend(frameon=False, fontsize=8, labelcolor=PRIMARY_INK, markerscale=2.5)
    layer_indices = list(layers)
    axes[1].plot(
        layer_indices,
        [spearman(layers[index]["disabled"], layers[index]["screening"]) for index in layer_indices],
        color=SERIES_COLORS[0],
        linewidth=0,
        marker="o",
        markersize=7,
    )
    axes[1].set_ylim(0.9, 1.0)
    axes[1].set_xlabel("warstwa (bez 2, 13, 25: te są w etapie 1)")
    axes[1].set_ylabel("zgodność rankingów (Spearman)")
    axes[1].set_title("Zgodność w każdej warstwie", fontsize=10, loc="left")
    save_figure(
        figure,
        str(arguments.figures / "etap2-przesiew-vs-dokladnie.png"),
        "Etap 2: przesiew a pomiar dokładny w całym modelu",
    )


def asymmetry_figure(arguments: argparse.Namespace, layers: dict[int, dict[str, torch.Tensor]]) -> None:
    for layer_index in PILOT_LAYERS:
        kl = exact_pilot_kl(arguments.stage1, layer_index)
        layers[layer_index] = {"disabled": kl[:, 0], "amplified": kl[:, 3]}
    disabled = torch.cat([values["disabled"] for values in layers.values()])
    amplified = torch.cat([values["amplified"] for values in layers.values()])
    asymmetric = (amplified - disabled).abs() / torch.maximum(amplified, disabled) > ASYMMETRY_THRESHOLD
    figure, axes = new_figure(2, width_per_panel=4.8, height=4.0)
    log_scatter(axes[0], disabled[~asymmetric], amplified[~asymmetric], SERIES_COLORS[0], "symetryczne")
    log_scatter(axes[0], disabled[asymmetric], amplified[asymmetric], SERIES_COLORS[1], "asymetryczne (> 50%)")
    diagonal(axes[0], 1e-6, 6e-2)
    axes[0].set_xlabel("KL po wyłączeniu (δ = −1)")
    axes[0].set_ylabel("KL po podwojeniu (δ = +1)")
    axes[0].set_title("Każdy zmierzony dokładnie neuron", fontsize=10, loc="left")
    axes[0].legend(frameon=False, fontsize=8, labelcolor=PRIMARY_INK, markerscale=2.5)
    layer_indices = sorted(layers)
    disabling_worse, doubling_worse = [], []
    for layer_index in layer_indices:
        values = layers[layer_index]
        layer_asymmetric = (values["amplified"] - values["disabled"]).abs() / torch.maximum(
            values["amplified"], values["disabled"]
        ) > ASYMMETRY_THRESHOLD
        disabling_worse.append(int((layer_asymmetric & (values["disabled"] > values["amplified"])).sum()))
        doubling_worse.append(int((layer_asymmetric & (values["disabled"] <= values["amplified"])).sum()))
    axes[1].bar(layer_indices, disabling_worse, color=SERIES_COLORS[0], width=0.7, label="wyłączenie szkodzi bardziej")
    axes[1].bar(
        layer_indices,
        doubling_worse,
        bottom=disabling_worse,
        color=SERIES_COLORS[1],
        width=0.7,
        edgecolor="#fcfcfb",
        linewidth=1,
        label="podwojenie szkodzi bardziej",
    )
    axes[1].set_xlabel("warstwa (2, 13, 25: wszystkie neurony; reszta: 15%)")
    axes[1].set_ylabel("neurony asymetryczne")
    axes[1].set_title("Gdzie są i w którą stronę", fontsize=10, loc="left")
    axes[1].legend(frameon=False, fontsize=8, labelcolor=PRIMARY_INK)
    save_figure(
        figure,
        str(arguments.figures / "etap3-asymetria.png"),
        "Etap 3: wyłączenie a podwojenie neuronu (pomiar dokładny)",
    )


def neuron_choice_figure(arguments: argparse.Namespace) -> None:
    layer_index = arguments.layer
    screening = torch.load(arguments.stage2 / "fisher-map.pt")["coefficients"][layer_index].double()
    activation = torch.load(arguments.stage1 / "statistics.pt")["mean_absolute"][layer_index].double()
    width = screening.numel()
    removed = round(arguments.removed_fraction * width)
    removed_by_screening = torch.zeros(width, dtype=torch.bool)
    removed_by_activation = torch.zeros(width, dtype=torch.bool)
    removed_by_screening[screening.topk(removed, largest=False).indices] = True
    removed_by_activation[activation.topk(removed, largest=False).indices] = True
    groups = (
        (~removed_by_screening & ~removed_by_activation, "zostają w obu wyborach", "#b9b8b3"),
        (removed_by_screening & removed_by_activation, "wycięte w obu", SERIES_COLORS[2]),
        (removed_by_screening & ~removed_by_activation, "wycięte tylko wg przesiewu", SERIES_COLORS[0]),
        (~removed_by_screening & removed_by_activation, "wycięte tylko wg średniej |a|", SERIES_COLORS[1]),
    )
    figure, axes = new_figure(2, width_per_panel=4.8, height=4.0)
    for mask, label, color in groups:
        log_scatter(axes[0], activation[mask], screening[mask], color, f"{label} ({int(mask.sum())})")
    axes[0].xaxis.set_minor_formatter(NullFormatter())
    axes[0].set_xlabel("średnia |a| neuronu")
    axes[0].set_ylabel("przewidywana KL po wyłączeniu (przesiew)")
    axes[0].set_title(
        f"Warstwa {layer_index}: kogo wycinamy przy {round(100 * arguments.removed_fraction)}%", fontsize=10, loc="left"
    )
    axes[0].legend(frameon=False, fontsize=7.5, labelcolor=PRIMARY_INK, markerscale=2.5)
    rows = [
        json.loads(line)
        for line in (arguments.stage4 / f"layer-{layer_index:02d}" / "results.jsonl").read_text().splitlines()
    ]
    fractions = sorted({row["removed_fraction"] for row in rows if row["variant"] != "original"})
    kl = {
        (row["importance"], row["removed_fraction"], row["variant"]): row["kl"]
        for row in rows
        if row["variant"] != "original"
    }
    bar_width = 0.38
    for offset, (variant, label, color) in enumerate(
        (("least_squares", "+ najmniejsze kwadraty", SERIES_COLORS[0]), ("trained", "+ trening", SERIES_COLORS[2]))
    ):
        axes[1].bar(
            [position + (offset - 0.5) * bar_width for position in range(len(fractions))],
            [
                100 * kl[("perturbation", fraction, variant)] / kl[("perturbation", fraction, "sliced")]
                for fraction in fractions
            ],
            width=bar_width - 0.04,
            color=color,
            label=label,
        )
    axes[1].axhline(100, color=SECONDARY_INK, linewidth=1, linestyle="--")
    axes[1].set_xticks(range(len(fractions)), [f"{round(100 * fraction)}%" for fraction in fractions])
    axes[1].set_ylim(0, 135)
    axes[1].set_xlabel("wycięte neurony MLP")
    axes[1].set_ylabel("KL jako % KL samego wycięcia")
    axes[1].set_title("Ile KL zostaje po naprawie (wybór przesiewem)", fontsize=10, loc="left")
    axes[1].legend(frameon=False, fontsize=8, labelcolor=PRIMARY_INK, loc="upper left", ncol=2)
    save_figure(
        figure,
        str(arguments.figures / f"etap4-wybor-i-naprawa-{layer_index:02d}.png"),
        f"Etap 4: wybór neuronów i naprawa warstwy {layer_index}",
    )


def main() -> None:
    arguments = parse_arguments()
    delta_squared_figure(arguments)
    two_texts_figure(arguments)
    text_code_figure(arguments)
    layers = screened_layers(arguments)
    screening_check_figure(arguments, layers)
    asymmetry_figure(arguments, layers)
    neuron_choice_figure(arguments)


if __name__ == "__main__":
    main()
