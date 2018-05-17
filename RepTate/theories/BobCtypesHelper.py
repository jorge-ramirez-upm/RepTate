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
# Copyright (2017): Jorge Ramirez, Victor Boudara, Universidad Politécnica de Madrid, University of Leeds
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
from ctypes import CFUNCTYPE, CDLL, c_double, c_int, c_char_p, byref, c_bool
import sys
import os


class BobError(Exception):
    """Class for BoB exceptions"""
    pass


class BobCtypesHelper:
    """Wrapper class to call BoB C++ functions"""

    CB_FTYPE = CFUNCTYPE(None,
                         c_char_p)  # callback [return type, [args types]]

    def __init__(self, parent_theory):

        self.parent_theory = parent_theory
        # get the directory path of current file
        dir_path = os.path.dirname(os.path.realpath(__file__))
        # load the sharedlibrary
        if sys.maxsize > 2**32:
            # 64-bit system
            self.lib_path = dir_path + os.sep + 'bob2p5_lib_%s.so' % (
                sys.platform)
        else:
            # 32-bit system
            self.lib_path = dir_path + os.sep + 'bob2p5_lib_%s_i686.so' % (
                sys.platform)
        try:
            self.bob_lib = CDLL(self.lib_path)
        except:
            print('OS %s not recognized in BoB CH module' % (sys.platform))
        # link the C function to Python
        self.link_c_functions()

    def print_from_c(self, char):
        """Function called by BoB from the C++ code. 
        Called when error occured during BoB execution
        """
        err_msg = '\nERROR encountered in BoB:\n%s\n---------------' % (
            char.decode())
        self.parent_theory.Qprint(err_msg)

    def link_c_functions(self):
        """Declare the Python functions equivalents to the C functions"""
        self.bob_save_polyconf_and_return_gpc = self.bob_lib.reptate_save_polyconf_and_return_gpc
        self.bob_save_polyconf_and_return_gpc.restype = c_bool

        self.run_bob_lve = self.bob_lib.run_bob_lve
        self.run_bob_lve.restype = c_bool

        self.get_bob_lve = self.bob_lib.get_bob_lve
        self.get_bob_lve.restype = c_bool

        # callback C function from Python function
        self.cbfunc = self.CB_FTYPE(self.print_from_c)
        self.bob_lib.def_pycallback_func(self.cbfunc)

    def save_polyconf_and_return_gpc(self, arg_list, npol_tot):
        """Run BoB asking for a polyconf file only (no relaxation etc) and
        output the characteristics of the polymer configuration"""
        # prepare the arguments for bob_main function
        n_arg = len(arg_list)
        argv = (c_char_p * n_arg)()
        for i in range(n_arg):
            argv[i] = arg_list[i].encode('utf-8')

        # prepare the arguments for GPC
        nbin = self.parent_theory.parameters[
            "nbin"].value  # set the number of bins from param
        ncomp = c_int(-1)  # -1: all components
        ni = c_int(0)
        nf = c_int(npol_tot)  # all polymers
        lgmid_arr = (c_double * nbin)()
        wtbin_arr = (c_double * nbin)()
        brbin_arr = (c_double * nbin)()
        gbin_arr = (c_double * nbin)()
        mn = c_double()
        mw = c_double()

        #call C function, return False if error in BoB
        if self.bob_save_polyconf_and_return_gpc(
                c_int(n_arg), argv, c_int(nbin), ncomp, ni, nf, byref(mn),
                byref(mw), lgmid_arr, wtbin_arr, brbin_arr, gbin_arr):

            # return results
            arrs = [lgmid_arr[:], wtbin_arr[:], brbin_arr[:], gbin_arr[:]]
            return [mn.value, mw.value, arrs]

        # BoB encountered error
        raise BobError

    def return_bob_lve(self, arg_list):
        """Run BoB LVE and copy results to arrays"""
        # prepare the arguments for bob_main function
        n_arg = len(arg_list)
        argv = (c_char_p * n_arg)()
        for i in range(n_arg):
            argv[i] = arg_list[i].encode('utf-8')

        # run bob LVE and get size of results
        # call C function, return False if error in BoB
        out_size = c_int()
        if self.run_bob_lve(c_int(n_arg), argv, byref(out_size)):
            #allocate Python memory for results and copy bob results
            omega = (c_double * out_size.value)()
            g_p = (c_double * out_size.value)()
            g_pp = (c_double * out_size.value)()

            if self.get_bob_lve(omega, g_p, g_pp):
                return [omega[:], g_p[:], g_pp[:]]

        # BoB encountered error
        raise BobError