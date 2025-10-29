import sys
from pathlib import Path

# Add the project root to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import csv

from utils import CsvHeaders, Files

# Path to your CSV file
csv_filename = Files.ENCODER_DATA
output_filename = Files.WAYPOINTS

# Lists to hold x and y values
x_values: list[float] = []
y_values: list[float] = []

# Read CSV file
with open(csv_filename, "r") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        x_values.append(float(row[CsvHeaders.X]))
        y_values.append(float(row[CsvHeaders.Y]))

# Format arrays as C-style constants
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

with open(output_filename, "w") as outfile:
    outfile.write(f"#define WAYPOINT_COUNT {waypoint_count}\n")
    outfile.write(x_array)
    outfile.write(y_array)

print(f"✅ Waypoints successfully written to '{output_filename}'")
