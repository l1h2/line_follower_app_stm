import csv
import os
import shutil
import subprocess
import sys

from .constants import CsvHeaders, Files


class AppConfigs:
    """Application configuration constants."""

    APP_ID = "com.pet_uff.line_follower"
    APP_NAME = "Line Follower App"


def _write_csv_headers(filename: str, headers: str) -> None:
    """Writes headers to a CSV file."""
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers.split(","))


def clear_operation_logs() -> None:
    """
    Clears the operation log files.
    """
    open(Files.BINARY_FILE, "w").close()
    _write_csv_headers(Files.SENSOR_DATA, CsvHeaders.SENSOR_DATA)
    _write_csv_headers(Files.ENCODER_DATA, CsvHeaders.SENSOR_DATA)


def clean_dir(dir: str) -> None:
    """
    Cleans the specified directory by deleting its contents.

    Args:
        dir (str): The directory to clean.
    """
    if os.path.exists(dir):
        shutil.rmtree(dir)
    os.makedirs(dir)


def run_command(command: str) -> None:
    """
    Runs a system command.

    Args:
        command (str): The command to run.
    """
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        print(f"Error: Failed to run command: {command}", file=sys.stderr)
        sys.exit(1)
