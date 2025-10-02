from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QWidget

from robot import LineFollower
from utils import Booleans, RunningModes, SerialMessages, StopModes

from .mode_select import ModeSelect
from .num_input import NumInput


class SenderWidget(QWidget):
    """
    ### SenderWidget Class

    A widget that allows the user to send commands to the robot via Bluetooth.

    #### Attributes:
    - `kp_input (NumInput)`: Input field for the KP value.
    - `ki_input (NumInput)`: Input field for the KI value.
    - `kd_input (NumInput)`: Input field for the KD value.
    - `kff_input (NumInput)`: Input field for the KFF value.
    - `kb_input (NumInput)`: Input field for the KB value.
    - `base_pwm_input (NumInput)`: Input field for the base PWM value.
    - `turbine_pwm_input (NumInput)`: Input field for the turbine PWM value.
    - `laps_input (NumInput)`: Input field for the number of laps.
    - `stop_time_input (NumInput)`: Input field for the stop time value.
    - `running_mode_input (ModeSelect)`: Mode select for the running mode.
    - `stop_mode_input (ModeSelect)`: Mode select for the stop mode.
    - `log_data_input (ModeSelect)`: Mode select for logging data.
    - `send_all_button (QPushButton)`: Button to send all values to the robot.
    """

    def __init__(self):
        super().__init__()
        self._line_follower = LineFollower()

        self._init_ui()

    def _init_ui(self) -> None:
        """Initialize the UI components of the sender widget."""
        self._add_widgets()
        self._set_layout()

    def _add_widgets(self) -> None:
        """Add widgets to the sender widget."""
        self.kp_input = NumInput("KP:", SerialMessages.PID_KP)
        self.ki_input = NumInput("KI:", SerialMessages.PID_KI)
        self.kd_input = NumInput("KD:", SerialMessages.PID_KD)
        self.kff_input = NumInput("KFF:", SerialMessages.PID_KFF)
        self.kb_input = NumInput("KB:", SerialMessages.PID_KB)
        self.base_pwm_input = NumInput("Base PWM:", SerialMessages.PID_BASE_PWM, 1000)
        self.turbine_pwm_input = NumInput(
            "Turbine PWM:", SerialMessages.TURBINE_PWM, 1000
        )
        self.laps_input = NumInput("Laps:", SerialMessages.LAPS, 100)
        self.stop_time_input = NumInput("Stop Time (s):", SerialMessages.STOP_TIME, 180)

        self.running_mode_input = ModeSelect(
            "Running Mode:", SerialMessages.RUNNING_MODE, RunningModes
        )
        self.stop_mode_input = ModeSelect(
            "Stop Mode:", SerialMessages.STOP_MODE, StopModes
        )
        self.log_data_input = ModeSelect("Log Data:", SerialMessages.LOG_DATA, Booleans)

        self._add_send_all_button()

    def _add_send_all_button(self) -> None:
        """Add a button to send all values to the robot."""
        self.send_all_button = QPushButton("Send All")
        self.send_all_button.setFixedHeight(30)
        self.send_all_button.setToolTip("Send all values to the robot")
        self.send_all_button.setStyleSheet("background-color: #4CAF50; color: white;")
        self.send_all_button.clicked.connect(self._on_send_all)

    def _on_send_all(self) -> None:
        """Send all values to the robot."""
        self.kp_input.send_value()
        self.ki_input.send_value()
        self.kd_input.send_value()
        self.kff_input.send_value()
        self.kb_input.send_value()
        self.base_pwm_input.send_value()
        self.turbine_pwm_input.send_value()
        self.laps_input.send_value()
        self.stop_time_input.send_value()

        self.running_mode_input.send_value()
        self.stop_mode_input.send_value()
        self.log_data_input.send_value()

    def _set_layout(self) -> None:
        """Set the layout for the sender widget."""
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.kp_input)
        main_layout.addWidget(self.ki_input)
        main_layout.addWidget(self.kd_input)
        main_layout.addWidget(self.kff_input)
        main_layout.addWidget(self.kb_input)
        main_layout.addWidget(self.base_pwm_input)
        main_layout.addWidget(self.turbine_pwm_input)
        main_layout.addWidget(self.laps_input)
        main_layout.addWidget(self.stop_time_input)
        main_layout.addWidget(self.running_mode_input)
        main_layout.addWidget(self.stop_mode_input)
        main_layout.addWidget(self.log_data_input)
        main_layout.addWidget(self.send_all_button)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
