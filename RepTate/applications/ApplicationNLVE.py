# RepTate: Rheology of Entangled Polymers: Toolkit for the Analysis of Theory and Experiments
# http://blogs.upm.es/compsoftmatter/software/reptate/
# https://github.com/jorge-ramirez-upm/RepTate
# http://reptate.readthedocs.io
# Jorge Ramirez, jorge.ramirez@upm.es
# Victor Boudara, mmvahb@leeds.ac.uk
# Copyright (2017) Universidad Politécnica de Madrid, University of Leeds
# This software is distributed under the GNU General Public License. 
"""Module ApplicationNLVE

Module for handling data from start up of shear and extensional flow experiments.

""" 
from CmdBase import CmdBase, CmdMode
from Application import Application
from QApplicationWindow import QApplicationWindow
from View import View
from FileType import TXTColumnFile
import numpy as np
from TheoryRoliePoly import TheoryRoliePoly

class ApplicationNLVE(QApplicationWindow):
    """Application to Non-linear flow Data
    """
    name="NLVE"
    description="Non-Linear Flow"
    
    def __init__(self, name="NLVE", parent = None):
        super(ApplicationNLVE, self).__init__(name, parent)
        # if CmdBase.mode==CmdMode.GUI: #if GUI mode
        #     QApplication.__init__(self, name, self)

        # VIEWS
        self.views["Log(eta(t))"]=View("Log(eta(t))", "Log transient viscosity", "Log(t)", "Log($\eta$(t))", False, False, self.viewLogeta, 1, ["$\eta$(t)"])
        self.views["Log(sigma(t))"]=View("Log(sigma(t))", "Log transient shear stress", "Log($\gamma$)", "Log($\sigma_{xy}$($\gamma$))", False, False, self.viewLogSigma, 1, ["$\sigma_{xy}$($\gamma$)"])
        self.current_view=self.views["Log(eta(t))"]
        # if CmdBase.mode==CmdMode.GUI: #if GUI mode
        #     self.populateViews()

        # FILES
        ftype=TXTColumnFile("Start-up of shear flow", "shear", "Shear flow files", ['t','eta'], ['gdot','T'], ['s','Pa$\cdot$s'])
        self.filetypes[ftype.extension]=ftype

        # THEORIES
        self.theories[TheoryRoliePoly.thname]=TheoryRoliePoly

    def viewLogeta(self, dt, file_parameters):
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = np.log10(dt.data[:, 0])
        y[:, 0] = np.log10(dt.data[:, 1]) #exp data files contain eta, so does Rolie-Poly
        return x, y, True

    def viewLogSigma(self, dt, file_parameters):
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = np.log10(dt.data[:, 0]*float(file_parameters["gdot"])) #compute strain
        y[:, 0] = np.log10(dt.data[:, 1]*float(file_parameters["gdot"])) #compute stress
        return x, y, True
