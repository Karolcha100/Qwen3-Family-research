import matplotlib

matplotlib.use("Agg")

from matplotlib import pyplot
from matplotlib.axes import Axes
from matplotlib.figure import Figure

SERIES_COLORS = ("#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#6250d6", "#e34948")
SEQUENTIAL_BLUE = ("#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#184f95", "#0d366b")
SURFACE = "#fcfcfb"
PRIMARY_INK = "#0b0b0b"
SECONDARY_INK = "#52514e"
GRID = "#e4e3df"


def new_figure(
    columns: int, rows: int = 1, width_per_panel: float = 4.2, height: float = 3.6
) -> tuple[Figure, list[Axes]]:
    figure, axes = pyplot.subplots(
        rows, columns, figsize=(width_per_panel * columns, height * rows), squeeze=False, facecolor=SURFACE
    )
    flat_axes = [axis for row in axes for axis in row]
    for axis in flat_axes:
        style_axis(axis)
    return figure, flat_axes


def style_axis(axis: Axes) -> None:
    axis.set_facecolor(SURFACE)
    for side in ("top", "right"):
        axis.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        axis.spines[side].set_color(SECONDARY_INK)
        axis.spines[side].set_linewidth(0.8)
    axis.tick_params(colors=SECONDARY_INK, labelsize=8)
    axis.grid(True, color=GRID, linewidth=0.6)
    axis.set_axisbelow(True)
    axis.title.set_color(PRIMARY_INK)
    axis.xaxis.label.set_color(SECONDARY_INK)
    axis.yaxis.label.set_color(SECONDARY_INK)


def save_figure(figure: Figure, path: str, title: str) -> None:
    figure.suptitle(title, color=PRIMARY_INK, fontsize=11, x=0.01, ha="left")
    figure.tight_layout()
    figure.savefig(path, dpi=130, facecolor=SURFACE)
    pyplot.close(figure)
