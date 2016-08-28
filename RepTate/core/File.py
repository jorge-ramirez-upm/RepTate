from FileType import *

class File(object):
    """Basic class that describes elements of a DataSet"""

    def __init__(self, file_name="", ):
        """ Constructor:
            file_name: Full path
            file_name_short: Just the file name
            header_lines: 
        """
        self.file_name = file_name
        tmpname = file_name.split('/')
        self.file_name_short=tmpname[len(tmpname)-1]
        self.file_type = TXTColumnFile #None # Not sure if this is necessary
        self.header_lines=[]
        self.file_parameters={}
        self.active = True
        


