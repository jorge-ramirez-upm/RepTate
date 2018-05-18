/*
frac_unrelaxed.cpp : This file is part bob-rheology (bob) 
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

/* fraction of unrelaxed material phi.  Uses supertube relaxation.
Returns true fraction if supertube is not activated.
Else returns the fraction at the begining of supertube activation */
#include <math.h>
#include "../../../include/bob.h"
#include <stdio.h>

double frac_unrelaxed(void)
{
  static bool supertube_activated = false;
  static double phi_ST_0 = 1.0;
  static double ST_activ_time = 1.0;
  extern int num_poly;
  extern std::vector<arm> arm_pool;
  extern std::vector<polymer> branched_poly;
  extern double phi, phi_true, cur_time, phi_ST, DtMult;
  int n1, n2;
  double tmpvar;
  extern int SlavePhiToPhiST;
  extern double Alpha;

  phi_true = 0.0;
  double phi_mol;
  double LtRsLHS;
  LtRsLHS = 0.0;
  extern int LateRouse;
  for (int i = 0; i < num_poly; i++)
  {
    if (branched_poly[i].alive)
    {
      phi_mol = 0.0;
      n1 = branched_poly[i].first_free;
      phi_mol += (arm_pool[n1].arm_len_end - arm_pool[n1].z) * arm_pool[n1].vol_fraction / arm_pool[n1].arm_len;
      n2 = arm_pool[n1].free_down;
      while (n2 != n1)
      {
        phi_mol += (arm_pool[n2].arm_len_end - arm_pool[n2].z) * arm_pool[n2].vol_fraction / arm_pool[n2].arm_len;
        n2 = arm_pool[n2].free_down;
      }
      n1 = branched_poly[i].first_end;
      if (!arm_pool[n1].relaxing)
      {
        phi_mol += arm_pool[n1].vol_fraction;
      }
      n2 = arm_pool[n1].down;
      while (n2 != n1)
      {
        if (!arm_pool[n2].relaxing)
        {
          phi_mol += arm_pool[n2].vol_fraction;
        }
        n2 = arm_pool[n2].down;
      }
      phi_true += phi_mol;
      if (LateRouse == 0)
      {
        LtRsLHS += branched_poly[i].wtfrac *
                   exp(1.50 * log(branched_poly[i].gfac * phi_mol * branched_poly[i].molmass / branched_poly[i].wtfrac)) /
                   branched_poly[i].molmass;
      }
    }
  }

  if (LateRouse == 0)
  {
    extern double LtRsFactor;
    extern int LtRsActivated;
    if (LtRsActivated != 0)
    {
      if (LtRsLHS < LtRsFactor)
      {
        LtRsActivated = 0;
        printf("Late Rouse : LtRsLHS = %e , phi_true = %e \n", LtRsLHS, phi_true);
      }
    }
  }

  if (!supertube_activated)
  {
    if (phi_true < (phi * exp(-log(DtMult) / (2.0 * Alpha))))
    {
      supertube_activated = true;
      phi_ST_0 = phi;
      ST_activ_time = cur_time / DtMult;
      phi_ST = phi * exp(-log(DtMult) / (2.0 * Alpha));
      if (SlavePhiToPhiST == 0)
      {
        return (phi_ST);
      }
      else
      {
        return (phi);
      }
    }
    else
    {
      phi_ST = phi_true;
      return (phi_true);
    }
  }
  else
  {
    tmpvar = phi_ST_0 * exp(log(ST_activ_time / cur_time) / (2.0 * Alpha));
    if (tmpvar > phi_true)
    {
      phi_ST = tmpvar;
      // Changes 15 Oct 2008. Let the chain explore via Rouse dynamics
      // return(phi_ST);
      if (SlavePhiToPhiST == 0)
      {
        return (phi_ST);
      }
      else
      {
        return (phi);
      }
    }
    else
    {
      phi_ST = phi_true;
      supertube_activated = false;
      return (phi_true);
    }
  }
}
