import os
import sys

from gui import start_gui
from utils import AppConfigs, Paths, setup_logger

if __name__ == "__main__":
    if sys.platform == "win32":
        try:
            import ctypes

            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
                AppConfigs.APP_ID
            )
        except Exception:
            pass

    os.makedirs(Paths.DATA, exist_ok=True)
    setup_logger()
    start_gui()
