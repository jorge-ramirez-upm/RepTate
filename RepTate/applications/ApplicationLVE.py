from Application import *
import numpy as np
#from TheoryMaxwellModes import TheoryMaxwellModesTime

class ApplicationLVE(Application):
    """Application to Analyze Linear Viscoelastic Data
       TODO: DO WE NEED A SEPARATE APPLICATION FROM TTS???
    """
    name="LVE"
    description="Linear Viscoelasticity"
    
    def __init__(self, parent = None):
        super(ApplicationLVE, self).__init__()

        # VIEWS
        self.views.append(View("Log(G',G''(w))", "Log Storage,Loss moduli", "Log(w)", "Log(G'(w),G''(w))", False, False, self.viewLogG1G2, 2, ["G'(w)","G''(w)"]))
        self.views.append(View("G',G''(w)", "Storage,Loss moduli", "w", "G'(w),G''(w)", True, True, self.viewG1G2, 2, ["G'(w)","G''(w)"]))
        self.current_view=self.views[0]

        # FILES
        ftype=TXTColumnFile("LVE files", "tts", "LVE files", 0, 2, ['w','G1','G2'], [0], ['Mw','T'], [])
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
