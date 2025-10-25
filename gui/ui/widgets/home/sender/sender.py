from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QPushButton, QVBoxLayout, QWidget

from utils import Styles

from .general_sender import GeneralSender
from .pwm_sender import PwmSender
from .speed_sender import SpeedSender


class SenderWidget(QWidget):
    """
    ### SenderWidget Class

    A widget that allows the user to send commands to the robot via Bluetooth.

    #### Attributes:
    - `pwm_sender (PwmSender)`: Widget for sending PWM-related parameters.
    - `speed_sender (SpeedSender)`: Widget for sending Speed-related parameters.
    - `general_sender (GeneralSender)`: Widget for sending general parameters.
    - `send_all_button (QPushButton)`: Button to send all values to the robot.
    """

    def __init__(self):
        super().__init__()

        self._init_ui()

    def _init_ui(self) -> None:
        """Initialize the UI components of the sender widget."""
        self._add_widgets()
        self._set_layout()

    def _add_widgets(self) -> None:
        """Add widgets to the sender widget."""
        self.pwm_sender = PwmSender()
        self.speed_sender = SpeedSender()
        self.general_sender = GeneralSender()
        self._add_send_all_button()

    def _add_send_all_button(self) -> None:
        """Add a button to send all values to the robot."""
        self.send_all_button = QPushButton("Send All")
        self.send_all_button.setFixedHeight(60)
        self.send_all_button.setFixedWidth(600)
        self.send_all_button.setToolTip("Send all values to the robot")
        self.send_all_button.setStyleSheet(Styles.SEND_ALL_BUTTON)
        self.send_all_button.clicked.connect(self._on_send_all)

    def _on_send_all(self) -> None:
        """Send all values to the robot."""
        self.pwm_sender.send_all()
        self.speed_sender.send_all()
        self.general_sender.send_all()

    def _set_layout(self) -> None:
        """Set the layout for the sender widget."""
        pid_layout = QHBoxLayout()
        pid_layout.addWidget(self.pwm_sender)
        pid_layout.addWidget(self.speed_sender)

        main_layout = QVBoxLayout(self)
        main_layout.addLayout(pid_layout)
        main_layout.addWidget(self.general_sender)
        main_layout.addWidget(
            self.send_all_button, alignment=Qt.AlignmentFlag.AlignHCenter
        )
