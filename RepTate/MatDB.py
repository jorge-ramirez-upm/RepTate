# RepTate: Rheology of Entangled Polymers: Toolkit for the Analysis of Theory and Experiments
# --------------------------------------------------------------------------------------------------------
#
# Authors:
#     Jorge Ramirez, jorge.ramirez@upm.es
#     Victor Boudara, victor.boudara@gmail.com
#
# Useful links:
#     http://blogs.upm.es/compsoftmatter/software/reptate/
#     https://github.com/jorge-ramirez-upm/RepTate
#     http://reptate.readthedocs.io
#
# --------------------------------------------------------------------------------------------------------
#
# Copyright (2017-2020): Jorge Ramirez, Victor Boudara, Universidad Politécnica de Madrid, University of Leeds
#
# This file is part of RepTate.
#
# RepTate is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# RepTate is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with RepTate.  If not, see <http://www.gnu.org/licenses/>.
#
# --------------------------------------------------------------------------------------------------------
"""Module MatDB

Main program that launches the Materials Database

"""
import os
import sys
import argparse
import traceback
import logging

from RepTate.core.CmdBase import CmdBase, CalcMode, CmdMode
from RepTate.gui.QApplicationManager import QApplicationManager
from RepTate.tools.ToolMaterialsDatabase import ToolMaterialsDatabase
from RepTate.applications.ApplicationCreep import ApplicationCreep
from PyQt5.QtWidgets import QApplication, QMessageBox, QShortcut
from PyQt5.QtGui import QDesktopServices, QIcon, QKeySequence
from PyQt5.QtCore import QUrl, Qt, QCoreApplication


def main():
    start_MatDB(sys.argv[1:])


def start_MatDB(argv):
    """
    Materials Database application. 
    
    :param list argv: Command line parameters passed to MatDB
    """
    parser = argparse.ArgumentParser(
        description="RepTate: Rheologhy of Entangled Polymers: Toolkit for the Analysis of Theory and Experiment.",
        epilog="(c) Jorge Ramirez - jorge.ramirez@upm.es - UPM , Victor Boudara - U. Leeds (2018)",
    )
    parser.add_argument(
        "-d", "--dpi", help="High DPI support on Windows", action="store_true"
    )
    parser.add_argument(
        "-v", "--verbose", help="Write debug information to stdout", action="store_true"
    )
    parser.add_argument(
        "-V", "--version", help="Print RepTate version and exit", action="store_true"
    )
    parser.add_argument("finlist", nargs="*")

    args = parser.parse_args(args=argv)
    if args.version:
        print(QApplicationManager.intro)
        sys.exit()

    if args.verbose:
        loglevel = logging.DEBUG
    else:
        loglevel = logging.INFO

    QApplication.setStyle("Fusion")  # comment that line for a native look
    # for a list of available styles: "from PyQt5.QtWidgets import QStyleFactory; print(QStyleFactory.keys())"

    if args.dpi:
        os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
        QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)

    CmdBase.mode = CmdMode.GUI
    tmpex = QApplicationManager(loglevel=loglevel)
    tmpapp = ApplicationCreep("tmpapp", tmpex)
    ex = ToolMaterialsDatabase("MatDB", tmpapp)
    ex.setWindowIcon(QIcon("RepTate/gui/Images/DataTable3D.ico"))
    ex.setWindowTitle("RepTate Material" "s Database")
    ex.resize(300, 900)
    ex.move(100, 20)

    shortcut = QShortcut(QKeySequence("Ctrl+Q"), ex)
    shortcut.activated.connect(app.quit)

    CmdBase.calcmode = CalcMode.singlethread

    def my_excepthook(type, value, tb):
        """Catch exceptions and print error message. Open email client to report bug to devlopers"""
        tb_msg = ""
        for e in traceback.format_tb(tb):
            tb_msg += str(e)
        tb_msg += "%s: %s\n" % (type.__name__, str(value))
        # print(tb_msg) # JR: Not needed anymore
        l = logging.getLogger("RepTate")
        if CmdBase.mode == CmdMode.GUI:
            l.error(tb_msg.replace("\n", "<br>"))
        else:
            l.error(tb_msg)
        msg = (
            'Sorry, something went wrong:\n "%s: %s".\nTry to save your work and quit RepTate.\nDo you want to help RepTate developers by reporting this bug?'
            % (type.__name__, str(value))
        )
        ans = QMessageBox.critical(
            ex, "Critical Error", msg, QMessageBox.Yes | QMessageBox.No
        )
        if ans == QMessageBox.Yes:
            address = "reptate.rheology@gmail.com"
            subject = "Something went wrong"
            body = (
                "%s\nIf you can, please describe below what you were doing with RepTate when the error happened (apps and theories or tools open if any) and send the message\nPlease, do NOT include confidential information\n%s\nError Traceback:\n %s"
                % ("-" * 60, "-" * 60 + "\n" * 10 + "-" * 60, tb_msg)
            )
            QDesktopServices.openUrl(
                QUrl(
                    "mailto:?to=%s&subject=%s&body=%s" % (address, subject, body),
                    QUrl.TolerantMode,
                )
            )

    sys.excepthook = my_excepthook

    ex.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
