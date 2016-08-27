from Theory import *

class DataSet(object):
    """Abstract class to describe a data set"""

    def __init__(self, name="", description="", type=TheoryType.point):
        "Constructor"
        files=[]
        
        
