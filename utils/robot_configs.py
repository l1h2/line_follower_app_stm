from enum import IntEnum

from .serial_protocol import SerialMessages


class RobotStates(IntEnum):
    """List of robot states used in the program."""

    INIT = 0
    IDLE = 1
    RUNNING = 2
    STOPPED = 3
    ERROR = 4


class RunningModes(IntEnum):
    """List of running modes used by the robot."""

    INIT = 0
    SENSOR_TEST = 1
    TURBINE_TEST = 2
    ENCODER_TEST = 3
    PID = 4
    PURE_PURSUIT = 5


class StopModes(IntEnum):
    """List of stop modes used by the robot."""

    NONE = 0
    TIME = 1
    LAPS = 2


PARAM_MAX_VALUES = {
    SerialMessages.PID_BASE_PWM: 1000,
    SerialMessages.PID_ACCEL: 2000,
    SerialMessages.TURBINE_PWM: 1000,
    SerialMessages.LAPS: 100,
    SerialMessages.STOP_TIME: 180,
    SerialMessages.BASE_SPEED: 635,
    SerialMessages.PID_ALPHA: 100,
}
