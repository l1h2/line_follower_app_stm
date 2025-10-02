class Styles:
    """This class contains styles for the GUI elements in the application."""

    START_BUTTONS = """
        color: black;
        background-color: green;
        font-weight: bold;
        font-size: 16px;
    """

    STOP_BUTTONS = """
        color: black;
        background-color: red;
        font-weight: bold;
        font-size: 16px;
    """

    DISABLED_BUTTONS = """
        font-weight: bold;
        font-size: 16px;
    """

    CHECK_BUTTONS = """
        QPushButton {
            background-color: rgba(255, 255, 255, 0.8);
            border: 1px solid gray;
            border-radius: 5px;
        }
        QPushButton:checked {
            background-color: rgba(0, 128, 0, 0.8);
            color: white;
            font-weight: bold;
            border: 1px solid darkgreen;
        }
    """
