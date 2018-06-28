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
import ctypes as ct
import sys
import os

dir_path = os.path.dirname(
    os.path.realpath(__file__))  # get the directory path of current file
if sys.maxsize > 2**32:
    # 64-bit system
    lib_path = dir_path + os.sep + 'react_lib_%s.so' % (sys.platform)
else:
    # 32-bit system
    lib_path = dir_path + os.sep + 'react_lib_%s_i686.so' % (sys.platform)
try:
    react_lib = ct.CDLL(lib_path)
except:
    print('OS %s not recognized in React CH module' % (sys.platform))

###############
# polybits.c
###############


#struct
class polybits_global_const(ct.Structure):
    _fields_ = [("maxbobbins", ct.c_int), ("maxmwdbins", ct.c_int),
                ("maxarm", ct.c_int), ("maxpol", ct.c_int), ("maxreact",
                                                             ct.c_int)]


class polybits_global(ct.Structure):
    _fields_ = [("first_in_pool", ct.c_int), ("first_poly_in_pool", ct.c_int),
                ("first_dist_in_pool",
                 ct.c_int), ("mmax", ct.c_int), ("num_react", ct.c_int),
                ("arms_left", ct.c_int), ("react_pool_initialised", ct.c_bool),
                ("react_pool_declared", ct.c_bool), ("arms_avail", ct.c_bool),
                ("polys_avail", ct.c_bool), ("dists_avail", ct.c_bool)]


class arm(ct.Structure):
    _fields_ = [("arm_len", ct.c_double), ("arm_conv", ct.c_double),
                ("arm_time", ct.c_double), ("arm_tm", ct.c_double),
                ("arm_tddb", ct.c_double), ("L1", ct.c_int), ("L2", ct.c_int),
                ("R1", ct.c_int), ("R2", ct.c_int), ("up", ct.c_int),
                ("down", ct.c_int), ("armnum", ct.c_int), ("armcat", ct.c_int),
                ("ended",
                 ct.c_int), ("endfin",
                             ct.c_int), ("scission",
                                         ct.c_int), ("senio",
                                                     ct.c_int), ("prio",
                                                                 ct.c_int)]


class polymer(ct.Structure):
    _fields_ = [("first_end", ct.c_int), ("num_br", ct.c_int), ("bin",
                                                                ct.c_int),
                ("num_sat", ct.c_int), ("num_unsat", ct.c_int), ("armnum",
                                                                 ct.c_int),
                ("nextpoly",
                 ct.c_int), ("tot_len", ct.c_double), ("gfactor", ct.c_double),
                ("saved", ct.c_bool), ("max_senio", ct.c_int), ("max_prio",
                                                                ct.c_int)]


class reactresults(ct.Structure):
    _fields_ = [
        ("wt", ct.POINTER(ct.c_double)), ("avbr", ct.POINTER(
            ct.c_double)), ("wmass", ct.POINTER(ct.c_double)),
        ("avg", ct.POINTER(ct.c_double)), ("lgmid", ct.POINTER(
            ct.c_double)), ("numinbin", ct.POINTER(ct.c_int)), ("monmass",
                                                                ct.c_double),
        ("M_e", ct.c_double), ("N_e", ct.c_double), ("boblgmin", ct.c_double),
        ("boblgmax", ct.c_double), ("m_w", ct.c_double), ("m_n", ct.c_double),
        ("brav", ct.c_double), ("first_poly", ct.c_int), ("next", ct.c_int),
        ("nummwdbins", ct.c_int), ("numbobbins",
                                   ct.c_int), ("bobbinmax",
                                               ct.c_int), ("nsaved", ct.c_int),
        ("npoly",
         ct.c_int), ("simnumber",
                     ct.c_int), ("polysaved",
                                 ct.c_bool), ("name", ct.c_char_p), ("nlin",
                                                                     ct.c_int),
        ("nstar",
         ct.c_int), ("nH",
                     ct.c_int), ("n5arm",
                                 ct.c_int), ("n7arm",
                                             ct.c_int), ("ncomb",
                                                         ct.c_int), ("nother",
                                                                     ct.c_int),
                                                                     ("nsaved_arch",
                                                                     ct.c_int),
                                                                    ("arch_minwt",
                                                                     ct.c_double),
                                                                    ("arch_maxwt",
                                                                     ct.c_double)
    ]


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

# return_arm_pool = react_lib.return_arm_pool
# return_arm_pool.restype = arm_pointer

# return_br_poly = react_lib.return_br_poly
# return_br_poly.restype = polymer_pointer

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

set_do_prio_senio = react_lib.set_do_prio_senio
set_do_prio_senio.restype = None

set_flag_stop_all = react_lib.set_flag_stop_all
set_flag_stop_all.restype = None

init_bin_prio_vs_senio = react_lib.init_bin_prio_vs_senio
init_bin_prio_vs_senio.restype = None

return_prio_vs_senio = react_lib.return_prio_vs_senio
return_prio_vs_senio.restype = ct.c_double


#initialise lists
react_dist = None


def link_react_dist():
    """link the Python list react_dist with the C array react_dist"""
    global reactresults_pointers
    global react_dist
    reactresults_pointers = reactresults_pointer * (
        pb_global_const.maxreact + 1)
    react_dist = reactresults_pointers(*list([
        return_react_dist(ct.c_int(i))
        for i in range(pb_global_const.maxreact + 1)
    ]))


react_pool_init()
link_react_dist()

###############
# tobitabatch.c
###############


#struct
class tobitabatch_global(ct.Structure):
    _fields_ = [("tobbatchnumber", ct.c_int), ("tobitabatcherrorflag",
                                               ct.c_bool)]


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


#struct
class binsandbob_global(ct.Structure):
    _fields_ = [("multi_m_w", ct.c_double), ("multi_m_n", ct.c_double),
                ("multi_brav", ct.c_double), ("multi_nummwdbins", ct.c_int)]


#global variable
bab_global = binsandbob_global.in_dll(react_lib, "bab_global")

#function
molbin = react_lib.molbin
molbin.restype = None

polyconfwrite = react_lib.polyconfwrite
polyconfwrite.restype = None

multipolyconfwrite = react_lib.multipolyconfwrite
multipolyconfwrite.restype = ct.c_ulonglong

multimolbin = react_lib.multimolbin
multimolbin.restype = None

return_binsandbob_multi_avbr = react_lib.return_binsandbob_multi_avbr
return_binsandbob_multi_avbr.restype = ct.c_double

return_binsandbob_multi_avg = react_lib.return_binsandbob_multi_avg
return_binsandbob_multi_avg.restype = ct.c_double

return_binsandbob_multi_lgmid = react_lib.return_binsandbob_multi_lgmid
return_binsandbob_multi_lgmid.restype = ct.c_double

return_binsandbob_multi_wmass = react_lib.return_binsandbob_multi_wmass
return_binsandbob_multi_wmass.restype = ct.c_double

return_binsandbob_multi_wt = react_lib.return_binsandbob_multi_wt
return_binsandbob_multi_wt.restype = ct.c_double

set_react_dist_monmass = react_lib.set_react_dist_monmass
set_react_dist_monmass.restype = ct.c_double

set_react_dist_M_e = react_lib.set_react_dist_M_e
set_react_dist_M_e.restype = ct.c_double

###############
# tobitaCSTR.c
###############


#struct
class tobitaCSTR_global(ct.Structure):
    _fields_ = [("tobCSTRnumber", ct.c_int), ("tobitaCSTRerrorflag",
                                              ct.c_bool)]


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
    _fields_ = [("mulmetCSTRnumber", ct.c_int), ("mulmetCSTRerrorflag",
                                                 ct.c_bool)]


#global variable
MMCSTR_global = mulmetCSTR_global.in_dll(react_lib, "MMCSTR_global")

#function
mulmetCSTRstart = react_lib.mulmetCSTRstart
mulmetCSTRstart.restype = None

mulmetCSTR = react_lib.mulmetCSTR
mulmetCSTR.restype = ct.c_bool

#############
# Other
############

def end_print(parent_theory, ndist, do_architecture):
    """Print the simulation information at the end of the run. 
    Print priority and seniority information if needed"""
    parent_theory.Qprint('<hr style="border-top: dotted 2px;" /><b>Simulation Results:</b>')
    table='''<table border="1" width="100%">'''
    table+= '''<tr><td>%s</td><td>%d</td></tr>'''% ('Polymer made', react_dist[ndist].contents.npoly)
    table+= '''<tr><td>%s</td><td>%d</td></tr>'''% ('Polymer saved', react_dist[ndist].contents.nsaved)
    table+= '''<tr><td>%s</td><td>%d</td></tr>'''% ('Arm left in memory', pb_global.arms_left)
    table+= '''<tr><td>%s</td><td>%.3g</td></tr>'''% ('Mn (kg/mol)', react_dist[ndist].contents.m_n / 1000.0)
    table+= '''<tr><td>%s</td><td>%.3g</td></tr>'''% ('Mw (kg/mol)', react_dist[ndist].contents.m_w / 1000.0)
    table+= '''<tr><td>%s</td><td>%.3g</td></tr>'''% ('br/1000C', react_dist[ndist].contents.brav)
    table+= '''</table><br>'''
    parent_theory.Qprint(table)
    
    if(do_architecture):
        norm = react_dist[ndist].contents.nsaved_arch / 100
        if norm != 0:
            parent_theory.Qprint('<b>Architecture of %d Polymers: %.3g &lt; M &lt; %.3g kg/mol:</b>' % (react_dist[ndist].contents.nsaved_arch, parent_theory.xmin/1000, parent_theory.xmax/1000))
            table='''<table border="1" width="100%">'''
            table+= '''<tr><td>%s</td><td>%.3g%%</td></tr>'''% ('Linear', react_dist[ndist].contents.nlin / norm)
            table+= '''<tr><td>%s</td><td>%.3g%%</td></tr>'''% ('Star', react_dist[ndist].contents.nstar / norm)
            table+= '''<tr><td>%s</td><td>%.3g%%</td></tr>'''% ('H', react_dist[ndist].contents.nH / norm)
            table+= '''<tr><td>%s</td><td>%.3g%%</td></tr>'''% ('7-arm', react_dist[ndist].contents.nH / norm)
            table+= '''<tr><td>%s</td><td>%.3g%%</td></tr>'''% ('Comb', react_dist[ndist].contents.ncomb / norm)
            table+= '''<tr><td>%s</td><td>%.3g%%</td></tr>'''% ('Other', react_dist[ndist].contents.nother / norm)
            table+= '''</table><br>'''
            parent_theory.Qprint(table)

def prio_v_senio(parent_theory, f, ndist, do_architecture):
    """Get the priority vs seniority form C and save it in the
    theory DataTable"""
    if not do_architecture:
        return
    import matplotlib.pyplot as plt
    import numpy as np
    pvs = []
    for s in range(1, 1000):
        val = return_prio_vs_senio(ct.c_int(s))
        if val == 0:
            break
        pvs.append(val)
    tt = parent_theory.tables[f.file_name_short]
    nrow = len(tt.data[:, 0])
    if nrow < len(pvs):
        tt.data.resize(len(pvs), tt.num_columns)
        tt.num_rows = len(pvs)
    tt.data[:, 4] = np.arange(1, tt.num_rows + 1)
    tt.data[:len(pvs), 5] = pvs[:]
    tt.data[len(pvs):, 5] = np.nan
