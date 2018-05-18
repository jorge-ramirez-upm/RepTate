/*
user_get_arm_type.cpp : This file is part bob-rheology (bob) 
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

//called via poly_start : set up arm variables correctly
#include <math.h>
#include <stdio.h>
#include "../../../include/bob.h"
void user_get_arm_type(int *arm_type, double *mass, double *pdi)
{
  printf("Type 0 for strictly monodisperse \n");
  printf("     1 for Gaussian distribution in segment lengths \n");
  printf("     2 for Lognormal  \n");
  printf("     3 for Semi-living (several monomer acts as unit to match PDI\n");
  printf("     4 for Flory distribution  \n");
  printf("arm type ?  ");
  scanf("%d", &arm_type[0]);
  if ((arm_type[0] < 0) || (arm_type[0] > 4))
  {
    printf("Unknown arm type %d \n", arm_type[0]);
    printf("Assuming monodisperse \n");
    arm_type[0] = 0;
  }

  printf("M_w of single segment (in g/mol) ?  ");
  scanf("%le", &mass[0]);

  if (arm_type[0] != 0)
  {
    printf("Polydispersity Index ?  ");
    scanf("%le", &pdi[0]);
  }
}
