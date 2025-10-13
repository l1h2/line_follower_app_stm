from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget

from robot import LineFollower

from .widgets import HomeWidget


class MainWindow(QMainWindow):
    """
    ### MainWindow Class

    The main window of the application. It serves as the main interface for the user to interact with the
    application.

    #### Attributes:
    - `main_widget (QWidget)`: The main widget of the window.
    - `home_widget (HomeWidget)`: The home widget of the application.
    """

    def __init__(self):
        super().__init__()
        self._line_follower = LineFollower()
        self._init_ui()

    def _init_ui(self) -> None:
        """Initialize the UI components of the main window."""
        self._set_window()
        self._set_main_widget()
        self._add_widgets()
        self._set_layout()

    def _set_window(self) -> None:
        """Set the main window properties."""
        self.setWindowTitle("Line Follower App")
        self.resize(1600, 960)

    def _set_main_widget(self) -> None:
        """Set the main widget for the main window."""
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)

    def _add_widgets(self) -> None:
        """Add widgets to the main window."""
        self.home_widget = HomeWidget()

    def _set_layout(self) -> None:
        """Set the layout for the main window."""
        main_layout = QVBoxLayout(self.main_widget)
        main_layout.addWidget(self.home_widget)
