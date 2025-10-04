from collections.abc import Callable

from PyQt6.QtCore import QObject, pyqtSignal

from utils import RobotStates, RunningModes, SerialMessage, SerialMessages, StopModes

from .api import BluetoothApi


class SignalHandler(QObject):
    """
    ### SignalHandler Class

    Handles signals for the LineFollower class. Inherits from QObject to use signals and slots.

    #### Signals:
    - `state_change (RobotStates)`: Signal emitted when the state changes.

    #### Methods:
    - `signal_state_change(state: RobotStates) -> None`: Emits the state change signal.
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
    - `kp (int | None)`: Proportional gain for PID controller.
    - `ki (int | None)`: Integral gain for PID controller.
    - `kd (int | None)`: Derivative gain for PID controller.
    - `kff (int | None)`: Feedforward gain for PID controller.
    - `kb (int | None)`: Brake gain for PID controller.
    - `base_pwm (int | None)`: Base PWM value for motor control.
    - `max_pwm (int | None)`: Maximum PWM value for motor control.
    - `state (RobotStates | None)`: Current state of the robot.
    - `running_mode (RunningModes | None)`: Current running mode of the robot.
    - `stop_mode (StopModes | None)`: Current stop mode of the robot.
    - `laps (int)`: Number of laps completed.
    - `stop_time (int)`: Time to stop the robot.
    - `log_data (bool)`: Indicates if data logging is enabled.

    #### Methods:
    - `update_config(message: SerialMessages, value: int) -> None`: Updates the configuration of the robot based on the message received.
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
        self._base_pwm = None
        self._max_pwm = None
        self._state = None
        self._running_mode = None
        self._stop_mode = None
        self._laps = 0
        self._stop_time = 0
        self._log_data = False
        self._turbine_pwm = 0

        self._bluetooth = BluetoothApi()

        self._bluetooth.serial_output.connect(self._handle_serial_message)

        self._config_map = {
            SerialMessages.PID_KP: self._update_kp,
            SerialMessages.PID_KI: self._update_ki,
            SerialMessages.PID_KD: self._update_kd,
            SerialMessages.PID_KFF: self._update_kff,
            SerialMessages.PID_KB: self._update_kb,
            SerialMessages.PID_BASE_PWM: self._update_base_pwm,
            SerialMessages.PID_MAX_PWM: self._update_max_pwm,
            SerialMessages.STATE: self._update_state,
            SerialMessages.RUNNING_MODE: self._update_running_mode,
            SerialMessages.STOP_MODE: self._update_stop_mode,
            SerialMessages.LAPS: self._update_laps,
            SerialMessages.STOP_TIME: self._update_stop_time,
            SerialMessages.LOG_DATA: self._set_log_data,
            SerialMessages.TURBINE_PWM: self._update_turbine_pwm,
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
    def kp(self) -> int | None:
        """Proportional gain for PID controller."""
        return self._kp

    @property
    def ki(self) -> int | None:
        """Integral gain for PID controller."""
        return self._ki

    @property
    def kd(self) -> int | None:
        """Derivative gain for PID controller."""
        return self._kd

    @property
    def kff(self) -> int | None:
        """Feedforward gain for PID controller."""
        return self._kff

    @property
    def kb(self) -> int | None:
        """Brake gain for PID controller."""
        return self._kb

    @property
    def base_pwm(self) -> int | None:
        """Base PWM value for motor control."""
        return self._base_pwm

    @property
    def max_pwm(self) -> int | None:
        """Maximum PWM value for motor control."""
        return self._max_pwm

    @property
    def state(self) -> RobotStates | None:
        """Current state of the robot."""
        return self._state

    @property
    def running_mode(self) -> RunningModes | None:
        """Current running mode of the robot."""
        return self._running_mode

    @property
    def stop_mode(self) -> StopModes | None:
        """Current stop mode of the robot."""
        return self._stop_mode

    @property
    def laps(self) -> int:
        """Number of laps completed."""
        return self._laps

    @property
    def stop_time(self) -> int:
        """Time to stop the robot."""
        return self._stop_time

    @property
    def log_data(self) -> bool:
        """Indicates if data logging is enabled."""
        return self._log_data

    @property
    def turbine_pwm(self) -> int | None:
        """Turbine PWM value for motor control."""
        return self._turbine_pwm

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
        if message.message not in self._config_map:
            return

        value = int.from_bytes(message.payload, byteorder="little")
        changed = self._config_map[message.message](value)

        if not changed:
            return

        if message.message == SerialMessages.STATE:
            self._signal_handler.signal_state_changed(self._state)  # type: ignore

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
