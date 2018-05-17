// RepTate: Rheology of Entangled Polymers: Toolkit for the Analysis of Theory and Experiments
// --------------------------------------------------------------------------------------------------------

// Authors:
//     Jorge Ramirez, jorge.ramirez@upm.es
//     Victor Boudara, victor.boudara@gmail.com
//     Chinmay Das, chinmaydas@yahoo.com

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
//    THE FOLLOWING IS FOR REPTATE COMPATIBILITY
#ifndef REPTATE_FUNC_H
#define REPTATE_FUNC_H
#include <vector>

// callback function
typedef void pyfunc(char* s);
extern pyfunc *py_callback;

// functions used by Python
extern "C" void def_pycallback_func(pyfunc F);
extern "C" bool reptate_save_polyconf_and_return_gpc(int argc, char **argv, int nbin, int ncomp, int ni, int nf, double *mn, double *mw, double *lgmid_out, double *wtbin_out, double *brbin_out, double *gbin_out);
extern "C" bool run_bob_lve(int argc, char **argv, int* n);
extern "C" bool get_bob_lve(double *omega_out, double* gp_out, double * gpp_out);

// other functions
void get_mn_mw(double *mn, double *mw);
void return_gpcls(int nbin, int ncomp, int ni, int nf, double *lgmid_out, double *wtbin_out, double *brbin_out, double *gbin_out);

void return_gpchist(int ncomp, int n_cur_comp, double *mass_ar, double *gfac_ar, double *branch_ar, double *wt_frac,
                    double *lgmid_out, double *wtbin_out, double *brbin_out, double *gbin_out);

extern double *omega, *g_p, *g_pp;
extern int n_lve_out;

#endif
