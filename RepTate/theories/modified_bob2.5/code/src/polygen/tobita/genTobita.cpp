/*
genTobita.cpp : This file is part bob-rheology (bob) 
bob-2.5 : rheology of Branch-On-Branch polymers
Copyright (C) 2006-2011, 2012 C. Das, D.J. Read, T.C.B. McLeish
 
  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 3 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details. You can find a copy
  of the license at <http://www.gnu.org/licenses/gpl.txt>
*/

// Checked 3 Oct 2008
#include "../../../include/bob.h"
#include <stdio.h>

void genTobita(int ni, int nf)
{
  extern FILE *infofl;
  extern FILE *inpfl;
  extern std::vector<polymer> branched_poly;
  double tau, beta, cs, cb, fin_conv;
  extern int runmode;
  extern polymer polygenTobita(double, double, double, double, double);
  if (runmode == 2)
  {
    printf("LDPE : Tobita scheme \n");
    printf("tau ?   ");
    scanf("%lf", &tau);
    printf("beta ?   ");
    scanf("%lf", &beta);
    printf("cs ?   ");
    scanf("%lf", &cs);
    printf("cb ?   ");
    scanf("%lf", &cb);
    printf("final conversion ?   ");
    scanf("%lf", &fin_conv);
  }
  else
  {
    fscanf(inpfl, "%lf %lf %lf %lf %lf", &tau, &beta, &cs, &cb, &fin_conv);
  }

  fprintf(infofl, "Selected LDPE polymers \n");
  fprintf(infofl, "tau=%e, beta=%e, cs=%e, cb=%e, fin_conv=%e \n", tau, beta, cs, cb, fin_conv);
  for (int i = ni; i < nf; i++)
  {
    branched_poly[i] = polygenTobita(tau, beta, cs, cb, fin_conv);
  }
  fprintf(infofl, "Created %d LDPE  polymers \n", nf - ni);
}
