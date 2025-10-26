from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QStackedLayout, QVBoxLayout, QWidget

from gui.workers import BluetoothListenerWorker
from utils import SerialMessage, SerialMessages, debug_enabled

from .debug_button import DebugButton
from .str_display import StrDisplay
from .text_display import TextDisplayContainer


class ListenerWidget(QWidget):
    """
    ### ListenerWidget Class

    A widget that listens for incoming data from the robot via Bluetooth and displays it in a user-friendly format.

    #### Attributes:
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

        self.output_display = TextDisplayContainer(parent=self)
        self.debug_button = DebugButton(self)

    def _set_layout(self) -> None:
        """Set the layout for the widget."""
        text_output_layout = QStackedLayout()
        text_output_layout.addWidget(self.debug_button)
        text_output_layout.addWidget(self.output_display)
        text_output_layout.setStackingMode(QStackedLayout.StackingMode.StackAll)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.state_display)
        main_layout.addLayout(text_output_layout)

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
        if debug_enabled():
            self.output_display.print_text(message.string)
