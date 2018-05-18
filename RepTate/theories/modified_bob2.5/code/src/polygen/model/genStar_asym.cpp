/*
genStar_asym.cpp : This file is part bob-rheology (bob) 
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
void genStar_asym(int ni, int nf)
{
  extern FILE *infofl;
  extern FILE *inpfl;
  extern double mass_mono;
  extern std::vector<polymer> branched_poly;
  extern int runmode;
  int arm_type, arm_type_short;
  double mass, pdi, mass_short, pdi_short;
  if (runmode == 3)
  {
    fscanf(inpfl, "%d", &arm_type);
    fscanf(inpfl, "%le %le", &mass, &pdi);
    fscanf(inpfl, "%d", &arm_type_short);
    fscanf(inpfl, "%le %le", &mass_short, &pdi_short);
  }
  else
  {
    printf("Long arms : \n");
    user_get_arm_type(&arm_type, &mass, &pdi);
    printf("Short arm : \n");
    user_get_arm_type(&arm_type_short, &mass_short, &pdi_short);
  }

  fprintf(infofl, "Selected asymmetric Star ");
  print_arm_type(arm_type, mass, pdi);

  mass = mass / mass_mono;
  if (arm_type != 0)
  {
    mass = mass / pdi;
  }
  mass_short = mass_short / mass_mono;
  if (arm_type_short != 0)
  {
    mass_short = mass_short / pdi_short;
  }

  for (int i = ni; i < nf; i++)
  {
    branched_poly[i] = polygenStar_asym(arm_type, mass, pdi, arm_type_short, mass_short, pdi_short);
  }
  fprintf(infofl, "created %d asymmetric Stars \n", nf - ni);
}
