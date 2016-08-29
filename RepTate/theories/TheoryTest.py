from Theory import *

class TheoryTest(Theory):
    """Theory to play with the different functionalities of Reptate"""
    thname="ThTest1"
    description="Playground theory 1"

    def __init__(self, name="ThTest1"):
        super(TheoryTest, self).__init__(name, TheoryType.point)
    
class TheoryTest2(Theory):
    """Theory to play with the different functionalities of Reptate"""
    thname="ThTest2"
    description="Playground theory 2"

    def __init__(self, name="ThTest2"):
        super(TheoryTest2, self).__init__(name, TheoryType.point)
    
        
