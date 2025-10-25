from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget

from utils import SerialMessages, Styles

from .fields.param_setter import ParamSetter


class PwmSender(QWidget):
    """
    ### PwmSender Class

    A widget that allows the user to send PWM-related parameters to the robot via Bluetooth.

    #### Attributes:
    - `kp_input (ParamSetter)`: Input field for the KP value.
    - `ki_input (ParamSetter)`: Input field for the KI value.
    - `kd_input (ParamSetter)`: Input field for the KD value.
    - `kff_input (ParamSetter)`: Input field for the KFF value.
    - `kb_input (ParamSetter)`: Input field for the KB value.
    - `accel_input (ParamSetter)`: Input field for the acceleration value.
    - `alpha_input (ParamSetter)`: Input field for the alpha value.
    - `clamp_input (ParamSetter)`: Input field for the clamp value.
    - `base_pwm_input (ParamSetter)`: Input field for the base PWM value.

    #### Methods:
    - `send_all() -> None`: Sends all PWM-related parameters to the robot.
    """

    def __init__(self):
        super().__init__()

        self._init_ui()

    def send_all(self):
        """
        Send all PWM-related parameters to the robot.
        """
        self.kp_input.send_value()
        self.ki_input.send_value()
        self.kd_input.send_value()
        self.kff_input.send_value()
        self.kb_input.send_value()
        self.accel_input.send_value()
        self.alpha_input.send_value()
        self.clamp_input.send_value()
        self.base_pwm_input.send_value()

    def _init_ui(self) -> None:
        """Initialize the UI components of the PWM sender widget."""
        self._add_widgets()
        self._set_layout()

    def _add_widgets(self) -> None:
        """Add widgets to the PWM sender widget."""
        self._add_tittle()

        self.kp_input = ParamSetter("KP:", SerialMessages.PID_KP)
        self.ki_input = ParamSetter("KI:", SerialMessages.PID_KI)
        self.kd_input = ParamSetter("KD:", SerialMessages.PID_KD)
        self.kff_input = ParamSetter("KFF:", SerialMessages.PID_KFF)
        self.kb_input = ParamSetter("KB:", SerialMessages.PID_KB)
        self.alpha_input = ParamSetter("Alpha (%):", SerialMessages.PID_ALPHA)
        self.clamp_input = ParamSetter("Clamp:", SerialMessages.PID_CLAMP)
        self.accel_input = ParamSetter("Acceleration:", SerialMessages.PID_ACCEL)
        self.base_pwm_input = ParamSetter("Base PWM:", SerialMessages.PID_BASE_PWM)

    def _add_tittle(self) -> None:
        """Add title to the GeneralSender widget."""
        self._tittle = QLabel("PWM Parameters")
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
        main_layout.addWidget(self.kb_input)
        main_layout.addWidget(self.alpha_input)
        main_layout.addWidget(self.clamp_input)
        main_layout.addWidget(self.accel_input)
        main_layout.addWidget(self.base_pwm_input)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        main_layout.setContentsMargins(0, 0, 0, 0)
