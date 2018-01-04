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

lib_path = 'theories/react_lib_%s.so'%(sys.platform)
try:
    react_lib = CDLL(lib_path)
except:
    print('OS %s not recognized'%(sys.platform))

###############
# polybits.c
###############

#struct
class polybits_global_const(Structure):
    _fields_ = [("maxbobbins", c_int), ("maxmwdbins", c_int), ("maxarm", c_int), ("maxpol", c_int), ("maxreact", c_int)]

class polybits_global(Structure):
    _fields_ = [("first_in_pool", c_int), ("first_poly_in_pool", c_int), ("first_dist_in_pool", c_int), ("mmax", c_int), ("num_react", c_int), ("arms_left", c_int), ("react_pool_initialised", c_bool), ("react_pool_declared", c_bool), ("arms_avail", c_bool), ("polys_avail", c_bool), ("dists_avail", c_bool)]

class arm(Structure):
    _fields_ = [("arm_len", c_double), ("arm_conv", c_double), ("arm_time", c_double), ("arm_tm", c_double), ("arm_tddb", c_double), ("L1", c_int),("L2", c_int), ("R1", c_int), ("R2", c_int), ("up", c_int), ("down", c_int), ("armnum", c_int), ("armcat", c_int),("ended", c_int), ("endfin", c_int), ("scission", c_int)]   

class polymer(Structure):
    _fields_ = [("first_end", c_int), ("num_br", c_int), ("bin", c_int), ("num_sat", c_int), ("num_unsat", c_int), ("armnum", c_int), ("nextpoly", c_int), ("tot_len", c_double), ("gfactor", c_double), ("saved", c_bool)]

class reactresults(Structure):
     _fields_ = [("wt", POINTER(c_double)), ("avbr", POINTER(c_double)), ("wmass", POINTER(c_double)), ("avg", POINTER(c_double)), ("lgmid", POINTER(c_double)), ("numinbin", POINTER(c_int)), ("monmass", c_double), ("M_e", c_double), ("N_e", c_double), ("boblgmin", c_double), ("boblgmax", c_double), ("m_w", c_double), ("m_n", c_double), ("brav", c_double), ("first_poly", c_int), ("next", c_int), ("nummwdbins", c_int), ("numbobbins", c_int), ("bobbinmax", c_int), ("nsaved", c_int), ("npoly", c_int), ("simnumber", c_int), ("polysaved", c_bool), ("name", c_char_p)]

#global variable
pb_global_const = polybits_global_const.in_dll(react_lib, "pb_global_const")
pb_global = polybits_global.in_dll(react_lib, "pb_global")

#pointer
arm_pointer = POINTER(arm)
arm_pointers = arm_pointer * (pb_global_const.maxarm + 1)

polymer_pointer = POINTER(polymer)
polymer_pointers = polymer_pointer * (pb_global_const.maxpol + 1)

reactresults_pointer = POINTER(reactresults)
reactresults_pointers = reactresults_pointer * (pb_global_const.maxreact + 1)

#list
arm_pool = arm_pointers()
br_poly = polymer_pointers()
react_dist = reactresults_pointers()

#function
react_pool_init = react_lib.react_pool_init
react_pool_init.restype = None

request_dist = react_lib.request_dist
request_dist.restype = c_bool

return_dist_polys = react_lib.return_dist_polys
return_dist_polys.restype = None

return_dist = react_lib.return_dist
return_dist.restype = None

request_poly = react_lib.request_poly
request_poly.restype = c_bool

return_arm_pool = react_lib.return_arm_pool
return_arm_pool.restype = arm_pointer

return_br_poly = react_lib.return_br_poly
return_br_poly.restype = polymer_pointer

return_react_dist = react_lib.return_react_dist
return_react_dist.restype = reactresults_pointer



###############
# tobitabatch.c
###############

#struct
class tobitabatch_global(Structure):
    _fields_ = [("tobbatchnumber", c_int), ("tobitabatcherrorflag",c_bool)]

#global variable
tb_global = tobitabatch_global.in_dll(react_lib, "tb_global")

#function
tobbatchstart = react_lib.tobbatchstart
tobbatchstart.restype = None

tobbatch = react_lib.tobbatch
tobbatch.restype = c_bool



###############
# binsandbob.c
###############

#function
molbin = react_lib.molbin
molbin.restype = None
