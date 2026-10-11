import csv
import os
import shutil
import subprocess
import sys
from datetime import datetime

from .constants import CsvHeaders, Files, Paths, RunLogs


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


def archive_operation_logs() -> None:
    """
    Copies the operation logs to a new timestamped folder in data/runs, if they hold
    operation data. Only the last run of the text log is copied, as it isn't cleared
    between runs.
    """
    if os.path.getsize(Files.BINARY_FILE) == 0:
        return

    folder = os.path.join(Paths.RUNS, datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
    os.makedirs(folder)
    for file in (Files.BINARY_FILE, Files.SENSOR_DATA, Files.ENCODER_DATA):
        shutil.copy2(file, folder)

    _copy_last_run(Files.TEXT_FILE, folder)


def _copy_last_run(file: str, folder: str) -> None:
    """Copies the text log of the last run, from its start to its return to IDLE."""
    with open(file, "rb") as f:
        log = f.read()

    end = log.rfind(RunLogs.END.encode())
    previous_end = log.rfind(RunLogs.END.encode(), 0, end)
    start = log.rfind(RunLogs.START.encode(), previous_end + 1, end)
    if end == -1 or start == -1:
        return

    end = log.index(b"\n", end) + 1
    with open(os.path.join(folder, os.path.basename(file)), "wb") as f:
        f.write(log[start:end])


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
