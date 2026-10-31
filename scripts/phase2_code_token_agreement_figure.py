import argparse
import json
from pathlib import Path

from qwen_compression.plotting import PRIMARY_INK, SECONDARY_INK, SERIES_COLORS, new_figure, save_figure

REDUCED_PRECISION = "original-bf16"
MODELS = (
    ("layer13-40-window", "w. 13, cel za warstwą", "layer-13-perturbation-40-trained"),
    ("layer13-40-output", "w. 13, cel na wyjściu", "layer-13-perturbation-40-trained_output"),
    ("layer13-40-code-only", "w. 13, mapa 100% kod", "layer-13-code-only-40-trained"),
    ("layer26-40-output", "w. 26, cel na wyjściu", "layer-26-perturbation-40-trained_output"),
)
PANELS = (
    (("code",), "Python z zestawu do KL (32 768 tokenów)"),
    (("humaneval", "mbpp"), "odpowiedzi oryginału na zadania EvalPlus (42 343 tokeny)"),
)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--agreement", type=Path, default=Path("results/phase2/code-eval/token-agreement.json"))
    parser.add_argument("--comparison", type=Path, default=Path("results/phase2/code-eval/comparison.json"))
    parser.add_argument("--figures", type=Path, default=Path("AGENTS/phases/phase-2/figures"))
    return parser.parse_args()


def pooled_agreement(sets: dict, sources: tuple[str, ...], variant: str) -> float:
    agreeing = sum(sets[source][variant]["top1_agreement"] * sets[source][variant]["tokens"] for source in sources)
    return agreeing / sum(sets[source][variant]["tokens"] for source in sources)


def main() -> None:
    arguments = parse_arguments()
    sets = json.loads(arguments.agreement.read_text())["sets"]
    solved = {
        row["name"]: row["humaneval_plus"]["solved"] + row["mbpp_plus"]["solved"]
        for row in json.loads(arguments.comparison.read_text())
    }
    figure, axes = new_figure(2, width_per_panel=6.0, height=4.4)
    for axis, (sources, title) in zip(axes, PANELS, strict=True):
        noise_floor = 100 * pooled_agreement(sets, sources, REDUCED_PRECISION)
        axis.axvline(noise_floor, color=SECONDARY_INK, linewidth=1.0, linestyle="--")
        axis.text(noise_floor, 211, " oryginał w bf16\n (sam szum liczb)", fontsize=7, color=SECONDARY_INK, va="top")
        axis.scatter(
            [100.0], [solved["original"]], s=70, color=PRIMARY_INK, edgecolors="white", linewidths=1.5, zorder=3
        )
        axis.annotate(
            "oryginał",
            (100.0, solved["original"]),
            xytext=(-8, 6),
            textcoords="offset points",
            ha="right",
            fontsize=8,
            color=SECONDARY_INK,
        )
        for position, (name, label, variant) in enumerate(MODELS):
            agreement = 100 * pooled_agreement(sets, sources, variant)
            axis.scatter(
                [agreement],
                [solved[name]],
                s=70,
                color=SERIES_COLORS[position],
                edgecolors="white",
                linewidths=1.5,
                zorder=3,
                label=label,
            )
            axis.annotate(
                label,
                (agreement, solved[name]),
                xytext=(6, -3 - 9 * (position % 2)),
                textcoords="offset points",
                fontsize=7,
                color=SECONDARY_INK,
            )
        axis.set_xlim(97.6, 100.25)
        axis.set_ylim(178, 212)
        axis.set_xlabel("zgodność najbardziej prawdopodobnego tokenu z oryginałem (%)")
        axis.set_ylabel("rozwiązane zadania HumanEval+ i MBPP+ (z 542)")
        axis.set_title(title, fontsize=10, loc="left")
    axes[0].legend(frameon=False, fontsize=7, labelcolor=PRIMARY_INK, loc="lower right")
    save_figure(
        figure,
        str(arguments.figures / "kod-k43-zgodnosc-tokenu.png"),
        "Czy zgodność tokenu przewiduje liczbę rozwiązanych zadań?",
    )


if __name__ == "__main__":
    main()
