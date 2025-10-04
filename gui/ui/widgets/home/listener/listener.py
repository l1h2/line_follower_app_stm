from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QStackedLayout, QVBoxLayout, QWidget

from gui.workers import BluetoothListenerWorker
from utils import SerialMessage, SerialMessages, app_configs

from .debug_button import DebugButton
from .str_display import StrDisplay
from .text_display import TextDisplay


class ListenerWidget(QWidget):
    """
    ### ListenerWidget Class

    A widget that listens for incoming data from the robot via Bluetooth and displays it in a user-friendly format.

    #### Attributes:
    - `kp_display (StrDisplay)`: Display for the KP value.
    - `ki_display (StrDisplay)`: Display for the KI value.
    - `kd_display (StrDisplay)`: Display for the KD value.
    - `kff_display (StrDisplay)`: Display for the KFF value.
    - `kb_display (StrDisplay)`: Display for the KB value.
    - `base_pwm_display (StrDisplay)`: Display for the base PWM value.
    - `turbine_pwm_display (StrDisplay)`: Display for the turbine PWM value.
    - `laps_display (StrDisplay)`: Display for the number of laps.
    - `stop_time_display (StrDisplay)`: Display for the stop time value.
    - `running_mode_display (StrDisplay)`: Display for the running mode.
    - `stop_mode_display (StrDisplay)`: Display for the stop mode.
    - `log_data_display (StrDisplay)`: Display for the log data.
    - `state_display (StrDisplay)`: Display for the robot state.
    - `output_display (TextDisplay)`: Display for the output text.
    - `debug_button (DebugButton)`: Button to toggle debug mode.
    """

    def __init__(self):
        super().__init__()
        self._worker = BluetoothListenerWorker()

        self._init_ui()
        self._start_worker()

    def _init_ui(self) -> None:
        """Initialize the UI components of the listener widget."""
        self._add_widgets()
        self._set_layout()

    def _add_widgets(self) -> None:
        """Add widgets to the listener widget."""
        self.state_display = StrDisplay(
            SerialMessages.STATE, "STATE:", Qt.AlignmentFlag.AlignCenter
        )

        self.output_display = TextDisplay(parent=self)
        self.debug_button = DebugButton(self)

    def _set_layout(self) -> None:
        """Set the layout for the widget."""
        state_layout = QHBoxLayout()
        state_layout.addWidget(self.state_display)

        text_output_layout = QStackedLayout()
        text_output_layout.addWidget(self.debug_button)
        text_output_layout.addWidget(self.output_display)
        text_output_layout.setStackingMode(QStackedLayout.StackingMode.StackAll)

        text_display_layout = QVBoxLayout()
        text_display_layout.addLayout(state_layout)
        text_display_layout.addLayout(text_output_layout)

        main_layout = QHBoxLayout(self)
        main_layout.addLayout(text_display_layout)

    def _start_worker(self) -> None:
        """Starts the Bluetooth listener worker."""
        self._worker.log_output.connect(self._handle_log_output)
        self._worker.serial_output.connect(self._handle_serial_message)
        self._worker.start()

    def _handle_log_output(self, data: str) -> None:
        """Handle the log output from the Bluetooth listener worker."""
        self.output_display.print_text(data)

    def _handle_serial_message(self, message: SerialMessage) -> None:
        """Handle incoming serial messages from the robot."""
        if app_configs.DEBUG_ENABLED:
            self.output_display.print_text(message.string)
