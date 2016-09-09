from Application import *
#from TheoryMaxwellModes import TheoryMaxwellModesTime

class ApplicationMWD(Application):
    """Application to analyze Molecular Weight distributions
       TODO: IS IT NECESSARY TO KEEP TWO SEPARATE APPLICATIONS FOR REACT AND FOR MWD???
    """
    name="MWD"
    description="Experimental Molecular weight distributions"
    
    def __init__(self, name="MWD", parent = None):
        super(ApplicationMWD, self).__init__(name, parent)

        # VIEWS
        self.views.append(View("W(M)", "Molecular weight distribution", "M", "W(M)", True, False, self.viewWM, 1, ["W(M)"]))
        self.current_view=self.views[0]

        # FILES
        ftype=TXTColumnFile("GPC Files", "gpc", "Molecular Weight Distribution", 0, -1, ['M','W(logM)'], [0], ['Mw','Mn','PDI'], [])
        self.filetypes[ftype.extension]=ftype

        # THEORIES
        #self.theories[TheoryMaxwellModesTime.thname]=TheoryMaxwellModesTime

    def viewWM(self, vec, x, y, file_parameters):
        x[0]=vec[0]
        y[0]=vec[1]
        return True
