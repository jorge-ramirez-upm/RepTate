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

def start_RepTate(argv):
    """
    Main RepTate application. 
    
    :param list argv: Command line parameters passed to Reptate
    """
    GUI = True
    QApplication.setStyle("Fusion") #comment that line for a native look
    #for a list of available styles: "from PyQt5.QtWidgets import QStyleFactory; print(QStyleFactory.keys())"
    
    app = QApplication(sys.argv)
    ex = QApplicationManager()
    ex.show()
    
    ########################################################
    # THE FOLLOWING LINES ARE FOR TESTING A PARTICULAR CASE
    # Open a particular application
    ex.new_tts_window()
    
    # Open a Dataset
    pi_dir = "data%sPI_LINEAR%sosc%s"%((os.sep,)*3)
    ex.applications["TTS1"].new_tables_from_files([
                                                   pi_dir + "PI223k-14c_-45C_FS2_PP10.osc",
                                                   pi_dir + "PI223k-14c_-40C_FS_PP10.osc",
                                                   pi_dir + "PI223k-14c_-30C_FS_PP10.osc",
                                                   pi_dir + "PI223k-14_-10C_FS_PP10.osc",
                                                   pi_dir + "PI223k-14c_-20C_FS_PP10.osc",
                                                   pi_dir + "PI223k-14b_0C_FS4_PP10.osc",
                                                   pi_dir + "PI223k-14_10C_FS_PP10.osc",
                                                   pi_dir + "PI223k-14b_25C_FS3_PP10.osc",
                                                   pi_dir + "PI223k-14_25C_FS3_PP10.osc",
                                                   pi_dir + "PI223k-14c_30C_FS3_PP10.osc",
                                                   pi_dir + "PI223k-14_40C_FS_PP10.osc",
                                                   pi_dir + "PI223k-14_50C_FS_PP10.osc",
                                                   ])

    # Open a theory
    ex.applications["TTS1"].datasets["Set1"].new_theory("TTSShiftAutomatic")
    
    # Minimize the theory
    ex.applications["TTS1"].datasets["Set1"].handle_actionMinimize_Error()
                                                   
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    start_RepTate(sys.argv[1:])
