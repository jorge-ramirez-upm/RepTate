import sys

from pathlib import Path


def get_root_dir() -> str:
    """Return the runtime root that contains top-level data and docs folders."""
    return str(Path(__file__).resolve().parents[1])


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
