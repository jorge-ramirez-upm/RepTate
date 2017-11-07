from Application import *
import numpy as np
from TheoryRoliePoly import TheoryRoliePoly
from ApplicationWindow import *


class ApplicationNLVE(Application, ApplicationWindow):
    """Application to Non-linear flow Data
    """
    name="NLVE"
    description="Non-Linear Flow"
    
    def __init__(self, name="NLVE", parent = None):
        super(ApplicationNLVE, self).__init__(name, parent)
        if CmdBase.mode==CmdMode.GUI: #if GUI mode
            ApplicationWindow.__init__(self, name, self)

        # VIEWS
        self.views["Log(eta(t))"]=View("Log(eta(t))", "Log transient viscosity", "Log(t)", "Log($\eta$(t))", False, False, self.viewLogeta, 1, ["$\eta$(t)"])
        self.views["Log(sigma(t))"]=View("Log(sigma(t))", "Log transient shear stress", "Log($\gamma$)", "Log($\sigma_{xy}$($\gamma$))", False, False, self.viewLogSigma, 1, ["$\sigma_{xy}$($\gamma$)"])
        self.current_view=self.views["Log(eta(t))"]

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
