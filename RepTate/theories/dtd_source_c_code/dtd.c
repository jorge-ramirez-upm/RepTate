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
#include <stdbool.h>
#include <math.h>
#include "qtrap.h"

static double a, tau_e, z, w, t;

double Ueff(double s)
{
    //Effective potential
    return 3 * z * (1.0 - pow(1.0 - s, 1.0 + a) * (1.0 + (1.0 + a) * s)) / (1.0 + a) / (2.0 + a);
}

double tau_early(double s)
{
    // Relaxation time early
    return 9.0 * pow(M_PI, 3) / 16 * tau_e * pow(s * z, 4);
}

double tau_late(double s)
{
    //Relaxation time arm
    return tau_e * pow(z, 1.5) * sqrt(pow(M_PI, 5) / 6) * exp(Ueff(s)) / sqrt(s * s * pow(1 - s, 2 * a) + pow((1.0 + a) / z / 3.0, 2 * a / (a + 1)) / exp(2 * lgamma(1 / (a + 1))));
}

double tau(double s)
{
    // Relaxation time for segment s
    double eUe, te, tl;

    eUe = exp(Ueff(s));
    te = tau_early(s);
    tl = tau_late(s);
    return te * eUe / (1.0 + eUe * te / tl);
}

double Gp(double s)
{
    // Integrand of the G'(w) function
    double sqrtau, sqrw;
    sqrtau = tau(s);
    sqrtau *= sqrtau;
    sqrw = w * w;
    return pow(1 - s, a) * sqrw * sqrtau / (1.0 + sqrw * sqrtau);
}

double Gpp(double s)
{
    // Integrand of the G''(w) function
    double t, sqrtau, sqrw;
    t = tau(s);
    sqrtau = t * t;
    sqrw = w * w;
    return pow(1 - s, a) * w * t / (1.0 + sqrw * sqrtau);
}

double GppRouse(double w)
{
    // G''(w) due to fast Rouse modes
    return exp(-1.0 / (w * z * z * tau_e)) * sqrt(tau_e * w);
}

bool dynamic_tube_dilution_freq(double G0, double a0, double tau_e0, double z0, int n, double *omega, double *gp, double *gpp, double EPS)
{
    double y;
    int i;
    bool success = true;

    // define global variables
    a = a0;
    tau_e = tau_e0;
    z = z0;

    for (i = 0; i < n; i++)
    {
        w = omega[i];
        y = qtrap(Gp, 0, 1, &success, EPS);
        if (!success)
        {
            return false;
        }
        gp[i] = (1 + a) * G0 * y + G0 * GppRouse(w);
        y = qtrap(Gpp, 0, 1, &success, EPS);
        if (!success)
        {
            return false;
        }
        gpp[i] = (1 + a) * G0 * y + G0 * GppRouse(w);
    }
    return true;
}

double Gt(double s)
{
    // Integrand of the G(t) function
    return pow(1 - s, a) * exp(-t / tau(s));
}

bool dynamic_tube_dilution_time(double G0, double a0, double tau_e0, double z0, int n, double *times, double *gt, double EPS)
{
    double y;
    int i;
    bool success = true;

    // define global variables
    a = a0;
    tau_e = tau_e0;
    z = z0;

    for (i = 0; i < n; i++)
    {
        t = times[i];
        y = qtrap(Gt, 0, 1, &success, EPS);
        if (!success)
        {
            return false;
        }
        gt[i] = (1 + a) * G0 * y;
    }
    return true;
}
