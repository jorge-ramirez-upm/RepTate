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

// Copyright (2017-2020): Jorge Ramirez, Victor Boudara, Universidad Politécnica de Madrid, University of Leeds


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
#define FUNC(x) ((*func)(x))

double trapzd(double (*func)(double), double a, double b, int n)
{
	double x, tnm, sum, del;
	static double s;
	int it, j;

	if (n == 1)
	{
		return (s = 0.5 * (b - a) * (FUNC(a) + FUNC(b)));
	}
	else
	{
		for (it = 1, j = 1; j < n - 1; j++)
			it <<= 1;
		tnm = it;
		del = (b - a) / tnm;
		x = a + 0.5 * del;
		for (sum = 0.0, j = 1; j <= it; j++, x += del)
			sum += FUNC(x);
		s = 0.5 * (s + (b - a) * sum / tnm);
		return s;
	}
}
#undef FUNC
