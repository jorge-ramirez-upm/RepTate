/*
genProto.cpp : This file is part bob-rheology (bob) 
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

#include "../../../include/bob.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void genProto(int ni, int nf)
{
  extern int runmode;
  extern std::vector<polymer> branched_poly;
  extern double mass_mono;
  if (runmode != 3)
  {
    printf("Looking for prototype file ...  ");
  }
  extern FILE *protofl;
  extern bool reptate_flag;
  if (!reptate_flag)
  {
    if (protofl == NULL)
    {
      protofl = fopen("poly.proto", "r");
    }
    if (protofl == NULL)
    {
      errmsg(101);
    }
  }
  extern char polycode[10];

  int err;
  extern int getline(FILE *, char *);
  char tmpcar[256];
  if (reptate_flag)
  {
    /* case 0: send filename containing polyconf input 
         case 1: send polycode for prototype (max 9 caracters) */
    int code = 1;
    get_string(tmpcar, code);
  }
  else
    err = getline(protofl, tmpcar);

  int nnk = strlen(tmpcar);
  if (nnk < 9)
  {
    for (int k2 = 0; k2 < nnk; k2++)
    {
      polycode[k2] = tmpcar[k2];
    }
    polycode[nnk] = '\0';
  }
  else
  {
    for (int k2 = 0; k2 < 9; k2++)
    {
      polycode[k2] = tmpcar[k2];
    }
    polycode[9] = '\0';
  }

  int narm;

  // fscanf(protofl, "%d", &narm);
  narm = (int)get_next_proto();

  int *arm_type = new int[narm];
  int *LL1 = new int[narm];
  int *LL2 = new int[narm];
  int *RR1 = new int[narm];
  int *RR2 = new int[narm];
  double *mass = new double[narm];
  double *pdi = new double[narm];
  for (int j = 0; j < narm; j++)
  {
    // fscanf(protofl, "%d %d %d %d %d %lf %lf", &LL1[j], &LL2[j], &RR1[j], &RR2[j],
    //        &arm_type[j], &mass[j], &pdi[j]);
    LL1[j] = (int)get_next_proto();
    LL2[j] = (int)get_next_proto();
    RR1[j] = (int)get_next_proto();
    RR2[j] = (int)get_next_proto();
    arm_type[j] = (int)get_next_proto();
    mass[j] = get_next_proto();
    pdi[j] = get_next_proto();
    mass[j] = mass[j] / mass_mono;
    if (arm_type[j] != 0)
    {
      mass[j] = mass[j] / pdi[j];
    }
  }

  for (int i = ni; i < nf; i++)
  {
    branched_poly[i] = polygenProto(narm, arm_type, LL1, LL2, RR1, RR2, mass, pdi);
  }
  extern FILE *infofl;
  extern bool reptate_flag;
  if (!reptate_flag)
    fprintf(infofl, "created %d %s \n", nf - ni, polycode);

  delete[] LL1;
  delete[] LL2;
  delete[] RR1;
  delete[] RR2;
  delete[] arm_type;
  delete[] mass;
  delete[] pdi;
}
