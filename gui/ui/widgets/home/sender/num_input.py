from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QPushButton, QWidget

from robot import LineFollower
from utils import SERIAL_MESSAGE_SIZES, Messages, SerialMessages, UIConstants


class NumInput(QWidget):
    """
    ### NumInput Widget

    A widget that allows the user to input a numeric value and send it via a callback function.

    #### Parameters:
    - `label (str)`: The label for the input field.
    - `message (SerialMessages)`: The type of message to be sent.
    - `max_value (int)`: The maximum value allowed for the input.

    #### Attributes:
    - `label (QLabel)`: The label for the input field.
    - `input (QLineEdit)`: The input field for the numeric value.
    - `button (QPushButton)`: The button to send the input value.

    #### Methods:
    - `send_value() -> None`: Sends the value from the input field to the callback function.
    """

    def __init__(
        self,
        label: str,
        message: SerialMessages,
        max_value: int | None = None,
    ):
        super().__init__()
        self._message = message
        self._max_value = (
            max_value
            if max_value is not None
            else (1 << (8 * SERIAL_MESSAGE_SIZES[message])) - 1
        )
        self._line_follower = LineFollower()

        self.setFixedHeight(UIConstants.ROW_HEIGHT)
        self._init_ui(label)

    def send_value(self) -> None:
        """
        Send the value from the input field to the callback function.
        """
        self._on_input()

    def _init_ui(self, label: str) -> None:
        """Initialize the UI components of the ByteInput widget."""
        self._add_widgets(label)
        self._set_layout()

    def _add_widgets(self, label: str) -> None:
        """Add widgets to the ByteInput widget."""
        self._add_label(label)
        self._add_input()
        self._add_button()

    def _add_label(self, label: str) -> None:
        """Add a label to the widget."""
        self.label = QLabel(label)
        self.label.setFixedWidth(80)

    def _add_input(self) -> None:
        """Add an input field for the byte value."""
        self.input = QLineEdit()
        self.input.setFixedWidth(60)
        self.input.setMaxLength(3)
        self.input.setPlaceholderText(f"0-{self._max_value}")
        self.input.setValidator(QIntValidator(0, self._max_value))
        self.input.setToolTip(f"Enter a value between 0 and {self._max_value}")
        self.input.textChanged.connect(self._on_text_changed)
        self.input.returnPressed.connect(self._on_input)

    def _add_button(self) -> None:
        """Add a button to send the input value."""
        self.button = QPushButton("Send")
        self.button.setFixedWidth(50)
        self.button.setToolTip("Send the value")
        self.button.clicked.connect(self._on_input)

    def _on_text_changed(self, text: str) -> None:
        """Handle text changes in the input field."""
        if text.isdigit() and int(text) > self._max_value:
            self.input.setText(f"{self._max_value}")

    def _on_input(self) -> None:
        """Handle the input value and send it to the callback function."""
        value = self.input.text()

        if not value.isdigit():
            return

        self._line_follower.send_message(Messages.from_int(self._message, int(value)))

    def _set_layout(self) -> None:
        """Set the layout for the widget."""
        layout = QHBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.input)
        layout.addWidget(self.button)
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
