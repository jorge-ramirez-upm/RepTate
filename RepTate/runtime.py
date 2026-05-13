import os
import sys
from typing import Any, cast


def get_root_dir() -> str:
    """Return the runtime root that contains top-level data and docs folders."""
    if getattr(sys, "frozen", False):
        return cast(str, cast(Any, sys)._MEIPASS)
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


root_dir: str = get_root_dir()


def configure_numpy_errors() -> None:
    import numpy as np

    np.seterr(all="call")


def install_exception_hook() -> None:
    from RepTate.gui.error_handling import my_excepthook

    sys.excepthook = my_excepthook


def bootstrap_gui_runtime() -> None:
    configure_numpy_errors()
    install_exception_hook()
