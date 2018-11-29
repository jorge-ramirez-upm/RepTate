/*
genComb_fxd.cpp : This file is part bob-rheology (bob) 
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
void genComb_fxd(int ni, int nf)
{
  extern FILE *infofl;
  extern FILE *inpfl;
  extern double mass_mono;
  extern std::vector<polymer> branched_poly;
  extern int runmode;
  double m_bbone, m_arm;
  int num_arm;
  double pdi_arm, pdi_bbone;
  int arm_typeb, arm_typea;
  if (runmode == 2)
  {
    printf("Information about the backbone .. \n");
    user_get_arm_type(&arm_typeb, &m_bbone, &pdi_bbone);
    printf("Information about the side arms .. \n");
    user_get_arm_type(&arm_typea, &m_arm, &pdi_arm);
    printf("Number of side arms per molecule (integer) ?  ");
    scanf("%d", &num_arm);
  }
  else
  {
    fscanf(inpfl, "%d %le %le", &arm_typeb, &m_bbone, &pdi_bbone);
    fscanf(inpfl, "%d %le %le %d", &arm_typea, &m_arm, &pdi_arm, &num_arm);
  }
  extern bool reptate_flag;
  if (!reptate_flag)
  {
    fprintf(infofl, "Selected Comb with %d side-arms \n", num_arm);
    fprintf(infofl, "backbone : ");
  }
  print_arm_type(arm_typeb, m_bbone, pdi_bbone);
  if (!reptate_flag)
    fprintf(infofl, "side-arms :");
  print_arm_type(arm_typea, m_arm, pdi_arm);

  m_bbone = m_bbone / mass_mono;
  if (arm_typeb != 0)
  {
    m_bbone = m_bbone / pdi_bbone;
  }
  m_arm = m_arm / mass_mono;
  if (arm_typea != 0)
  {
    m_arm = m_arm / pdi_arm;
  }

  for (int i = ni; i < nf; i++)
  {
    branched_poly[i] = polygenComb_fxd(arm_typeb, m_bbone, pdi_bbone,
                                       arm_typea, m_arm, pdi_arm, num_arm);
  }

  if (!reptate_flag)
    fprintf(infofl, "created %d Comb polymers. \n", nf - ni);
}
