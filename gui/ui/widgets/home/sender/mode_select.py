from enum import IntEnum

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QComboBox, QHBoxLayout, QLabel, QPushButton, QWidget

from robot import LineFollower
from utils import Messages, SerialMessages, UIConstants


class ModeSelect(QWidget):
    """
    ### ModeSelect Widget

    A widget that allows the user to select a mode from a combo box and send it to a callback function.

    #### Parameters:
    - `label (str)`: The label for the combo box.
    - `command (SerialOutputs)`: The command associated with the selected mode.
    - `enum_class (type[Enum])`: The enum class containing the available modes.

    #### Attributes:
    - `label (QLabel)`: The label for the combo box.
    - `options (QComboBox)`: The combo box for selecting the mode.
    - `button (QPushButton)`: The button to send the selected mode.

    #### Methods:
    - `send_value() -> None`: Sends the selected mode to the callback function.
    """

    def __init__(
        self,
        label: str,
        message: SerialMessages,
        enum_class: type[IntEnum],
    ):
        super().__init__()
        self._message = message
        self._enum_class = enum_class
        self._line_follower = LineFollower()

        self.setFixedHeight(UIConstants.ROW_HEIGHT)
        self._init_ui(label)

    def send_value(self) -> None:
        """
        Send the value from the combo box to the callback function.
        """
        self._on_input()

    def _init_ui(self, label: str) -> None:
        """Initialize the UI components of the ModeSelect widget."""
        self._add_widgets(label)
        self._set_layout()

    def _add_widgets(self, label: str) -> None:
        """Add widgets to the ModeSelect widget."""
        self._add_label(label)
        self._add_options()
        self._add_button()

    def _add_label(self, label: str) -> None:
        """Add a label to the widget."""
        self.label = QLabel(label)
        self.label.setFixedWidth(90)

    def _add_options(self) -> None:
        """Add a combo box for selecting the mode."""
        self.options = QComboBox()
        self.options.setFixedWidth(120)
        self.options.addItems([e.name for e in self._enum_class])
        self.options.setToolTip("Select a mode")

    def _add_button(self) -> None:
        """Add a button to send the selected mode."""
        self.button = QPushButton("Send")
        self.button.setFixedWidth(50)
        self.button.setToolTip("Send the value")
        self.button.clicked.connect(self._on_input)

    def _on_input(self) -> None:
        """Handle the input from the user."""
        value = self.options.currentText()

        if not value:
            return

        self._line_follower.send_message(
            Messages.from_int(self._message, self._enum_class[value].value)
        )

    def _set_layout(self) -> None:
        """Set the layout for the widget."""
        layout = QHBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.options)
        layout.addWidget(self.button)
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
