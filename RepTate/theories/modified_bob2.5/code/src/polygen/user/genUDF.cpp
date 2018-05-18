/*
genUDF.cpp : This file is part bob-rheology (bob) 
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

/* User defined polymer : The skeletal code */

#include "../../../include/bob.h"
#include <stdio.h>
#define UDF_segment_num 9 // The polymer has this many segments

void genUDF(int ni, int nf)
{
  extern FILE *infofl;
  extern FILE *inpfl;
  extern double mass_mono;
  extern int runmode;
  extern std::vector<polymer> branched_poly;

  int arm_type[UDF_segment_num];
  double mass[UDF_segment_num];
  double pdi[UDF_segment_num];

  if (runmode == 3)
  { // non-interactive mode : read from input file
    for (int i = 0; i < UDF_segment_num; i++)
    {
      fscanf(inpfl, "%d %le %le", &arm_type[i], &mass[i], &pdi[i]);
    }
  }
  else
  { // interactive mode
    for (int i = 0; i < UDF_segment_num; i++)
    { // user_get_arm_type prompts to input one arm at a time
      printf("User Defined Polymer : segment index i \n");
      user_get_arm_type(&arm_type[i], &mass[i], &pdi[i]);
    }
  }

  fprintf(infofl, "User defined polymer with %d segments \n", UDF_segment_num);
  for (int i = 0; i < UDF_segment_num; i++)
  {
    print_arm_type(arm_type[i], mass[i], pdi[i]);
    // express mass in terms of number of monomer. convert to M_N
    mass[i] = mass[i] / mass_mono;
    if (arm_type[i] != 0)
    {
      mass[i] = mass[i] / pdi[i];
    }
  }

  for (int i = ni; i < nf; i++)
  { // The first polymer is ni. (nf - ni) UDF polymer
    branched_poly[i] = polygenUDF(arm_type, mass, pdi);
  }

  fprintf(infofl, "Created %d user defined polymers \n", nf - ni);
}
