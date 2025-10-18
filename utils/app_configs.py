import csv

from .constants import CsvHeaders, Files

DEBUG_ENABLED = False


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
