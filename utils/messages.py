from .robot_configs import RunningModes, StopModes
from .serial_protocol import SERIAL_MESSAGE_SIZES, SerialMessage, SerialMessages


class Messages:
    """List of messages that can be sent to the robot."""

    START_SIGNAL = SerialMessage.from_message(SerialMessages.START)
    STOP_SIGNAL = SerialMessage.from_message(SerialMessages.STOP)

    @staticmethod
    def SET_KP(value: int) -> SerialMessage:
        return Messages._int_message(SerialMessages.PID_KP, value)

    @staticmethod
    def SET_KI(value: int) -> SerialMessage:
        return Messages._int_message(SerialMessages.PID_KI, value)

    @staticmethod
    def SET_KD(value: int) -> SerialMessage:
        return Messages._int_message(SerialMessages.PID_KD, value)

    @staticmethod
    def SET_KB(value: int) -> SerialMessage:
        return Messages._int_message(SerialMessages.PID_KB, value)

    @staticmethod
    def SET_KFF(value: int) -> SerialMessage:
        return Messages._int_message(SerialMessages.PID_KFF, value)

    @staticmethod
    def SET_ACCEL(value: int) -> SerialMessage:
        return Messages._int_message(SerialMessages.PID_ACCEL, value)

    @staticmethod
    def SET_BASE_PWM(value: int) -> SerialMessage:
        return Messages._int_message(SerialMessages.PID_BASE_PWM, value)

    @staticmethod
    def SET_MAX_PWM(value: int) -> SerialMessage:
        return Messages._int_message(SerialMessages.PID_MAX_PWM, value)

    @staticmethod
    def SET_RUNNING_MODE(mode: RunningModes) -> SerialMessage:
        return SerialMessage.from_message(SerialMessages.RUNNING_MODE, mode.to_bytes())

    @staticmethod
    def SET_STOP_MODE(mode: StopModes) -> SerialMessage:
        return SerialMessage.from_message(SerialMessages.STOP_MODE, mode.to_bytes())

    @staticmethod
    def SET_LAPS(value: int) -> SerialMessage:
        return Messages._int_message(SerialMessages.LAPS, value)

    @staticmethod
    def SET_STOP_TIME(value: int) -> SerialMessage:
        return Messages._int_message(SerialMessages.LAPS, value)

    @staticmethod
    def SET_LOG_DATA(value: bool) -> SerialMessage:
        return Messages._bool_message(SerialMessages.LOG_DATA, value)

    @staticmethod
    def SET_TURBINE_PWM(value: int) -> SerialMessage:
        return Messages._int_message(SerialMessages.TURBINE_PWM, value)

    @staticmethod
    def from_int(message: SerialMessages, value: int) -> SerialMessage:
        """
        Create a SerialMessage from an integer value.

        Args:
            message (SerialMessages): The message type.
            value (int): The integer value to include in the message.

        Returns:
            SerialMessage: The constructed SerialMessage.
        """
        bytes_needed = SERIAL_MESSAGE_SIZES.get(message, 0)
        return SerialMessage.from_message(
            message, value.to_bytes(bytes_needed, byteorder="little")
        )

    @staticmethod
    def _int_message(message: SerialMessages, value: int) -> SerialMessage:
        """Create a message with an integer value."""
        bytes_needed = SERIAL_MESSAGE_SIZES.get(message, 0)
        return SerialMessage.from_message(
            message, value.to_bytes(bytes_needed, byteorder="little")
        )

    @staticmethod
    def _bool_message(message: SerialMessages, value: bool) -> SerialMessage:
        """Create a message with a boolean value."""
        byte = b"\x01" if value else b"\x00"
        return SerialMessage.from_message(message, byte)
