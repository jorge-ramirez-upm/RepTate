import sys
import os
import numpy as np
from ._version import get_versions

__version__ = get_versions()["version"]
del get_versions

# RepTate root directory where the "data/" and "docs/" folders are located
if getattr(sys, "frozen", False):
    # If the application is run as a bundle, the PyInstaller bootloader
    # extends the sys module by a flag frozen=True and sets the app
    # path into variable _MEIPASS'.
    root_dir = sys._MEIPASS
else:
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# setup NumPy log level
np.seterr(all="call")