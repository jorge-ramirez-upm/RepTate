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
"""Module ReptateCL

Main program that launches the CL version of RepTate.

""" 
import os
import sys
import glob
import argparse
from logging import *
basicConfig(level=INFO)

sys.path.append('core')
sys.path.append('gui')
sys.path.append('console')
sys.path.append('applications')
sys.path.append('theories')
from ApplicationManager import ApplicationManager
from time import time, sleep
from PyQt5.QtWidgets import QApplication
from CmdBase import CmdBase, CalcMode, CmdMode

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
    # FOR DEBUGGING PURPOSES: Set Single or MultiThread (default)
    CmdBase.calcmode = CalcMode.singlethread

    GUI = False

    parser = argparse.ArgumentParser(
        description='RepTate: Rheologhy of Entangled Polymers: Toolkit for the Analysis of Theory and Experiment.',
        epilog='(c) Jorge Ramirez - jorge.ramirez@upm.es - UPM , Victor Boudara - U. Leeds (2018)')
    parser.add_argument('-v', '--verbose', help='Write debug information to stdout', action='store_true')
    parser.add_argument('-b', '--batch', help='Run in batch mode (no graphics)', action='store_true')
    parser.add_argument('-V', '--version', help='Print RepTate version and exit', action='store_true')
    parser.add_argument('finlist', nargs='*')

    args = parser.parse_args() 

    if args.batch: 
        CmdBase.mode = CmdMode.batch

    # Get files from command line
    dictfiles=get_argument_files(args.finlist)

    if args.version:
        print(ApplicationManager.intro)
        sys.exit()
    
    qapp = QApplication(sys.argv)
    app = ApplicationManager()

    # Handle files & open apps accordingly
    d = {app.extension: app.appname for app in  list(app.available_applications.values())}
    for k in dictfiles.keys():
        if (k in d.keys()):
            app.new(d[k])
            appname="%s%d"%(d[k],app.application_counter)
            ds, dsname = app.applications[appname].new("")
            app.applications[appname].datasets[dsname]=ds
            for f in dictfiles[k]:
                #app.applications[appname].datasets[dsname].do_open(f)
                ds.do_open(f)
            ds.do_plot()
            #app.applications[dsname].datasets[dsname].do_plot()
        else:
            print("File type %s cannot be opened"%k)

    sys.exit(app.cmdloop())

if __name__ == '__main__':
    start_RepTate(sys.argv[1:])
