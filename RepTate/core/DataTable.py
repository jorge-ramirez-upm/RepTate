import numpy as np

class DataTable(object):
    """Class that stores data and series"""
    MAX_NUM_SERIES=3

    def __init__(self, ):
        """Constructor:

        Args:
            num_columns     (int): Number of columns in table
            num_rows        (int): Number of rows in table
            column_names   (list): Names of columns
            column_units   (list): ??? To be defined
            data       (np.array): Actual data
        """
        self.num_columns=0
        self.num_rows=0
        self.column_names=[]
        self.column_units=[]
        self.data=np.zeros((num_rows,num_columns))
