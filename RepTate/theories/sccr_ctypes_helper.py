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

sccr_dy = sccr_lib.sccr_dy
sccr_dy.restype = c_bool

def calculate_sccr_dy(params, EPS):
    """Calculate dynamic tube dilution in frequency domain"""
    G0, a, tau_e, z, w = params
    n = len(w)

    w_arr = (c_double * n)()
    gp_arr = (c_double * n)()
    gpp_arr = (c_double * n)()
    w_arr[:] = w[:]
    gp_arr[:] = np.zeros(n)[:]
    gpp_arr[:] = np.zeros(n)[:]

    success = sccr_dy(
        c_double(G0), c_double(a), c_double(tau_e), c_double(z), c_int(n),
        w_arr, gp_arr, gpp_arr, c_double(EPS))

    # convert ctypes array to numpy
    return (np.asarray(gp_arr[:]), np.asarray(gpp_arr[:]), success)
