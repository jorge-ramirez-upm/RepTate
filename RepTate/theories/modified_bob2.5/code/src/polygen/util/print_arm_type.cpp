/*
print_arm_type.cpp : This file is part bob-rheology (bob) 
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
void print_arm_type(int arm_type, double mass, double pdi)
{
  extern FILE *infofl;
  extern FILE *errfl;
  extern bool reptate_flag;
  if (reptate_flag)
    return;
  switch (arm_type)
  {
  case 0:
    fprintf(infofl, ": monodisperse with M_w = %le", mass);
    break;
  case 1:
    fprintf(infofl, "from Gaussian distribution with M_w = %le and PDI = %le", mass, pdi);
    break;
  case 2:
    fprintf(infofl, "from Lognormal distribution with M_w = %le and PDI = %le", mass, pdi);
    break;
  case 3:
    fprintf(infofl, "from (semi)Living distribution with M_w = %le and PDI = %le", mass, pdi);
    break;
  case 4:
    fprintf(infofl, "from Flory distribution with M_w = %le and PDI = %le", mass, pdi);
    break;
  default:
    fprintf(errfl, "ERROR : Found wrong arm_type in print_arm_type.cpp \n");
    break;
  }
  fprintf(infofl, "\n");
}
