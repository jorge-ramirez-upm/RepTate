from Theory import *
from FileType import *
from File import *

class DataSet(object):
    """Abstract class to describe a data set"""

    def __init__(self, name="DataSet", description=""):
        "Constructor"
        self.name=name
        self.description=description
        self.files=[]
        self.current_file=None
        self.num_files=0


    def add_empty_file(self, ftype):
        self.num_files+=1
        f = File("DummyFile%d"%self.num_files)
        self.files.append(f)
        self.current_file=f
        
