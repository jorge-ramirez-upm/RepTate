"""
    Module for handling FRS experiments and simulations.
"""
from Application import Application

class ApplicationFRS_I(Application):
    """Application to FRS Intensity simulations"""
    name="FRS_I"
    description="FRS Intensity"

    def __init__(self, name = "FRS_I", parent = None):
        super(ApplicationFRS_I, self).__init__(name, parent)
        
        # VIEWS
        self.views["I(t)"]=View("I(t)", "FRS Intensity decay", "t", "I(t)", True, True, self.viewIt, 1, ["I(t)"])
        self.views["Log[I(t)]"]=View("Log[I(t)]", "Log FRS Intensity decay", "log(t)", "log(I(t))", False, False, self.viewLogIt, 1, ["log(I(t))"])
        self.current_view=self.views["I(t)"]

        # FILES
        ftype=TXTColumnFile("I(t) FRS files", "FRS_INTENSITY", "I(t) decay from FRS", ['t','I'], ['d','Na','ka','Ns','ka','Keq','beta'], ['s', 'Pa'])
        self.filetypes[ftype.extension]=ftype

    def viewIt(self, dt, file_parameters):
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = dt.data[:, 0]
        y[: ,0] = dt.data[:, 1]
        return x, y, True

    def viewLogIt(self, dt, file_parameters):
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = np.log10(dt.data[:, 0])
        y[: ,0] = np.log10(dt.data[:, 1])
        return x, y, True


       
 
 

