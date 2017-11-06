import numpy as np

class Table:
    """ Basic class for experimental and theory data storage and handling """
    
    def __init__(self, file_name="", data_file_type=None, num_columns=0 ,num_lines=0):
        self.file_name=file_name
        tmpname = file_name.split('/')
        self.file_name_short=tmpname[len(tmpname)-1]
        self.num_columns=num_columns
        self.num_lines=num_lines
        self.data_file_type=data_file_type
        self.index=0 # Don't know if I need it
        self.file_parameters={}
        self.header_lines=[] # Header lines in file
        self.series=[] # list with all series
        self.data=np.zeros((self.num_columns, self.num_lines)) # actual data
        self.min_of_columns=np.zeros(self.num_columns) # Array with min values per column
        self.max_of_columns=np.zeros(self.num_columns) # Array with max values per column
        self.line_is_active=np.zeros(self.num_lines, dtype=bool) # Points active in plot and/or calculation
    
    