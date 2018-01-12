# RepTate: Rheology of Entangled Polymers: Toolkit for the Analysis of Theory and Experiments
# http://blogs.upm.es/compsoftmatter/software/reptate/
# https://github.com/jorge-ramirez-upm/RepTate
# http://reptate.readthedocs.io
# Jorge Ramirez, jorge.ramirez@upm.es
# Victor Boudara, mmvahb@leeds.ac.uk
# Copyright (2017) Universidad Politécnica de Madrid, University of Leeds
# This software is distributed under the GNU General Public License. 
"""
Define the C-variables and functions from the C-files that are needed in Python
"""
from ctypes import *
import sys

lib_path = 'theories/Schwarzl_lib_%s.so'%(sys.platform)
try:
    schwarzl_lib = CDLL(lib_path)
except:
    print('OS %s not recognized'%(sys.platform))

schwarzl_gt = schwarzl_lib.schwarzl_gt
schwarzl_gt.restype = None

def do_schwarzl_gt(n_data, value_g_of_t, time_g_of_t):

    c_gt = (c_double * n_data)()
    c_time = (c_double * n_data)()
    out_wp = (c_double * n_data)()
    out_Gp = (c_double * n_data)()
    out_wpp = (c_double * n_data)()
    out_Gpp = (c_double * n_data)()

    for i in range(n_data):
        c_gt[i] = c_double(value_g_of_t[i])
        c_time[i] = c_double(time_g_of_t[i])

    omega_Gp_omega_Gpp = (c_double * n_data * n_data)()
    schwarzl_gt(c_int(n_data), c_gt, c_time, out_wp, out_Gp, out_wpp, out_Gpp)
    # print("%9s %9s %9s %9s"%("wp", "G'", "wpp", "G''") )
    # for i in range(n_data):
    #     print("%9.4e %9.4e %9.4e %9.4e"%(out_wp[i], out_Gp[i], out_wpp[i], out_Gpp[i]) )
    return out_wp, out_Gp, out_wpp, out_Gpp

