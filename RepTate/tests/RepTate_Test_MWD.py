# RepTate: Rheology of Entangled Polymers: Toolkit for the Analysis of Theory and Experiments
# http://blogs.upm.es/compsoftmatter/software/reptate/
# https://github.com/jorge-ramirez-upm/RepTate
# http://reptate.readthedocs.io
# Jorge Ramirez, jorge.ramirez@upm.es
# Victor Boudara, mmvahb@leeds.ac.uk
# Copyright (2017) Universidad Politécnica de Madrid, University of Leeds
# This software is distributed under the GNU General Public License. 
"""Module Reptate

Main program that launches the GUI.

""" 
import os
import sys
import getopt
sys.path.append('core')
sys.path.append('gui')
sys.path.append('console')
sys.path.append('applications')
sys.path.append('theories')
sys.path.append('visual')
from QApplicationManager import QApplicationManager
#from ApplicationManager import * #solved the issue with the matplot window not opening on Mac
from PyQt5.QtWidgets import QApplication
from SplashScreen import SplashScreen
from time import time, sleep
from CmdBase import CmdBase, CalcMode


def start_RepTate(argv):
    """
    Main RepTate application. 
    
    :param list argv: Command line parameters passed to Reptate
    """
    GUI = True
    QApplication.setStyle("Fusion") #comment that line for a native look
    #for a list of available styles: "from PyQt5.QtWidgets import QStyleFactory; print(QStyleFactory.keys())"
    
    app = QApplication(sys.argv)
    
    # FOR DEBUGGING PURPOSES: Set Single or MultiThread (default)
    CmdBase.calcmode = CalcMode.singlethread
    
    ex = QApplicationManager()
    ex.setStyleSheet("QTabBar::tab { color:black; height: 22px; }")

    ex.show()
    
    ########################################################
    # THE FOLLOWING LINES ARE FOR TESTING A PARTICULAR CASE
    # Open a particular application
    ex.new_mwd_window()
    
    #####################
    # TEST MaxwellModesTime
    # Open a Dataset
    gt_dir = "data%sMWD%s"%((os.sep,)*2)
    ex.applications["MWD1"].new_tables_from_files([
                                                   gt_dir + "Munstedt_PSIII.gpc",
                                                   ])
    # Open a theory
    ex.applications["MWD1"].datasets["Set1"].new_theory("MWDiscr")

    ex.new_mwd_window()
    ex.applications["MWD2"].new_tables_from_files([
                                                   gt_dir + "Munstedt_PSIV.gpc",
                                                   ])
    # Open a theory
    ex.applications["MWD2"].datasets["Set1"].new_theory("MWDiscr")


    sys.exit(app.exec_())

if __name__ == '__main__':
    start_RepTate(sys.argv[1:])
