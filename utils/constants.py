import os
import sys
from enum import IntEnum
from pathlib import Path


class Paths:
    """List of important directory paths used in the program."""

    ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    DATA = (
        str(Path(sys.executable).parent / "data")
        if getattr(sys, "frozen", False)
        else os.path.join(ROOT, "data")
    )
    ASSETS = os.path.join(ROOT, "assets")
    BUILDS_DIR = os.path.join(ROOT, "builds")
    PYINSTALLER_BUILD = os.path.join(ROOT, "pyinstaller_build")
    PYINSTALLER_WORK = os.path.join(PYINSTALLER_BUILD, "build")
    PYINSTALLER_DIST = os.path.join(PYINSTALLER_BUILD, "dist")
    PYINSTALLER_SPEC = os.path.join(PYINSTALLER_BUILD, "app.spec")


class Files:
    """List of file names used in the program."""

    MAIN = os.path.join(Paths.ROOT, "main.py")
    BINARY_FILE = os.path.join(Paths.DATA, "serial_data_log.bin")
    TEXT_FILE = os.path.join(Paths.DATA, "serial_data_log.txt")
    SENSOR_DATA = os.path.join(Paths.DATA, "sensors.csv")
    ENCODER_DATA = os.path.join(Paths.DATA, "encoder.csv")


class Assets:
    """Paths to asset files used in the program."""

    ICON_IMAGE = os.path.join(Paths.ASSETS, "app_icon.ico")
    ALT_ICON_IMAGE = os.path.join(Paths.ASSETS, "alt_icon.ico")


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
    PING_TIMEOUT = TIMEOUT * 1.1


class UIConstants:
    """UI constants for the program."""

    MAX_DISPLAY_LINES = 70
    ROW_HEIGHT = 40
    DISPLAY_WIDTH = 450


class Booleans(IntEnum):
    """List of boolean values used in the program."""

    OFF = 0
    ON = 1
