import sys
from pathlib import Path

# Add the project root to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import csv
import os

from utils import CsvHeaders, Files, Paths


def get_array_strings(file: str) -> tuple[str, str, int]:
    x_values: list[float] = []
    y_values: list[float] = []

    with open(file, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            x_values.append(float(row[CsvHeaders.X]) / 10)
            y_values.append(float(row[CsvHeaders.Y]) / 10)

    waypoint_count = len(x_values)

    x_array = (
        "const float waypoints_x[WAYPOINT_COUNT] = {"
        + ", ".join(f"{x:.1f}f" for x in x_values)
        + "};"
    )
    y_array = (
        "const float waypoints_y[WAYPOINT_COUNT] = {"
        + ", ".join(f"{y:.1f}f" for y in y_values)
        + "};"
    )
    return x_array, y_array, waypoint_count


def write_header_file(filename: str, waypoint_count: int) -> None:
    with open(f"{os.path.join(Paths.TRACKS, filename)}.h", "w") as f:
        f.write(f"#ifndef TRACK_{filename.upper()}_H\n")
        f.write(f"#define TRACK_{filename.upper()}_H\n\n")
        f.write(f"#define WAYPOINT_COUNT {waypoint_count}\n\n")
        f.write(f"extern const float waypoints_x[WAYPOINT_COUNT];\n")
        f.write(f"extern const float waypoints_y[WAYPOINT_COUNT];\n\n")
        f.write(f"#endif // TRACK_{filename.upper()}_H\n")


def write_source_file(filename: str, x_array: str, y_array: str) -> None:
    with open(f"{os.path.join(Paths.TRACKS, filename)}.c", "w") as f:
        f.write(f'#include "track/tracks/{filename}.h"\n\n')
        f.write(f'#include "config.h"\n\n')
        f.write(f"#if SELECTED_TRACK == {track_name.upper()}\n")
        f.write(x_array + "\n")
        f.write(y_array + "\n")
        f.write(f"#endif\n")


def generate_waypoint_files(input_csv: str, track_name: str) -> None:
    x_array, y_array, waypoint_count = get_array_strings(input_csv)
    os.makedirs(Paths.TRACKS, exist_ok=True)

    write_header_file(track_name, waypoint_count)
    write_source_file(track_name, x_array, y_array)
    print("Waypoint files generated successfully.")


if __name__ == "__main__":
    input_csv = Files.ENCODER_DATA
    track_name = "test_track"

    generate_waypoint_files(input_csv, track_name)
