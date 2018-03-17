// RepTate: Rheology of Entangled Polymers: Toolkit for the Analysis of Theory and Experiments
// --------------------------------------------------------------------------------------------------------

// Authors:
//     Jorge Ramirez, jorge.ramirez@upm.es
//     Victor Boudara, victor.boudara@gmail.com

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
#include <stdlib.h>
#include <math.h>

static double calculate_fene(double l_square, double lmax)
{
    //calculate finite extensibility function value
    double ilm2, l2_lm2;
    ilm2 = 1.0 / (lmax * lmax); // 1/lambda_max^2
    l2_lm2 = l_square * ilm2;   //(lambda/lambda_max)^2
    return (3.0 - l2_lm2) / (1.0 - l2_lm2) * (1.0 - ilm2) / (3.0 - ilm2);
}

void derivs_rp_blend_shear(double *deriv, double *sigma, double *phi, double *taus, double *taud, double *p, double t)
{
    //Calculates the derivaties at time t
    // sigma is an array of size c*n^2 (c=3 in shear, c=2 in uext)
    // phi, taus, taud are arrays of size n

    double *stretch;
    double lmax, beta, delta, gamma_dot;
    double trace, tdi, tdj, tsi, tsj, li, lj, ret, rep, rccr, auxj;
    double sxx, syy, sxy;
    int i, j;
    int n;
    int with_fene;
    int I, c = 3;

    n = p[0];
    lmax = p[1];
    beta = p[2];
    delta = p[3];
    gamma_dot = p[4];
    with_fene = p[5];

    stretch = (double *)malloc(sizeof(double) * n);
    for (i = 0; i < n; i++)
    {
        I = c * n * i;
        trace = 0;
        for (j = 0; j < n; j++)
        {
            trace += phi[j] * (sigma[I + c * j] + 2 * sigma[I + c * j + 1]);
        }
        stretch[i] = sqrt(trace / 3.0);
    }

    for (i = 0; i < n; i++)
    {
        I = c * n * i;
        tdi = taud[i];
        tsi = taus[i];
        li = stretch[i];
        ret = 2.0 * (1.0 - 1.0 / li) / tsi;
        if (with_fene == 1)
        {
            ret *= calculate_fene(li * li, lmax);
        }

        for (j = 0; j < n; j++)
        {
            tdj = taud[j];
            tsj = taus[j];
            sxx = sigma[I + c * j];
            syy = sigma[I + c * j + 1];
            sxy = sigma[I + c * j + 2];
            lj = stretch[j];
            rep = 1.0 / (2.0 * tdi) + 1.0 / (2.0 * tdj); // assumes beta_thermal = 1

            auxj = 2.0 * beta * (1.0 - 1.0 / lj) / tsj;
            if (with_fene == 1)
            {
                auxj *= calculate_fene(lj * lj, lmax);
            }
            rccr = auxj * pow(li, 2.0 * delta);

            deriv[I + c * j] = 2.0 * gamma_dot * sxy - rep * (sxx - 1.0) - ret * sxx - rccr * (sxx - 1.0);
            deriv[I + c * j + 1] = -rep * (syy - 1.0) - ret * syy - rccr * (syy - 1.0);
            deriv[I + c * j + 2] = gamma_dot * syy - rep * sxy - ret * sxy - rccr * sxy;
        }
    }
    free(stretch);
}

void derivs_rp_blend_uext(double *deriv, double *sigma, double *phi, double *taus, double *taud, double *p, double t)
{
    //Calculates the derivaties at time t
    // sigma is an array of size c*n^2 (c=3 in shear, c=2 in uext)
    // phi, taus, taud are arrays of size n

    double *stretch;
    double lmax, beta, delta, epsilon_dot;
    double trace, tdi, tdj, tsi, tsj, li, lj, ret, rep, rccr, auxj;
    double sxx, syy;
    int i, j;
    int n;
    int with_fene;
    int I;
    int c = 2;

    n = p[0];
    lmax = p[1];
    beta = p[2];
    delta = p[3];
    epsilon_dot = p[4];
    with_fene = p[5];

    stretch = (double *)malloc(sizeof(double) * n);
    for (i = 0; i < n; i++)
    {
        I = c * n * i;
        trace = 0;
        for (j = 0; j < n; j++)
        {
            trace += phi[j] * (sigma[I + c * j] + 2 * sigma[I + c * j + 1]);
        }
        stretch[i] = sqrt(trace / 3.0);
    }

    for (i = 0; i < n; i++)
    {
        I = c * n * i;
        tdi = taud[i];
        tsi = taus[i];
        li = stretch[i];
        ret = 2.0 * (1.0 - 1.0 / li) / tsi;
        if (with_fene == 1)
        {
            ret *= calculate_fene(li * li, lmax);
        }

        for (j = 0; j < n; j++)
        {
            tdj = taud[j];
            tsj = taus[j];
            sxx = sigma[I + c * j];
            syy = sigma[I + c * j + 1];
            lj = stretch[j];
            rep = 1.0 / (2.0 * tdi) + 1.0 / (2.0 * tdj); // assumes beta_thermal = 1

            auxj = 2.0 * beta * (1.0 - 1.0 / lj) / tsj;
            if (with_fene == 1)
            {
                auxj *= calculate_fene(lj * lj, lmax);
            }
            rccr = auxj * pow(li, 2.0 * delta);

            deriv[I + c * j] = 2.0 * epsilon_dot * sxx - rep * (sxx - 1.0) - ret * sxx - rccr * (sxx - 1.0);
            deriv[I + c * j + 1] = -epsilon_dot * syy - rep * (syy - 1.0) - ret * syy - rccr * (syy - 1.0);
        }
    }
    free(stretch);
}