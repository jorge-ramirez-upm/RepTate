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
"""Module Reptate

Main program that launches the GUI.

"""
import os
import sys
import glob
import argparse
import numpy as np
import logging

from RepTate.core.CmdBase import CmdBase, CalcMode
#from RepTate.gui.QApplicationManager import QApplicationManager

from PySide6.QtWidgets import QApplication
#from PySide6.QtCore import Qt, QCoreApplication
# from RepTate.gui.SplashScreen import SplashScreen

# from time import time, sleep


def main():
    start_RepTate(sys.argv[1:])


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


def start_RepTate(argv):
    """
    Main RepTate application.

    :param list argv: Command line parameters passed to Reptate
    """

    parser = argparse.ArgumentParser(
        description="RepTate: Rheology of Entangled Polymers: Toolkit for the Analysis of Theory and Experiment.",
        epilog="(c) Jorge Ramirez (jorge.ramirez@upm.es, UPM), Victor Boudara (U. Leeds) (2017-2023)",
    )
    # parser.add_argument(
    #     "-d", "--dpi", help="High DPI support on Windows", action="store_true"
    # )
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
    # for a list of available styles: "from PySide6.QtWidgets import QStyleFactory; print(QStyleFactory.keys())"

    # if args.dpi or sys.platform == "darwin":
    #     os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    #     QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    #     QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    #     QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    app.setApplicationName("RepTate")

    # if args.dpi and sys.platform == "win32":
    #     #os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    #     import matplotlib
    #     #matplotlib.pyplot.matplotlib.rcParams['figure.dpi'] = int (np.round(app.desktop().physicalDpiX()/10))
    #     matplotlib.pyplot.matplotlib.rcParams['figure.dpi'] = 34
    #     #matplotlib.pyplot.matplotlib.rcParams['figure.dpi'] = app.desktop().physicalDpiX()/4

    from RepTate.gui.SplashScreen import SplashScreen
    splash = SplashScreen()
    splash.show()

    from RepTate.gui.QApplicationManager import QApplicationManager
    ex = QApplicationManager(loglevel=loglevel)
    ex.setStyleSheet("QTabBar::tab { color:black; height: 22px; }")
    # splash.showMessage("Loading RepTate...")

    splash.finish(ex)

    # Handle files & open apps accordingly
    CmdBase.calcmode = (
        CalcMode.singlethread
    )  # avoid troubles when loading multiple apps/files/theories
    d = {ex.extension: ex.appname for ex in list(ex.available_applications.values())}
    toolopen = False    
    for k in dictfiles.keys():
        if k == "rept":
            ex.open_project(dictfiles[k][0])
        elif np.any([k == key for key in d.keys()]):
            # exact match
            ex.handle_new_app(d[k])
            appname = "%s%d" % (d[k], ex.application_counter)
            ex.applications[appname].new_tables_from_files(dictfiles[k])
            if args.theory in list(ex.applications[appname].theories.keys()):
                ex.applications[appname].datasets["Set1"].new_theory(args.theory)
            if args.tool in (
                list(ex.applications[appname].availabletools.keys())
                + list(ex.applications[appname].extratools.keys())
            ):
                ex.applications[appname].new_tool(args.tool)
                ex.applications[appname].update_all_ds_plots()
                ex.applications[appname].showDataInspector(True)
                toolopen = True

        elif np.any([k in key for key in d.keys()]):  # works with spaces in extensions
            for key in d.keys():
                if k in key:
                    ex.handle_new_app(d[key])
                    appname = "%s%d" % (d[key], ex.application_counter)
                    ex.applications[appname].new_tables_from_files(dictfiles[k])
                    if args.theory in list(ex.applications[appname].theories.keys()):
                        ex.applications[appname].datasets["Set1"].new_theory(
                            args.theory
                        )
                    if args.tool in (
                        list(ex.applications[appname].availabletools.keys())
                        + list(ex.applications[appname].extratools.keys())
                    ):
                        ex.applications[appname].new_tool(args.tool)
                        ex.applications[appname].update_all_ds_plots()
                        ex.applications[appname].showDataInspector(True)
                        toolopen = True
                    break
        else:
            print("File type %s cannot be opened" % k)
    # set the calmode back
    if args.single:
        CmdBase.calcmode = CalcMode.singlethread
    else:
        CmdBase.calcmode = CalcMode.multithread

    ex.showMaximized()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
