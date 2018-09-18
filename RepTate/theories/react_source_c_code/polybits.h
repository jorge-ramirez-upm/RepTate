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
#ifndef POLYBITS_H
#define POLYBITS_H

#include <stdbool.h>
#include "react_structs.h"

extern polybits_global_const pb_global_const;
extern polybits_global pb_global;

extern arm *arm_pool;
extern polymer *br_poly;
extern reactresults *react_dist;

extern void react_pool_init(void);
extern void pool_reinit(void);
extern bool request_arm(int *); // returns false if no arms left
extern void return_arm(int);
extern bool request_poly(int *); // returns false if no polymers left
extern void return_poly_arms(int);
extern void return_poly(int);
extern bool request_dist(int *); // returns false if no distributions left
extern void return_dist(int);
extern void return_dist_polys(int);
extern void armupdown(int, int);
extern reactresults *return_react_dist(int i);

// random number generator seed
extern long iy3;

#endif
