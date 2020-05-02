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
"""Module ReptateCL

Main program that launches the CL version of RepTate.

"""
import os
import sys
import glob
import argparse
import logging
import numpy as np

from RepTate.core.ApplicationManager import ApplicationManager
from time import time, sleep
from PyQt5.QtWidgets import QApplication
from RepTate.core.CmdBase import CmdBase, CalcMode, CmdMode

def main():
    start_RepTate(sys.argv[1:])

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
    parser.add_argument('-b', '--batch', help='Run in batch mode (no graphics)', action='store_true')
    parser.add_argument('-s', '--single', help='Run Reptate as a single thread application', action='store_true')
    parser.add_argument('-t', '--theory', help='Open the given theory (if available)', default='')
    parser.add_argument('-v', '--verbose', help='Write debug information to stdout', action='store_true')
    parser.add_argument('-V', '--version', help='Print RepTate version and exit', action='store_true')
    parser.add_argument('finlist', nargs='*')

    args = parser.parse_args()

    if args.batch:
        CmdBase.mode = CmdMode.batch

    if args.verbose:
        loglevel=logging.DEBUG
    else:
        loglevel=logging.INFO

    # Get files from command line
    dictfiles=get_argument_files(args.finlist)

    if args.version:
        print(ApplicationManager.intro)
        sys.exit()

    qapp = QApplication(sys.argv)  # Needed, because some internal functions use Qt
    app = ApplicationManager(loglevel=loglevel)

    # Handle files & open apps accordingly
    CmdBase.calcmode = CalcMode.singlethread # avoid troubles when loading multiple apps/files/theories
    d = {app.extension: app.appname for app in  list(app.available_applications.values())}
    fileopen = False
    theoryopen = False
    for k in dictfiles.keys():
        if k == 'rept':
            #ex.open_project(dictfiles[k][0])
            app.logger.warning("Open RepTate projects not implemented for the Command Line version")
            pass # Not implemented yet
        elif np.any([k == key for key in d.keys()]):
            app.new(d[k])
            appname="%s%d"%(d[k],app.application_counter)
            ds, dsname = app.applications[appname].new("")
            app.applications[appname].datasets[dsname]=ds
            for f in dictfiles[k]:
                ds.do_open(f)
            fileopen = True
            if args.theory in list(app.applications[appname].theories.keys()):
                th, thname = ds.new(args.theory)
                if th != None:
                    theoryopen = True
            ds.do_plot()
        elif np.any([k in key for key in d.keys()]): # works with spaces in extensions
            for key in d.keys():
                if k in key:
                    app.new(d[key])
                    appname="%s%d"%(d[key],app.application_counter)
                    ds, dsname = app.applications[appname].new("")
                    app.applications[appname].datasets[dsname]=ds
                    for f in dictfiles[k]:
                        ds.do_open(f)
                    fileopen = True
                    if args.theory in list(app.applications[appname].theories.keys()):
                        th, thname = ds.new(args.theory)
                        if th != None:
                            theoryopen = True
                    ds.do_plot()
                    break
        else:
            print("File type %s cannot be opened"%k)
    # set the calmode back
    if args.single:
        CmdBase.calcmode = CalcMode.singlethread
    else:
        CmdBase.calcmode = CalcMode.multithread

    def my_excepthook(type, value, tb):
        """Catch exceptions and print error message. Open email client to report bug to devlopers"""
        tb_msg = ''
        for e in traceback.format_tb(tb):
            tb_msg += str(e)
        tb_msg += "%s: %s\n" % (type.__name__, str(value))
        app.logger.critical(tb_msg)
        msg = 'Sorry, something went wrong:\n \"%s: %s\".\nTry to save your work and quit RepTate.' % (type.__name__, str(value))
        app.logger.critical(msg)
        msg = 'Report bug to reptate.rheology@gmail.com: Describe the error, attach logfile and datafiles'
        app.logger.critical(msg)

    sys.excepthook = my_excepthook

    if fileopen and theoryopen:
        app.cmdqueue.append("switch %s.%s.%s"%(appname,dsname,thname))
    elif fileopen:
        app.cmdqueue.append("switch %s.%s"%(appname,dsname))
    try:
        sys.exit(app.cmdloop())
    except SystemExit:
        pass

if __name__ == '__main__':
    main()
