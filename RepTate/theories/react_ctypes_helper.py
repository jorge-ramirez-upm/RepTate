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
import ctypes as ct
import sys

lib_path = 'theories/react_lib_%s.so'%(sys.platform)
try:
    react_lib = ct.CDLL(lib_path)
except:
    print('OS %s not recognized'%(sys.platform))

###############
# polybits.c
###############

#struct
class polybits_global_const(ct.Structure):
    _fields_ = [("maxbobbins", ct.c_int), ("maxmwdbins", ct.c_int), ("maxarm", ct.c_int), ("maxpol", ct.c_int), ("maxreact", ct.c_int)]

class polybits_global(ct.Structure):
    _fields_ = [("first_in_pool", ct.c_int), ("first_poly_in_pool", ct.c_int), ("first_dist_in_pool", ct.c_int), ("mmax", ct.c_int), ("num_react", ct.c_int), ("arms_left", ct.c_int), ("react_pool_initialised", ct.c_bool), ("react_pool_declared", ct.c_bool), ("arms_avail", ct.c_bool), ("polys_avail", ct.c_bool), ("dists_avail", ct.c_bool)]

class arm(ct.Structure):
    _fields_ = [("arm_len", ct.c_double), ("arm_conv", ct.c_double), ("arm_time", ct.c_double), ("arm_tm", ct.c_double), ("arm_tddb", ct.c_double), ("L1", ct.c_int),("L2", ct.c_int), ("R1", ct.c_int), ("R2", ct.c_int), ("up", ct.c_int), ("down", ct.c_int), ("armnum", ct.c_int), ("armcat", ct.c_int),("ended", ct.c_int), ("endfin", ct.c_int), ("scission", ct.c_int)]   

class polymer(ct.Structure):
    _fields_ = [("first_end", ct.c_int), ("num_br", ct.c_int), ("bin", ct.c_int), ("num_sat", ct.c_int), ("num_unsat", ct.c_int), ("armnum", ct.c_int), ("nextpoly", ct.c_int), ("tot_len", ct.c_double), ("gfactor", ct.c_double), ("saved", ct.c_bool)]

class reactresults(ct.Structure):
     _fields_ = [("wt", ct.POINTER(ct.c_double)), ("avbr", ct.POINTER(ct.c_double)), ("wmass", ct.POINTER(ct.c_double)), ("avg", ct.POINTER(ct.c_double)), ("lgmid", ct.POINTER(ct.c_double)), ("numinbin", ct.POINTER(ct.c_int)), ("monmass", ct.c_double), ("M_e", ct.c_double), ("N_e", ct.c_double), ("boblgmin", ct.c_double), ("boblgmax", ct.c_double), ("m_w", ct.c_double), ("m_n", ct.c_double), ("brav", ct.c_double), ("first_poly", ct.c_int), ("next", ct.c_int), ("nummwdbins", ct.c_int), ("numbobbins", ct.c_int), ("bobbinmax", ct.c_int), ("nsaved", ct.c_int), ("npoly", ct.c_int), ("simnumber", ct.c_int), ("polysaved", ct.c_bool), ("name", ct.c_char_p)]

#global variable
pb_global_const = polybits_global_const.in_dll(react_lib, "pb_global_const")
pb_global = polybits_global.in_dll(react_lib, "pb_global")

#pointer
arm_pointer = ct.POINTER(arm)
arm_pointers = arm_pointer * (pb_global_const.maxarm + 1)

polymer_pointer = ct.POINTER(polymer)
polymer_pointers = polymer_pointer * (pb_global_const.maxpol + 1)

reactresults_pointer = ct.POINTER(reactresults)
reactresults_pointers = reactresults_pointer * (pb_global_const.maxreact + 1)


#function
react_pool_init = react_lib.react_pool_init
react_pool_init.restype = None

request_dist = react_lib.request_dist
request_dist.restype = ct.c_bool

return_dist_polys = react_lib.return_dist_polys
return_dist_polys.restype = None

return_dist = react_lib.return_dist
return_dist.restype = None

request_poly = react_lib.request_poly
request_poly.restype = ct.c_bool

return_arm_pool = react_lib.return_arm_pool
return_arm_pool.restype = arm_pointer

return_br_poly = react_lib.return_br_poly
return_br_poly.restype = polymer_pointer

return_react_dist = react_lib.return_react_dist
return_react_dist.restype = reactresults_pointer

set_br_poly_nextpoly = react_lib.set_br_poly_nextpoly
set_br_poly_nextpoly.restype = None

increase_arm_records_in_arm_pool = react_lib.increase_arm_records_in_arm_pool
increase_arm_records_in_arm_pool.restype = ct.c_bool

increase_polymer_records_in_br_poly = react_lib.increase_polymer_records_in_br_poly
increase_polymer_records_in_br_poly.restype = ct.c_bool

increase_dist_records_in_react_dist = react_lib.increase_dist_records_in_react_dist
increase_dist_records_in_react_dist.restype = ct.c_bool


#initialise lists
react_dist = None

def link_react_dist():
    """link the Python list react_dist with the C array react_dist"""
    global reactresults_pointers
    global react_dist
    reactresults_pointers = reactresults_pointer * (pb_global_const.maxreact + 1)
    react_dist =  reactresults_pointers(*list([return_react_dist(ct.c_int(i)) for i in range(pb_global_const.maxreact + 1)]))
    
react_pool_init()
link_react_dist()


###############
# tobitabatch.c
###############

#struct
class tobitabatch_global(ct.Structure):
    _fields_ = [("tobbatchnumber", ct.c_int), ("tobitabatcherrorflag", ct.c_bool)]

#global variable
tb_global = tobitabatch_global.in_dll(react_lib, "tb_global")

#function
tobbatchstart = react_lib.tobbatchstart
tobbatchstart.restype = None

tobbatch = react_lib.tobbatch
tobbatch.restype = ct.c_bool



###############
# binsandbob.c
###############

#function
molbin = react_lib.molbin
molbin.restype = None

polyconfwrite = react_lib.polyconfwrite
polyconfwrite.restype = None


###############
# tobitaCSTR.c
###############

#struct
class tobitaCSTR_global(ct.Structure):
    _fields_ = [("tobCSTRnumber", ct.c_int), ("tobitaCSTRerrorflag", ct.c_bool)]

#global variable
tCSTR_global = tobitaCSTR_global.in_dll(react_lib, "tCSTR_global")

#function
tobCSTRstart = react_lib.tobCSTRstart
tobCSTRstart.restype = None

tobCSTR = react_lib.tobCSTR
tobCSTR.restype = ct.c_bool

################
# MultiMetCSTR.c
################

#struct
class mulmetCSTR_global(ct.Structure):
    _fields_ = [("mulmetCSTRnumber", ct.c_int), ("mulmetCSTRerrorflag", ct.c_bool)]

#global variable
MMCSTR_global = mulmetCSTR_global.in_dll(react_lib, "MMCSTR_global")

#function
mulmetCSTRstart = react_lib.mulmetCSTRstart
mulmetCSTRstart.restype = None

mulmetCSTR = react_lib.mulmetCSTR
mulmetCSTR.restype = ct.c_bool