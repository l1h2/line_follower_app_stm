from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QWidget

from utils import SerialMessages, Styles

from .fields.param_setter import ParamSetter


class GeneralSender(QWidget):
    """
    ### GeneralSender Class

    A widget that allows the user to send general parameters to the robot via Bluetooth.

    #### Attributes:
    - `turbine_pwm_input (ParamSetter)`: Input field for the turbine PWM value.
    - `laps_input (ParamSetter)`: Input field for the number of laps.
    - `stop_time_input (ParamSetter)`: Input field for the stop time value.
    - `stop_distance_input (ParamSetter)`: Input field for the stop distance value.
    - `running_mode_input (ParamSetter)`: Mode select for the running mode.
    - `stop_mode_input (ParamSetter)`: Mode select for the stop mode.
    - `log_data_input (ParamSetter)`: Mode select for logging data.
    """

    def __init__(self):
        super().__init__()

        self._init_ui()

    def send_all(self):
        """
        Send all PWM-related parameters to the robot.
        """
        self.turbine_pwm_input.send_value()
        self.laps_input.send_value()
        self.stop_time_input.send_value()
        self.stop_distance_input.send_value()

        self.running_mode_input.send_value()
        self.stop_mode_input.send_value()
        self.log_data_input.send_value()

    def _init_ui(self) -> None:
        """Initialize the UI components of the PWM sender widget."""
        self._add_widgets()
        self._set_layout()

    def _add_widgets(self) -> None:
        """Add widgets to the PWM sender widget."""
        self._add_tittle()

        self.turbine_pwm_input = ParamSetter("Turbine PWM:", SerialMessages.TURBINE_PWM)
        self.laps_input = ParamSetter("Laps:", SerialMessages.LAPS)
        self.stop_time_input = ParamSetter("Stop Time (s):", SerialMessages.STOP_TIME)
        self.stop_distance_input = ParamSetter(
            "Stop Distance (cm):", SerialMessages.STOP_DISTANCE
        )

        self.running_mode_input = ParamSetter(
            "Running Mode:", SerialMessages.RUNNING_MODE
        )
        self.stop_mode_input = ParamSetter("Stop Mode:", SerialMessages.STOP_MODE)
        self.log_data_input = ParamSetter("Log Data:", SerialMessages.LOG_DATA)

    def _add_tittle(self) -> None:
        """Add title to the GeneralSender widget."""
        self._tittle = QLabel("General Parameters")
        self._tittle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._tittle.setStyleSheet(Styles.TITTLES)

    def _set_layout(self) -> None:
        """Set the layout for the sender widget."""
        first_column_layout = QVBoxLayout()
        first_column_layout.addWidget(self.turbine_pwm_input)
        first_column_layout.addWidget(self.laps_input)
        first_column_layout.addWidget(self.stop_time_input)
        first_column_layout.addWidget(self.stop_distance_input)
        first_column_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        second_column_layout = QVBoxLayout()
        second_column_layout.addWidget(self.running_mode_input)
        second_column_layout.addWidget(self.stop_mode_input)
        second_column_layout.addWidget(self.log_data_input)
        second_column_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        inputs_layout = QHBoxLayout()
        inputs_layout.addLayout(first_column_layout)
        inputs_layout.addLayout(second_column_layout)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self._tittle)
        main_layout.addLayout(inputs_layout)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.setContentsMargins(0, 0, 0, 0)
