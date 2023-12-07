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

// Copyright (2017-2023): Jorge Ramirez, Victor Boudara, Universidad Politécnica de Madrid, University of Leeds


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
#include <stdbool.h>
#include <math.h>
#include "trapz.h"
// #define EPS 1.0e-5
#define JMAX 20

double qtrap(double (*func)(double), double a, double b, bool *success, double EPS)
{
	int j;
	double s, olds = 0.0;

	for (j = 1; j <= JMAX; j++)
	{
		s = trapzd(func, a, b, j);
		if (j > 5)
			if (fabs(s - olds) < EPS * fabs(olds) ||
				(s == 0.0 && olds == 0.0))
			{
				*success = true;
				return s;
			}
		olds = s;
	}
	*success = false;
	return 0.0;
}
#undef EPS
#undef JMAX
