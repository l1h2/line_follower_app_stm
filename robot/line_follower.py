from collections.abc import Callable

from PyQt6.QtCore import QObject, pyqtSignal

from utils import RobotStates, RunningModes, SerialMessage, SerialMessages, StopModes

from .api import BluetoothApi


class StateChanger(QObject):
    """
    ### StateChanger Class

    Handles state changes and emit signals. Inherits from QObject to use signals and slots.

    #### Signals:
    - `state_change`: Signal emitted when the state changes.
    """

    state_change = pyqtSignal()

    def __init__(self):
        super().__init__()

    def signal_state_change(self) -> None:
        self.state_change.emit()


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
        if not hasattr(self, "_initialized"):
            self._state_changer = StateChanger()

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
            self._initialized = True

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
                SerialMessages.TURBINE_PWM: self._update_turbine_pwm,
            }

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

    def connect_state_changer(self, slot: Callable[[], None]) -> None:
        """
        Connects a slot to the state change signal.

        Args:
            slot (Callable[[], None]): The slot to connect.
        """
        self._state_changer.state_change.connect(slot)

    def _handle_serial_message(self, message: SerialMessage) -> None:
        """Handles incoming serial messages and updates config params."""
        if message.message not in self._config_map:
            return

        value = int.from_bytes(message.payload, byteorder="little")
        self._config_map[message.message](value)

    def _update_kp(self, kp: int) -> None:
        """Updates the proportional gain for PID controller."""
        self._kp = kp

    def _update_ki(self, ki: int) -> None:
        """Updates the integral gain for PID controller."""
        self._ki = ki

    def _update_kd(self, kd: int) -> None:
        """Updates the derivative gain for PID controller."""
        self._kd = kd

    def _update_kff(self, kff: int) -> None:
        """Updates the feedforward gain for PID controller."""
        self._kff = kff

    def _update_kb(self, kb: int) -> None:
        """Updates the brake gain for PID controller."""
        self._kb = kb

    def _update_base_pwm(self, base_pwm: int) -> None:
        """Updates the base PWM value for motor control."""
        self._base_pwm = base_pwm

    def _update_max_pwm(self, max_pwm: int) -> None:
        """Updates the maximum PWM value for motor control."""
        self._max_pwm = max_pwm

    def _update_state(self, state: int) -> None:
        """Updates the state of the robot."""
        self._state = RobotStates(state)
        self._state_changer.signal_state_change()

    def _update_running_mode(self, mode: int) -> None:
        """Updates the running mode of the robot."""
        self._running_mode = RunningModes(mode)

    def _update_stop_mode(self, mode: int) -> None:
        """Updates the stop mode of the robot."""
        self._stop_mode = StopModes(mode)

    def _update_laps(self, laps: int) -> None:
        """Updates the number of laps completed."""
        self._laps = laps

    def _update_stop_time(self, stop_time: int) -> None:
        """Updates the time to stop the robot."""
        self._stop_time = stop_time

    def _set_log_data(self, log_data: int) -> None:
        """Sets the log data flag."""
        self._log_data = log_data == 1

    def _update_turbine_pwm(self, turbine_pwm: int) -> None:
        """Updates the turbine PWM value for motor control."""
        self._turbine_pwm = turbine_pwm
