// RepTate: Rheology of Entangled Polymers: Toolkit for the Analysis of Theory and Experiments
// --------------------------------------------------------------------------------------------------------

// Authors:
//     Jorge Ramirez, jorge.ramirez@upm.es
//     Victor Boudara, victor.boudara@gmail.com
//     Daniel Read, d.j.read@leeds.ac.uk

// Useful links:
//     http://blogs.upm.es/compsoftmatter/software/reptate/
//     https://github.com/jorge-ramirez-upm/RepTate
//     http://reptate.readthedocs.io

// --------------------------------------------------------------------------------------------------------

// Copyright (2017): Jorge Ramirez, Victor Boudara, Universidad Politécnica de Madrid, University of Leeds

// This file is part of RepTate.

// RepTate is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.

// RepTate is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.

// You should have received a copy of the GNU General Public License
// along with RepTate.  If not, see <http://www.gnu.org/licenses/>.

// --------------------------------------------------------------------------------------------------------
#ifndef REACT_STRUCTS_H
#define REACT_STRUCTS_H

#include <stdbool.h>

typedef struct
{
    double arm_len, arm_conv, arm_time, arm_tm, arm_tdb;
    int L1, L2, R1, R2, up, down, armnum, armcat;
    bool ended, endfin, scission;
    int senio, prio;
} arm;

typedef struct
{
    int first_end, num_br, bin, num_sat, num_unsat, armnum, nextpoly;
    double tot_len, gfactor;
    bool saved;
    int max_senio, max_prio;
} polymer;

typedef struct
{
    double *wt, *avbr, *wmass, *avg, *lgmid; //array[1..maxmwdbins] of ;
    int *numinbin;                           // array[1..maxbobbins] of integer;
    double monmass, M_e, N_e, boblgmin, boblgmax, m_w, m_n, brav;
    int first_poly, next, nummwdbins, numbobbins, bobbinmax, nsaved, npoly, simnumber;
    bool polysaved;
    char *name;
    int nlin, nstar, nH, n5arm, n7arm, ncomb, nother, nsaved_arch;
    double arch_minwt, arch_maxwt;
} reactresults;

typedef struct
{
    int maxbobbins;
    int maxmwdbins;
    int maxarm; //  maxarm=10000000;
    int maxpol;
    int maxreact;
} polybits_global_const; //these are not really constants, can be changed at runtime

typedef struct
{
    int first_in_pool;
    int first_poly_in_pool;
    int first_dist_in_pool;
    int mmax;
    int num_react;
    int arms_left;
    bool react_pool_initialised;
    bool react_pool_declared;
    bool arms_avail;  // these flags simply record
    bool polys_avail; // availability of arms
    bool dists_avail;
} polybits_global;

typedef struct
{
    double multi_m_w;
    double multi_m_n;
    double multi_brav;
    int multi_nummwdbins;
} binsandbob_global;

typedef struct
{
    int mulmetCSTRnumber;
    bool mulmetCSTRerrorflag;
} mulmetCSTR_global;

typedef struct
{
    int tobbatchnumber;
    bool tobitabatcherrorflag;
} tobitabatch_global;

typedef struct
{
    int tobCSTRnumber;
    bool tobitaCSTRerrorflag;
} tobitaCSTR_global;

#endif
