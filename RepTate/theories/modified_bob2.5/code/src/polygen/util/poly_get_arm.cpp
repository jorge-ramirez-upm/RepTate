/*
poly_get_arm.cpp : This file is part bob-rheology (bob) 
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

// returns an arm of the given type
#include "../../../include/bob.h"
#include <math.h>
#include <stdio.h>
double poly_get_arm(int arm_type, double mn_arm, double pdi)
{
  double cur_arm;
  extern double N_e;
  extern int runmode;
  double logprob;
  switch (arm_type)
  {
  case 0:
    cur_arm = mn_arm / N_e;
    break; // monodisperse
  case 1:
    cur_arm = armlen_gaussian(mn_arm, pdi) / N_e;
    break; // Gaussian
  case 2:
    cur_arm = armlen_lognormal(mn_arm, pdi) / N_e;
    break; //Lognormal
  case 3:
    cur_arm = armlen_semiliving(mn_arm, pdi) / N_e;
    break;
  case 4:
    logprob = log(1.0 - 1.0 / mn_arm);
    cur_arm = flory_distb(logprob) / N_e;
    break;
  default:
    if (runmode == 3)
    {
      extern FILE *errfl;
      fprintf(errfl, "Unknown arm type %d \n", arm_type);
      fprintf(errfl, "Assuming monodisperse. \n");
    }
    else
    {
      printf("Unknown arm type %d \n", arm_type);
      printf("Assuming monodisperse. \n");
    }
    cur_arm = mn_arm / N_e;
    break;
  }

  return (cur_arm);
}
