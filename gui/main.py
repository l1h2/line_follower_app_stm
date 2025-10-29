import sys

from PyQt6.QtCore import Qt, qInstallMessageHandler  # type: ignore
from PyQt6.QtGui import QColor, QIcon, QPalette
from PyQt6.QtWidgets import QApplication

from utils import Assets

from .ui import MainWindow


def _qt_msg_handler(_mode, _context, message: str) -> None:  # type: ignore
    """Custom QT message handler to suppress specific warnings."""
    if (
        "setHighDpiScaleFactorRoundingPolicy must be called before creating the QGuiApplication instance"
        in message
    ):
        return
    sys.stderr.write(message + "\n")


def _get_dark_pallet() -> QPalette:
    """Create and return a dark color palette for the application."""
    dark = QPalette()
    dark.setColor(QPalette.ColorRole.Window, QColor(45, 45, 45))
    dark.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
    dark.setColor(QPalette.ColorRole.Base, QColor(30, 30, 30))
    dark.setColor(QPalette.ColorRole.AlternateBase, QColor(45, 45, 45))
    dark.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.white)
    dark.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
    dark.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
    dark.setColor(QPalette.ColorRole.Button, QColor(45, 45, 45))
    dark.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
    dark.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
    dark.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black)
    dark.setColor(QPalette.ColorRole.PlaceholderText, QColor(150, 150, 150))

    return dark


def start_gui() -> None:
    """
    Start the GUI application.
    """
    qInstallMessageHandler(_qt_msg_handler)
    app = QApplication([])

    app.setWindowIcon(QIcon(Assets.ALT_ICON_IMAGE))
    app.setStyle("Fusion")
    app.setPalette(_get_dark_pallet())

    window = MainWindow()
    window.show()

    app.exec()
