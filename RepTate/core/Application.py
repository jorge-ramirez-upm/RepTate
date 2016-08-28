import logging
from FileType import *
from View import *
from Theory import *
from DataSet import *

class Application(object):
    """Main abstract class that represents an application"""    
    name="Template"
    description="Abstract class that defines basic functionality"

    def __init__(self,):
        """Constructor of Application"""
        self.logger = logging.getLogger('ReptateLogger')
        self.views=[]
        self.filetypes={}
        self.theories=[]
        self.datasets=[]
        self.current_view=0
        self.current_theory=0
        self.current_dataset=0
        self.num_datasets=0

    def add_empty_dataset(self, name="DataSet", description=""):
        """Creates an empty dataset and adds it to the current application"""
        ds = DataSet(name, description)
        self.datasets.append(ds)
        self.current_dataset=ds
        self.num_datasets+=1
