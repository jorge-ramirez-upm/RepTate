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
    lib_path = dir_path + os.sep + 'sccr_lib_%s.so' % (sys.platform)
else:
    # 32-bit system
    lib_path = dir_path + os.sep + 'sccr_lib_%s_i686.so' % (sys.platform)
try:
    sccr_lib = CDLL(lib_path)
except:
    print('OS %s not recognized in SCCR CH' % (sys.platform))

set_static_int = sccr_lib.set_static_int
set_static_int.restype = None

set_static_double = sccr_lib.set_static_double
set_static_double.restype = None

set_yeq_static_in_C = sccr_lib.set_yeq_static_in_C
set_yeq_static_in_C.restype = None

sccr_dy = sccr_lib.sccr_dy
sccr_dy.restype = None

def set_yeq_static(yeq):
    n = len(yeq)
    arr = (c_double * n)(*yeq[:])
    set_yeq_static_in_C(arr, c_int(n))
