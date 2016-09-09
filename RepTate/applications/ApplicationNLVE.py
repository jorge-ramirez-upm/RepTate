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
        self.views.append(View("Log(eta(t))", "Log transient viscosity", "Log(eta)", "Log(eta(t))", False, False, self.viewLogeta, 2, ["eta(t)"]))
        self.current_view=self.views[0]

        # FILES
        ftype=TXTColumnFile("LVE files", "tts", "LVE files", 0, 2, ['w','G1','G2'], [0], ['Mw','T'], [])
        self.filetypes[ftype.extension]=ftype

        # THEORIES
        #self.theories[TheoryMaxwellModesTime.thname]=TheoryMaxwellModesTime

    def viewLogeta(self, vec, x, y, file_parameters):
        x[0]=np.log10(vec[0])
        y[0]=np.log10(vec[1]) #/file_parameters["gdot"]
        return True
