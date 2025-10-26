import atexit
import re
from time import time

import serial
from PyQt6.QtCore import QObject, pyqtSignal
from serial.tools import list_ports, list_ports_common

from utils import SerialConfig, SerialMessage, SerialMessages, SerialParser, get_logger


class BluetoothApi(QObject):
    """
    ### BluetoothApi Class

    Handles Bluetooth communication with the robot. Inherits from QObject to use signals and slots.

    #### Signals:
    - `connection_failed (str)`: Signal emitted when a connection fails, with an error message.
    - `connection_change`: Signal emitted when the Bluetooth connection changes.
    - `log_output (bool)`: Signal emitted when a log message is received.
    - `serial_output (SerialMessage)`: Signal emitted when a serial message is received.

    #### Properties:
    - `port (str)`: Current COM port for the Bluetooth connection.
    - `ports (list[str])`: List of available COM ports.
    - `connected (bool)`: Indicates if the Bluetooth connection is open.

    #### Methods:
    - `list_available_ports() -> list[str]`: Lists all available COM ports.
    - `set_com_port(com_port: str) -> bool`: Sets the COM port for the Bluetooth connection.
    - `connect_serial() -> bool`: Connects to the Bluetooth device using the specified COM port.
    - `disconnect_serial() -> None`: Disconnects from the Bluetooth device.
    - `read_data() -> None`: Reads data from the Bluetooth device.
    - `write_data(data: bytes) -> None`: Writes binary data to the Bluetooth device.
    """

    connection_failed = pyqtSignal(str)
    connection_change = pyqtSignal()
    log_output = pyqtSignal(str)
    serial_output = pyqtSignal(SerialMessage)

    def __init__(self):
        super().__init__()
        self._bluetooth: serial.Serial | None = None
        self._com_port = self._get_initial_port()
        self._parser = SerialParser(self._on_frame, self._on_log)
        self._last_receive_time = 0
        self._logger = get_logger()

        atexit.register(self._safe_disconnect)

    @property
    def port(self) -> str:
        """Get the current COM port."""
        if self._com_port not in self.ports:
            self._com_port = self._get_initial_port()

        return self._com_port

    @property
    def ports(self) -> list[str]:
        """Get the list of available COM ports."""
        return self.list_available_ports()

    @property
    def connected(self) -> bool:
        """Check if the Bluetooth connection is open."""
        return self._bluetooth is not None and self._bluetooth.is_open

    @staticmethod
    def _port_key(port: list_ports_common.ListPortInfo) -> tuple[int | float, str]:
        m = re.search(r"(\d+)$", port.device)
        return (int(m.group(1)) if m else float("inf"), port.device.lower())

    @staticmethod
    def list_available_ports() -> list[str]:
        """
        List all available COM ports.

        Returns:
            list[str]: List of available COM ports.
        """
        return [
            port.device
            for port in sorted(list_ports.comports(), key=BluetoothApi._port_key)
        ]

    def set_com_port(self, com_port: str) -> bool:
        """
        Set the COM port for the Bluetooth connection.

        Args:
            com_port (str): The COM port to set.

        Returns:
            bool: True if the COM port was changed successfully, False otherwise.
        """
        if com_port == self._com_port:
            return False

        if self.connected:
            self._logger.warning("Disconnect before changing port.")
            return False

        if com_port not in self.ports:
            self._logger.error(f"Port {com_port} is not available.")
            return False

        self._com_port = com_port
        return True

    def connect_serial(self) -> bool:
        """
        Connect to the Bluetooth device using the specified COM port.

        Returns:
            bool: True if the connection was successful, False otherwise.
        """
        self._logger.info(f"Connecting to Bluetooth on port {self._com_port}...")
        try:
            self._bluetooth = serial.Serial(
                self._com_port,
                SerialConfig.BAUD_RATE,
                timeout=SerialConfig.TIMEOUT,
                write_timeout=SerialConfig.TIMEOUT,
            )
            self._logger.info("Bluetooth connected.")
            self.connection_change.emit()
        except serial.SerialException as e:
            msg = f"Failed to connect to Bluetooth device: {e}"
            self._logger.error(msg)
            self._bluetooth = None
            self.connection_failed.emit(msg)

        return self.connected

    def disconnect_serial(self) -> None:
        """
        Disconnect from the Bluetooth device.
        """
        if self.connected:
            self._bluetooth.close()  # type: ignore[union-attr]
        self._bluetooth = None

        self._logger.info("Bluetooth disconnected.")
        self.connection_change.emit()

    def read_data(self) -> None:
        """
        Read data from the Bluetooth device.
        """
        if not self.connected:
            return

        try:
            if self._bluetooth.in_waiting <= 0:  # type: ignore[union-attr]
                self._check_timeout()
                return

            self._last_receive_time = time()
            data = self._bluetooth.read(self._bluetooth.in_waiting)  # type: ignore[union-attr]
            for byte in data:
                self._parser.feed_byte(byte)

        except serial.SerialException as e:
            msg = f"Failed to read data from Bluetooth device: {e}"
            self._logger.critical(msg)
            self.disconnect_serial()
            self.connection_failed.emit(msg)

    def write_data(self, data: bytes) -> None:
        """
        Write binary data to the Bluetooth device.

        Args:
            data (bytes): The binary data to write.
        """
        if not self.connected:
            return

        try:
            self._bluetooth.write(data)  # type: ignore[union-attr]
            self._logger.info(f"Sent: {data}")
        except serial.SerialException as e:
            msg = f"Failed to write data to Bluetooth device: {e}"
            self._logger.critical(msg)
            self.disconnect_serial()
            self.connection_failed.emit(msg)

    def _get_initial_port(self) -> str:
        """Get the initial COM port for the Bluetooth connection."""
        ports = self.ports
        if SerialConfig.PORT in ports:
            return SerialConfig.PORT
        return ports[0] if ports else ""

    def _check_timeout(self) -> None:
        """Check for read timeout and handle it."""
        self._check_current_port()
        if time() - self._last_receive_time <= SerialConfig.PING_TIMEOUT:
            return

        self._ping_robot()

    def _check_current_port(self) -> None:
        """Check if the current COM port is still available."""
        if self._com_port not in self.ports:
            self._logger.warning(f"Port {self._com_port} is no longer available.")
            self._com_port = self._get_initial_port()
            raise serial.SerialException("COM port disconnected.")

    def _ping_robot(self) -> None:
        """Send a ping command to the robot to check connectivity."""
        self._send_ping()
        self._wait_for_ping_response()

    def _send_ping(self) -> None:
        ping_msg = SerialMessage.from_message(SerialMessages.PING).frame

        try:
            self._bluetooth.write(ping_msg)  # type: ignore[union-attr]
            self._logger.info(f"Sent: {ping_msg}")
        except serial.SerialException:
            raise serial.SerialException("Could not send ping message to the robot.")

    def _wait_for_ping_response(self) -> None:
        try:
            data = self._bluetooth.read(3)  # type: ignore[union-attr]
            message = SerialMessage.from_frame(data)
            self._logger.info(message.string)

            if message.message != SerialMessages.PING:
                raise serial.SerialException("Invalid ping response received.")

            self._last_receive_time = time()

        except serial.SerialException:
            raise serial.SerialException("Robot took too long to respond.")

    def _safe_disconnect(self) -> None:
        """Safely disconnect from the Bluetooth device when the program exits."""
        if self.connected:
            self._bluetooth.close()  # type: ignore[union-attr]
        self._bluetooth = None

    def _on_log(self, log: str) -> None:
        """Handle log messages from the SerialParser."""
        self._logger.info(f"LOG: {log}")
        self.log_output.emit(log)

    def _on_frame(self, message: SerialMessage) -> None:
        """Handle received serial messages from the SerialParser."""
        self._logger.debug(message.string)
        self.serial_output.emit(message)
