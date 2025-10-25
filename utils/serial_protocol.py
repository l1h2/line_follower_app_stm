from collections.abc import Callable
from dataclasses import dataclass
from enum import IntEnum

SERIAL_FRAME_START = 0xAA
SERIAL_MESSAGE_MAX_PAYLOAD = 8
SERIAL_MESSAGE_MINIMUM_SIZE = 3  # Start + ID + Checksum


class SerialMessages(IntEnum):
    """Enumeration of serial message types."""

    INVALID_MESSAGE = 0
    PING = 1
    START = 2
    STOP = 3
    STATE = 4
    RUNNING_MODE = 5
    STOP_MODE = 6
    LAPS = 7
    STOP_TIME = 8
    STOP_DISTANCE = 9
    LOG_DATA = 10
    PID_KP = 11
    PID_KI = 12
    PID_KD = 13
    PID_KB = 14
    PID_KFF = 15
    PID_ALPHA = 16
    PID_CLAMP = 17
    PID_ACCEL = 18
    PID_BASE_PWM = 19
    PID_MAX_PWM = 20
    TURBINE_PWM = 21
    SPEED_KP = 22
    SPEED_KI = 23
    SPEED_KD = 24
    SPEED_KFF = 25
    BASE_SPEED = 26
    LOOKAHEAD = 27
    WHEEL_BASE_CORRECTION = 28
    IMU_ALPHA = 29
    OPERATION_DATA = 30


SERIAL_MESSAGE_SIZES: dict[SerialMessages, int] = {
    SerialMessages.INVALID_MESSAGE: 0,
    SerialMessages.PING: 0,
    SerialMessages.START: 0,
    SerialMessages.STOP: 0,
    SerialMessages.STATE: 1,
    SerialMessages.RUNNING_MODE: 1,
    SerialMessages.STOP_MODE: 1,
    SerialMessages.LAPS: 1,
    SerialMessages.STOP_TIME: 1,
    SerialMessages.LOG_DATA: 1,
    SerialMessages.PID_KP: 1,
    SerialMessages.PID_KI: 1,
    SerialMessages.PID_KD: 2,
    SerialMessages.PID_KB: 1,
    SerialMessages.PID_KFF: 1,
    SerialMessages.PID_ACCEL: 2,
    SerialMessages.PID_BASE_PWM: 2,
    SerialMessages.PID_MAX_PWM: 2,
    SerialMessages.TURBINE_PWM: 2,
    SerialMessages.SPEED_KP: 2,
    SerialMessages.SPEED_KI: 2,
    SerialMessages.SPEED_KD: 2,
    SerialMessages.BASE_SPEED: 2,
    SerialMessages.PID_ALPHA: 2,
    SerialMessages.PID_CLAMP: 2,
    SerialMessages.STOP_DISTANCE: 2,
    SerialMessages.OPERATION_DATA: 8,
    SerialMessages.LOOKAHEAD: 1,
    SerialMessages.SPEED_KFF: 2,
    SerialMessages.WHEEL_BASE_CORRECTION: 2,
    SerialMessages.IMU_ALPHA: 2,
}

FLOAT_MESSAGES = {
    SerialMessages.BASE_SPEED: 2,
    SerialMessages.PID_ALPHA: 2,
    SerialMessages.SPEED_KI: 4,
    SerialMessages.WHEEL_BASE_CORRECTION: 2,
    SerialMessages.IMU_ALPHA: 2,
}


@dataclass
class SerialMessage:
    """
    ### Representation of a serial message.

    Message object used for communication over serial protocol.

    #### Attributes:
    - `message (SerialMessages)`: The type of the message.
    - `payload (bytes)`: The payload of the message.
    - `size (int)`: The size of the payload.

    ### Properties:
    - `frame (bytes)`: The byte frame representation of the message.
    - `string (str)`: String representation of the message.

    #### Methods:
    - `from_frame(frame: bytes) -> "SerialMessage"`: Creates a SerialMessage from a byte frame.
    - `from_message(message: SerialMessages, payload: bytes, checksum: int) -> "SerialMessage"`: Creates a SerialMessage from its components.
    - `from_int(message: SerialMessages, value: int) -> "SerialMessage"`: Create a SerialMessage from an integer value.
    - `from_bool(message: SerialMessages, value: bool) -> "SerialMessage"`: Create a SerialMessage from a boolean value.
    - `from_float(message: SerialMessages, value: float) -> "SerialMessage"`: Create a SerialMessage from a float value.
    """

    message: SerialMessages
    payload: bytes = b""
    size: int = 0

    @staticmethod
    def _validate_checksum(msg: SerialMessages, payload: bytes, checksum: int) -> bool:
        """Validate the checksum of a message."""
        calculated_checksum = msg.value
        for byte in payload:
            calculated_checksum ^= byte
        calculated_checksum &= 0xFF
        return calculated_checksum == checksum

    @staticmethod
    def from_frame(frame: bytes) -> "SerialMessage":
        """
        Creates a SerialMessage from a byte frame.

        Args:
            frame (bytes): The byte frame to parse.

        Returns:
            SerialMessage: The parsed SerialMessage object.
        """
        if len(frame) < SERIAL_MESSAGE_MINIMUM_SIZE:
            return SerialMessage(SerialMessages.INVALID_MESSAGE, b"", 0)

        if frame[0] != SERIAL_FRAME_START:
            return SerialMessage(SerialMessages.INVALID_MESSAGE, b"", 0)

        if frame[1] not in SerialMessages:
            return SerialMessage(SerialMessages.INVALID_MESSAGE, b"", 0)

        message_type = SerialMessages(frame[1])
        expected_size = SERIAL_MESSAGE_SIZES.get(message_type, 0)

        if len(frame) != expected_size + SERIAL_MESSAGE_MINIMUM_SIZE:
            return SerialMessage(SerialMessages.INVALID_MESSAGE, b"", 0)

        payload = frame[2 : 2 + expected_size]

        if not SerialMessage._validate_checksum(message_type, payload, frame[-1]):
            return SerialMessage(SerialMessages.INVALID_MESSAGE, b"", 0)

        return SerialMessage(message_type, payload, expected_size)

    @staticmethod
    def from_message(
        message: SerialMessages,
        payload: bytes = b"",
        checksum: int | None = None,
    ) -> "SerialMessage":
        """
        Creates a SerialMessage from its components.

        Args:
            message (SerialMessages): The type of the message.
            payload (bytes): The payload of the message.
            checksum (int | None): The checksum of the message.

        Returns:
            SerialMessage: The constructed SerialMessage object.
        """
        expected_size = SERIAL_MESSAGE_SIZES.get(message, 0)
        if len(payload) != expected_size:
            return SerialMessage(SerialMessages.INVALID_MESSAGE)

        if checksum is not None and not SerialMessage._validate_checksum(
            message, payload, checksum
        ):
            return SerialMessage(SerialMessages.INVALID_MESSAGE)

        return SerialMessage(message, payload, expected_size)

    @staticmethod
    def from_int(message: SerialMessages, value: int) -> "SerialMessage":
        """
        Create a SerialMessage from an integer value.

        Args:
            message (SerialMessages): The message type.
            value (int): The integer value to include in the message.

        Returns:
            SerialMessage: The constructed SerialMessage.
        """
        expected_size = SERIAL_MESSAGE_SIZES.get(message, 0)
        return SerialMessage.from_message(
            message, value.to_bytes(expected_size, byteorder="little")
        )

    @staticmethod
    def from_bool(message: SerialMessages, value: bool) -> "SerialMessage":
        """
        Create a SerialMessage from a boolean value.

        Args:
            message (SerialMessages): The message type.
            value (bool): The boolean value to include in the message.

        Returns:
            SerialMessage: The constructed SerialMessage.
        """
        byte = b"\x01" if value else b"\x00"
        return SerialMessage.from_message(message, byte)

    @staticmethod
    def from_float(message: SerialMessages, value: float) -> "SerialMessage":
        """
        Create a SerialMessage from a float value.

        Args:
            message (SerialMessages): The message type.
            value (float): The float value to include in the message.

        Returns:
            SerialMessage: The constructed SerialMessage.
        """
        value = int(value * 100)  # Convert to integer representation
        expected_size = SERIAL_MESSAGE_SIZES.get(message, 0)
        return SerialMessage.from_message(
            message, value.to_bytes(expected_size, byteorder="little")
        )

    @property
    def frame(self) -> bytes:
        """The byte frame representation of the message."""
        return bytes([self.message.value]) + self.payload

    @property
    def string(self) -> str:
        """String representation of the message."""
        return f"Message: {self.message.name}, Payload: {self.payload}, Frame: {self.frame}"


class SerialParser:
    """
    ### Parser for serial data streams.

    Parses incoming bytes from a serial data stream and reconstructs messages based on the defined protocol.

    #### Parameters:
    - `on_frame (Callable[[SerialMessage], None])`: Callback function invoked when a complete message is parsed.
    - `on_log (Callable[[str], None])`: Callback function invoked when a log message is parsed.

    #### Methods:
    - `feed_byte(byte: int) -> None`: Feeds a single byte into the parser.
    """

    _SYNC, _ID, _PAYLOAD, _CHECKSUM = range(4)

    def __init__(
        self, on_frame: Callable[[SerialMessage], None], on_log: Callable[[str], None]
    ) -> None:
        self._state = self._SYNC
        self._msg_id = SerialMessages.INVALID_MESSAGE
        self._expected_payload_size = 0
        self._payload = bytearray()
        self._log_buffer = bytearray()
        self._message = None

        self._on_frame = on_frame
        self._on_log = on_log

    def feed_byte(self, byte: int) -> None:
        """
        Feeds a single byte into the parser.

        Args:
            byte (int): The byte to feed into the parser.
        """
        if self._state != self._SYNC:
            self._handle_data_byte(byte)
            return

        if byte == 0xAA:
            self._state = self._ID
        else:
            self._handle_log_byte(byte)

    def _handle_data_byte(self, byte: int) -> None:
        """Handle bytes that are part of a data message."""
        if self._state == self._ID:
            self._handle_id_byte(byte)
        elif self._state == self._PAYLOAD:
            self._handle_payload_byte(byte)
        elif self._state == self._CHECKSUM:
            self._handle_checksum_byte(byte)

    def _handle_id_byte(self, byte: int) -> None:
        """Handle the message ID byte."""
        self._msg_id = (
            SerialMessages(byte)
            if byte in SerialMessages
            else SerialMessages.INVALID_MESSAGE
        )
        self._expected_payload_size = SERIAL_MESSAGE_SIZES.get(self._msg_id, 0)
        self._payload.clear()

        if self._expected_payload_size > 0:
            self._state = self._PAYLOAD
        else:
            self._state = self._CHECKSUM

    def _handle_payload_byte(self, byte: int) -> None:
        """Handle bytes that are part of the payload."""
        self._payload.append(byte)
        if len(self._payload) == self._expected_payload_size:
            self._state = self._CHECKSUM

    def _handle_checksum_byte(self, byte: int) -> None:
        """Handle the checksum byte and finalize the message."""
        checksum = byte
        self._message = SerialMessage.from_message(
            self._msg_id, bytes(self._payload), checksum
        )
        self._state = self._SYNC
        self._on_frame(self._message)

    def _handle_log_byte(self, byte: int) -> None:
        """Handle bytes that are part of log messages."""
        if byte != 0x0A:  # Newline ('\n')
            self._log_buffer.append(byte)
            return

        data = self._log_buffer.decode("latin-1")
        self._log_buffer.clear()
        self._on_log(data)


class OperationData:
    """
    ### Parser for operation data received from the robot.

    Parses the operation data payload received from the robot and provides
    access to its components.

    #### Parameters:
    - `payload (bytes | None)`: The payload bytes containing the operation data. If `None` or invalid, initializes all attributes to zero.

    #### Attributes:
    - `central_sensors_byte (int)`: Byte representing the state of central sensors.
    - `left_sensor (int)`: State of the left sensor (0 or 1).
    - `right_sensor (int)`: State of the right sensor (0 or 1).
    - `sensors (list[int])`: List of sensor states in the order [left, central sensors..., right].
    - `x (int)`: X coordinate of the robot.
    - `y (int)`: Y coordinate of the robot.
    - `heading (int)`: Heading angle of the robot.

    #### Methods:
    - `update(payload: bytes) -> None`: Updates the operation data with a new payload
    """

    def __init__(self, payload: bytes | None = None) -> None:
        if payload is None or len(payload) != 8:
            self._empty_init()
            return

        self.update(payload)

    def update(self, payload: bytes) -> None:
        """
        Updates the operation data with a new payload.

        Args:
            payload (bytes): The new payload containing the operation data.
        """
        self.central_sensors_byte = payload[0]
        self.left_sensor = payload[1] & 0x01
        self.right_sensor = (payload[1] >> 1) & 0x01
        self._organize_sensor_array()

        self.x = int.from_bytes(payload[2:4], byteorder="little", signed=True)
        self.y = int.from_bytes(payload[4:6], byteorder="little", signed=True)
        self.heading = (
            float(int.from_bytes(payload[6:8], byteorder="little", signed=True)) / 10000
        )

    def _empty_init(self) -> None:
        """Initializes all attributes to zero."""
        self.central_sensors_byte = 0
        self.left_sensor = 0
        self.right_sensor = 0
        self.sensors = [0] * 10
        self.x = 0
        self.y = 0
        self.heading = 0

    def _organize_sensor_array(self) -> None:
        """Organizes the sensor array in a specific order."""
        self.sensors = [self.left_sensor]
        for i in range(8):
            self.sensors.append((self.central_sensors_byte >> i) & 0x01)
        self.sensors.append(self.right_sensor)
