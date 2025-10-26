from enum import IntEnum

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QComboBox, QHBoxLayout, QLabel, QPushButton, QWidget

from robot import LineFollower
from utils import SerialMessage, SerialMessages, UIConstants


class ModeSelect(QWidget):
    """
    ### ModeSelect Widget

    A widget that allows the user to select a mode from a combo box and send it to the robot.

    #### Parameters:
    - `label (str)`: The label for the combo box.
    - `command (SerialOutputs)`: The command associated with the selected mode.
    - `enum_class (type[Enum])`: The enum class containing the available modes.

    #### Properties:
    - `value (str)`: The currently selected mode.

    #### Attributes:
    - `label (QLabel)`: The label for the combo box.
    - `options (QComboBox)`: The combo box for selecting the mode.
    - `button (QPushButton)`: The button to send the selected mode.

    #### Methods:
    - `send_value() -> None`: Sends the selected mode to the robot.
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

    @property
    def value(self) -> str:
        """Get the currently selected mode."""
        return self.options.currentText()

    def send_value(self) -> None:
        """
        Send the value from the combo box to the robot.
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
        self.label.setFixedWidth(105)

    def _add_options(self) -> None:
        """Add a combo box for selecting the mode."""
        self.options = QComboBox()
        self.options.setFixedWidth(120)
        self.options.addItems([e.name for e in self._enum_class])
        self.options.setCursor(Qt.CursorShape.PointingHandCursor)
        self.options.setToolTip("Select a mode")

    def _add_button(self) -> None:
        """Add a button to send the selected mode."""
        self.button = QPushButton("Send")
        self.button.setFixedWidth(50)
        self.button.setToolTip("Send the value")
        self.button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.button.clicked.connect(self._on_input)

    def _on_input(self) -> None:
        """Handle the input from the user."""
        value = self.options.currentText()

        if not value:
            return

        self._line_follower.send_message(
            SerialMessage.from_int(self._message, self._enum_class[value].value)
        )

    def _set_layout(self) -> None:
        """Set the layout for the widget."""
        layout = QHBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.options)
        layout.addWidget(self.button)
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
