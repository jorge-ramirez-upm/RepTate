"""
Define the C-variables and functions from the C-files that are needed in Python
"""
import numpy as np
from ctypes import c_double, c_int, c_bool, CDLL
import sys
import os

dir_path = os.path.dirname(
    os.path.realpath(__file__))  # get the directory path of current file
if sys.maxsize > 2**32:
    # 64-bit system
    lib_path = dir_path + os.sep + 'kww_lib_%s.so' % (sys.platform)
else:
    # 32-bit system
    lib_path = dir_path + os.sep + 'kww_lib_%s_i686.so' % (sys.platform)
try:
    kww_lib = CDLL(lib_path)
except:
    print('OS %s not recognized in DTD CH' % (sys.platform))

kwwc = kww_lib.kwwc
kwwc.argtypes = [c_double, c_double]
kwwc.restype = c_double
kwws = kww_lib.kwws
kwws.argtypes = [c_double, c_double]
kwws.restype = c_double
    