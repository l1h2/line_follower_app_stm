import sys
from pathlib import Path

# Add the project root to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from utils import CsvHeaders, Files

OFFSET_DIST = 30


def plot_markers(df: pd.DataFrame, x: np.ndarray, y: np.ndarray) -> None:
    heading = df[CsvHeaders.HEADING].to_numpy()
    perp_angle = heading + np.pi / 2.0
    perp_dx = np.cos(perp_angle)
    perp_dy = np.sin(perp_angle)

    left_x = x + perp_dx * OFFSET_DIST
    left_y = y + perp_dy * OFFSET_DIST
    right_x = x - perp_dx * OFFSET_DIST
    right_y = y - perp_dy * OFFSET_DIST

    left_ir = df[CsvHeaders.LEFT_IR].to_numpy()
    right_ir = df[CsvHeaders.RIGHT_IR].to_numpy()

    left_mask = left_ir.astype(bool)
    right_mask = right_ir.astype(bool)

    if left_mask.any():
        plt.scatter(
            left_x[left_mask],
            left_y[left_mask],
            c="red",
            label="Left Markers",
            zorder=5,
        )
    if right_mask.any():
        plt.scatter(
            right_x[right_mask],
            right_y[right_mask],
            c="blue",
            label="Right Markers",
            zorder=5,
        )


def plot_path(df: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
    x = df[CsvHeaders.X].to_numpy()
    y = df[CsvHeaders.Y].to_numpy()

    plt.figure(figsize=(10, 6))
    plt.plot(x, y, marker="o", linestyle="-", label="Robot Path")

    return x, y


def show_plot() -> None:
    plt.axis("equal")
    plt.xlabel("X Position")
    plt.ylabel("Y Position")
    plt.grid()
    plt.legend()
    plt.show()


if __name__ == "__main__":
    df = pd.read_csv(Files.ENCODER_DATA)
    x, y = plot_path(df)
    plot_markers(df, x, y)
    show_plot()
