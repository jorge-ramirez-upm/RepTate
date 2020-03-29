"""
Define the C-variables and functions from the C-files that are needed in Python
"""

from ctypes import c_double, c_int, c_bool, CDLL
import sys
import os

dir_path = os.path.dirname(
    os.path.realpath(__file__))  # get the directory path of current file
if sys.maxsize > 2**32:
    # 64-bit system
    lib_path = dir_path + os.sep + 'landscape_%s.so' % (sys.platform)
else:
    # 32-bit system
    lib_path = dir_path + os.sep + 'landscape_%s_i686.so' % (sys.platform)

try:
    landscape_function_lib = CDLL(lib_path)
except:
    print('OS %s not recognized' % (sys.platform))

python_c_landscape = landscape_function_lib.landscape
python_c_landscape.restype = c_double

def GO_Landscape( NT, epsilon, mu):
        """Wrapper functions to call c code to compute quiescent landscape"""
        c_doub_NT = (c_double )(NT)
        c_doub_mu = (c_double )(mu)
        c_doub_epsilon = (c_double )(epsilon)
        return python_c_landscape( c_doub_NT, c_doub_mu, c_doub_epsilon)
