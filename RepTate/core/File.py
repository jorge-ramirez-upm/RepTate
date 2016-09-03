import os
from FileType import *
from DataTable import *

class File(object):
    """Basic class that describes elements of a DataSet"""

    def __init__(self, file_name="", ax=None):
        """ Constructor:
            file_name: Full path
            file_name_short: Just the file name
            header_lines: 
        """
        self.file_full_path = os.path.abspath(file_name)
        tmpname = file_name.split(os.sep)
        tmpname = tmpname[len(tmpname)-1]
        lst = tmpname.split('.')
        short = '.'.join(lst[:-1])      
        self.file_name_short=short
        #self.file_type = TXTColumnFile #None # Not sure if this is necessary
        self.header_lines=[]
        self.file_parameters={}
        self.active = True
        self.data_table = DataTable(ax)
        
    def __repr__(self):
        return '%s: %s' % (self.file_full_path, self.file_parameters)