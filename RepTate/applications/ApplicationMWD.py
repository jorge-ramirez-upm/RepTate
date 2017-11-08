from Application import *
import numpy as np
from TheoryDiscrMWD import TheoryDiscrMWD
#from TheoryMaxwellModes import TheoryMaxwellModesTime

from ApplicationWindow import *


class ApplicationMWD(ApplicationWindow):
    """
    Application to analyze Molecular Weight distributions
    
    .. todo:: IS IT NECESSARY TO KEEP TWO SEPARATE APPLICATIONS FOR REACT AND FOR MWD???
    """
    name="MWD"
    description="Experimental Molecular weight distributions"
    
    def __init__(self, name="MWD", parent = None):
        super(ApplicationMWD, self).__init__(name, parent)
        # if CmdBase.mode==CmdMode.GUI: #if GUI mode
        #     ApplicationWindow.__init__(self, name, self)

        # VIEWS
        self.views["W(M)"]=View("W(M)", "Molecular weight distribution", "M", "W(M)", True, False, self.viewWM, 1, ["W(M)"])
        self.current_view=self.views["W(M)"]
        # if CmdBase.mode==CmdMode.GUI: #if GUI mode
        #     self.populateViews()
        
        # FILES
        ftype=TXTColumnFile("React Files", "reac", "Relaxation modulus", ['M','W(logM)', 'g', 'br/1000C'], [], [])
        self.filetypes[ftype.extension]=ftype
        ftype=TXTColumnFile("GPC Files", "gpc", "Molecular Weight Distribution", ['M','W(logM)'], ['Mw','Mn','PDI'], ['kDa', '-'])
        #ftype=TXTColumnFile("GPC Files", "gpc", "Molecular Weight Distribution", ['M','W(logM)'], [], ['kDa', '-'])
        self.filetypes[ftype.extension]=ftype

        # THEORIES
        self.theories[TheoryDiscrMWD.thname] = TheoryDiscrMWD
        #self.theories[TheoryMaxwellModesTime.thname]=TheoryMaxwellModesTime

    def viewWM(self, dt, file_parameters):
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        max_y = np.max(dt.data[:, 1])
        x[:, 0] = dt.data[:, 0]
        y[:, 0] = dt.data[:, 1]/max_y
        return x, y, True
