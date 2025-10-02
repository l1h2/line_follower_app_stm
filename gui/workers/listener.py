from PyQt6.QtCore import QThread, pyqtSignal

from robot import LineFollower
from utils import Files, SerialMessage, app_configs


class BluetoothListenerWorker(QThread):
    """
    ### BluetoothListenerWorker Class

    This class is responsible for listening to the Bluetooth device and processing the received data.
    It inherits from QThread to run in a separate thread.

    #### Signals:
    - `log_output (str)`: Signal emitted when new log is received from the Bluetooth device.
    - `serial_output (SerialMessage)`: Signal emitted when new serial message is received from the Bluetooth device.

    #### Properties:
    - `listening (bool)`: Indicates if the listener is currently active.

    #### Methods:
    - `run()`: Starts the listener thread.
    - `stop()`: Stops the listener thread.
    """

    log_output = pyqtSignal(str)
    serial_output = pyqtSignal(SerialMessage)

    def __init__(self):
        super().__init__()
        self._line_follower = LineFollower()
        self._listening = False

        self._line_follower.bluetooth.log_output.connect(self._on_log_output)
        self._line_follower.bluetooth.serial_output.connect(self._on_serial_output)

    @property
    def listening(self) -> bool:
        """Check if the listener is currently active."""
        return self._listening

    def run(self) -> None:
        """
        Starts the listener thread.
        """
        self._listening = True

        while self._listening:
            self._line_follower.bluetooth.read_data()

    def stop(self) -> None:
        """
        Stops the listener thread.
        """
        self._listening = False

    def _on_log_output(self, log: str) -> None:
        """Handle log output from the Bluetooth device."""
        with open(Files.TEXT_FILE, "a", encoding="latin-1") as f:
            f.write(f"{log}\n")
            f.flush()
        self.log_output.emit(log)

    def _on_serial_output(self, message: SerialMessage) -> None:
        """Handle serial message output from the Bluetooth device."""
        if app_configs.DEBUG_ENABLED:
            with open(Files.TEXT_FILE, "a", encoding="latin-1") as f:
                f.write(f"{message.string}\n")
                f.flush()
        self.serial_output.emit(message)
