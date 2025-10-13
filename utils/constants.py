from enum import IntEnum


class Files:
    """List of file names used in the program."""

    BINARY_FILE = "data/serial_data_log.bin"
    TIMESTAMP_FILE = "data/timestamps.txt"
    TEXT_FILE = "data/serial_data_log.txt"
    SENSOR_DATA = "data/sensors.csv"
    ENCODER_DATA = "data/encoder.csv"


class CsvHeaders:
    """CSV file headers."""

    SENSOR_DATA = "left_ir,ir1,ir2,ir3,ir4,ir5,ir6,ir7,ir8,right_ir,x,y,heading"
    LEFT_IR = "left_ir"
    IR1 = "ir1"
    IR2 = "ir2"
    IR3 = "ir3"
    IR4 = "ir4"
    IR5 = "ir5"
    IR6 = "ir6"
    IR7 = "ir7"
    IR8 = "ir8"
    RIGHT_IR = "right_ir"
    X = "x"
    Y = "y"
    HEADING = "heading"


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
