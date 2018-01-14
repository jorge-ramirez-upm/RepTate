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
from CmdBase import CmdBase, CalcMode
from QApplicationManager import QApplicationManager
#from ApplicationManager import * #solved the issue with the matplot window not opening on Mac
from PyQt5.QtWidgets import QApplication
from SplashScreen import SplashScreen
from time import time, sleep

def start_RepTate(argv):
    """
    Main RepTate application. 
    
    :param list argv: Command line parameters passed to Reptate
    """
    GUI = True
    QApplication.setStyle("Fusion") #comment that line for a native look
    #for a list of available styles: "from PyQt5.QtWidgets import QStyleFactory; print(QStyleFactory.keys())"
    
    # app = QApplication(sys.argv)

    # FOR DEBUGGING PURPOSES: Set Single or MultiThread (default)
    CmdBase.calcmode = CalcMode.singlethread

    ex = QApplicationManager()
    ex.setStyleSheet("QTabBar::tab { color:black; height: 22px; }")

    ########################################################
    # THE FOLLOWING LINES ARE FOR TESTING A PARTICULAR CASE
    # Open a particular application
    ex.new_React_window()
    
    #####################
    # TEST Likhtman-McLeish
    # Open a Dataset
    ex.applications["React1"].new_tables_from_files([
                                                   "data%sReact%sout1.reac"%((os.sep,)*2),
                                                   ])
    # Open a theory
    ex.applications["React1"].datasets["Set1"].new_theory("TobitaCSTRTheory")

    print(ex.applications["React1"].multiplots.axarr[0].get_position())
    ex.applications["React1"].multiplots.plotselecttabWidget.setCurrentIndex(1)
    print(ex.applications["React1"].multiplots.axarr[0].get_position())
    # Calculate the theory
    ex.applications["React1"].datasets["Set1"].handle_actionCalculate_Theory()
    print(ex.applications["React1"].multiplots.axarr[0].get_position())

    ex.applications["React1"].multiplots.plotselecttabWidget.setCurrentIndex(0)
    print(ex.applications["React1"].multiplots.axarr[0].get_position())
    ex.applications["React1"].multiplots.plotselecttabWidget.setCurrentIndex(1)
    print(ex.applications["React1"].multiplots.axarr[0].get_position())

    ex.applications["React1"].datasets["Set1"].new_theory("TobitaBatchTheory")


    ex.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    start_RepTate(sys.argv[1:])
