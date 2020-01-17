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
"""Module Reptate

Main program that launches the GUI.

""" 
import os
import sys
sys.path.append('core')
sys.path.append('gui')
sys.path.append('console')
sys.path.append('applications')
sys.path.append('theories')
sys.path.append('visual')
sys.path.append('tools')
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
    # CmdBase.calcmode = CalcMode.singlethread
    
    ex = QApplicationManager()
    ex.setStyleSheet("QTabBar::tab { color:black; height: 22px; }")

    ex.show()
    
    ########################################################
    # THE FOLLOWING LINES ARE FOR TESTING A PARTICULAR CASE
    # Open a particular application
    ex.handle_new_app('LVE')
    
    #####################
    # TEST Likhtman-McLeish
    # Open a Dataset
    pi_dir = "data%sPI_LINEAR%s"%((os.sep,)*2)
    ex.applications["LVE1"].new_tables_from_files([
                                                   pi_dir + "PI_13.5k_T-35.tts",
                                                   pi_dir + "PI_23.4k_T-35.tts",
                                                   pi_dir + "PI_33.6k_T-35.tts",
                                                   pi_dir + "PI_94.9k_T-35.tts",
                                                   pi_dir + "PI_225.9k_T-35.tts",
                                                   pi_dir + "PI_483.1k_T-35.tts",
                                                   pi_dir + "PI_634.5k_T-35.tts",
                                                   pi_dir + "PI_1131k_T-35.tts",
                                                   ])
    # Open a theory
    ex.applications["LVE1"].datasets["Set1"].new_theory("Likhtman-McLeish")
    # Minimize the theory
    ex.applications["LVE1"].datasets["Set1"].handle_actionMinimize_Error()

    # Open a theory
    ex.applications["LVE1"].datasets["Set1"].new_theory("Rouse")
    # Minimize the theory
    ex.applications["LVE1"].datasets["Set1"].handle_actionMinimize_Error()


    #####################
    # TEST Carreau-Yasuda
    # Open a Dataset
    ex.handle_new_app('LVE')
    ex.applications["LVE2"].new_tables_from_files([
                                                   pi_dir + "PI_483.1k_T-35.tts",
                                                   ])
    # Switch the view
    ex.applications["LVE2"].view_switch("logetastar")
    # Open a theory
    ex.applications["LVE2"].datasets["Set1"].new_theory("Carreau-Yasuda")
    # Minimize the theory
    ex.applications["LVE2"].datasets["Set1"].handle_actionMinimize_Error()
    
    # Open a theory
    ex.applications["LVE2"].datasets["Set1"].new_theory("Maxwell Modes")
    # Minimize the theory
    ex.applications["LVE2"].datasets["Set1"].handle_actionMinimize_Error()
    

    #####################
    # TEST DTD
    # Open a Dataset
    ex.handle_new_app('LVE')
    pi_dir = "data%sPI_STAR%s"%((os.sep,)*2)
    ex.applications["LVE3"].new_tables_from_files([
                                                   pi_dir + "S6Z8.1T40.tts",
                                                   pi_dir + "S6Z12T40.tts",
                                                   pi_dir + "S6Z16T40.tts",
                                                   ])

    ex.applications["LVE3"].datasets["Set1"].new_theory("DTD Stars")
    ex.applications["LVE3"].datasets["Set1"].handle_actionMinimize_Error()

    sys.exit(app.exec_())

if __name__ == '__main__':
    start_RepTate(sys.argv[1:])
