from Theory import *

class TheoryTest(Theory):
    """Theory to play with the different functionalities of Reptate"""
    name="Test"
    description="Playground Theory"

    def __init__(self, parent = None):
        super(TheoryTest, self).__init__("Test", "Simple test", TheoryType.point)
    
        

