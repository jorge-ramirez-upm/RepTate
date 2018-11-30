/*
genMPE_wtav.cpp : This file is part bob-rheology (bob) 
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
#include <math.h>
void genMPE_wtav(int ni, int nf)
{
  extern FILE *infofl;
  extern FILE *inpfl;
  extern std::vector<polymer> branched_poly;
  double mass, b_m;
  extern int runmode;
  int wtav_poly_type = 0;
  extern bool reptate_flag;
  if (runmode == 2)
  {
    printf(" Weight averaged ensemble for MPE \n");
    printf("M_W ? ..");
    scanf("%le", &mass);
    printf("Av. number of branch per molecule, b_m ? ..");
    scanf("%le", &b_m);
  }
  else
  {
    // fscanf(inpfl, "%le %le", &mass, &b_m);
    mass = get_next_inp();
    b_m = get_next_inp();
  }
  if (!reptate_flag)
    fprintf(infofl, "Selected weight averaged metallocene PE \n");

  mass = mass / (2.0 * (b_m + 1.0));
  double mn_arm = mass / (2.0 * b_m + 1.0);
  mn_arm = mn_arm / 28.0; // segment length
  if (!reptate_flag)
  {
    fprintf(infofl, "b_m = %e \n", b_m);
    fprintf(infofl, "M_n = %e \n", mass);
    fprintf(infofl, "lambda = %e \n", 14.0e3 * b_m / mass);
    fprintf(infofl, "P_B = %e \n", b_m / (1.0 + 2.0 * b_m));
    fprintf(infofl, "M_w = %e \n", 2.0 * (b_m + 1.0) * mass);
  }
  double prop_prob = 1.0 - 28.0 * (b_m + 1.0) / mass;
  double mono_prob = (1.0 - 28.0 * (2.0 * b_m + 1.0) / mass) / prop_prob;

  if (!reptate_flag)
  {
    fprintf(infofl, "Propagation probability = %e \n", prop_prob);
    fprintf(infofl, "Monomer addition probability = %e \n", mono_prob);
  }
  double logprob = log(1.0 - 1.0 / mn_arm);
  double b_u = b_m / (1.0 + 2.0 * b_m);
  for (int i = ni; i < nf; i++)
  {
    branched_poly[i] = polygen_wtav(wtav_poly_type, logprob, b_u);
  }

  if (!reptate_flag)
    fprintf(infofl, "created %d wt av metallocene-PE polymers. \n", nf - ni);
}
