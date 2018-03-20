/*
dumpgpcres.cpp : This file is part bob-rheology (bob) 
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

#include <stdio.h>
#include <math.h>
#include <string.h>
#include "../../../include/bob.h"
void dumpgpcres(int ncomp, int nnn, double *wtbin, double *brbin,
                double *gbin, double lgmin, double lgstep)
{
  char fname[80];
  char extn[80];
  if (ncomp < 0)
  { // whole system
    strcpy(fname, "gpclssys.dat");
  }
  else
  {
    strcpy(fname, "gpcls");
    extern void inttochar(int, char *);
    inttochar(ncomp + 1, extn);
    strcat(fname, extn);
    strcpy(extn, ".dat");
    strcat(fname, extn);
  }

  FILE *ftmp = fopen(fname, "w");
  for (int i = 0; i < nnn; i++)
  {
    double lgmid = lgmin + (((double)i) + 0.5) * lgstep;
    fprintf(ftmp, "%e %e %e %e\n", exp(lgmid * log(10.0)), wtbin[i], brbin[i], gbin[i]);
  }
  fclose(ftmp);
}
