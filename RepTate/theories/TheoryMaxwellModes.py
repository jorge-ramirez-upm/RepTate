from Theory import *
from QTheory import *
from PyQt5.QtWidgets import QWidget, QToolBar, QComboBox, QSpinBox

class TheoryMaxwellModesFrequency(CmdBase):
    """Fit Maxwell modes to a frequency dependent relaxation function"""
    thname="MaxwellModesFrequency"
    description="Fit Maxwell modes to frequency dependent function"
    single_file = True 

    def __new__(cls, name="ThMaxwellFrequency", parent_dataset=None, ax=None):
        return GUITheoryMaxwellModesFrequency(name, parent_dataset, ax) if (CmdBase.mode==CmdMode.GUI) else CLTheoryMaxwellModesFrequency(name, parent_dataset, ax)
 
class BaseTheoryMaxwellModesFrequency:
    def __init__(self, name="ThMaxwellFrequency", parent_dataset=None, ax=None):
        super().__init__(name, parent_dataset, ax)
        print("BaseTheoryMaxwellModesFrequency ended")
        self.function = self.MaxwellModesFrequency
        self.has_modes = True
        self.parameters["logwmin"]=Parameter("logwmin", -5, "Log of frequency range minimum", ParameterType.real, True)
        self.parameters["logwmax"]=Parameter("logwmax", 4, "Log of frequency range maximum", ParameterType.real, True)
        self.parameters["nmodes"]=Parameter("nmodes", 5, "Number of Maxwell modes", ParameterType.integer, False)
        for i in range(self.parameters["nmodes"].value):
            self.parameters["logG%02d"%i]=Parameter("logG%02d"%i,5.0,"Log of Mode %d amplitude"%i, ParameterType.real, True)

    def set_param_value(self, name, value):
        if (name=="nmodes"):
            oldn=self.parameters["nmodes"].value
        super(BaseTheoryMaxwellModesFrequency, self).set_param_value(name, value) #what does that do?
        if (name=="nmodes"):
            for i in range(self.parameters["nmodes"].value):
                self.parameters["logG%02d"%i]=Parameter("logG%02d"%i,5.0,"Log of Mode %d amplitude"%i, ParameterType.real, True)
            if (oldn>self.parameters["nmodes"].value):
                for i in range(self.parameters["nmodes"].value,oldn):
                    del self.parameters["logG%02d"%i]

    def get_modes(self):
        nmodes=self.parameters["nmodes"].value
        freq=np.logspace(self.parameters["logwmin"].value, self.parameters["logwmax"].value, nmodes)
        tau=1.0/freq
        G=np.zeros(nmodes)
        for i in range(nmodes):
            G[i]=np.power(10, self.parameters["logG02%d"%i].value)
        return tau, G

    def set_modes(self, tau, G):
        print("set_modes not allowed in this theory (%s)"%self.name)

    def MaxwellModesFrequency(self, f=None):
        ft=f.data_table
        tt=self.tables[f.file_name_short]
        tt.num_columns=ft.num_columns
        tt.num_rows=ft.num_rows
        tt.data=np.zeros((tt.num_rows, tt.num_columns))
        tt.data[:,0]=ft.data[:,0]

        nmodes=self.parameters["nmodes"].value
        freq=np.logspace(self.parameters["logwmin"].value, self.parameters["logwmax"].value, nmodes)
        tau=1.0/freq

        for i in range(nmodes):
            wT=tt.data[:,0]*tau[i]
            wTsq=wT**2
            G=np.power(10, self.parameters["logG%02d"%i].value)
            tt.data[:,1]+=G*wTsq/(1+wTsq)
            tt.data[:,2]+=G*wT/(1+wTsq)

class CLTheoryMaxwellModesFrequency(BaseTheoryMaxwellModesFrequency, Theory):
    def __init__(self, name="ThMaxwellFrequency", parent_dataset=None, ax=None):
        super().__init__(name, parent_dataset, ax)
        
class GUITheoryMaxwellModesFrequency(BaseTheoryMaxwellModesFrequency, QTheory):
    def __init__(self, name="ThMaxwellFrequency", parent_dataset=None, ax=None):
        super().__init__(name, parent_dataset, ax)
        print("GUITheoryMaxwellModesFrequency")
        
        # add widgets specific to the theory
        tb = QToolBar()
        tb.setIconSize(QSize(24,24))
        self.spinbox = QSpinBox()
        self.spinbox.setRange(1, 20) # min and max number of modes
        self.spinbox.setSuffix(" modes")
        self.spinbox.setValue(self.parameters["nmodes"].value) #initial value
        tb.addWidget(self.spinbox)
        self.thToolsLayout.insertWidget(0, tb)
        connection_id = self.spinbox.valueChanged.connect(self.handle_spinboxValueChanged)

    # def nmode_non_editable(self):
    #     item = self.thParamTable.findItems("nmodes", Qt.MatchCaseSensitive, column=0)
    #     item.setDisabled(True)

    def handle_spinboxValueChanged(self, value):
        """Handle a change of the parameter 'nmode'"""
        self.set_param_value("nmodes", value)


########################################
########################################

class TheoryMaxwellModesTime(CmdBase):
    """Fit Maxwell modes to a time depenendent relaxation function"""
    thname="MaxwellModesTime"
    description="Fit Maxwell modes to time dependent function"
    citations=""
    def __new__(cls, name="ThMaxwellTime", parent_dataset=None, ax=None):
        return GUITheoryMaxwellModesTime(name, parent_dataset, ax) if (CmdBase.mode==CmdMode.GUI) else CLTheoryMaxwellModesTime(name, parent_dataset, ax)
      
class BaseTheoryMaxwellModesTime(CmdBase):
    def __init__(self, name="ThMaxwellTime", parent_dataset=None, ax=None):
        super().__init__(name, parent_dataset, ax)
        self.function = self.MaxwellModesTime

    def MaxwellModesTime(self, f=None):
        pass   

class CLTheoryMaxwellModesTime(BaseTheoryMaxwellModesTime, Theory):
    def __init__(self, name="ThMaxwellTime", parent_dataset=None, ax=None):
        super().__init__(name, parent_dataset, ax)
        
class GUITheoryMaxwellModesTime(BaseTheoryMaxwellModesTime, QTheory):
    def __init__(self, name="ThMaxwellTime", parent_dataset=None, ax=None):
        super().__init__(name, parent_dataset, ax)

