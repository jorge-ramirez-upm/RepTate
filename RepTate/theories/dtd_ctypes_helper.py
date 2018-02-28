"""
Define the C-variables and functions from the C-files that are needed in Python
"""
import numpy as np
from ctypes import c_double, c_int, c_bool, CDLL
import sys

lib_path = 'theories/dtd_lib_%s.so' % (sys.platform)
try:
    dtd_lib = CDLL(lib_path)
except:
    print('OS %s not recognized' % (sys.platform))

dynamic_tube_dilution = dtd_lib.dynamic_tube_dilution
dynamic_tube_dilution.restype = c_bool


def calculate_dtd(params):
    """Calculate dynamic tube dilution"""
    G0, a, tau_e, z, w = params
    n = len(w)

    w_arr = (c_double * n)()
    gp_arr = (c_double * n)()
    gpp_arr = (c_double * n)()
    w_arr[:] = w[:]
    gp_arr[:] = np.zeros(n)[:]
    gpp_arr[:] = np.zeros(n)[:]

    success = dynamic_tube_dilution(
        c_double(G0), c_double(a), c_double(tau_e), c_double(z), c_int(n),
        w_arr, gp_arr, gpp_arr)

    # convert ctypes array to numpy
    return (np.asarray(gp_arr[:]), np.asarray(gpp_arr[:]), success)
