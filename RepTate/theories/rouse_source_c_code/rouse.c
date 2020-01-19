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
#include <stdlib.h>
#include <stdio.h>
#include <math.h>

void continuous_rouse_freq_interp(int n, double G, double tau, double N, double *w, double *gp, double *gpp)
{ //Continuous Rouse model in frequency domain with interpolation
    double aux, temp, temp2;
    int i, p;
    int N1, N2;

    if (N == 0)
        return;

    N1 = floorf(N);
    N2 = ceilf(N);
    if (N1 == N2)
    {
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
    else
    {
        double temp1sq, temp2sq;
        double sum1p[n];
        double sum1pp[n];
        double sum2p[n];
        double sum2pp[n];
        for (i = 0; i < n; i++)
        {
            sum1p[i] = 0.0;
            sum2p[i] = 0.0;
            sum1pp[i] = 0.0;
            sum2pp[i] = 0.0;
        }
        for (p = 1; p <= N1; p++)
        {

            aux = tau / (2.0 * p * p);
            for (i = 0; i < n; i++)
            {
                temp = w[i] * aux;
                temp1sq = temp * N1 * N1;
                temp1sq *= temp1sq;
                temp2sq = temp * N2 * N2;
                temp2sq *= temp2sq;

                sum1p[i] += temp1sq / (1.0 + temp1sq);
                sum2p[i] += temp2sq / (1.0 + temp2sq);

                sum1pp[i] += temp * N1 * N1 / (1.0 + temp1sq);
                sum2pp[i] += temp * N2 * N2 / (1.0 + temp2sq);
            }
        }
        // case p = N2 (= N1+1)
        for (i = 0; i < n; i++)
        {
            aux = w[i] * tau;
            aux *= aux;
            sum2p[i] += aux / (1.0 + aux);
            sum2pp[i] += w[i] * tau / (1.0 + aux);
        }

        aux = (double)(N - N1) / (double)(N2 - N1);
        for (i = 0; i < n; i++) // interpolate
        {
            gp[i] = G * ((1.0 - aux) * sum1p[i] / N1 + aux * sum2p[i] / N2);
            gpp[i] = G * ((1.0 - aux) * sum1pp[i] / N1 + aux * sum2pp[i] / N2);
        }
    }
}

void continuous_rouse_time_interp(int n, double G, double tau, double N, double *t, double *gt)
{ //Continuous Rouse model in time domain with interpolation
    double aux;
    int i, p;
    int N1, N2;

    if (N == 0)
        return;

    N1 = floorf(N);
    N2 = ceilf(N);
    if (N1 == N2)
    {
        for (p = 1; p <= N; p++)
        {
            aux = -2.0 * p * p / (N * N * tau);
            for (i = 0; i < n; i++)
                gt[i] += exp(aux * t[i]);
        }
        for (i = 0; i < n; i++)
            gt[i] *= G / N;
    }
    else
    {
        double sum1[n];
        double sum2[n];
        for (i = 0; i < n; i++)
        {
            sum1[i] = 0.0;
            sum2[i] = 0.0;
        }
        for (p = 1; p <= N1; p++)
        {
            aux = -2.0 * p * p / tau;
            for (i = 0; i < n; i++)
            {
                sum1[i] += exp(t[i] * aux / (N1 * N1));
                sum2[i] += exp(t[i] * aux / (N2 * N2));
            }
        }
        // case p = N2 (= N1+1)
        for (i = 0; i < n; i++)
            sum2[i] += exp(-2.0 * t[i] / tau);

        aux = (double)(N - N1) / (double)(N2 - N1);
        for (i = 0; i < n; i++) // interpolate
            gt[i] = G * ((1.0 - aux) * sum1[i] / N1 + aux * sum2[i] / N2);
    }
}
