import sys
import os
import traceback
import logging
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

def my_excepthook(type, value, tb):
    """Catch exceptions and print error message. Open email client to report bug to developers"""
    tb_msg = ""
    for e in traceback.format_tb(tb):
        tb_msg += str(e)
    tb_msg += "%s: %s\n" % (type.__name__, str(value))
    msg = (
        'Sorry, something went wrong:\n "%s: %s".'
        % (type.__name__, str(value))
    )
    l = logging.getLogger("RepTate")
    from PySide6.QtWidgets import QMessageBox
    from PySide6.QtGui import QDesktopServices
    from PySide6.QtCore import QUrl
    # l = logging.getLogger("RepTate")
    l.error(tb_msg)
    msg += "\nTry to save your work and quit RepTate.\nDo you want to help RepTate developers by reporting this bug?"
    ans = QMessageBox.critical(
        None, "Critical Error", msg, QMessageBox.Yes | QMessageBox.No
    )
    if ans == QMessageBox.Yes:
        address = "reptate.rheology@gmail.com"
        subject = "[RepTate] Something went wrong"
        body = (
            "Please describe the actions leading to the Error (apps, theories or tools opened).\nDo NOT include confidential information.\n%s\nRepTate v%s\nError Traceback:\n %s"
            % ("*" * 91 + "\n" * 10 + "*" * 91, __version__, tb_msg)
        )
        QDesktopServices.openUrl(
            QUrl(
                "mailto:?to=%s&subject=%s&body=%s" % (address, subject, body),
                QUrl.TolerantMode,
            )
        )

sys.excepthook = my_excepthook