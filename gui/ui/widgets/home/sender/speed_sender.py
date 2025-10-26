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
    - `lookahead (ParamSetter)`: Input field for the lookahead distance.

    #### Methods:
    - `send_all() -> None`: Sends all Speed-related parameters to the robot.
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
        self.kff_input.send_value()
        self.base_speed.send_value()
        self.lookahead.send_value()
        self.curvature_gain.send_value()
        self.imu_alpha.send_value()

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
        self.kff_input = ParamSetter("Speed KFF:", SerialMessages.SPEED_KFF)
        self.base_speed = ParamSetter("Base Speed (cm/s):", SerialMessages.BASE_SPEED)
        self.lookahead = ParamSetter("Lookahead (cm):", SerialMessages.LOOKAHEAD)
        self.curvature_gain = ParamSetter(
            "Curvature Gain:", SerialMessages.WHEEL_BASE_CORRECTION
        )
        self.imu_alpha = ParamSetter("IMU Alpha (%):", SerialMessages.IMU_ALPHA)

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
        main_layout.addWidget(self.kff_input)
        main_layout.addWidget(self.base_speed)
        main_layout.addWidget(self.lookahead)
        main_layout.addWidget(self.curvature_gain)
        main_layout.addWidget(self.imu_alpha)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        main_layout.setContentsMargins(0, 0, 0, 0)
