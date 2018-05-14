"""
Define the C-variables and functions from the C-files that are needed in Python
"""
import numpy as np
from ctypes import c_double, c_int, CDLL
import sys
import os

dir_path = os.path.dirname(
    os.path.realpath(__file__))  # get the directory path of current file
if sys.maxsize > 2**32:
    # 64-bit system
    lib_path = dir_path + os.sep + 'rouse_lib_%s.so' % (sys.platform)
else:
    # 32-bit system    
    lib_path = dir_path + os.sep + 'rouse_lib_%s_i686.so' % (sys.platform)
try:
    rouse_lib = CDLL(lib_path)
except:
    print('OS %s not recognized in Rouse CH module' % (sys.platform))

continuous_rouse_freq_interp = rouse_lib.continuous_rouse_freq_interp
continuous_rouse_freq_interp.restype = None

continuous_rouse_time_interp = rouse_lib.continuous_rouse_time_interp
continuous_rouse_time_interp.restype = None


def approx_rouse_frequency(params):
    """Continuous Rouse frequency with interpolation for N"""
    G0, tau0, N, w = params
    n = len(w)

    w_arr = (c_double * n)()
    gp_arr = (c_double * n)()
    gpp_arr = (c_double * n)()
    w_arr[:] = w[:]
    gp_arr[:] = np.zeros(n)[:]
    gpp_arr[:] = np.zeros(n)[:]

    continuous_rouse_freq_interp(
        c_int(n), c_double(G0), c_double(tau0), c_double(N), w_arr, gp_arr,
        gpp_arr)

    # convert ctypes array to numpy
    return (np.asarray(gp_arr[:]), np.asarray(gpp_arr[:]))


def approx_rouse_time(params):
    """Continuous Rouse time with interpolation for N"""
    G0, tau0, N, t = params
    n = len(t)

    t_arr = (c_double * n)()
    gt_arr = (c_double * n)()
    t_arr[:] = t[:]
    gt_arr[:] = np.zeros(n)[:]

    continuous_rouse_time_interp(
        c_int(n), c_double(G0), c_double(tau0), c_double(N), t_arr, gt_arr)
    
    # convert ctypes array to numpy
    return (np.asarray(gt_arr[:]))
