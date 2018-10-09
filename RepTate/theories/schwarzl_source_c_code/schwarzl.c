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

/* 
Numerical formulae for calculations of elastic and loss moduli from relaxation
modulus using Schwarzl method (1971), Rheologica Acta.

compile library for python using
gcc -o ../schwarzl_Gt.so -shared -fPIC -O2 schwarzl_Gt.c 
*/
#include <stdlib.h>
#include <math.h>

double LinearInterpolate(
    double y1, double y2,
    double mu)
{
    return (y1 * (1 - mu) + y2 * mu);
}

double CosineInterpolate(
    double y1, double y2,
    double mu)
{
    double mu2;
    mu2 = (1 - cos(mu * M_PI)) / 2;
    return (y1 * (1 - mu2) + y2 * mu2);
}

void schwarzl_gt(int n_data, double *value_G_of_t, double *time_G_of_t, double *out_wp, double *out_Gp, double *out_wpp, double *out_Gpp)
{
    //temporary variables
    double t, Gp, G2p;
    double a, b, c, d, e, f, g, k;
    double tintmin, tintmax, mu;
    double *times, *gvalues;
    int m, p, N, ref_time_index;
    int i, j, start, finish;

    //output
    // double **omega_Gp_omega_Gpp;
    // omega_Gp_omega_Gpp = (double **)malloc(sizeof(double *) * 4); //create 4 columns: | w1 | G'(w1) | w2 | G''(w2) |
    // for (j = 0; j < 4; j++)
    // {
    //     omega_Gp_omega_Gpp[j] = (double *)malloc(sizeof(double) * n_data);
    // }
    // for (j = 0; j < 4; j++)
    // {
    //     for (i = 0; i < n_data; i++)
    //     {
    //         omega_Gp_omega_Gpp[j][i] = 0.0;
    //     }
    // }
    //*********************************
    //         Elastic Modulus
    //*********************************

    // index0: t/64, index1: t/32, ... index6: t, index7: 2*t, index8: 4*t, index9: 8*t
    N = 10;             //number of time indexes
    ref_time_index = 6; //index number of the value 't'
    times = (double *)malloc(sizeof(double) * N);
    gvalues = (double *)malloc(sizeof(double) * N);

    //coefficients from Schwarzl 1970 - Rheologica Acta
    a = -0.142;
    b = 0.717;
    c = 0.046;
    d = 0.099;
    e = 0.103;
    f = 0.0010;
    g = 0.00716;
    k = 0.000451;
    start = 0;
    finish = n_data;
    if (time_G_of_t[0] == 0.0) //skip t=0 value
    {
        start++;
    }
    if (time_G_of_t[n_data - 1] == 0.0) //skip t=0 value
    {
        finish--;
    }
    for (i = start; i < finish; i++)
    {
        times[0] = time_G_of_t[i] / 64.; //set up the time indexes
        for (p = 1; p < N; p++)
            times[p] = times[p - 1] * 2.;
        p = 0;
        while (p < N)
        {
            if (times[p] <= time_G_of_t[0])
                gvalues[p] = value_G_of_t[0]; //set the out-of-range time values by extending the boundary points
            else if (time_G_of_t[n_data - 1] <= times[p])
                gvalues[p] = value_G_of_t[n_data - 1];
            else
            { // linear interpolation to get the values of G(t) at the different time indexes
                m = 0;
                while (time_G_of_t[m] < times[p])
                    m++;
                tintmin = time_G_of_t[m - 1];
                tintmax = time_G_of_t[m];
                mu = (times[p] - tintmin) / (tintmax - tintmin);
                gvalues[p] =
                    //CosineInterpolate(value_G_of_t[m-1], value_G_of_t[m], mu);
                    LinearInterpolate(value_G_of_t[m - 1], value_G_of_t[m], mu);
                //value_G_of_t[m-1]*(1-mu)+value_G_of_t[m]*mu;
            }
            p++;
        }
        //Formulae for G' from Schwarzl 1970 - Rheologica Acta
        Gp = gvalues[6] + a * (gvalues[8] - gvalues[9]) + b * (gvalues[7] - gvalues[8]) + c * (gvalues[6] - gvalues[7]) + d * (gvalues[5] - gvalues[6]) + e * (gvalues[4] - gvalues[5]) + f * (gvalues[3] - gvalues[4]) + g * (gvalues[2] - gvalues[3]) + k * (gvalues[0] - gvalues[1]);

        out_wp[i] = 1. / times[ref_time_index];
        out_Gp[i] = Gp;
    }

    //*********************************
    //         Loss Modulus
    //*********************************

    //coefficients from Schwarzl 1970 - Rheologica Acta
    a = -0.441;
    b = 1.547;
    c = 0.412;
    d = 0.397;
    e = 0.191;
    f = 0.0668;
    g = 0.0181;
    k = 0.0;
    //index0: t/64, index1: t/32, index2: t/16, index3: t/8, index4: t/4, index5: t/2, index6: t, index7: 2*t, index8: 4*t
    N = 9;
    ref_time_index = 6; // //index number of the value 't'
    for (i = start; i < finish; i++)
    {
        times[0] = time_G_of_t[i] / 64.;
        for (p = 1; p < N; p++)
            times[p] = times[p - 1] * 2.;
        times[ref_time_index] = time_G_of_t[i];
        p = 0;
        while (p < N)
        {
            if (times[p] <= time_G_of_t[0])
                gvalues[p] = value_G_of_t[0]; //set the out-of-range time values by extending the boundary points
            else if (time_G_of_t[n_data - 1] <= times[p])
                gvalues[p] = value_G_of_t[n_data - 1];
            else
            { // linear interpolation to get the values of G(t) at the different time indexes
                m = 0;
                while (time_G_of_t[m] < times[p])
                    m++;
                tintmin = time_G_of_t[m - 1];
                tintmax = time_G_of_t[m];
                mu = (times[p] - tintmin) / (tintmax - tintmin);
                gvalues[p] =
                    //CosineInterpolate(value_G_of_t[m-1], value_G_of_t[m], mu);
                    LinearInterpolate(value_G_of_t[m - 1], value_G_of_t[m], mu);
                //value_G_of_t[m-1]*(1-mu)+value_G_of_t[m]*mu;
            }
            p++;
        }
        //Formulae for G'' from Schwarzl 1970 - Rheologica Acta
        G2p = 0.03125 * 2.12 * (gvalues[0] - gvalues[1]) + a * (gvalues[7] - gvalues[8]) + b * (gvalues[6] - gvalues[7]) + c * (gvalues[5] - gvalues[6]) + d * (gvalues[4] - gvalues[5]) + e * (gvalues[3] - gvalues[4]) + f * (gvalues[2] - gvalues[3]) + g * (gvalues[1] - gvalues[2]);

        out_wpp[i] = 1. / times[ref_time_index];
        out_Gpp[i] = G2p;
    }
    free(times);
    free(gvalues);
}