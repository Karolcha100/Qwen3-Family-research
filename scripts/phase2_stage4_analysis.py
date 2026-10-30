import argparse
import json
from pathlib import Path

from qwen_compression.plotting import PRIMARY_INK, SERIES_COLORS, new_figure, save_figure

VARIANTS = {"sliced": "tylko wycięcie", "least_squares": "+ najmniejsze kwadraty", "trained": "+ trening"}
IMPORTANCES = {"perturbation": ("przesiew KL", "-"), "activation": ("średnia |a|", "--")}


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--layer", type=int, required=True)
    parser.add_argument("--results", type=Path, default=Path("results/phase2/stage4"))
    parser.add_argument("--figures", type=Path, default=Path("AGENTS/phases/phase-2/figures"))
    return parser.parse_args()


def main() -> None:
    arguments = parse_arguments()
    rows = [
        json.loads(line)
        for line in (arguments.results / f"layer-{arguments.layer:02d}" / "results.jsonl").read_text().splitlines()
    ]
    original = next(row for row in rows if row["variant"] == "original")
    figure, axes = new_figure(2, width_per_panel=5.0, height=3.8)
    for metric, axis, label in (
        ("kl", axes[0], "KL do oryginału (nat / token)"),
        ("wikitext2_perplexity", axes[1], "perpleksja WikiText-2"),
    ):
        for position, (variant, variant_label) in enumerate(VARIANTS.items()):
            for importance, (importance_label, line_style) in IMPORTANCES.items():
                selected = sorted(
                    (row for row in rows if row["variant"] == variant and row["importance"] == importance),
                    key=lambda row: row["removed_fraction"],
                )
                axis.plot(
                    [0.0] + [100 * row["removed_fraction"] for row in selected],
                    [original[metric]] + [row[metric] for row in selected],
                    color=SERIES_COLORS[position],
                    linestyle=line_style,
                    linewidth=2,
                    marker="o",
                    markersize=4,
                    label=f"{variant_label}, {importance_label}",
                )
        axis.set_xlabel("wycięte neurony MLP warstwy (%)")
        axis.set_ylabel(label)
        axis.set_xticks([0, 5, 10, 20, 40])
    axes[1].axhline(original["wikitext2_perplexity"], color=PRIMARY_INK, linewidth=0.8)
    axes[0].legend(frameon=False, fontsize=7.5, labelcolor=PRIMARY_INK)
    save_figure(
        figure,
        str(arguments.figures / f"etap4-warstwa-{arguments.layer:02d}.png"),
        f"Zmniejszanie warstwy {arguments.layer}: linia ciągła = wybór przesiewem, przerywana = średnia |a|",
    )


if __name__ == "__main__":
    main()
