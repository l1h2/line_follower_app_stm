from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QWidget

from robot import LineFollower
from utils import (
    Booleans,
    RobotStates,
    RunningModes,
    SerialMessages,
    StopModes,
    UIConstants,
)


class StrDisplay(QWidget):
    """
    ### StrDisplay Widget

    A widget that displays a string value in a read-only field. It is used to show the current value
    of a parameter in the robot.

    #### Parameters:
    - `label (str)`: The label for the display field.
    - `align (Qt.AlignmentFlag)`: The alignment of the label and value display.

    #### Attributes:
    - `label (QLabel)`: The label for the display field.
    - `value (QLineEdit)`: The read-only field for displaying the numeric value.

    #### Methods:
    - `set_value(value: str) -> None`: Sets the value of the display.
    """

    def __init__(
        self,
        message: SerialMessages,
        label: str = "Current value:",
        align: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignLeft,
    ) -> None:
        super().__init__()
        self._message = message
        self._line_follower = LineFollower()

        self.setFixedHeight(UIConstants.ROW_HEIGHT)
        self._init_ui(label, align)

        self._line_follower.connect_attr_changer(self._update_value)

    def set_value(self, value: str) -> None:
        """
        Set the value of the display.

        Args:
            value (str): The value to be displayed.
        """
        self.value.setText(value)

    def _init_ui(self, label: str, align: Qt.AlignmentFlag) -> None:
        """Initialize the UI components of the NumDisplay widget."""
        self._add_widgets(label)
        self._set_layout(align)

    def _add_widgets(self, label: str) -> None:
        """Add widgets to the NumDisplay widget."""
        self._add_label(label)
        self._add_value()

    def _add_label(self, label: str) -> None:
        """Add a label to the widget."""
        self.label = QLabel(label)
        self.label.setFixedWidth(80)

    def _add_value(self) -> None:
        """Add a value display to the widget."""
        self.value = QLineEdit()
        self.value.setText("-")
        self.value.setFixedWidth(100)
        self.value.setToolTip("Current value in the robot")
        self.value.setReadOnly(True)

    def _set_layout(self, align: Qt.AlignmentFlag) -> None:
        """Set the layout for the widget."""
        layout = QHBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.value)
        layout.setAlignment(align)

    def _update_value(self, message: SerialMessages, value: int) -> None:
        """Update the value display when the corresponding attribute changes."""
        if message != self._message:
            return

        str_value = str(value)

        if message == SerialMessages.STATE:
            str_value = RobotStates(value).name
        elif message == SerialMessages.RUNNING_MODE:
            str_value = RunningModes(value).name
        elif message == SerialMessages.STOP_MODE:
            str_value = StopModes(value).name
        elif message == SerialMessages.LOG_DATA:
            str_value = Booleans(value).name

        self.value.setText(str_value)
