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
from ctypes import CDLL, c_double, c_int, c_char_p, byref
import sys
import os


class BobCtypesHelper:
    """Wrapper class to call BoB C++ functions"""

    def __init__(self, parent_theory):

        self.parent_theory = parent_theory
        # get the directory path of current file
        dir_path = os.path.dirname(os.path.realpath(__file__))
        # load the sharedlibrary
        self.lib_path = dir_path + os.sep + 'bob2p5_lib_%s.so' % (sys.platform)
        try:
            self.bob_lib = CDLL(self.lib_path)
        except:
            print('OS %s not recognized in BoB CH module' % (sys.platform))
        # link the C function to Python
        self.link_c_functions()

    def link_c_functions(self):
        """Declare the Python functions equivalents to the C functions"""
        self.reptate_save_polyconf_and_return_gpc = self.bob_lib.reptate_save_polyconf_and_return_gpc
        self.reptate_save_polyconf_and_return_gpc.restype = None

        self.set_GPCNumBin = self.bob_lib.set_GPCNumBin
        self.set_GPCNumBin.restype = None

        self.get_mn_mw = self.bob_lib.get_mn_mw
        self.get_mn_mw.restype = None

    def free_lib(self):
        """Unload the library. This is equivalent to closing BoB"""
        import _ctypes
        _ctypes.dlclose(self.bob_lib._handle)

    def reload_lib(self):
        """Unload and load the shared library. 
        "Reset" all the library variables Equivalent to a fresh start
        """
        self.free_lib()
        self.bob_lib = CDLL(self.lib_path)
        self.link_c_functions()
        # self.do_rcread() # create default values of global C variables

    def run_bob_main(self, arg_list, npol_tot):
        """Run BoB asking for a polyconf file only (no relaxation etc) and
        output the characteristics of the polymer configuration"""
        # reset the library
        self.reload_lib() 
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
        #call C function
        self.reptate_save_polyconf_and_return_gpc(
            c_int(n_arg), argv, c_int(nbin), ncomp, ni, nf, byref(mn),
            byref(mw), lgmid_arr, wtbin_arr, brbin_arr, gbin_arr)
        #unload the library
        self.free_lib()
        # return results
        arrs = [lgmid_arr[:], wtbin_arr[:], brbin_arr[:], gbin_arr[:]]
        return [mn.value, mw.value, arrs]
