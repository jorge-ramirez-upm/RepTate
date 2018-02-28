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

void continuous_rouse_freq(int n, double G, double tau, int N, double *w, double *gp, double *gpp)
{ //Continuous Rouse model in frequency domain
    double aux, temp, temp2;
    int i, p;

    if (N == 0)
        return;
    for (p = 1; p <= N; p++)
    {
        aux = N * N * tau / (2.0 * p * p);
        for (i = 0; i < n; i++)
        {
            temp = w[i] * aux;
            temp2 = temp * temp;
            gp[i] += temp2 / (1.0 + temp2);
            gpp[i] += temp / (1.0 + temp2);
        }
    }
    for (i = 0; i < n; i++)
    {
        gp[i] *= G / N;
        gpp[i] *= G / N;
    }
}

void continuous_rouse_time(int n, double G, double tau, int N, double *t, double *gt)
{ //Continuous Rouse model in time domain
    double aux;
    int i, p;

    if (N == 0)
        return;
    for (p = 1; p <= N; p++)
    {
        aux = -2.0 * p * p / (N * N * tau);
        for (i = 0; i < n; i++)
            gt[i] += exp(aux * t[i]);
    }
    for (i = 0; i < n; i++)
        gt[i] *= G / N;
}