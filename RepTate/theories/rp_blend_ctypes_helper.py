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
    lib_path = dir_path + os.sep + 'rp_blend_lib_%s.so' % (sys.platform)
else:
    # 32-bit system
    lib_path = dir_path + os.sep + 'rp_blend_lib_%s_i686.so' % (sys.platform)
try:
    rp_blend_lib = CDLL(lib_path)
except:
    print('OS %s not recognized in Rouse CH module' % (sys.platform))

derivs_rp_blend_shear = rp_blend_lib.derivs_rp_blend_shear
derivs_rp_blend_shear.restype = None

derivs_rp_blend_uext = rp_blend_lib.derivs_rp_blend_uext
derivs_rp_blend_uext.restype = None


def compute_derivs_shear(sigma, p, t, with_fene):
    """Derivatives at time t"""
    c = 3
    n, lmax, phi, taud, taus, beta, delta, gamma_dot, _ = p
    # void derivs_rp_blend_shear(double *deriv, double *sigma, double *phi, double *taus, double *taud, double *p, double t)
    # n = p[0];
    # lmax = p[1];
    # beta = p[2];
    # delta = p[3];
    # gamma_dot = p[4];
    # with_fene = p[5];

    p_arr = (c_double * 6)()
    p_arr[:] = [n, lmax, beta, delta, gamma_dot, with_fene]
    deriv_arr = (c_double * (c * n * n))(*np.zeros(c * n * n))
    sigma_arr = (c_double * (c * n * n))(*sigma[:])
    phi_arr = (c_double * n)(*phi[:])
    taud_arr = (c_double * n)(*np.array(taud)/2.0) # hard coded factor 2 in C routine
    taus_arr = (c_double * n)(*taus[:])

    derivs_rp_blend_shear(deriv_arr, sigma_arr, phi_arr, taus_arr, taud_arr,
                          p_arr, c_double(t))

    # return results as numpy array
    return deriv_arr[:]


def compute_derivs_uext(sigma, p, t, with_fene):
    """Derivatives at time t"""
    c = 2
    n, lmax, phi, taud, taus, beta, delta, gamma_dot, _ = p
    # void derivs_rp_blend_shear(double *deriv, double *sigma, double *phi, double *taus, double *taud, double *p, double t)
    # n = p[0];
    # lmax = p[1];
    # beta = p[2];
    # delta = p[3];
    # gamma_dot = p[4];
    # with_fene = p[5];

    p_arr = (c_double * 6)()
    p_arr[:] = [n, lmax, beta, delta, gamma_dot, with_fene]

    deriv_arr = (c_double * (c * n * n))(*np.zeros(c * n * n))
    sigma_arr = (c_double * (c * n * n))(*sigma[:])
    phi_arr = (c_double * n)(*phi[:])
    taud_arr = (c_double * n)(*np.array(taud)/2.0) # hard coded factor 2 in C routine
    taus_arr = (c_double * n)(*taus[:])

    derivs_rp_blend_uext(deriv_arr, sigma_arr, phi_arr, taus_arr, taud_arr,
                          p_arr, c_double(t))

    # return results as numpy array
    return deriv_arr[:]
