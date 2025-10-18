from PyQt6.QtCore import Qt
from PyQt6.QtGui import QDoubleValidator, QIntValidator
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QPushButton, QWidget

from robot import LineFollower
from utils import (
    EXTENDED_FLOAT_MESSAGES,
    FLOAT_MESSAGES,
    PARAM_MAX_VALUES,
    SERIAL_MESSAGE_SIZES,
    SerialMessage,
    SerialMessages,
    UIConstants,
)


class NumInput(QWidget):
    """
    ### NumInput Widget

    A widget that allows the user to input a numeric value and send it to the robot.

    #### Parameters:
    - `label (str)`: The label for the input field.
    - `message (SerialMessages)`: The type of message to be sent.

    #### Properties:
    - `value (str)`: The current value of the input field.

    #### Attributes:
    - `label (QLabel)`: The label for the input field.
    - `input (QLineEdit)`: The input field for the numeric value.
    - `button (QPushButton)`: The button to send the input value.

    #### Methods:
    - `send_value() -> None`: Sends the value from the input field to the robot.
    """

    def __init__(
        self,
        label: str,
        message: SerialMessages,
    ):
        super().__init__()
        self._message = message
        self._is_float = message in FLOAT_MESSAGES
        self._is_extended_float = message in EXTENDED_FLOAT_MESSAGES
        self._line_follower = LineFollower()

        self.setFixedHeight(UIConstants.ROW_HEIGHT)
        self._set_max_value()
        self._init_ui(label)

    @property
    def value(self) -> str:
        """Get the current value of the input field."""
        return self.input.text()

    def send_value(self) -> None:
        """
        Send the value from the input field to the robot.
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
        self.label.setFixedWidth(105)

    def _add_input(self) -> None:
        """Add an input field for the byte value."""
        self.input = QLineEdit()
        self.input.setFixedWidth(60)

        if self._is_float:
            self.input.setMaxLength(6)
            self.input.setPlaceholderText(f"0-{self._max_value:.2f}")
            self.input.setValidator(QDoubleValidator(0, self._max_value, 2))
            self.input.setToolTip(f"Enter a value between 0 and {self._max_value:.2f}")
        elif self._is_extended_float:
            self.input.setMaxLength(6)
            self.input.setPlaceholderText(f"0-{self._max_value:.4f}")
            self.input.setValidator(QDoubleValidator(0, self._max_value, 4))
            self.input.setToolTip(f"Enter a value between 0 and {self._max_value:.4f}")
        else:
            self.input.setMaxLength(5)
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
        if not text:
            return

        if self._is_float or self._is_extended_float:
            try:
                value = float(text)
            except ValueError:
                return

            if value > self._max_value:
                value = (
                    f"{self._max_value:.4f}"
                    if self._is_extended_float
                    else f"{self._max_value:.2f}"
                )
                self.input.setText(value)

        else:
            if text.isdigit() and int(text) > self._max_value:
                self.input.setText(f"{self._max_value}")

    def _on_input(self) -> None:
        """Handle the input value and send it to the robot."""
        value = self.input.text()

        if not value:
            return

        if self._is_float:
            value = float(value) * 100 + 0.5
        elif self._is_extended_float:
            value = float(value) * 10000 + 0.5

        value = int(value)

        self._line_follower.send_message(SerialMessage.from_int(self._message, value))

    def _set_layout(self) -> None:
        """Set the layout for the widget."""
        layout = QHBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.input)
        layout.addWidget(self.button)
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

    def _set_max_value(self) -> None:
        """Set the maximum value for the input field."""
        robot_max = PARAM_MAX_VALUES.get(self._message)

        if robot_max is not None:
            self._max_value = robot_max
            return

        self._max_value = (1 << (8 * SERIAL_MESSAGE_SIZES[self._message])) - 1
