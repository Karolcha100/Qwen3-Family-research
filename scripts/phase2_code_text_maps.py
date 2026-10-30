import argparse
import json
from pathlib import Path

import torch

from qwen_compression.plotting import PRIMARY_INK, SECONDARY_INK, SERIES_COLORS, new_figure, save_figure


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage1", type=Path, default=Path("results/phase2/stage1"))
    parser.add_argument("--stage2", type=Path, default=Path("results/phase2/stage2"))
    parser.add_argument("--figures", type=Path, default=Path("AGENTS/phases/phase-pomysl/figures"))
    parser.add_argument("--removed-fractions", type=float, nargs="+", default=[0.2, 0.4])
    parser.add_argument("--repeats", type=int, default=8)
    parser.add_argument("--seed", type=int, default=0)
    return parser.parse_args()


def normalized(importance: torch.Tensor) -> torch.Tensor:
    return importance / importance.sum(dim=1, keepdim=True)


def candidate_maps(
    coefficients: torch.Tensor, code_rows: list[int], text_rows: list[int], mean_absolute: torch.Tensor
) -> dict[str, torch.Tensor]:
    code_map, text_map = coefficients[code_rows].mean(dim=0), coefficients[text_rows].mean(dim=0)
    return {
        "tylko tekst": text_map,
        "mieszanka 75% tekst / 25% kod (obecna)": coefficients[code_rows + text_rows].mean(dim=0),
        "pół na pół": 0.5 * normalized(code_map) + 0.5 * normalized(text_map),
        "75% kod / 25% tekst": 0.75 * normalized(code_map) + 0.25 * normalized(text_map),
        "tylko kod": code_map,
        "średnia |a| (bez KL)": mean_absolute,
    }


def removed_damage(importance: torch.Tensor, evaluation: torch.Tensor, removed_fraction: float) -> float:
    removed = round(removed_fraction * importance.shape[1])
    indices = importance.topk(removed, dim=1, largest=False).indices
    return float(evaluation.gather(1, indices).sum())


def main() -> None:
    arguments = parse_arguments()
    stored = torch.load(arguments.stage2 / "fisher-per-sequence-64.pt")
    coefficients, sources = stored["coefficients"].double(), stored["sources"]
    mean_absolute = torch.load(arguments.stage1 / "statistics.pt")["mean_absolute"].double()
    code_rows = [index for index, source in enumerate(sources) if source == "code"]
    text_rows = [index for index, source in enumerate(sources) if source == "c4"]
    generator = torch.Generator().manual_seed(arguments.seed)
    damage: dict[float, dict[str, list[tuple[float, float]]]] = {
        fraction: {} for fraction in arguments.removed_fractions
    }
    for _ in range(arguments.repeats):
        code_order = [code_rows[index] for index in torch.randperm(len(code_rows), generator=generator)]
        text_order = [text_rows[index] for index in torch.randperm(len(text_rows), generator=generator)]
        code_half, text_half = len(code_order) // 2, len(text_order) // 2
        maps = candidate_maps(coefficients, code_order[:code_half], text_order[:text_half], mean_absolute)
        code_evaluation = coefficients[code_order[code_half:]].mean(dim=0)
        text_evaluation = coefficients[text_order[text_half:]].mean(dim=0)
        for fraction in arguments.removed_fractions:
            for name, importance in maps.items():
                damage[fraction].setdefault(name, []).append(
                    (
                        removed_damage(importance, code_evaluation, fraction),
                        removed_damage(importance, text_evaluation, fraction),
                    )
                )
    summary: dict[str, dict[str, dict[str, float]]] = {}
    for fraction, per_map in damage.items():
        best_code = sum(code for code, _ in per_map["tylko kod"]) / arguments.repeats
        best_text = sum(text for _, text in per_map["tylko tekst"]) / arguments.repeats
        summary[str(fraction)] = {
            name: {
                "code_damage_relative": sum(code for code, _ in values) / arguments.repeats / best_code,
                "text_damage_relative": sum(text for _, text in values) / arguments.repeats / best_text,
            }
            for name, values in per_map.items()
        }
    (arguments.stage2 / "code-text-maps.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False))
    figure, axes = new_figure(len(arguments.removed_fractions), width_per_panel=4.6, height=4.2)
    bar_width = 0.38
    for position, (axis, fraction) in enumerate(zip(axes, arguments.removed_fractions, strict=True)):
        names = list(summary[str(fraction)])
        for offset, (key, label, color) in enumerate(
            (
                ("code_damage_relative", "szkoda dla kodu", SERIES_COLORS[0]),
                ("text_damage_relative", "szkoda dla tekstu", SERIES_COLORS[1]),
            )
        ):
            axis.barh(
                [position + (offset - 0.5) * bar_width for position in range(len(names))],
                [summary[str(fraction)][name][key] for name in names],
                height=bar_width - 0.04,
                color=color,
                label=label,
            )
        axis.axvline(1, color=SECONDARY_INK, linewidth=1, linestyle="--")
        axis.set_yticks(range(len(names)), names if position == 0 else [""] * len(names), fontsize=8)
        axis.invert_yaxis()
        axis.set_xlabel("szkoda / najmniejsza możliwa (1 = najlepiej)")
        axis.set_title(f"Wycięte {round(100 * fraction)}% neuronów w każdej warstwie", fontsize=10, loc="left")
    axes[0].legend(frameon=False, fontsize=8, labelcolor=PRIMARY_INK, loc="lower right")
    save_figure(
        figure,
        str(arguments.figures / "etap2-mapa-dla-kodu.png"),
        "Według jakiej mapy wycinać, żeby chronić kod (mapa z połowy sekwencji, szkoda na drugiej połowie)",
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
