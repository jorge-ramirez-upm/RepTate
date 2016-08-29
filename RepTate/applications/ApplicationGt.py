from Application import *
from TheoryMaxwellModes import TheoryMaxwellModesTime

class ApplicationGt(Application):
    """Application to analyze the relaxation modulus"""
    name="Gt"
    description="Relaxation modulus"
    
    def __init__(self, parent = None):
        super(ApplicationGt, self).__init__()

        # VIEWS
        self.views.append(View("G(t)", "Relaxation modulus", "t", "G(t)", True, True, self.viewGt, 1, ["G(t)"]))
        self.views.append(View("Log[G(t)]", "Log Relaxation modulus", "log(t)", "log(G(t))", False, False, self.viewLogGt, 1, ["log(G(t))"]))
        self.current_view=self.views[0]

        # FILES
        ftype=TXTColumnFile("G(t) files", "gt", "Relaxation modulus", 0, 2, ['t','Gt'], [0], ['Mw','ncontri'], [])
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
