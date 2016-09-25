import numpy as np
from scipy import interp
from Theory import *

class TheoryLikhtmanMcLeish2002(Theory, CmdBase):
    """Fit Likhtman-McLeish theory for linear rheology of linear entangled polymers"""
    thname="Likhtman-McLeish"
    description="Fit Likhtman-McLeish theory for linear rheology of linear entangled polymers"
    cite="Likhtman A.E. and McLeish T.C.B.\n\
Quantitative Theory for Linear Dynamics of Linear Entangled Polymers\n\
Macromolecules 2002, 35, 6332-6343"
    
    def __init__(self, name="ThLikhtmanMcLeish2002", parent_dataset=None, ax=None):
        super(TheoryLikhtmanMcLeish2002, self).__init__(name, parent_dataset, ax)
        self.function = self.LikhtmanMcLeish2002
        self.parameters["taue"]=Parameter("taue", 2e-6, "Rouse time of one Entanglement", ParameterType.real, True)
        self.parameters["Ge"]=Parameter("Ge", 1e6, "Entanglement moduluas", ParameterType.real, True)
        self.parameters["Me"]=Parameter("Me", 5, "Entanglement molecular weight", ParameterType.real, True)
        self.parameters["cnu"]=Parameter("cnu", 0.1, "Constraint Release parameter", ParameterType.real, False)

        f=np.load("theories\linlin.npz")
        self.Zarray=f['Z']
        self.cnuarray=f['cnu']
        self.data=f['data']
        
    def LikhtmanMcLeish2002(self, f=None):
        ft=f.data_table
        tt=self.tables[f.file_name_short]
        tt.num_columns=ft.num_columns
        tt.num_rows=ft.num_rows
        tt.data=np.zeros((tt.num_rows, tt.num_columns))
        tt.data[:,0]=ft.data[:,0] 

        taue=self.parameters["taue"].value
        Ge=self.parameters["Ge"].value
        Me=self.parameters["Me"].value
        cnu=self.parameters["cnu"].value
        Mw=float(f.file_parameters["Mw"])
        
        Z=np.round(Mw/Me) # For the time being, we don't interpolate
        
        indZ = (np.where(self.Zarray==Z))[0][0]
        indcnu = (np.where(self.cnuarray==cnu))[0][0]

        table=self.data[indZ]
        ind1=1+indcnu*2
        ind2=ind1+1

        tt.data[:,1]=interp(tt.data[:,0], table[:,0]/taue, Ge*table[:,ind1])
        tt.data[:,2]=interp(tt.data[:,0], table[:,0]/taue, Ge*table[:,ind2])
                       
