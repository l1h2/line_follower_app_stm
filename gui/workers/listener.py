import atexit
from io import TextIOWrapper

from PyQt6.QtCore import QThread, QTimer, pyqtSignal

from robot import LineFollower
from utils import Files, SerialConfig, SerialMessage, debug_enabled


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
    - `stop()`: Stops the listener thread, waiting for its current read to finish.
    """

    log_output = pyqtSignal(str)
    serial_output = pyqtSignal(SerialMessage)

    def __init__(self):
        super().__init__()
        self._line_follower = LineFollower()
        self._listening = False
        self._text_file: TextIOWrapper | None = None

        self._close_timer = QTimer(self)
        self._close_timer.setSingleShot(True)
        self._close_timer.setInterval(int(SerialConfig.LOG_FLUSH_INTERVAL * 1000))
        self._close_timer.timeout.connect(self._close_text_file)

        self._line_follower.bluetooth.log_output.connect(self._on_log_output)
        self._line_follower.bluetooth.serial_output.connect(self._on_serial_output)

        atexit.register(self._close_text_file)

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
            if not self._line_follower.bluetooth.read_data():
                self.msleep(SerialConfig.POLL_INTERVAL_MS)

    def stop(self) -> None:
        """
        Stops the listener thread, waiting for its current read to finish.
        """
        self._listening = False
        self.wait()

    def _on_log_output(self, log: str) -> None:
        """Handle log output from the Bluetooth device."""
        self._write_text_file(log)
        self.log_output.emit(log)

    def _on_serial_output(self, message: SerialMessage) -> None:
        """Handle serial message output from the Bluetooth device."""
        if debug_enabled():
            self._write_text_file(message.string)
        self.serial_output.emit(message)

    def _write_text_file(self, text: str) -> None:
        """Write a line to the text log file, which a timer closes to write in batches."""
        if self._text_file is None:
            self._text_file = open(Files.TEXT_FILE, "a", encoding="latin-1")
            self._close_timer.start()

        self._text_file.write(f"{text}\n")

    def _close_text_file(self) -> None:
        """Close the text log file, writing its buffered lines."""
        if self._text_file is not None:
            self._text_file.close()
            self._text_file = None
