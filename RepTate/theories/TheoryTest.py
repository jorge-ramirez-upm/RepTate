from Theory import *
import numpy as np

class TheoryTest(Theory, CmdBase):
    """Theory to play with the different functionalities of Reptate"""
    thname="ThTest"
    description="Playground theory"

    def __init__(self, name="ThTest", parent_dataset=None, ax=None):
        super(TheoryTest, self).__init__(name, parent_dataset, ax)
        self.function = self.testfunction
        self.parameters["A"]=1.0
        self.parameters["B"]=2.0

    def testfunction(self, f=None):
        ft=f.data_table
        tt=self.tables[f.file_name_short]
        tt.num_columns=ft.num_columns
        tt.num_rows=ft.num_rows
        tt.data=np.zeros((tt.num_rows, tt.num_columns))
        tt.data[:,0]=ft.data[:,0]
        tt.data[:,1]=self.parameters["A"]*tt.data[:,0]+self.parameters["B"]

class TheoryTest2(Theory):
    """Theory to play with the different functionalities of Reptate"""
    thname="ThTest2"
    description="Playground theory 2"

    def __init__(self, name="ThTest2"):
        super(TheoryTest2, self).__init__(name)
    
        
