/*
genCayley.cpp : This file is part bob-rheology (bob) 
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
void genCayley(int ni, int nf)
{
  extern FILE *infofl;
  extern FILE *inpfl;
  extern double mass_mono;
  extern std::vector<polymer> branched_poly;

  extern int runmode;

  int levl;
  if (runmode == 2)
  {
    printf("We consider Cayley tree from inside out.\n");
    printf("generation 0 is just a star polymer. \n");
    printf("For higher gen, two more arms get added to the previous gen. \n");
    printf("How many generations the polymers have ? ...");
    scanf("%d", &levl);
  }
  else
  {
    fscanf(inpfl, "%d", &levl);
  }
  int *arm_type = new int[levl + 1];
  double *mass = new double[levl + 1];
  double *pdi = new double[levl + 1];
  if (runmode == 2)
  {
    for (int i = 0; i <= levl; i++)
    {
      printf("Information about generation %d : \n", i);
      user_get_arm_type(&arm_type[i], &mass[i], &pdi[i]);
    }
  }
  else
  {
    for (int i = 0; i <= levl; i++)
    {
      fscanf(inpfl, "%d %lf %lf", &arm_type[i], &mass[i], &pdi[i]);
    }
  }

  fprintf(infofl, "Selected Cayley tree. \n");
  for (int i = 0; i <= levl; i++)
  {
    fprintf(infofl, " Generation %d :", i);
    print_arm_type(arm_type[i], mass[i], pdi[i]);
    mass[i] = mass[i] / mass_mono;
    if (arm_type[i] != 0)
    {
      mass[i] = mass[i] / pdi[i];
    }
  }
  for (int i = ni; i < nf; i++)
  {
    branched_poly[i] = polygenCayley(levl, &arm_type[0], &mass[0], &pdi[0]);
  }

  fprintf(infofl, "Created %d Cayley trees \n", nf - ni);

  delete[] arm_type;
  delete[] mass;
  delete[] pdi;
}
