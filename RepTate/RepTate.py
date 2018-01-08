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

def start_RepTate(argv):
    """
    Main RepTate application. 
    
    :param list argv: Command line parameters passed to Reptate
    """
    GUI = True
    QApplication.setStyle("Fusion") #comment that line for a native look
    #for a list of available styles: "from PyQt5.QtWidgets import QStyleFactory; print(QStyleFactory.keys())"
    
    app = QApplication(sys.argv)
    start = time() 
    splash = SplashScreen()
    splash.showMessage("Loading RepTate...\n")
    splash.show()
    ex = QApplicationManager()
    ex.setStyleSheet("QTabBar::tab { color:black; height: 22px; }")
    splash.showMessage("Loading RepTate...\nVersion " + ex.version + ' ' + ex.date)

    # #### DEBUG
    # new_app = ex.new_React_window()
    # new_app.new_tables_from_files(['data/React/out1.reac'])
    # # ####
    # while time() - start < .1:
    #     sleep(0.001)
    #     if (time()-start < 0.5):
    #         splash.showMessage("Loading Reptate...")
    #     else:
    #     app.processEvents()


    # ex.new_lve_window()
    splash.finish(ex)
    ex.showMaximized()
    sys.exit(app.exec_())

if __name__ == '__main__':
    start_RepTate(sys.argv[1:])
