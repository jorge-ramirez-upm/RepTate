/*
genGEL_wtav.cpp : This file is part bob-rheology (bob) 
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
void genGEL_wtav(int ni, int nf)
{
  extern FILE *infofl;
  extern FILE *inpfl;
  extern std::vector<polymer> branched_poly;
  extern double mass_mono;
  double mn_arm, b_u;
  extern int runmode;
  int wtav_poly_type = 1;
  if (runmode == 2)
  {
    printf(" Weight averaged gelation polymer ensemble \n");
    printf("segment molar mass M_{N,S} ? ..");
    scanf("%le", &mn_arm);
    printf("branching prob p ? ..");
    scanf("%le", &b_u);
  }
  else
  {
    fscanf(inpfl, "%le %le", &mn_arm, &b_u);
  }
  fprintf(infofl, "Selected weight averaged gelation ensemble \n");

  fprintf(infofl, "M_{N,S} = %e \n", mn_arm);
  fprintf(infofl, "p = %e \n", b_u);

  mn_arm = mn_arm / mass_mono; // segment length

  double logprob = log(1.0 - 1.0 / mn_arm);
  for (int i = ni; i < nf; i++)
  {
    branched_poly[i] = polygen_wtav(wtav_poly_type, logprob, b_u);
  }

  fprintf(infofl, "created %d wt av gelation polymers. \n", nf - ni);
}
