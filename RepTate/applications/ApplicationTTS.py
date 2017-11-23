from Application import *
from QApplicationWindow import *
import numpy as np
from TheoryTTS import TheoryWLFShift


class ApplicationTTS(CmdBase):
    """
    Application to Analyze Linear Viscoelastic Data
    
    .. todo:: DO WE NEED A SEPARATE APPLICATION FROM TTS???
    """
    name = "TTS"
    description = "Linear Viscoelasticity"

    def __new__(cls, name="TTS", parent = None):
        return GUIApplicationTTS(name, parent) if (CmdBase.mode==CmdMode.GUI) else CLApplicationTTS(name, parent)

class BaseApplicationTTS:
    def __init__(self, name="TTS", parent = None):
        super().__init__(name, parent)

        # VIEWS
        self.views["log(G',G''(w))"] = View(name="log(G',G''(w))", description="log Storage,Loss moduli", x_label="log($\omega$)", y_label="log(G'($\omega$),G''($\omega$))", x_units="rad/s", y_units="Pa", log_x=False, log_y=False, view_proc=self.viewLogG1G2, n=2, snames=["G'(w)","G''(w)"])
        self.views["G',G''(w)"] = View("G',G''(w)", "Storage,Loss moduli", "$\omega$", "G'($\omega$),G''($\omega$)", "rad/s", "Pa", True, True, self.viewG1G2, 2, ["G'(w)","G''(w)"])
        self.views["etastar"] = View("etastar", "Complex Viscosity", "$\omega$", "$|\eta^*(\omega)|$", "rad/s", "Pa.s", True, True, self.viewEtaStar, 1, ["eta*(w)"])
        self.views["delta"] = View("delta", "delta", "$\omega$", "$\delta(\omega)$", "rad/s", "-", True, True, self.viewDelta, 1, ["delta(w)"])
        self.views["tan(delta)"] = View("tan(delta)", "tan(delta)", "$\omega$", "tan($\delta$)", "rad/s", "-", True, True, self.viewTanDelta, 1, ["tan(delta((w))"])
        self.current_view=self.views["log(G',G''(w))"]

        # FILES
        ftype=TXTColumnFile("OSC files", "osc", "Small-angle oscillatory masurements from the Rheometer", ['w','G\'','G\'\''], ['Mw','T'], ['rad/s','Pa','Pa'])
        self.filetypes[ftype.extension] = ftype

        # THEORIES
        self.theories[TheoryWLFShift.thname]=TheoryWLFShift

    def viewLogG1G2(self, dt, file_parameters):
        x = np.zeros((dt.num_rows, 2))
        y = np.zeros((dt.num_rows, 2))
        x[:, 0] = np.log10(dt.data[:, 0])
        x[:, 1] = np.log10(dt.data[:, 0])
        y[: ,0] = np.log10(dt.data[:, 1])
        y[: ,1] = np.log10(dt.data[:, 2])
        return x, y, True

    def viewG1G2(self, dt, file_parameters):
        x = np.zeros((dt.num_rows, 2))
        y = np.zeros((dt.num_rows, 2))
        x[:, 0] = dt.data[:, 0]
        x[:, 1] = dt.data[:, 0]
        y[: ,0] = dt.data[:, 1]
        y[: ,1] = dt.data[:, 2]
        return x, y, True

    def viewEtaStar(self, dt, file_parameters):
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = dt.data[:, 0]
        y[: ,0] = np.sqrt(dt.data[:, 1]**2 + dt.data[:, 2]**2)/dt.data[:, 0]
        return x, y, True        

    def viewDelta(self, dt, file_parameters):
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = dt.data[:, 0]
        y[: ,0] = np.arctan2(dt.data[:, 2], dt.data[:, 1])*180/np.pi
        return x, y, True
    
    def viewTanDelta(self, dt, file_parameters):
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = dt.data[:, 0]
        y[: ,0] = dt.data[:, 2]/dt.data[:, 1]
        return x, y, True

class CLApplicationTTS(BaseApplicationTTS, Application):
    def __init__(self, name="TTS", parent = None):
        super().__init__(name, parent)
        

class GUIApplicationTTS(BaseApplicationTTS, QApplicationWindow):
    def __init__(self, name="TTS", parent = None):
        super().__init__(name, parent)

        self.populate_views() #populate the view ComboBox
        
