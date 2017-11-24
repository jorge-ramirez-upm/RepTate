from Application import Application
from QApplicationWindow import *
import numpy as np
from TheoryMaxwellModes import TheoryMaxwellModesTime

class ApplicationGt(CmdBase):
    """Application to analyze the relaxation modulus"""
    name="Gt"
    description="Relaxation modulus"
    
    def __new__(cls, name="Gt", parent = None):
        return GUIApplicationGt(name, parent) if (CmdBase.mode==CmdMode.GUI) else CLApplicationGt(name, parent)

class BaseApplicationGt:
    def __init__(self, name = "Gt", parent = None):
        super().__init__(name, parent)

        # VIEWS
        self.views["G(t)"]=View("G(t)", "Relaxation modulus", "t", "G(t)", "s", "Pa", True, True, self.viewGt, 1, ["G(t)"])
        self.views["Log[G(t)]"]=View("Log[G(t)]", "Log Relaxation modulus", "log(t)", "log(G(t))", "s", "Pa", False, False, self.viewLogGt, 1, ["log(G(t))"])
        self.current_view=self.views["Log[G(t)]"]

        # FILES
        ftype=TXTColumnFile("G(t) files", "gt", "Relaxation modulus", ['t','Gt'], ['Mw','ncontri'], ['s', 'Pa'])
        self.filetypes[ftype.extension]=ftype

        # THEORIES
        self.theories[TheoryMaxwellModesTime.thname]=TheoryMaxwellModesTime

    def viewGt(self, dt, file_parameters):
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = dt.data[:, 0]
        y[: ,0] = dt.data[:, 1]
        return x, y, True

    def viewLogGt(self, dt, file_parameters):
        validindex = np.logical_and(dt.data[:, 0]>0, dt.data[:, 1]>0)
        x = np.zeros((np.sum(validindex), 1))
        y = np.zeros((np.sum(validindex), 1))
        x[:, 0] = np.log10(dt.data[validindex, 0])
        y[:, 0] = np.log10(dt.data[validindex, 1])
        return x, y, True

class CLApplicationGt(BaseApplicationGt, Application):
    def __init__(self, name="Gt", parent = None):
        super().__init__(name, parent)
        

class GUIApplicationGt(BaseApplicationGt, QApplicationWindow):
    def __init__(self, name="Gt", parent = None):
        super().__init__(name, parent)

        self.populate_views() #populate the view ComboBox
