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
"""Module UV

Main program that launches the Universal Viewer of RepTate

"""
import os
import sys
import glob
import argparse
import traceback
import logging
import configparser

from PyQt5.QtWidgets import QApplication, QMessageBox, QShortcut
from PyQt5.QtGui import QDesktopServices, QIcon, QKeySequence
from PyQt5.QtCore import QUrl, Qt, QCoreApplication
from RepTate.core.DataTable import DataTable

DataTable.MAX_NUM_SERIES = 10
from RepTate.core.CmdBase import CmdBase, CalcMode, CmdMode
from RepTate.gui.QApplicationManager import QApplicationManager
from RepTate.applications.ApplicationUniversalViewer import ApplicationUniversalViewer


def main():
    start_UV(sys.argv[1:])


def get_argument_files(finlist):
    """
    Parse files from command line and group them by extension

    :param list finlist: List of files from argparse
    """
    df = {}
    if not finlist:
        return df
    full_paths = [os.path.join(os.getcwd(), path) for path in finlist]
    for path in full_paths:
        if os.path.isfile(path):
            items = path.split(".")
            extension = items[len(items) - 1]
            if extension in df.keys():
                df[extension].append(path)
            else:
                df[extension] = [path]
        else:
            lll = glob.glob(path)
            for f in lll:
                items = f.split(".")
                extension = items[len(items) - 1]
                if extension in df.keys():
                    df[extension].append(f)
                else:
                    df[extension] = [f]
    return df


def start_UV(argv):
    """
    Start Universal Viewer app. 
    
    :param list argv: Command line parameters passed to UV
    """
    GUI = True

    parser = argparse.ArgumentParser(
        description="RepTate: Rheology of Entangled Polymers: Toolkit for the Analysis of Theory and Experiment.",
        epilog="(c) Jorge Ramirez (jorge.ramirez@upm.es, UPM), Victor Boudara (U. Leeds) (2017-2020)",
    )
    parser.add_argument(
        "-d", "--dpi", help="High DPI support on Windows", action="store_true"
    )
    parser.add_argument(
        "-l", "--tool", help="Open the tool L (if available)", default="", metavar="L"
    )
    parser.add_argument(
        "-s",
        "--single",
        help="Run Reptate as a single thread application",
        action="store_true",
    )
    parser.add_argument(
        "-t",
        "--theory",
        help="Open the theory T (if available)",
        default="",
        metavar="T",
    )
    parser.add_argument(
        "-v", "--verbose", help="Write debug information to stdout", action="store_true"
    )
    parser.add_argument(
        "-V", "--version", help="Print RepTate version and exit", action="store_true"
    )
    parser.add_argument("finlist", nargs="*")

    args = parser.parse_args(args=argv)

    # Get files from command line
    dictfiles = get_argument_files(args.finlist)

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

    # 1. Find if all argument files have the same extension
    if len(dictfiles) > 1 or len(dictfiles) == 0:
        tmpex.logger.error("Universal Viewer must be invoked with at least one file!")
        sys.exit()
    # 2. Find if in the folder of the first file there is an ini file that describes that extension
    inifile = None
    inifilepath = None
    nplots_max = 1
    pathtofirstfile = os.path.dirname(list(dictfiles.values())[0][0])
    for file in os.listdir(pathtofirstfile):
        if file.endswith(".ini"):
            config = configparser.ConfigParser()
            config.read_file(open(pathtofirstfile + os.sep + file))
            ext = config.get("file1", "extension").split(".")[1]
            if ext in dictfiles.keys():
                inifile = file
                inifilepath = pathtofirstfile
                nplot_max = config.getint("application", "ncharts")
                break
    # 3. If not, show an error message and exit
    if inifile == None:
        tmpex.logger.error(
            "INI file describing the data not found in the first file folder"
        )
        sys.exit()

    ex = ApplicationUniversalViewer(
        "UniversalViewer",
        tmpex,
        inifile=inifilepath + os.sep + inifile,
        nplot_max=nplot_max,
    )
    ex.setWindowIcon(QIcon("RepTate/gui/Images/UView_Icon.ico"))
    ex.setWindowTitle(
        "RepTate %s %s - Universal Viewer - INI: %s"
        % (tmpex.version, tmpex.date, inifile)
    )
    shortcut = QShortcut(QKeySequence("Ctrl+Q"), ex)
    shortcut.activated.connect(app.quit)

    # Handle files & open apps accordingly
    CmdBase.calcmode = (
        CalcMode.singlethread
    )  # avoid troubles when loading multiple apps/files/theories
    for k in dictfiles.keys():
        ex.new_tables_from_files(dictfiles[k])
    if args.theory in list(ex.theories.keys()):
        ex.datasets["Set1"].new_theory(args.theory)
    if args.tool in (list(ex.availabletools.keys()) + list(ex.extratools.keys())):
        ex.new_tool(args.tool)
        ex.update_all_ds_plots()
        ex.showDataInspector(True)
    # set the calmode back
    if args.single:
        CmdBase.calcmode = CalcMode.singlethread
    else:
        CmdBase.calcmode = CalcMode.multithread

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

    ex.showMaximized()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
