from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget

from robot import LineFollower

from .connector.connector import ControllerWidget
from .listener.listener import ListenerWidget
from .sender.sender import SenderWidget


class HomeWidget(QWidget):
    """
    ### HomeWidget Class

    The home widget of the application. It serves as the main interface for the user to interact with the
    application.

    #### Attributes:
    - `sender_widget (SenderWidget)`: The sender widget for sending commands to the robot.
    - `listener_widget (ListenerWidget)`: The listener widget for receiving data from the robot.
    - `connector_widget (ControllerWidget)`: The connector widget for managing the Bluetooth connection.
    """

    def __init__(self):
        super().__init__()
        self._line_follower = LineFollower()

        self._init_ui()

    def _init_ui(self) -> None:
        """Initialize the UI components of the home widget."""
        self._add_widgets()
        self._set_layout()

    def _add_widgets(self) -> None:
        """Add widgets to the home widget."""
        self.sender_widget = SenderWidget()
        self.listener_widget = ListenerWidget()
        self.connector_widget = ControllerWidget()

    def _set_layout(self) -> None:
        """Set the layout for the home widget."""
        main_layout = QVBoxLayout(self)

        display_layout = QHBoxLayout()
        display_layout.addWidget(self.sender_widget)
        display_layout.addWidget(self.listener_widget)

        main_layout.addLayout(display_layout)
        main_layout.addWidget(self.connector_widget)
