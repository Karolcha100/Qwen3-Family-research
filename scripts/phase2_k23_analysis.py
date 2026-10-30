import argparse
import json
from pathlib import Path

from qwen_compression.plotting import PRIMARY_INK, SERIES_COLORS, new_figure, save_figure


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--layer", type=int, default=13)
    parser.add_argument("--runs", type=Path, default=Path("results/phase2/k23"))
    parser.add_argument("--baseline", type=Path, default=Path("results/phase2/stage4"))
    parser.add_argument("--figures", type=Path, default=Path("AGENTS/phases/phase-2/figures"))
    return parser.parse_args()


def trained_rows(path: Path) -> dict[float, dict]:
    rows = [json.loads(line) for line in path.read_text().splitlines()]
    return {
        row["removed_fraction"]: row
        for row in rows
        if row["variant"] == "trained" and row["importance"] == "perturbation"
    }


def main() -> None:
    arguments = parse_arguments()
    layer_directory = f"layer-{arguments.layer:02d}"
    baseline = trained_rows(arguments.baseline / layer_directory / "results.jsonl")
    runs = {
        path.name.removeprefix("lr-"): trained_rows(path / layer_directory / "results.jsonl")
        for path in sorted(arguments.runs.glob("lr-*"))
        if (path / layer_directory / "results.jsonl").exists()
    }
    summary = []
    for fraction, row in sorted(baseline.items()):
        if fraction not in next(iter(runs.values()), {}):
            continue
        summary.append(
            {
                "removed_fraction": fraction,
                "setting": "4 epoki, lr 5e-5 (noc)",
                "kl": row["kl"],
                "wikitext2_perplexity": row["wikitext2_perplexity"],
                "best_epoch": row["best_epoch"],
            }
        )
        for learning_rate, rows in runs.items():
            if fraction in rows:
                summary.append(
                    {
                        "removed_fraction": fraction,
                        "setting": f"16 epok, lr {learning_rate}",
                        "kl": rows[fraction]["kl"],
                        "wikitext2_perplexity": rows[fraction]["wikitext2_perplexity"],
                        "best_epoch": rows[fraction]["best_epoch"],
                    }
                )
    (arguments.runs / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False))
    for row in summary:
        print(json.dumps(row, ensure_ascii=False))
    fractions = sorted({fraction for rows in runs.values() for fraction in rows})
    figure, axes = new_figure(len(fractions), width_per_panel=4.8, height=3.8)
    for axis, fraction in zip(axes, fractions, strict=True):
        for position, (learning_rate, rows) in enumerate(runs.items()):
            if fraction not in rows:
                continue
            row = rows[fraction]
            losses = [row["window_loss_before"], *row["epoch_losses"]]
            axis.plot(
                range(len(losses)),
                [100 * loss / losses[0] for loss in losses],
                color=SERIES_COLORS[position],
                linewidth=2,
                marker="o",
                markersize=3,
                label=f"krok uczenia {learning_rate}",
            )
        axis.set_xlabel("epoka (0 = start z najmniejszych kwadratów)")
        axis.set_ylabel("błąd za następną warstwą (% startu)")
        axis.set_title(f"Zmniejszenie o {round(100 * fraction)}%", fontsize=10, loc="left")
        axis.legend(frameon=False, fontsize=8, labelcolor=PRIMARY_INK)
    save_figure(
        figure,
        str(arguments.figures / f"k23-dlugi-trening-{arguments.layer:02d}.png"),
        f"Warstwa {arguments.layer}: błąd na walidacji w kolejnych epokach treningu",
    )


if __name__ == "__main__":
    main()
