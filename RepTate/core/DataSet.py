from Theory import *
from FileType import *
from File import *
#from DataTable import *

class DataSet(object):
    """Abstract class to describe a data set"""

    def __init__(self, name="DataSet", description=""):
        "Constructor"
        self.name=name
        self.description=description
        self.files=[]
        self.current_file=None
        self.num_files=0
        self.theories=[]
        self.current_theory=None
        self.num_theories=0

    def new_file(self, ftype, ax, name=""):
        self.num_files+=1
        if (name==""):
            f = File("DummyFile%02d"%self.num_files, ax)
        else:
            f = File(name, ax)
        self.files.append(f)
        self.current_file=f
        
    def new_theory(self, theory):
        self.num_theories+=1
        self.theories.append(theory)
        self.current_theory=theory

    def sort(self, line, rev=False):
        if line in self.current_file.file_parameters:
            self.files.sort(key = lambda x: float(x.file_parameters[line]), reverse=rev)
        else:
            print("Parameter %s not found in files"%line)