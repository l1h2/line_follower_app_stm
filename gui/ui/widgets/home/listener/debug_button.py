from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QHBoxLayout, QPushButton, QWidget

from utils import Styles, app_configs


class DebugButton(QWidget):
    """
    ### DebugButton Widget

    A widget that contains a button to enable or disable debug prints.

    #### Parameters:
    - `parent (QWidget | None)`: The parent widget of the DebugButton.

    #### Signals:
    - `debug_state_changed (bool)`: Emitted when the debug button is clicked, indicating the new debug state.
    """

    debug_state_changed = pyqtSignal(bool)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent=parent)

        self.setFixedHeight(50)
        self.setContentsMargins(0, 0, 20, 0)
        self._init_ui()

    def _init_ui(self) -> None:
        """Initialize the UI components of the DebugButton widget."""
        self._add_widgets()
        self._set_layout()

    def _add_widgets(self) -> None:
        """Add widgets to the DebugButton widget."""
        self._add_debug_button()

    def _add_debug_button(self) -> None:
        """Add a debug button to the widget."""
        self._debug_button = QPushButton("Debug")
        self._debug_button.setCheckable(True)
        self._debug_button.setChecked(False)
        self._debug_button.setToolTip("Enable debug prints")
        self._debug_button.setStyleSheet(Styles.CHECK_BUTTONS)
        self._debug_button.setFixedSize(70, 30)
        self._debug_button.clicked.connect(self._set_debug_state)

    def _set_debug_state(self) -> None:
        """Set the debug state in app_configs."""
        app_configs.DEBUG_ENABLED = self._debug_button.isChecked()

    def _set_layout(self) -> None:
        """Set the layout for the DebugButton widget."""
        main_layout = QHBoxLayout(self)
        main_layout.addWidget(self._debug_button)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
