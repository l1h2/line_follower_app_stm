from enum import IntEnum


class Files:
    """List of file names used in the program."""

    BINARY_FILE = "data/serial_data_log.bin"
    TIMESTAMP_FILE = "data/timestamps.txt"
    TEXT_FILE = "data/serial_data_log.txt"
    SENSOR_DATA = "data/sensors.csv"


class SerialConfig:
    """Serial port configuration."""

    PORT = "COM3"
    BAUD_RATE = 115200
    TIMEOUT = 1


class UIConstants:
    """UI constants for the program."""

    MAX_DISPLAY_LINES = 70
    ROW_HEIGHT = 40
    DISPLAY_WIDTH = 450


class Booleans(IntEnum):
    """List of boolean values used in the program."""

    OFF = 0
    ON = 1
