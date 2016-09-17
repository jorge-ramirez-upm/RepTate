from Application import *
import numpy as np
from TheoryRoliePoly import TheoryRoliePoly

class ApplicationNLVE(Application):
    """Application to Non-linear flow Data
    """
    name="NLVE"
    description="Non-Linear Flow"
    
    def __init__(self, name="NLVE", parent = None):
        super(ApplicationNLVE, self).__init__(name, parent)

        # VIEWS
        self.views.append(View("Log(eta(t))", "Log transient viscosity", "Log(t)", "Log($\eta$(t))", False, False, self.viewLogeta, 1, ["$\eta$(t)"]))
        self.views.append(View("Log(sigma(t))", "Log transient shear stress", "Log($\gamma$)", "Log($\sigma_{xy}$($\gamma$))", False, False, self.viewLogSigma, 1, ["$\sigma_{xy}$($\gamma$)"]))
        self.current_view=self.views[0]

        # FILES
        ftype=TXTColumnFile("Start-up of shear flow", "shear", "Shear flow files", 2, -1, ['t','eta'], [0, 1], ['gdot','T'], ['s','Pa$\cdot$s'])
        self.filetypes[ftype.extension]=ftype

        # THEORIES
        self.theories[TheoryRoliePoly.thname]=TheoryRoliePoly

    def viewLogeta(self, dt, file_parameters):
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = np.log10(dt.data[:, 0])
        y[: ,0] = np.log10(dt.data[:, 1]/float(file_parameters["gdot"]))
        return x, y, True

    def viewLogSigma(self, dt, file_parameters):
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = np.log10(dt.data[:, 0]*float(file_parameters["gdot"]))
        y[: ,0] = np.log10(dt.data[:, 1])
        return x, y, True
