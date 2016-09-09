from Application import *
import numpy as np
#from TheoryMaxwellModes import TheoryMaxwellModesTime

class ApplicationNLVE(Application):
    """Application to Non-linear flow Data
    """
    name="NLVE"
    description="Non-Linear Flow"
    
    def __init__(self, name="NLVE", parent = None):
        super(ApplicationNLVE, self).__init__(name, parent)

        # VIEWS
        self.views.append(View("Log(eta(t))", "Log transient viscosity", "Log(t)", "Log($\eta$(t))", False, False, self.viewLogeta, 2, ["$\eta$(t)"]))
        self.views.append(View("Log(sigma(t))", "Log transient shear stress", "Log(t)", "Log($\sigma_{xy}$(t))", False, False, self.viewLogSigma, 2, ["$\sigma_{xy}$(t)"]))
        self.current_view=self.views[0]

        # FILES
        ftype=TXTColumnFile("Start-up of shear flow", "shear", "Shear flow files", 2, -1, ['t','eta'], [0, 1], ['gdot','T'], ['s','Pa$\cdot$s'])
        self.filetypes[ftype.extension]=ftype

        # THEORIES
        #self.theories[TheoryMaxwellModesTime.thname]=TheoryMaxwellModesTime

    def viewLogeta(self, vec, file_parameters):
        x=np.zeros((1,1))
        y=np.zeros((1,1))
        x[0]=np.log10(vec[0])
        y[0]=np.log10(vec[1]/float(file_parameters["gdot"]))
        return x, y, True

    def viewLogSigma(self, vec, file_parameters):
        x=np.zeros((1,1))
        y=np.zeros((1,1))
        x[0]=np.log10(vec[0])
        y[0]=np.log10(vec[1])*float(file_parameters["gdot"])
        return x, y, True
