import sys

from pathlib import Path


def get_root_dir() -> str:
    """Return the runtime root that contains top-level data and docs folders.

    In a Nuitka macOS application bundle, top-level data files are kept in
    ``Contents/Resources``.  Package-local files (for example the native
    theory libraries) continue to be resolved relative to their package
    ``__file__`` paths and are intentionally not redirected here.
    """
    module_path = Path(__file__).resolve()
    for parent in (module_path.parent, *module_path.parents):
        if (
            parent.name == "MacOS"
            and parent.parent.name == "Contents"
            and parent.parent.parent.suffix == ".app"
        ):
            return str(parent.parent / "Resources")
    return str(module_path.parents[1])


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
