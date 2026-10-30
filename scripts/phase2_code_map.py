import argparse
import json
from pathlib import Path

import torch

from qwen_compression.analysis import spearman


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--code-weight", type=float, default=0.75)
    parser.add_argument("--samples", type=int, default=64)
    parser.add_argument("--stage2", type=Path, default=Path("results/phase2/code/stage2"))
    parser.add_argument("--previous-map", type=Path, default=Path("results/phase2/stage2/fisher-map.pt"))
    return parser.parse_args()


def normalized(importance: torch.Tensor) -> torch.Tensor:
    return importance / importance.sum(dim=1, keepdim=True)


def main() -> None:
    arguments = parse_arguments()
    stored = torch.load(arguments.stage2 / f"fisher-per-sequence-{arguments.samples}.pt")
    coefficients, sources = stored["coefficients"].double(), stored["sources"]
    code_rows = [index for index, source in enumerate(sources) if source == "code"]
    text_rows = [index for index, source in enumerate(sources) if source == "c4"]
    code_map, text_map = coefficients[code_rows].mean(dim=0), coefficients[text_rows].mean(dim=0)
    weighted = arguments.code_weight * normalized(code_map) + (1 - arguments.code_weight) * normalized(text_map)
    weighted = weighted * code_map.sum(dim=1, keepdim=True)
    torch.save(
        {
            "coefficients": weighted.float(),
            "code": code_map.float(),
            "text": text_map.float(),
            "code_weight": arguments.code_weight,
        },
        arguments.stage2 / "fisher-map.pt",
    )
    previous = torch.load(arguments.previous_map)["coefficients"].double()
    half = len(code_rows) // 2
    first_half, second_half = coefficients[code_rows[:half]].mean(dim=0), coefficients[code_rows[half:]].mean(dim=0)
    layers = range(coefficients.shape[1])
    summary = {
        "code_sequences": len(code_rows),
        "text_sequences": len(text_rows),
        "code_half_vs_half_spearman": [spearman(first_half[layer], second_half[layer]) for layer in layers],
        "code_vs_text_spearman": [spearman(code_map[layer], text_map[layer]) for layer in layers],
        "new_map_vs_previous_map_spearman": [spearman(weighted[layer], previous[layer]) for layer in layers],
        "code_kl_sum_per_layer": code_map.sum(dim=1).tolist(),
        "text_kl_sum_per_layer": text_map.sum(dim=1).tolist(),
    }
    (arguments.stage2 / "code-map-summary.json").write_text(json.dumps(summary, indent=2))
    for key in ("code_half_vs_half_spearman", "code_vs_text_spearman", "new_map_vs_previous_map_spearman"):
        values = summary[key]
        print(key, f"mean {sum(values) / len(values):.3f} min {min(values):.3f} max {max(values):.3f}")


if __name__ == "__main__":
    main()
