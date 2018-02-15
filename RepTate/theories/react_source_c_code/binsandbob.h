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
#ifndef BINSANDBOB_H
#define BINSANDBOB_H

#include <stdbool.h>
#include "react_structs.h"

extern void molbin(int);
extern void multimolbin(int reqbins, double *weights, int *dist, int ndists);
extern void bobinit(int n);
extern void bobcount(int m, int n);
extern void polyconfwrite(int, char *fname);
unsigned long long multipolyconfwrite(char *fname, double *weights, int *dists, int n_inmix);
// extern void multipolyconfwrite(char *fname, double *weights, bool *inmix, int *numsaved_out);
extern double return_binsandbob_multi_avbr(int i);
extern double return_binsandbob_multi_avg(int i);
extern double return_binsandbob_multi_lgmid(int i);
extern double return_binsandbob_multi_wmass(int i);
extern double return_binsandbob_multi_wt(int i);
extern void set_react_dist_monmass(int i, double monmass);
extern void set_react_dist_M_e(int i, double M_e);

extern binsandbob_global bab_global;

#endif
