from Application import *
from ApplicationWindow import *
import numpy as np
from TheoryMaxwellModes import TheoryMaxwellModesFrequency
from TheoryLikhtmanMcLeish2002 import TheoryLikhtmanMcLeish2002
from TheoryTTS import TheoryWLFShift

class ApplicationLVE(Application, ApplicationWindow):
    """
    Application to Analyze Linear Viscoelastic Data
    
    .. todo:: DO WE NEED A SEPARATE APPLICATION FROM TTS???
    """
    name="LVE"
    description="Linear Viscoelasticity"
    
    def __init__(self, name="LVE", parent = None):
        print("ApplicationLVE.__init__(self) called")
        super(ApplicationLVE, self).__init__(name, parent)
        #problem with cmd.Cmd not using super(): no call to ApplicationWindow.__init__
        if CmdBase.mode==CmdMode.GUI: #if GUI mode
            ApplicationWindow.__init__(self, name, self)
        print("ApplicationLVE.__init__(self) ended")
        
        # VIEWS
        self.views["Log(G',G''(w))"]=View("Log(G',G''(w))", "Log Storage,Loss moduli", "Log($\omega$)", "Log(G'($\omega$),G''($\omega$))", True, True, self.viewLogG1G2, 2, ["G'(w)","G''(w)"])
        self.views["G',G''(w)"]=View("G',G''(w)", "Storage,Loss moduli", "$\omega$", "G'($\omega$),G''($\omega$)", True, True, self.viewG1G2, 2, ["G'(w)","G''(w)"])
        self.views["etastar"]=View("etastar", "Complex Viscosity", "$\omega$", "$\eta^*(\omega)$", True, True, self.viewEtaStar, 1, ["eta*(w)"])
        self.views["delta"]=View("delta", "delta", "$\omega$", "$\delta(\omega)$", True, False, self.viewDelta, 1, ["delta(w)"])
        self.views["tan(delta)"]=View("tan(delta)", "tan(delta)", "$\omega$", "tan($\delta$)", True, True, self.viewTanDelta, 1, ["tan(delta((w))"])
        self.current_view=self.views["Log(G',G''(w))"]
        if CmdBase.mode==CmdMode.GUI: #if GUI mode
            self.populateViews()

        # FILES
        ftype=TXTColumnFile("LVE files", "tts", "LVE files", ['w','G\'','G\'\''], ['Mw','T'], ['rad/s','Pa','Pa'])
        self.filetypes[ftype.extension]=ftype
        ftype=TXTColumnFile("OSC files", "osc", "Small-angle oscillatory masurements from the Rheometer", ['w','G\'','G\'\''], ['Mw','T'], ['rad/s','Pa','Pa'])
        self.filetypes[ftype.extension]=ftype

        # THEORIES
        self.theories[TheoryMaxwellModesFrequency.thname]=TheoryMaxwellModesFrequency
        self.theories[TheoryLikhtmanMcLeish2002.thname]=TheoryLikhtmanMcLeish2002
        self.theories[TheoryWLFShift.thname]=TheoryWLFShift
        #self.theories[TheoryRouseFrequency.thname]=TheoryRouseFrequency

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
        y[: ,0] = np.log10(dt.data[:, 2]/dt.data[:, 1])
        return x, y, True