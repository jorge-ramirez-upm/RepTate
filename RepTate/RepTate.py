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
# Copyright (2017): Jorge Ramirez, Victor Boudara, Universidad Politécnica de Madrid, University of Leeds
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
from logging import *
basicConfig(level=INFO)
 
# os.chdir(os.path.dirname(sys.argv[0])) # set cwd as *this* dir
sys.path.append('core')
sys.path.append('gui')
sys.path.append('console')
sys.path.append('applications')
sys.path.append('theories')
sys.path.append('visual')
from CmdBase import CmdBase, CalcMode
from QApplicationManager import QApplicationManager
#from ApplicationManager import * #solved the issue with the matplot window not opening on Mac
from PyQt5.QtWidgets import QApplication
from SplashScreen import SplashScreen
# from time import time, sleep

def get_argument_files(finlist):
    """
    Parse files from command line and group them by extension

    :param list finlist: List of files from argparse
    """
    df = {}
    if (not finlist):
        return df
    full_paths = [os.path.join(os.getcwd(), path) for path in finlist]
    for path in full_paths:
        if os.path.isfile(path):
            items=path.split('.')
            extension = items[len(items)-1]
            if (extension in df.keys()):
                df[extension].append(path)
            else:
                df[extension] = [path]
        else:
            lll=glob.glob(path)
            for f in lll:
                items=f.split('.')
                extension = items[len(items)-1]
                if (extension in df.keys()):
                    df[extension].append(f)
                else:
                    df[extension] = [f]
    return df

def start_RepTate(argv):
    """
    Main RepTate application. 
    
    :param list argv: Command line parameters passed to Reptate
    """
    GUI = True

    parser = argparse.ArgumentParser(
        description='RepTate: Rheologhy of Entangled Polymers: Toolkit for the Analysis of Theory and Experiment.',
        epilog='(c) Jorge Ramirez - jorge.ramirez@upm.es - UPM , Victor Boudara - U. Leeds (2018)')
    parser.add_argument('-v', '--verbose', help='Write debug information to stdout', action='store_true')
    parser.add_argument('-V', '--version', help='Print RepTate version and exit', action='store_true')
    parser.add_argument('finlist', nargs='*')

    args = parser.parse_args() 

    # Get files from command line
    dictfiles=get_argument_files(args.finlist)

    if args.version:
        print(QApplicationManager.intro)
        sys.exit()

    QApplication.setStyle("Fusion") #comment that line for a native look
                                    #for a list of available styles: "from PyQt5.QtWidgets import QStyleFactory; print(QStyleFactory.keys())"
    app = QApplication(sys.argv)
    splash = SplashScreen()
    splash.showMessage("Loading RepTate...\n")
    splash.show()
    
    # FOR DEBUGGING PURPOSES: Set Single or MultiThread (default)
    # CmdBase.calcmode = CalcMode.singlethread

    ex = QApplicationManager()
    ex.setStyleSheet("QTabBar::tab { color:black; height: 22px; }")
    splash.showMessage("Loading RepTate...\nVersion " + ex.version + ' ' + ex.date)

    splash.finish(ex)

    # Handle files & open apps accordingly
    d = {ex.extension: ex.name for ex in  list(ex.available_applications.values())}
    for k in dictfiles.keys():
        if (k in d.keys()):
            ex.new_app_from_name(d[k])
            appname="%s%d"%(d[k],ex.application_counter)
            ex.applications[appname].new_tables_from_files(dictfiles[k])
        else:
            print("File type %s cannot be opened"%k)

    ex.showMaximized()

    sys.exit(app.exec_())

if __name__ == '__main__':
    start_RepTate(sys.argv[1:])
