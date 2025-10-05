from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget

from utils import SerialMessages, Styles

from .fields.param_setter import ParamSetter


class SpeedSender(QWidget):
    """
    ### SpeedSender Class

    A widget that allows the user to send Speed-related parameters to the robot via Bluetooth.

    #### Attributes:
    - `kp_input (ParamSetter)`: Input field for the Speed KP value.
    - `ki_input (ParamSetter)`: Input field for the Speed KI value.
    - `kd_input (ParamSetter)`: Input field for the Speed KD value.
    - `base_speed (ParamSetter)`: Input field for the base speed value.
    """

    def __init__(self):
        super().__init__()

        self._init_ui()

    def send_all(self):
        """
        Send all Speed-related parameters to the robot.
        """
        self.kp_input.send_value()
        self.ki_input.send_value()
        self.kd_input.send_value()
        self.base_speed.send_value()

    def _init_ui(self) -> None:
        """Initialize the UI components of the Speed sender widget."""
        self._add_widgets()
        self._set_layout()

    def _add_widgets(self) -> None:
        """Add widgets to the Speed sender widget."""
        self._add_tittle()

        self.kp_input = ParamSetter("Speed KP:", SerialMessages.SPEED_KP)
        self.ki_input = ParamSetter("Speed KI:", SerialMessages.SPEED_KI)
        self.kd_input = ParamSetter("Speed KD:", SerialMessages.SPEED_KD)
        self.base_speed = ParamSetter("Base Speed (cm/s):", SerialMessages.BASE_SPEED)

    def _add_tittle(self) -> None:
        """Add title to the GeneralSender widget."""
        self._tittle = QLabel("Speed Parameters")
        self._tittle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._tittle.setStyleSheet(Styles.TITTLES)

    def _set_layout(self) -> None:
        """Set the layout for the sender widget."""
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self._tittle)
        main_layout.addWidget(self.kp_input)
        main_layout.addWidget(self.ki_input)
        main_layout.addWidget(self.kd_input)
        main_layout.addWidget(self.base_speed)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        main_layout.setContentsMargins(0, 0, 0, 0)
