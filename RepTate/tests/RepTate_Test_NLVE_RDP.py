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
import getopt
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
    QApplication.setStyle("Fusion")  #comment that line for a native look
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
    ex.handle_new_app('NLVE')

    #####################
    # TEST Rolie-Poly
    # Open a Dataset

    dow_dir = "data%sDOW%sNon-Linear_Rheology%sStart-up_Shear%s" % ((
        os.sep, ) * 4)
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
    ex.applications["NLVE1"].datasets["Set1"].new_theory("Rolie-Double-Poly")
    # Minimize the theory
    # ex.applications["NLVE1"].datasets["Set1"].handle_actionMinimize_Error()

    ########################################################
    # THE FOLLOWING LINES ARE FOR TESTING A PARTICULAR CASE
    # Open a particular application
    ex.handle_new_app('NLVE')

    #####################
    # TEST Rolie-Poly
    # Open a Dataset

    dow_dir = os.path.join('data', 'NLVE_Extension', '')
    ex.applications["NLVE2"].new_tables_from_files([
        dow_dir + "Minegishi_spiked_PS_0_572.uext",
        dow_dir + "Minegishi_spiked_PS_0_013.uext",
        dow_dir + "Minegishi_spiked_PS_0_047.uext",
        dow_dir + "Minegishi_spiked_PS_0_097.uext"
    ])
    # Open a theory
    ex.applications["NLVE2"].datasets["Set1"].new_theory("Rolie-Double-Poly")
    # Minimize the theory
    # ex.applications["NLVE1"].datasets["Set1"].handle_actionMinimize_Error()

    ####################
    #open MWD import Mead gpc
    ex.handle_new_app('MWD')
    dir = os.path.join('data', 'MWD', '')
    ex.applications["MWD3"].new_tables_from_files([
        dir + "Munstedt_PSIV.gpc",
    ])
    ex.applications["MWD3"].datasets["Set1"].new_theory("Discretize MWD")

    # ####################
    # #open linear rheology data to import the Maxwell modes
    # ex.handle_new_app('NLVE')
    # dow_dir = "data%sDOW%sLinear_Rheology_TTS%s" % ((
    #     os.sep, ) * 3)
    # ex.applications["LVE3"].new_tables_from_files([
    #     dow_dir + "DOWLDPEL150R_160C.tts",
    # ])
    # ex.applications["LVE3"].datasets["Set1"].new_theory("MaxwellModesFrequency")
    # ex.applications["LVE3"].datasets["Set1"].handle_actionMinimize_Error()

    sys.exit(app.exec_())


if __name__ == '__main__':
    start_RepTate(sys.argv[1:])
