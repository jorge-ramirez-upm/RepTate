from Application import *
import numpy as np
#from TheoryMaxwellModes import TheoryMaxwellModesTime

class ApplicationTTS(Application):
    """Application to perform Time Temperature Superposition
       TODO: DO WE NEED A SEPARATE APPLICATION FROM LVE???
    """
    name="TTS"
    description="Time-Temperature Superposition Shift"
    
    def __init__(self, name = "TTS", parent = None):
        super(ApplicationTTS, self).__init__(name, parent)

        # VIEWS
        self.views["Log(G',G''(w))"]=View("Log(G',G''(w))", "Log Storage,Loss moduli", "Log(w)", "Log(G'(w),G''(w))", False, False, self.viewLogG1G2, 2, ["G'(w)","G''(w)"])
        self.views["G',G''(w)"]=View("G',G''(w)", "Storage,Loss moduli", "w", "G'(w),G''(w)", True, True, self.viewG1G2, 2, ["G'(w)","G''(w)"])
        self.current_view=self.views["Log(G',G''(w))"]

        # FILES
        ftype=TXTColumnFile("Oscillatory shear files", "osc", "Oscillatory Shear Files from rheometer", 0, 2, ['w','G1','G2'], [0], ['Mw','ncontri'], [])
        self.filetypes[ftype.extension]=ftype

        # THEORIES
        #self.theories[TheoryMaxwellModesTime.thname]=TheoryMaxwellModesTime

    def viewLogG1G2(self, vec, x, y, file_parameters):
        x[0]=np.log10(vec[0])
        y[0]=np.log10(vec[1])
        y[1]=np.log10(vec[2])
        return True

    def viewG1G2(self, vec, x, y, file_parameters):
        x[0]=vec[0]
        y[0]=vec[1]
        y[1]=vec[2]
        return True
