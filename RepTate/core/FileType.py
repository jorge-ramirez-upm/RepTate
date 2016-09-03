import numpy as np
import logging
#from Table import *
from File import *
from DataTable import *

class TXTColumnFile(object):
	
    """Basic class for text-column based data files
    
    Columns should be separated by espaces or tabs
    
    """    
    def __init__(self, name='TXTColumn', extension='txt', 
                 description='Generic text file with columns', 
                 num_header_lines=0, col_names_line=-1, col_names=[],
                 col_index=[0, 1], basic_file_parameters=[], col_units=[]):
        self.name=name
        self.extension=extension
        self.description=description
        self.num_header_lines=num_header_lines
        self.col_names_line=col_names_line
        self.col_names=col_names
        self.col_index=col_index
        self.basic_file_parameters=basic_file_parameters # Those that will show by default in the dataset
        self.col_units=col_units
        self.logger = logging.getLogger('ReptateLogger')

    def read_file(self, filename, ax):
        file=File(filename, ax)
        f = open(filename, "r")
        line=f.readline()
        items=line.split(';')
        file.file_parameters={}
        # Get Parameters
        for i in range(len(items)):
            par=items[i].split('=')
            if len(par)>1:
                file.file_parameters[par[0]]=par[1]
        #self.logger.debug(file.file_parameters)
    
        # Get Columns
        if (self.col_names_line>0):
            #self.logger.debug(self.col_names_line)
            for i in range(2,self.col_names_line):
                file.header_lines.append(f.readline())
            line=f.readline()
            items=line.split()
            self.col_index=[]
            for col in self.col_names:
                for j in range(len(items)):
                    if (col==items[j]):
                        self.col_index.append(int(j))
                        break
        else:
            for i in range(self.num_header_lines):
               file.header_lines.append(f.readline())
        #self.logger.debug(file.header_lines)
        #self.logger.debug(self.col_index)
        file.data_table.num_columns=len(self.col_index)

        rawdata=[]
        while(True):
            line=f.readline()
            if not line: break 
            items=line.split()
            for j in self.col_index:
                rawdata.append(float(items[j]))
        file.data_table.num_rows=int(len(rawdata)/file.data_table.num_columns)
        file.data_table.data=np.reshape(rawdata,newshape=(file.data_table.num_rows, file.data_table.num_columns))
        #self.logger.debug(file.data_table.data)
        return file

if __name__ == '__main__':
    t = TXTColumnFile()
    # Two ways of defining the contents of the file
    # Form 1
    t.col_names_line=-1
    t.num_header_lines=3
    t.col_index=[0, 1]
    t.col_names=['t','Gt']
    # Form two
    #t.col_names_line=4
    #t.col_names=['t','Gt']
    t.read_file("/Users/Jorge/Downloads/C0024_NVT_450K_1atm.gt")
    
