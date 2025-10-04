from collections.abc import Callable
from dataclasses import dataclass
from enum import IntEnum

SERIAL_FRAME_START = 0xAA
SERIAL_MESSAGE_MAX_PAYLOAD = 4
SERIAL_MESSAGE_MINIMUM_SIZE = 3  # Start + ID + Checksum


class SerialMessages(IntEnum):
    """Enumeration of serial message types."""

    INVALID_MESSAGE = 0
    START = 1
    STOP = 2
    STATE = 3
    RUNNING_MODE = 4
    STOP_MODE = 5
    LAPS = 6
    STOP_TIME = 7
    LOG_DATA = 8
    PID_KP = 9
    PID_KI = 10
    PID_KD = 11
    PID_KB = 12
    PID_KFF = 13
    PID_ACCEL = 14
    PID_BASE_PWM = 15
    PID_MAX_PWM = 16
    TURBINE_PWM = 17


SERIAL_MESSAGE_SIZES: dict[SerialMessages, int] = {
    SerialMessages.INVALID_MESSAGE: 0,
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

    #### Methods:
    - `from_frame(frame: bytes) -> "SerialMessage"`: Creates a SerialMessage from a byte frame.
    - `from_message(message: SerialMessages, payload: bytes, checksum: int) -> "SerialMessage"`: Creates a SerialMessage from its components.
    """

    message: SerialMessages
    payload: bytes = b""
    size: int = 0

    @staticmethod
    def _validate_checksum(msg: SerialMessages, payload: bytes, checksum: int) -> bool:
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
        if self._state == self._ID:
            self._handle_id_byte(byte)
        elif self._state == self._PAYLOAD:
            self._handle_payload_byte(byte)
        elif self._state == self._CHECKSUM:
            self._handle_checksum_byte(byte)

    def _handle_id_byte(self, byte: int) -> None:
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
        self._payload.append(byte)
        if len(self._payload) == self._expected_payload_size:
            self._state = self._CHECKSUM

    def _handle_checksum_byte(self, byte: int) -> None:
        checksum = byte
        self._message = SerialMessage.from_message(
            self._msg_id, bytes(self._payload), checksum
        )
        self._state = self._SYNC
        self._on_frame(self._message)

    def _handle_log_byte(self, byte: int) -> None:
        if byte != 0x0A:  # Newline ('\n')
            self._log_buffer.append(byte)
            return

        data = self._log_buffer.decode("latin-1")
        self._log_buffer.clear()
        self._on_log(data)
