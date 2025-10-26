import sys
from pathlib import Path

# Add the project root to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))


from utils import AppConfigs, Assets, Files, Paths, clean_dir, run_command


def build() -> None:
    clean_dir(Paths.PYINSTALLER_BUILD)
    run_command(
        f"pyinstaller "
        f"--windowed "
        f"--clean "
        f"--noconfirm "
        f"--onefile "
        f'--name "{AppConfigs.APP_NAME}" '
        f'--specpath "{Paths.PYINSTALLER_BUILD}" '
        f'--distpath "{Paths.PYINSTALLER_DIST}" '
        f'--workpath "{Paths.PYINSTALLER_WORK}" '
        f'--add-data "{Paths.ASSETS}":assets '
        f'--icon "{Assets.ALT_ICON_IMAGE}" '
        f'"{Files.MAIN}"'
    )


if __name__ == "__main__":
    build()
