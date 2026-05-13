import logging
import traceback
from types import TracebackType

from RepTate import __version__


def my_excepthook(
    type: type[BaseException], value: BaseException, tb: TracebackType | None
) -> None:
    """Show unexpected GUI errors and guide users to the issue tracker."""
    tb_msg: str = ""
    for e in traceback.format_tb(tb):
        tb_msg += str(e)
    tb_msg += "%s: %s\n" % (type.__name__, str(value))
    msg = 'Sorry, something went wrong:\n "%s: %s".' % (type.__name__, str(value))
    l = logging.getLogger("RepTate")
    from PySide6.QtWidgets import QMessageBox
    from PySide6.QtGui import QDesktopServices

    l.error(tb_msg)
    msg += "\nTry to save your work and quit RepTate.\nDo you want to help RepTate developers by reporting this bug?"
    ans = QMessageBox.critical(
        None, "Critical Error", msg, QMessageBox.Yes | QMessageBox.No
    )
    if ans == QMessageBox.Yes:
        body = (
            "The RepTate project issue page on Github is going to be opened on a browser.\nPlease, create a new Issue and describe with as much detail as possible\nthe actions that led to the Error (which apps, theories or tools opened, what data).\n\nYou can copy and paste the text of this dialog to help you draft the Issue.\nDo NOT include confidential information.\n%s\nRepTate v%s\nError Traceback:\n %s"
            % ("*" * 91 + "\n" * 10 + "*" * 91, __version__, tb_msg)
        )
        QMessageBox.information(None, "Report Bug on Github", body)
        QDesktopServices.openUrl("https://github.com/jorge-ramirez-upm/RepTate/issues")
