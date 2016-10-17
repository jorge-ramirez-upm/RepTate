from Application import *
#from TheoryMaxwellModes import TheoryMaxwellModesTime

class ApplicationMWD(Application):
    """
    Application to analyze Molecular Weight distributions
    
    .. todo:: IS IT NECESSARY TO KEEP TWO SEPARATE APPLICATIONS FOR REACT AND FOR MWD???
    """
    name="MWD"
    description="Experimental Molecular weight distributions"
    
    def __init__(self, name="MWD", parent = None):
        super(ApplicationMWD, self).__init__(name, parent)

        # VIEWS
        self.views["W(M)"]=View("W(M)", "Molecular weight distribution", "M", "W(M)", True, False, self.viewWM, 1, ["W(M)"])
        self.current_view=self.views["W(M)"]
        ftype=TXTColumnFile("React Files", "reac", "Relaxation modulus", ['M','W(logM)', 'g', 'br/1000C'], [], [])
        self.filetypes[ftype.extension]=ftype

        # FILES
        ftype=TXTColumnFile("GPC Files", "gpc", "Molecular Weight Distribution", ['M','W(logM)'], ['Mw','Mn','PDI'], ['kDa', '-'])
        self.filetypes[ftype.extension]=ftype

        # THEORIES
        #self.theories[TheoryMaxwellModesTime.thname]=TheoryMaxwellModesTime

    def viewWM(self, vec, x, y, file_parameters):
        x[0]=vec[0]
        y[0]=vec[1]
        return True
