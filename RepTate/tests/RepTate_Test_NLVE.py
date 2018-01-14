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
    ex.new_nlve_window()
    
    #####################
    # TEST Rolie-Poly
    # Open a Dataset

    dow_dir = "data%sDOW%sNon-Linear_Rheology%sStart-up_Shear%s"%((os.sep,)*4)
    ex.applications["NLVE1"].new_tables_from_files([
                                                   dow_dir + "My_dow150-160-1 shear.shear",
                                                   dow_dir + "My_dow150-160-01 shear.shear",
                                                   dow_dir + "My_dow150-160-001 shear.shear",
                                                   dow_dir + "My_dow150-160-3 shear.shear",
                                                   dow_dir + "My_dow150-160-03 shear.shear",
                                                   dow_dir + "My_dow150-160-003 shear.shear",
                                                   dow_dir + "My_dow150-160-0003 shear.shear",
                                                   ])
    # Open a theory
    ex.applications["NLVE1"].datasets["Set1"].new_theory("RoliePoly")
    # Minimize the theory
    ex.applications["NLVE1"].datasets["Set1"].handle_actionMinimize_Error()


    # #####################
    # # TEST Carreau-Yasuda
    # # Open a Dataset
    # ex.new_lve_window()
    # ex.applications["LVE2"].new_tables_from_files([
    #                                                pi_dir + "PI_483.1k_T-35.tts",
    #                                                ])
    # # Switch the view
    # ex.applications["LVE2"].view_switch("logetastar")
    # # Open a theory
    # ex.applications["LVE2"].datasets["Set1"].new_theory("CarreauYasudaTheory")
    # # Minimize the theory
    # ex.applications["LVE2"].datasets["Set1"].handle_actionMinimize_Error()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    start_RepTate(sys.argv[1:])
