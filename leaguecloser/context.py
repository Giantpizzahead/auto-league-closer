import logging
from pathlib import Path
import sys


def get_module_path() -> Path:
    """Get absolute path to the base of the module, works for dev and for PyInstaller."""
    # https://stackoverflow.com/a/13790741
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = Path(sys._MEIPASS).parent.resolve()
    except Exception:
        base_path = Path(__file__).parent.resolve()
    return base_path


MODULE_PATH = Path(__file__).parent.resolve()

TEMP_DIR = MODULE_PATH / ".." / "temp"
TEMP_DIR.mkdir(parents=True, exist_ok=True)


def create_logger(name: str = __name__, level: int = logging.INFO):
    """Creates a logger for the module."""
    log = logging.getLogger(name)
    log.setLevel(level)

    formatter = logging.Formatter(
        "%(asctime)s %(levelname)7s | %(funcName)-24s | %(message)s"
    )
    file_handler = logging.FileHandler(str(TEMP_DIR / "log.log"))
    file_handler.setFormatter(formatter)
    log.addHandler(file_handler)

    stream_handler = logging.StreamHandler()
    formatter = logging.Formatter("%(levelname)-7s %(message)s")
    stream_handler.setFormatter(formatter)
    log.addHandler(stream_handler)

    log.debug("Logger created!")
    return log


LOG = create_logger(name=__name__, level=logging.INFO)

LOG.info(f"Module path: {str(MODULE_PATH)}")
LOG.info(f"Temp path: {str(TEMP_DIR)}")
