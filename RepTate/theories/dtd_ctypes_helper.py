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
    lib_path = dir_path + os.sep + 'dtd_lib_%s.so' % (sys.platform)
else:
    # 32-bit system
    lib_path = dir_path + os.sep + 'dtd_lib_%s_i686.so' % (sys.platform)
try:
    dtd_lib = CDLL(lib_path)
except:
    print('OS %s not recognized in DTD CH' % (sys.platform))

dynamic_tube_dilution_freq = dtd_lib.dynamic_tube_dilution_freq
dynamic_tube_dilution_freq.restype = c_bool

dynamic_tube_dilution_time = dtd_lib.dynamic_tube_dilution_time
dynamic_tube_dilution_time.restype = c_bool


def calculate_dtd_freq(params, EPS):
    """Calculate dynamic tube dilution in frequency domain"""
    G0, a, tau_e, z, w = params
    n = len(w)

    w_arr = (c_double * n)()
    gp_arr = (c_double * n)()
    gpp_arr = (c_double * n)()
    w_arr[:] = w[:]
    gp_arr[:] = np.zeros(n)[:]
    gpp_arr[:] = np.zeros(n)[:]

    success = dynamic_tube_dilution_freq(
        c_double(G0), c_double(a), c_double(tau_e), c_double(z), c_int(n),
        w_arr, gp_arr, gpp_arr, c_double(EPS))

    # convert ctypes array to numpy
    return (np.asarray(gp_arr[:]), np.asarray(gpp_arr[:]), success)


def calculate_dtd_time(params, EPS):
    """Calculate dynamic tube dilution in time domain"""
    G0, a, tau_e, z, t = params
    n = len(t)

    t_arr = (c_double * n)()
    gt_arr = (c_double * n)()
    t_arr[:] = t[:]
    gt_arr[:] = np.zeros(n)[:]

    success = dynamic_tube_dilution_time(
        c_double(G0), c_double(a), c_double(tau_e), c_double(z), c_int(n),
        t_arr, gt_arr, c_double(EPS))

    # convert ctypes array to numpy
    return (np.asarray(gt_arr[:]), success)
