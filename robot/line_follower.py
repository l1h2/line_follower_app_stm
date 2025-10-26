from collections.abc import Callable

from PyQt6.QtCore import QObject, pyqtSignal

from utils import RobotStates, RunningModes, SerialMessage, SerialMessages, StopModes

from .api import BluetoothApi
from .track_mapper import Mapper


class SignalHandler(QObject):
    """
    ### SignalHandler Class

    Handles signals for the LineFollower class. Inherits from QObject to use signals and slots.

    #### Signals:
    - `state_change (RobotStates)`: Signal emitted when the state changes.
    - `attr_changed (SerialMessages, int)`: Signal emitted when an attribute changes.

    #### Methods:
    - `signal_state_changed(state: RobotStates) -> None`: Emits the state change signal.
    - `signal_attr_changed(message: SerialMessages, value: int) -> None`: Emits the attribute change signal.
    """

    state_changed = pyqtSignal(RobotStates)
    attr_changed = pyqtSignal(SerialMessages, int)

    def __init__(self):
        super().__init__()

    def signal_state_changed(self, state: RobotStates) -> None:
        """
        Emits the state changed signal.

        Args:
            state (RobotStates): The new state of the robot.
        """
        self.state_changed.emit(state)

    def signal_attr_changed(self, message: SerialMessages, value: int) -> None:
        """
        Emits the attribute changed signal.

        Args:
            message (SerialMessages): The message type that changed.
            value (int): The new value of the attribute.
        """
        self.attr_changed.emit(message, value)


class LineFollower:
    """
    ### LineFollower Class

    Singleton class that manages the state of the line follower robot. It handles configuration updates and
    communicates with the robot via Bluetooth. Should be updated with the latest configuration values.

    #### Properties:
    - `is_running (bool)`: Indicates if the robot is currently running.
    - `bluetooth (BluetoothApi)`: Instance of BluetoothApi for Bluetooth communication.
    - `kp (int)`: Proportional gain for PID controller.
    - `ki (int)`: Integral gain for PID controller.
    - `kd (int)`: Derivative gain for PID controller.
    - `kb (int)`: Brake gain for PID controller.
    - `kff (int)`: Feedforward gain for PID controller.
    - `acceleration (int)`: Acceleration value for PID controller.
    - `alpha (float)`: Alpha value for PID controller.
    - `clamp (int)`: Clamp value for PID controller.
    - `base_pwm (int)`: Base PWM value for motor control.
    - `max_pwm (int)`: Maximum PWM value for motor control.
    - `state (RobotStates | None)`: Current state of the robot.
    - `running_mode (RunningModes | None)`: Current running mode of the robot.
    - `stop_mode (StopModes | None)`: Current stop mode of the robot.
    - `laps (int)`: Number of laps completed.
    - `stop_time (int)`: Time to stop the robot.
    - `stop_distance (int)`: Distance to stop the robot.
    - `log_data (bool)`: Indicates if data logging is enabled.
    - `turbine_pwm (int)`: Turbine PWM value for motor control.
    - `speed_kp (int)`: Proportional gain for speed PID controller.
    - `speed_ki (float)`: Integral gain for speed PID controller.
    - `speed_kd (int)`: Derivative gain for speed PID controller
    - `speed_kff (int)`: Feedforward gain for speed PID controller.
    - `base_speed (float)`: Base speed for the robot.
    - `lookahead (int)`: Lookahead distance for the robot.
    - `curvature_gain (float)`: Wheel base correction factor used in the robot.
    - `imu_alpha (float)`: Alpha value for the IMU fusion.

    #### Methods:
    - `send_message(message: SerialMessage) -> None`: Sends a serial message to the robot via Bluetooth.
    - `connect_state_changer(slot: Callable[[RobotStates], None]) -> None`: Connects a slot to the state change signal.
    - `connect_attr_changer(slot: Callable[[SerialMessages, int], None]) -> None`: Connects a slot to the attribute change signal.
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LineFollower, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, "_initialized"):
            return

        self._signal_handler = SignalHandler()

        self._kp = None
        self._ki = None
        self._kd = None
        self._kff = None
        self._kb = None
        self._acceleration = None
        self._alpha = None
        self._clamp = None
        self._base_pwm = None
        self._max_pwm = None
        self._state = None
        self._running_mode = None
        self._stop_mode = None
        self._laps = None
        self._stop_time = None
        self._stop_distance = None
        self._log_data = None
        self._turbine_pwm = None
        self._speed_kp = None
        self._speed_ki = None
        self._speed_kd = None
        self._speed_kff = None
        self._base_speed = None
        self._lookahead = None
        self._curvature_gain = None
        self._imu_alpha = None

        self._bluetooth = BluetoothApi()
        self._mapper = Mapper()

        self._bluetooth.serial_output.connect(self._handle_serial_message)

        self._config_map = {
            SerialMessages.PID_KP: self._update_kp,
            SerialMessages.PID_KI: self._update_ki,
            SerialMessages.PID_KD: self._update_kd,
            SerialMessages.PID_KB: self._update_kb,
            SerialMessages.PID_KFF: self._update_kff,
            SerialMessages.PID_ACCEL: self._update_acceleration,
            SerialMessages.PID_BASE_PWM: self._update_base_pwm,
            SerialMessages.PID_MAX_PWM: self._update_max_pwm,
            SerialMessages.STATE: self._update_state,
            SerialMessages.RUNNING_MODE: self._update_running_mode,
            SerialMessages.STOP_MODE: self._update_stop_mode,
            SerialMessages.LAPS: self._update_laps,
            SerialMessages.STOP_TIME: self._update_stop_time,
            SerialMessages.STOP_DISTANCE: self._update_stop_distance,
            SerialMessages.LOG_DATA: self._set_log_data,
            SerialMessages.TURBINE_PWM: self._update_turbine_pwm,
            SerialMessages.SPEED_KP: self._update_speed_kp,
            SerialMessages.SPEED_KI: self._update_speed_ki,
            SerialMessages.SPEED_KD: self._update_speed_kd,
            SerialMessages.SPEED_KFF: self._update_speed_kff,
            SerialMessages.BASE_SPEED: self._update_base_speed,
            SerialMessages.PID_ALPHA: self._update_alpha,
            SerialMessages.PID_CLAMP: self._update_clamp,
            SerialMessages.LOOKAHEAD: self._update_lookahead,
            SerialMessages.WHEEL_BASE_CORRECTION: self._update_curvature_gain,
            SerialMessages.IMU_ALPHA: self._update_imu_alpha,
        }

        self._initialized = True

    @property
    def is_running(self) -> bool:
        """Indicates if the robot is currently running."""
        return self._state == RobotStates.RUNNING

    @property
    def bluetooth(self) -> BluetoothApi:
        """Instance of BluetoothApi for Bluetooth communication."""
        return self._bluetooth

    @property
    def kp(self) -> int:
        """Proportional gain for PID controller."""
        return self._kp if self._kp is not None else 0

    @property
    def ki(self) -> int:
        """Integral gain for PID controller."""
        return self._ki if self._ki is not None else 0

    @property
    def kd(self) -> int:
        """Derivative gain for PID controller."""
        return self._kd if self._kd is not None else 0

    @property
    def kff(self) -> int:
        """Feedforward gain for PID controller."""
        return self._kff if self._kff is not None else 0

    @property
    def kb(self) -> int:
        """Brake gain for PID controller."""
        return self._kb if self._kb is not None else 0

    @property
    def alpha(self) -> float:
        """Alpha value for PID controller."""
        return self._alpha if self._alpha is not None else 0.0

    @property
    def clamp(self) -> int:
        """Clamp value for PID controller."""
        return self._clamp if self._clamp is not None else 0

    @property
    def base_pwm(self) -> int:
        """Base PWM value for motor control."""
        return self._base_pwm if self._base_pwm is not None else 0

    @property
    def max_pwm(self) -> int:
        """Maximum PWM value for motor control."""
        return self._max_pwm if self._max_pwm is not None else 0

    @property
    def state(self) -> RobotStates:
        """Current state of the robot."""
        return self._state if self._state is not None else RobotStates.INIT

    @property
    def running_mode(self) -> RunningModes:
        """Current running mode of the robot."""
        return (
            self._running_mode if self._running_mode is not None else RunningModes.INIT
        )

    @property
    def stop_mode(self) -> StopModes:
        """Current stop mode of the robot."""
        return self._stop_mode if self._stop_mode is not None else StopModes.NONE

    @property
    def laps(self) -> int:
        """Number of laps completed."""
        return self._laps if self._laps is not None else 0

    @property
    def stop_time(self) -> int:
        """Time to stop the robot."""
        return self._stop_time if self._stop_time is not None else 0

    @property
    def stop_distance(self) -> int:
        """Distance to stop the robot."""
        return self._stop_distance if self._stop_distance is not None else 0

    @property
    def log_data(self) -> bool:
        """Indicates if data logging is enabled."""
        return self._log_data if self._log_data is not None else False

    @property
    def turbine_pwm(self) -> int:
        """Turbine PWM value for motor control."""
        return self._turbine_pwm if self._turbine_pwm is not None else 0

    @property
    def speed_kp(self) -> int:
        """Proportional gain for speed PID controller."""
        return self._speed_kp if self._speed_kp is not None else 0

    @property
    def speed_ki(self) -> float:
        """Integral gain for speed PID controller."""
        return self._speed_ki if self._speed_ki is not None else 0.0

    @property
    def speed_kd(self) -> int:
        """Derivative gain for speed PID controller."""
        return self._speed_kd if self._speed_kd is not None else 0

    @property
    def speed_kff(self) -> int:
        """Feedforward gain for speed PID controller."""
        return self._speed_kff if self._speed_kff is not None else 0

    @property
    def base_speed(self) -> float:
        """Base speed for the robot."""
        return self._base_speed if self._base_speed is not None else 0.0

    @property
    def lookahead(self) -> int:
        """Lookahead distance for the robot."""
        return self._lookahead if self._lookahead is not None else 0

    @property
    def curvature_gain(self) -> float:
        """Wheel base correction factor used in the robot."""
        return self._curvature_gain if self._curvature_gain is not None else 0.0

    @property
    def imu_alpha(self) -> float:
        """Alpha value for the IMU fusion."""
        return self._imu_alpha if self._imu_alpha is not None else 0.0

    def send_message(self, message: SerialMessage) -> None:
        """
        Sends a serial message to the robot via Bluetooth.

        Args:
            message (SerialMessage): The message to send.
        """
        self._bluetooth.write_data(message.frame)

    def connect_state_changer(self, slot: Callable[[RobotStates], None]) -> None:
        """
        Connects a slot to the state change signal.

        Args:
            slot (Callable[[RobotStates], None]): The slot to connect.
        """
        self._signal_handler.state_changed.connect(slot)

    def connect_attr_changer(self, slot: Callable[[SerialMessages, int], None]) -> None:
        """
        Connects a slot to the attribute change signal.

        Args:
            slot (Callable[[SerialMessages, int], None]): The slot to connect.
        """
        self._signal_handler.attr_changed.connect(slot)

    def _handle_serial_message(self, message: SerialMessage) -> None:
        """Handles incoming serial messages and updates config params."""
        if message.message == SerialMessages.OPERATION_DATA:
            self._mapper.handle_operation_data(message.payload)
            return

        if message.message not in self._config_map:
            return

        value = int.from_bytes(message.payload, byteorder="little")
        changed = self._config_map[message.message](value)

        if message.message == SerialMessages.STATE:
            self._signal_handler.signal_state_changed(self._state)  # type: ignore

        if not changed:
            return

        self._signal_handler.signal_attr_changed(message.message, value)

    def _update_kp(self, kp: int) -> bool:
        """Updates the proportional gain for PID controller."""
        if self._kp == kp:
            return False

        self._kp = kp
        return True

    def _update_ki(self, ki: int) -> bool:
        """Updates the integral gain for PID controller."""
        if self._ki == ki:
            return False

        self._ki = ki
        return True

    def _update_kd(self, kd: int) -> bool:
        """Updates the derivative gain for PID controller."""
        if self._kd == kd:
            return False

        self._kd = kd
        return True

    def _update_kff(self, kff: int) -> bool:
        """Updates the feedforward gain for PID controller."""
        if self._kff == kff:
            return False

        self._kff = kff
        return True

    def _update_kb(self, kb: int) -> bool:
        """Updates the brake gain for PID controller."""
        if self._kb == kb:
            return False

        self._kb = kb
        return True

    def _update_acceleration(self, acceleration: int) -> bool:
        """Updates the acceleration value for PID controller."""
        if self._acceleration == acceleration:
            return False

        self._acceleration = acceleration
        return True

    def _update_alpha(self, alpha: int) -> bool:
        """Updates the alpha value for PID controller."""
        new_alpha = float(alpha) / 100.0
        if self._alpha == new_alpha:
            return False

        self._alpha = new_alpha
        return True

    def _update_clamp(self, clamp: int) -> bool:
        """Updates the clamp value for PID controller."""
        if self._clamp == clamp:
            return False

        self._clamp = clamp
        return True

    def _update_base_pwm(self, base_pwm: int) -> bool:
        """Updates the base PWM value for motor control."""
        if self._base_pwm == base_pwm:
            return False

        self._base_pwm = base_pwm
        return True

    def _update_max_pwm(self, max_pwm: int) -> bool:
        """Updates the maximum PWM value for motor control."""
        if self._max_pwm == max_pwm:
            return False

        self._max_pwm = max_pwm
        return True

    def _update_state(self, state: int) -> bool:
        """Updates the state of the robot."""
        new_state = RobotStates(state)
        if self._state == new_state:
            return False

        self._state = new_state
        return True

    def _update_running_mode(self, mode: int) -> bool:
        """Updates the running mode of the robot."""
        new_mode = RunningModes(mode)
        if self._running_mode == new_mode:
            return False

        self._running_mode = new_mode
        return True

    def _update_stop_mode(self, mode: int) -> bool:
        """Updates the stop mode of the robot."""
        new_mode = StopModes(mode)
        if self._stop_mode == new_mode:
            return False

        self._stop_mode = new_mode
        return True

    def _update_laps(self, laps: int) -> bool:
        """Updates the number of laps completed."""
        if self._laps == laps:
            return False

        self._laps = laps
        return True

    def _update_stop_time(self, stop_time: int) -> bool:
        """Updates the time to stop the robot."""
        if self._stop_time == stop_time:
            return False

        self._stop_time = stop_time
        return True

    def _update_stop_distance(self, stop_distance: int) -> bool:
        """Updates the distance to stop the robot."""
        if self._stop_distance == stop_distance:
            return False

        self._stop_distance = stop_distance
        return True

    def _set_log_data(self, log_data: int) -> bool:
        """Sets the log data flag."""
        new_bool = log_data == 1
        if self._log_data == new_bool:
            return False

        self._log_data = new_bool
        return True

    def _update_turbine_pwm(self, turbine_pwm: int) -> bool:
        """Updates the turbine PWM value for motor control."""
        if self._turbine_pwm == turbine_pwm:
            return False

        self._turbine_pwm = turbine_pwm
        return True

    def _update_speed_kp(self, kp: int) -> bool:
        """Updates the proportional gain for speed PID controller."""
        if self._speed_kp == kp:
            return False

        self._speed_kp = kp
        return True

    def _update_speed_ki(self, ki: int) -> bool:
        """Updates the integral gain for speed PID controller."""
        new_ki = float(ki) / 10000.0
        if self._speed_ki == new_ki:
            return False

        self._speed_ki = new_ki
        return True

    def _update_speed_kd(self, kd: int) -> bool:
        """Updates the derivative gain for speed PID controller."""
        if self._speed_kd == kd:
            return False

        self._speed_kd = kd
        return True

    def _update_speed_kff(self, kff: int) -> bool:
        """Updates the feedforward gain for speed PID controller."""
        if self._speed_kff == kff:
            return False

        self._speed_kff = kff
        return True

    def _update_base_speed(self, base_speed: int) -> bool:
        """Updates the base speed for the robot."""
        new_speed = float(base_speed) / 100.0
        if self._base_speed == new_speed:
            return False

        self._base_speed = new_speed
        return True

    def _update_lookahead(self, lookahead: int) -> bool:
        """Updates the lookahead distance for the robot."""
        if self._lookahead == lookahead:
            return False

        self._lookahead = lookahead
        return True

    def _update_curvature_gain(self, curvature_gain: int) -> bool:
        """Updates the wheel base correction factor used in the robot."""
        new_gain = float(curvature_gain) / 100.0
        if self._curvature_gain == new_gain:
            return False

        self._curvature_gain = new_gain
        return True

    def _update_imu_alpha(self, imu_alpha: int) -> bool:
        """Updates the alpha value for the IMU fusion."""
        new_alpha = float(imu_alpha) / 100.0
        if self._imu_alpha == new_alpha:
            return False

        self._imu_alpha = new_alpha
        return True
