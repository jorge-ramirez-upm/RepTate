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
# Copyright (2017-2023): Jorge Ramirez, Victor Boudara, Universidad Politécnica de Madrid, University of Leeds
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
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtGui import QDesktopServices, QIcon, QKeySequence, QShortcut
from PySide6.QtCore import QUrl, Qt, QCoreApplication


def main():
    start_MatDB(sys.argv[1:])


def start_MatDB(argv):
    """
    Materials Database application. 
    
    :param list argv: Command line parameters passed to MatDB
    """
    parser = argparse.ArgumentParser(
        description="RepTate: Rheology of Entangled Polymers: Toolkit for the Analysis of Theory and Experiment.",
        epilog="(c) Jorge Ramirez (jorge.ramirez@upm.es, UPM), Victor Boudara (U. Leeds) (2017-2023)",
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
    # for a list of available styles: "from PySide6.QtWidgets import QStyleFactory; print(QStyleFactory.keys())"

    if args.dpi:
        os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
        QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    app.setApplicationName("RepTate")

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

    ex.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
