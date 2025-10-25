from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtWidgets import QApplication

from .ui import MainWindow


def get_dark_pallet() -> QPalette:
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

    return dark


def start_gui() -> None:
    """Start the GUI application."""
    app = QApplication([])

    app.setStyle("Fusion")
    app.setPalette(get_dark_pallet())

    window = MainWindow()
    window.show()

    app.exec()
