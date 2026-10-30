import argparse
import json
from pathlib import Path

from qwen_compression.plotting import PRIMARY_INK, SERIES_COLORS, new_figure, save_figure


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", type=Path, default=Path("results/phase2/code/stage4"))
    parser.add_argument("--figures", type=Path, default=Path("AGENTS/phases/phase-2/figures"))
    return parser.parse_args()


def load_rows(results: Path) -> dict[int, list[dict]]:
    return {
        int(path.parent.name.removeprefix("layer-")): [json.loads(line) for line in path.read_text().splitlines()]
        for path in sorted(results.glob("layer-*/results.jsonl"))
    }


def main() -> None:
    arguments = parse_arguments()
    rows_per_layer = load_rows(arguments.results)
    table = []
    for layer_index, rows in rows_per_layer.items():
        for row in rows:
            if row["variant"] == "original":
                continue
            table.append(
                {
                    "layer": layer_index,
                    "importance": row["importance"],
                    "removed_fraction": row["removed_fraction"],
                    "variant": row["variant"],
                    "kl_code": row.get("kl_code"),
                    "kl_c4": row.get("kl_c4"),
                    "loss_change_code": row.get("loss_change_code"),
                    "loss_change_c4": row.get("loss_change_c4"),
                    "wikitext2_perplexity": row["wikitext2_perplexity"],
                    "best_epoch": row.get("best_epoch"),
                }
            )
    (arguments.results / "summary.json").write_text(json.dumps(table, indent=2))
    for row in table:
        print(json.dumps(row))
    layers = sorted(rows_per_layer)
    fractions = sorted({row["removed_fraction"] for row in table})
    figure, axes = new_figure(2, width_per_panel=5.2, height=4.0)
    for axis, (metric, title) in zip(
        axes, (("kl_code", "KL na odłożonym Pythonie"), ("kl_c4", "KL na odłożonym tekście C4")), strict=True
    ):
        bar_width = 0.8 / len(fractions)
        for position, fraction in enumerate(fractions):
            values = [
                next(
                    (
                        row[metric]
                        for row in table
                        if row["layer"] == layer_index
                        and row["removed_fraction"] == fraction
                        and row["variant"] == "trained"
                        and row["importance"] == "perturbation"
                    ),
                    0.0,
                )
                for layer_index in layers
            ]
            axis.bar(
                [index + (position - (len(fractions) - 1) / 2) * bar_width for index in range(len(layers))],
                values,
                width=bar_width - 0.04,
                color=SERIES_COLORS[position],
                label=f"zmniejszenie o {round(100 * fraction)}%",
            )
        axis.set_xticks(range(len(layers)), [f"warstwa {layer_index}" for layer_index in layers])
        axis.set_ylabel("KL do oryginału (nat / token)")
        axis.set_title(f"{title}, po treningu", fontsize=10, loc="left")
        axis.legend(frameon=False, fontsize=8, labelcolor=PRIMARY_INK)
    save_figure(
        figure,
        str(arguments.figures / "kod-etap4-warstwy.png"),
        "Zmniejszanie warstw na danych z Pythona (start z nowej mapy, naprawa 75% Python / 25% tekst)",
    )
    map_figure(table, fractions, arguments.figures)


def map_figure(table: list[dict], fractions: list[float], figures: Path) -> None:
    starts = (("perturbation", "start z mapy kodu (75/25)"), ("previous-map", "start z mapy tekstu (stara)"))
    figure, axes = new_figure(2, width_per_panel=5.2, height=4.0)
    for axis, (metric, title) in zip(
        axes, (("kl_code", "KL na odłożonym Pythonie"), ("kl_c4", "KL na odłożonym tekście C4")), strict=True
    ):
        bar_width = 0.8 / len(starts)
        for position, (importance, label) in enumerate(starts):
            values = [
                next(
                    row[metric]
                    for row in table
                    if row["layer"] == 13
                    and row["removed_fraction"] == fraction
                    and row["variant"] == "trained"
                    and row["importance"] == importance
                )
                for fraction in fractions
            ]
            axis.bar(
                [index + (position - (len(starts) - 1) / 2) * bar_width for index in range(len(fractions))],
                values,
                width=bar_width - 0.04,
                color=SERIES_COLORS[position],
                label=label,
            )
        axis.set_xticks(range(len(fractions)), [f"zmniejszenie o {round(100 * fraction)}%" for fraction in fractions])
        axis.set_ylabel("KL do oryginału (nat / token)")
        axis.set_title(f"{title}, po treningu", fontsize=10, loc="left")
        axis.legend(frameon=False, fontsize=8, labelcolor=PRIMARY_INK)
    save_figure(figure, str(figures / "kod-mapa-nowa-vs-stara-13.png"), "Warstwa 13: od której mapy zacząć")


if __name__ == "__main__":
    main()
