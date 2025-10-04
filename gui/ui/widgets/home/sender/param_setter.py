from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QWidget

from utils import Booleans, RunningModes, SerialMessages, StopModes, UIConstants

from ..listener.str_display import StrDisplay
from .mode_select import ModeSelect
from .num_input import NumInput


class ParamSetter(QWidget):
    """
    ### ParamSetter Widget

    A widget that combines an input field (either numeric or mode selection) with a display field to show
    the current value of a parameter in the robot.

    #### Parameters:
    - `label (str)`: The label for the input field.
    - `message (SerialMessages)`: The type of message to be sent and received.

    #### Attributes:
    - `input (NumInput | ModeSelect)`: The input field for the parameter value.
    - `display (StrDisplay)`: The display field for showing the current parameter value.

    #### Methods:
    - `send_value() -> None`: Sends the value from the input field to the robot.
    """

    def __init__(self, label: str, message: SerialMessages):
        super().__init__()
        self._label = label
        self._message = message

        self.setFixedHeight(UIConstants.ROW_HEIGHT)
        self._init_ui()

    def _init_ui(self) -> None:
        """Initialize the UI components of the ParamSetter widget."""
        self._add_widgets()
        self._set_layout()

    def send_value(self) -> None:
        """
        Send the value from the input field to the callback function.
        """
        if self.input.value == self.display.value.text():
            return

        self.input.send_value()

    def _add_widgets(self) -> None:
        """Add widgets to the ParamSetter widget."""
        if self._message == SerialMessages.RUNNING_MODE:
            self.input = ModeSelect(self._label, self._message, RunningModes)
        elif self._message == SerialMessages.STOP_MODE:
            self.input = ModeSelect(self._label, self._message, StopModes)
        elif self._message == SerialMessages.LOG_DATA:
            self.input = ModeSelect(self._label, self._message, Booleans)
        else:
            self.input = NumInput(self._label, self._message)

        self.input.setFixedWidth(300)

        self.display = StrDisplay(self._message)

    def _set_layout(self) -> None:
        """Set the layout for the widget."""
        layout = QHBoxLayout(self)
        layout.addWidget(self.input)
        layout.addWidget(self.display)
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
