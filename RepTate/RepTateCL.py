# RepTate: Rheology of Entangled Polymers: Toolkit for the Analysis of Theory and Experiments
# http://blogs.upm.es/compsoftmatter/software/reptate/
# https://github.com/jorge-ramirez-upm/RepTate
# http://reptate.readthedocs.io
# Jorge Ramirez, jorge.ramirez@upm.es
# Victor Boudara, mmvahb@leeds.ac.uk
# Copyright (2017) Universidad Politécnica de Madrid, University of Leeds
# This software is distributed under the GNU General Public License. 
"""Module ReptateCL

Main program that launches the CL version of RepTate.

""" 
import sys
import getopt
sys.path.append('core')
sys.path.append('gui')
sys.path.append('console')
sys.path.append('applications')
sys.path.append('theories')
from ApplicationManager import ApplicationManager
from time import time, sleep
from PyQt5.QtWidgets import QApplication
from CmdBase import CmdBase, CalcMode, CmdMode

def start_RepTate(argv):
    """
    Main RepTate application. 
    
    :param list argv: Command line parameters passed to Reptate
    """
    # FOR DEBUGGING PURPOSES: Set Single or MultiThread (default)
    CmdBase.calcmode = CalcMode.singlethread

    GUI = False
    try:
        opts, args = getopt.getopt(argv, "hb")
    except getopt.GetoptError:
        print('Invalid option. Usage:')
        print ('ReptateCL.py [-b < inputfile]')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h","--help"):
            print ('ReptateCL.py [-b < inputfile]')
            sys.exit()
        elif opt == '-b':
            CmdBase.mode = CmdMode.batch
    
    qapp = QApplication(sys.argv)
    app = ApplicationManager()
    sys.exit(app.cmdloop())

if __name__ == '__main__':
    start_RepTate(sys.argv[1:])
