/*
genstargel.cpp : This file is part bob-rheology (bob) 
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
void genstargel(int ni, int nf)
{
  extern FILE *infofl;
  extern FILE *inpfl;
  extern double mass_mono;
  extern std::vector<polymer> branched_poly;
  extern int runmode;
  int arm_type;
  double mass, pdi;
  double reaction_extent;
  if (runmode == 3)
  {
    fscanf(inpfl, "%d %le %le", &arm_type, &mass, &pdi);
    fscanf(inpfl, "%le", &reaction_extent);
  }
  else
  {
    user_get_arm_type(&arm_type, &mass, &pdi);
    printf(" Extent of reaction (p) ?  ");
    scanf("%le", &reaction_extent);
  }

  fprintf(infofl, "Selected crosslinked Star ");
  print_arm_type(arm_type, mass, pdi);

  mass = mass / mass_mono;
  if (arm_type != 0)
  {
    mass = mass / pdi;
  }

  for (int i = ni; i < nf; i++)
  {
    branched_poly[i] = polygenstargel(reaction_extent, arm_type, mass, pdi);
  }
}
