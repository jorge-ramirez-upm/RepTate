from Application import *
from TheoryMaxwellModes import TheoryMaxwellModesTime

class ApplicationGt(Application):
    """Application to analyze the relaxation modulus"""
    name="Gt"
    description="Relaxation modulus"
    
    def __init__(self, name = "Gt", parent = None):
        super(ApplicationGt, self).__init__(name, parent)

        # VIEWS
        self.views["G(t)"]=View("G(t)", "Relaxation modulus", "t", "G(t)", True, True, self.viewGt, 1, ["G(t)"])
        self.views["Log[G(t)]"]=View("Log[G(t)]", "Log Relaxation modulus", "log(t)", "log(G(t))", False, False, self.viewLogGt, 1, ["log(G(t))"])
        self.current_view=self.views["G(t)"]

        # FILES
        ftype=TXTColumnFile("G(t) files", "gt", "Relaxation modulus", ['t','Gt'], ['Mw','ncontri'], ['s', 'Pa'])
        self.filetypes[ftype.extension]=ftype

        # THEORIES
        self.theories[TheoryMaxwellModesTime.thname]=TheoryMaxwellModesTime

    def viewGt(self, vec, x, y, file_parameters):
        x[0]=vec[0]
        y[0]=vec[1]
        return True

    def viewLogGt(self, vec, x, y, file_parameters):
        x[0]=vec[0]
        y[0]=vec[1]
        return True
