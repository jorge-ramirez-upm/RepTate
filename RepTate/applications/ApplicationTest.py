from Application import *
from TheoryTest import *
from DataTable import *

class ApplicationTest(Application):
    """Application to play with the different functionalities of Reptate"""
    name="Test"
    description="Playground Application"

    def __init__(self, name="Test", parent = None):
        super(ApplicationTest, self).__init__(name, parent)

        # VIEWS
        self.views.append(View("TestView1", "y vs x", "t", "r", False, False, self.view1, 1, ["lolo"]))
        self.views.append(View("TestView2", "y^2 vs x", "t", "r2", False, False, self.view2, 1, ["lolo2"]))
        self.current_view=self.views[0]

        # FILES
        ftype=TXTColumnFile("Test files", "test", "Test files x y", 0, -1, ['x','y'], [0, 1], ['testparam1','testparam2'], [])
        self.filetypes[ftype.extension]=ftype
        #self.logger.debug(self.filetypes)

        # THEORIES
        self.theories[TheoryTest.thname]=TheoryTest
        self.theories[TheoryTest2.thname]=TheoryTest2

    def view1(self, dt, file_parameters):
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = dt.data[:, 0]
        y[:, 0] = dt.data[:, 1]
        return x, y, True

    def view2(self, dt, file_parameters):
        x = np.zeros((dt.num_rows, 1))
        y = np.zeros((dt.num_rows, 1))
        x[:, 0] = dt.data[:, 0]
        y[:, 0] = dt.data[:, 1]**2
        return x, y, True
    