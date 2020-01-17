# RepTate: Rheology of Entangled Polymers: Toolkit for the Analysis of Theory and Experiments
# --------------------------------------------------------------------------------------------------------
#
# Authors:
#     Jorge Ramirez, jorge.ramirez@upm.es
#     Victor Boudara, victor.boudara@gmail.com
#
# Useful links:
#     http://blogs.upm.es/compsoftmatter/software/reptate/
#     https://github.com/jorge-ramirez-upm/RepTate
#     http://reptate.readthedocs.io
#
# --------------------------------------------------------------------------------------------------------
#
# Copyright (2017-2020): Jorge Ramirez, Victor Boudara, Universidad Politécnica de Madrid, University of Leeds
#
# This file is part of RepTate.
#
# RepTate is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# RepTate is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with RepTate.  If not, see <http://www.gnu.org/licenses/>.
#
# --------------------------------------------------------------------------------------------------------
"""
Define the C-variables and functions from the C-files that are needed in Python
"""
from ctypes import *
import sys
import os

dir_path = os.path.dirname(
    os.path.realpath(__file__))  # get the directory path of current file
if sys.maxsize > 2**32:
    # 64-bit system
    lib_path = dir_path + os.sep + 'schwarzl_lib_%s.so' % (sys.platform)
else:
    # 32-bit system
    lib_path = dir_path + os.sep + 'schwarzl_lib_%s_i686.so' % (sys.platform)
try:
    schwarzl_lib = CDLL(lib_path)
except:
    print('OS %s not recognized in Schwarzl CH module' % (sys.platform))

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

    schwarzl_gt(c_int(n_data), c_gt, c_time, out_wp, out_Gp, out_wpp, out_Gpp)

    return out_wp, out_Gp, out_wpp, out_Gpp
