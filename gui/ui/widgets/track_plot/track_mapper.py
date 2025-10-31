import numpy as np
import pandas as pd
from matplotlib.axes import Axes
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt6.QtWidgets import QDialog, QMessageBox, QVBoxLayout

from utils import CsvHeaders, Files


def _plot_markers(ax: Axes, df: pd.DataFrame, x: np.ndarray, y: np.ndarray) -> None:
    """Plots the markers detected by the robot."""
    heading = df[CsvHeaders.HEADING].to_numpy()
    perp_angle = heading + np.pi / 2.0
    perp_dx = np.cos(perp_angle)
    perp_dy = np.sin(perp_angle)

    offset_dist = 30
    left_x = x + perp_dx * offset_dist
    left_y = y + perp_dy * offset_dist
    right_x = x - perp_dx * offset_dist
    right_y = y - perp_dy * offset_dist

    left_ir = df[CsvHeaders.LEFT_IR].to_numpy().astype(bool)
    right_ir = df[CsvHeaders.RIGHT_IR].to_numpy().astype(bool)

    if left_ir.any():
        ax.scatter(
            left_x[left_ir],
            left_y[left_ir],
            c="red",
            label="Left Markers",
            zorder=5,
        )
    if right_ir.any():
        ax.scatter(
            right_x[right_ir],
            right_y[right_ir],
            c="blue",
            label="Right Markers",
            zorder=5,
        )


def _plot_path(ax: Axes, df: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
    """Plots the robot's path."""
    x = df[CsvHeaders.X].to_numpy()
    y = df[CsvHeaders.Y].to_numpy()

    ax.plot(x, y, marker="o", linestyle="-", label="Robot Path")

    return x, y


def show_plot() -> None:
    """
    Displays the plot of the robot's path with markers.
    """
    try:
        df = pd.read_csv(Files.ENCODER_DATA)
    except Exception as e:
        QMessageBox.warning(None, "Plot error", f"Failed to load data:\n\n{e}")
        return

    dialog = QDialog()
    dialog.setWindowTitle("Mapped Track")
    layout = QVBoxLayout(dialog)

    fig = Figure(figsize=(10, 6), tight_layout=True)
    canvas = FigureCanvas(fig)
    ax = fig.add_subplot(111)

    x, y = _plot_path(ax, df)
    _plot_markers(ax, df, x, y)

    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel("X Position")
    ax.set_ylabel("Y Position")
    ax.grid(True)
    ax.legend()

    layout.addWidget(canvas)

    dialog.setFixedSize(1200, 800)
    dialog.setSizeGripEnabled(False)
    dialog.exec()
