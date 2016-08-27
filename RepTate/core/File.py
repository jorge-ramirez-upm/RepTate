from FileType import *

class File(object):
    """Basic class for text-column based data files"""

    def __init__(self, file_name="", ):
        self.file_name = file_name
        tmpname = file_name.split('/')
        self.file_name_short=tmpname[len(tmpname)-1]
        self.file_type = None # Not sure if this is necessary


