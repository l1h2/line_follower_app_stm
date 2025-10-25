import time

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QTextEdit, QWidget

from utils import UIConstants


class TextDisplayContainer(QWidget):
    """
    ### TextDisplayContainer Widget

    A container widget for the TextDisplay widget. It provides a layout to hold the TextDisplay.

    #### Parameters:
    - `parent (QWidget | None)`: The parent widget of the TextDisplayContainer.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent=parent)

        self._init_ui()

    def print_text(self, text: str) -> None:
        """
        Print text to the QTextEdit widget displaying the text in a scrollable area.

        Args:
            text (str): The text to be displayed.
        """
        self._text_display.print_text(text)

    def _init_ui(self) -> None:
        """Initialize the UI components of the TextDisplayContainer widget."""
        self._add_widgets()
        self._set_layout()

    def _add_widgets(self) -> None:
        """Add widgets to the TextDisplayContainer widget."""
        self._text_display = TextDisplay(parent=self)

    def _set_layout(self) -> None:
        """Set the layout for the TextDisplayContainer widget."""
        main_layout = QHBoxLayout(self)
        main_layout.addWidget(self._text_display)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignRight)


class TextDisplay(QTextEdit):
    """
    ### TextDisplay Widget

    A widget that displays text in a scrollable area. It is used to show the output of the robot's
    operations.

    #### Parameters:
    - `max_display_lines (int)`: The maximum number of lines to display in the text area.
    - `parent (QWidget | None)`: The parent widget of the TextDisplay widget.

    #### Methods:
    - `print_text(text: str) -> None`: Prints the given text to the text area.
    """

    def __init__(
        self,
        max_display_lines: int = UIConstants.MAX_DISPLAY_LINES,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent=parent)
        self.setReadOnly(True)
        self.setFixedWidth(UIConstants.DISPLAY_WIDTH)

        self._max_display_lines = max_display_lines
        self._last_crop_time = time.time()
        self._crop_interval = 0.034  # ~30 fps in seconds

    def print_text(self, text: str) -> None:
        """
        Print text to the QTextEdit widget displaying the text in a scrollable area.

        Args:
            text (str): The text to be displayed.
        """
        self.append(text)

        if self._last_crop_time + self._crop_interval < time.time():
            self._last_crop_time = time.time()
            self._crop_text()

    def _crop_text(self) -> None:
        """Crop the text in the QTextEdit widget to fit within the maximum display lines."""
        current_text = self.toPlainText()
        lines = current_text.split("\n")

        if len(lines) <= self._max_display_lines:
            return

        vertical_scrollbar = self.verticalScrollBar()
        if not vertical_scrollbar:
            return

        scroll_position = vertical_scrollbar.value()

        self.setPlainText("\n".join(lines[-self._max_display_lines :]))
        vertical_scrollbar.setValue(scroll_position)
