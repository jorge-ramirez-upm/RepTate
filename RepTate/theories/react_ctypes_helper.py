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
import numpy as np
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
                                                             ct.c_int), ("MAX_RLEVEL", ct.c_int), ("MAX_NBR", ct.c_int)]


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
        ("wt", ct.POINTER(ct.c_double)), ("avbr", ct.POINTER(ct.c_double)),
        ("wmass", ct.POINTER(ct.c_double)), ("avg", ct.POINTER(
            ct.c_double)), ("lgmid", ct.POINTER(
                ct.c_double)), ("numinbin",
                                ct.POINTER(ct.c_int)), ("numin_armwt_bin",
                                                        ct.POINTER(ct.c_int)),
                                                        ("numin_num_br_bin",
                                                        ct.POINTER(ct.c_int)),
        ("num_armwt_bin", ct.c_int), ("max_num_br", ct.c_int), ("monmass", ct.c_double), ("M_e",
                                                                ct.c_double),
        ("N_e", ct.c_double), ("boblgmin", ct.c_double), ("boblgmax",
                                                          ct.c_double),
        ("m_w", ct.c_double), ("m_n", ct.c_double), ("brav", ct.c_double),
        ("m_z", ct.c_double), ("m_zp1", ct.c_double), ("m_zp2", ct.c_double),
        ("first_poly",
         ct.c_int), ("next",
                     ct.c_int), ("nummwdbins",
                                 ct.c_int), ("numbobbins",
                                             ct.c_int), ("bobbinmax",
                                                         ct.c_int), ("nsaved",
                                                                     ct.c_int),
        ("npoly",
         ct.c_int), ("simnumber",
                     ct.c_int), ("polysaved",
                                 ct.c_bool), ("name", ct.c_char_p), 
        ("wlin", ct.c_double),
        ("wstar", ct.c_double), ("wH", ct.c_double), ("w7arm",
                                                                     ct.c_double),
        ("wcomb",
         ct.c_double), ("wother",
                     ct.c_double),
                                 ("nlin", ct.c_int),
        ("nstar", ct.c_int), ("nH", ct.c_int), ("n7arm",
                                                                     ct.c_int),
        ("ncomb",
         ct.c_int), ("nother",
                     ct.c_int), ("nsaved_arch",
                                 ct.c_int), ("arch_minwt",
                                             ct.c_double), ("arch_maxwt",
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
init_bin_prio_vs_senio.argtypes = [ct.c_int]

return_avarmlen_v_senio = react_lib.return_avarmlen_v_senio
return_avarmlen_v_senio.restype = ct.c_double

return_avarmlen_v_prio = react_lib.return_avarmlen_v_prio
return_avarmlen_v_prio.restype = ct.c_double

return_avprio_v_senio = react_lib.return_avprio_v_senio
return_avprio_v_senio.restype = ct.c_double

return_avsenio_v_prio = react_lib.return_avsenio_v_prio
return_avsenio_v_prio.restype = ct.c_double

return_proba_prio = react_lib.return_proba_prio
return_proba_prio.restype = ct.c_double

return_max_prio = react_lib.return_max_prio
return_max_prio.restype = ct.c_int

return_proba_senio = react_lib.return_proba_senio
return_proba_senio.restype = ct.c_double

return_max_senio = react_lib.return_max_senio
return_max_senio.restype = ct.c_int

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

###############
# dieneCSTR.c
###############


#struct
class dieneCSTR_global(ct.Structure):
    _fields_ = [("dieneCSTRnumber", ct.c_int), ("dieneCSTRerrorflag",
                                                ct.c_bool)]


#global variable
dCSTR_global = dieneCSTR_global.in_dll(react_lib, "dCSTR_global")

#function
dieneCSTRstart = react_lib.dieneCSTRstart
dieneCSTRstart.restype = None

dieneCSTR = react_lib.dieneCSTR
dieneCSTR.restype = ct.c_bool

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
    parent_theory.Qprint(
        '<b>Simulation Results:</b>')

    table = []
    table.append(['', '']) # no header
    table.append(['Polymer made', '%d' % react_dist[ndist].contents.npoly])
    table.append(['Polymer saved', '%d' % react_dist[ndist].contents.nsaved])
    table.append(['Arm left in memory', '%d' % pb_global.arms_left])
    table.append(['Mn (g/mol)', '%.3g' % react_dist[ndist].contents.m_n])
    table.append(['Mw (g/mol)', '%.3g' % react_dist[ndist].contents.m_w])
    table.append(['Mz (g/mol)', '%.3g' % react_dist[ndist].contents.m_z])
    table.append(['Mz+1 (g/mol)', '%.3g' % react_dist[ndist].contents.m_zp1])
    table.append(['Mz+2 (g/mol)', '%.3g' % react_dist[ndist].contents.m_zp2])
    table.append(['Br/1000C', '%.3g' % react_dist[ndist].contents.brav])
    table.append(['Max br', '%d' % react_dist[ndist].contents.max_num_br])
    parent_theory.Qprint(table)

    if (do_architecture):
        nlin = react_dist[ndist].contents.nlin
        nstar = react_dist[ndist].contents.nstar
        nH = react_dist[ndist].contents.nH
        n7arm = react_dist[ndist].contents.n7arm
        ncomb = react_dist[ndist].contents.ncomb
        nother = react_dist[ndist].contents.nother
        #
        wlin = react_dist[ndist].contents.wlin
        wstar = react_dist[ndist].contents.wstar
        wH = react_dist[ndist].contents.wH
        w7arm = react_dist[ndist].contents.w7arm
        wcomb = react_dist[ndist].contents.wcomb
        wother = react_dist[ndist].contents.wother
        
        name_list = ["Linear", "Star", "H", "7-arm", "Comb", "Other"]
        nlist = [nlin, nstar, nH, n7arm, ncomb, nother]
        wlist = [wlin, wstar, wH, w7arm, wcomb, wother]
        for i, n in enumerate(nlist):
            if n != 0:
                wlist[i] = wlist[i] / n

        norm = react_dist[ndist].contents.nsaved_arch / 100
        if norm != 0:
            parent_theory.Qprint(
                '<b>Architecture of %d Polymers: %.3g &lt; M &lt; %.3g g/mol:</b>'
                % (react_dist[ndist].contents.nsaved_arch, parent_theory.xmin,
                   parent_theory.xmax))
            table = '''<table border="1" width="100%">'''
            table += '''<tr><th>Type</th><th>Prop.</th><th>&lt;Mw&gt; (g/mol)</th></tr>'''
            for i in range(len(nlist)):
                table += '''<tr><td>%s</td><td>%.3g%%</td><td>%.3g</td></tr>''' % (
                    name_list[i], nlist[i] / norm, wlist[i])
            table += '''</table><br>'''
            parent_theory.Qprint(table)

def prio_and_senio(parent_theory, f, ndist, do_architecture):
    """Get the arm length prob. distr. and priority vs seniority form C and save it in the
    theory DataTable"""
    tt = parent_theory.tables[f.file_name_short]
    # arm length
    lgmax = np.log10(react_dist[ndist].contents.arch_maxwt * 1.01)
    lgmin = np.log10(react_dist[ndist].contents.monmass / 1.01)
    num_armwt_bin = react_dist[ndist].contents.num_armwt_bin
    lgstep = (lgmax - lgmin)/(1.0 * num_armwt_bin)
    tmp_x = np.power(10, [lgmin + ibin * lgstep - 0.5 * lgstep for ibin in range(1, num_armwt_bin + 1)])
    tmp_y = [react_dist[ndist].contents.numin_armwt_bin[ibin] for ibin in range(1, num_armwt_bin + 1)]
    # trim right zeros
    tmp_y = np.trim_zeros(tmp_y, 'b')
    new_len = len(tmp_y)
    tmp_x = tmp_x[:new_len]
    # trim left zeros
    tmp_y = np.trim_zeros(tmp_y, 'f')
    new_len = len(tmp_y)
    tmp_x = tmp_x[-new_len:]

    tt.extra_tables['proba_arm_wt'] = np.zeros((new_len, 2))
    tt.extra_tables['proba_arm_wt'][:, 0] = tmp_x
    tt.extra_tables['proba_arm_wt'][:, 1] = tmp_y
    # normalize
    try:
        tt.extra_tables['proba_arm_wt'][:, 1] /= tt.extra_tables['proba_arm_wt'][:, 1].sum()
    except ZeroDivisionError:
        pass

    # number of branch points branch point
    max_num_br = react_dist[ndist].contents.max_num_br
    
    # if max_num_br < 100:
    rmax = min(max_num_br + 1, pb_global_const.MAX_NBR)
    tt.extra_tables['proba_br_pt'] = np.zeros((max_num_br + 1, 2))
    tt.extra_tables['proba_br_pt'][:, 0] = np.arange(max_num_br + 1)
    tt.extra_tables['proba_br_pt'][:, 1] = [react_dist[ndist].contents.numin_num_br_bin[i] for i in range(max_num_br + 1)]
    try:
        tt.extra_tables['proba_br_pt'][:, 1] /= tt.extra_tables['proba_br_pt'][:, 1].sum()
    except ZeroDivisionError:
        pass
    # else:
    #     # bin the data
    #     tmp_x = list(np.arange(max_num_br + 1))
    #     tmp_y = [react_dist[ndist].contents.numin_num_br_bin[i] for i in range(max_num_br + 1)]
    #     hist, bin_edge = np.histogram(tmp_x, bins=20, weights=tmp_y, density=True)
    #     tt.extra_tables['proba_br_pt'] = np.zeros((len(hist), 2))
    #     tt.extra_tables['proba_br_pt'][:, 0] = np.diff(bin_edge) / 2 + bin_edge[:-1]
    #     tt.extra_tables['proba_br_pt'][:, 1] = hist

    if not do_architecture:
        return
    # P&S
    max_prio = return_max_prio()
    max_senio = return_max_senio()

    avarmlen_v_senio = [
        return_avarmlen_v_senio(ct.c_int(s), ct.c_int(ndist))
        for s in range(1, max_senio + 1)
    ]
    avarmlen_v_prio = [
        return_avarmlen_v_prio(ct.c_int(p), ct.c_int(ndist))
        for p in range(1, max_prio + 1)
    ]

    avprio_v_senio = [
        return_avprio_v_senio(ct.c_int(s)) for s in range(1, max_senio + 1)
    ]
    avsenio_v_prio = [
        return_avsenio_v_prio(ct.c_int(p)) for p in range(1, max_prio + 1)
    ]

    proba_senio = [
        return_proba_senio(ct.c_int(s)) for s in range(1, max_senio + 1)
    ]
    proba_prio = [
        return_proba_prio(ct.c_int(p)) for p in range(1, max_prio + 1)
    ]

    tt.extra_tables['avarmlen_v_senio'] = np.zeros((max_senio, 2))
    tt.extra_tables['avarmlen_v_senio'][:, 0] = np.arange(1, max_senio + 1)
    tt.extra_tables['avarmlen_v_senio'][:, 1] = avarmlen_v_senio[:]

    tt.extra_tables['avarmlen_v_prio'] = np.zeros((max_prio, 2))
    tt.extra_tables['avarmlen_v_prio'][:, 0] = np.arange(1, max_prio + 1)
    tt.extra_tables['avarmlen_v_prio'][:, 1] = avarmlen_v_prio[:]

    tt.extra_tables['avprio_v_senio'] = np.zeros((max_senio, 2))
    tt.extra_tables['avprio_v_senio'][:, 0] = np.arange(1, max_senio + 1)
    tt.extra_tables['avprio_v_senio'][:, 1] = avprio_v_senio[:]

    tt.extra_tables['avsenio_v_prio'] = np.zeros((max_prio, 2))
    tt.extra_tables['avsenio_v_prio'][:, 0] = np.arange(1, max_prio + 1)
    tt.extra_tables['avsenio_v_prio'][:, 1] = avsenio_v_prio[:]

    tt.extra_tables['proba_senio'] = np.zeros((max_senio, 2))
    tt.extra_tables['proba_senio'][:, 0] = np.arange(1, max_senio + 1)
    tt.extra_tables['proba_senio'][:, 1] = proba_senio[:]

    tt.extra_tables['proba_prio'] = np.zeros((max_prio, 2))
    tt.extra_tables['proba_prio'][:, 0] = np.arange(1, max_prio + 1)
    tt.extra_tables['proba_prio'][:, 1] = proba_prio[:]
