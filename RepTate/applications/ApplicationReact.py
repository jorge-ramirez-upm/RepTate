from Application import *
#from TheoryMaxwellModes import TheoryMaxwellModesTime

class ApplicationReact(Application):
    """Application to analyze the relaxation modulus"""
    name="React"
    description="Experimental GPC-light scattering data"
    
    def __init__(self, name="React", parent = None):
        super(ApplicationReact, self).__init__(name, parent)

        # VIEWS
        self.views["W(M)"]=View("W(M)", "Molecular weight distribution", "M", "W(M)", True, False, self.viewWM, 1, ["W(M)"])
        self.current_view=self.views["W(M)"]

        # FILES
        ftype=TXTColumnFile("React Files", "reac", "Relaxation modulus", 0, -1, ['M','W(logM)', 'g', 'br/1000C'], [0], [], [])
        self.filetypes[ftype.extension]=ftype

        # THEORIES
        #self.theories[TheoryMaxwellModesTime.thname]=TheoryMaxwellModesTime

    def viewWM(self, vec, x, y, file_parameters):
        x[0]=vec[0]
        y[0]=vec[1]
        return True
