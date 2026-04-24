import os
import sys


def get_root_dir():
    """Return the runtime root that contains top-level data and docs folders."""
    if getattr(sys, "frozen", False):
        return sys._MEIPASS
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


root_dir = get_root_dir()


def configure_numpy_errors():
    import numpy as np

    np.seterr(all="call")


def install_exception_hook():
    from RepTate.gui.error_handling import my_excepthook

    sys.excepthook = my_excepthook


def bootstrap_gui_runtime():
    configure_numpy_errors()
    install_exception_hook()
