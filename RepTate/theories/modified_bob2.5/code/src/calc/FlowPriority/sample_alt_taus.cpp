/*
sample_alt_taus.cpp : This file is part bob-rheology (bob) 
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
#include <math.h>
void sample_alt_taus(void)
{
  extern std::vector<polymer> branched_poly;
  extern std::vector<polycopy> br_copy;
  extern double cur_time;
  extern std::vector<arm> arm_pool;
  extern void alt_taus_assign(int, int, double);
  extern void alt_taus_assign2(int, int, double);
  extern int nlin_relaxing_arm(int, double);
  extern int num_poly;

  for (int i = 0; i < num_poly; i++)
  {
    if (branched_poly[i].alive)
    {
      int n1 = branched_poly[i].first_free;
      //  int orig_narm=br_copy[i].narm;
      double tau_s = arm_pool[n1].arm_len * arm_pool[n1].arm_len;
      alt_taus_assign(i, n1, tau_s);

      if (arm_pool[n1].compound)
      {
        double zeff = arm_pool[n1].arm_len_eff;
        int na = nlin_relaxing_arm(n1, zeff);
        if (na != n1)
        { // zeff is beyond n1
          double zlen = arm_pool[n1].arm_len;
          int nb = arm_pool[n1].nxt_relax;
          while (nb != na)
          { // Check nb and assign diff const
            zlen += arm_pool[nb].arm_len;
            alt_taus_assign(i, nb, cur_time);
            nb = arm_pool[nb].nxt_relax;
          }
          zlen += arm_pool[na].arm_len;
          if ((zlen - zeff) / arm_pool[na].arm_len < 1.0e-2)
          {
            alt_taus_assign(i, na, cur_time);
          }
          else
          {
            alt_taus_assign2(i, na, cur_time);
          }
        }
      }

      int n2 = arm_pool[n1].free_down;
      while (n2 != n1)
      {

        double tau_s = arm_pool[n2].arm_len * arm_pool[n2].arm_len;
        alt_taus_assign(i, n2, tau_s);

        if (arm_pool[n2].compound)
        {
          double zeff = arm_pool[n2].arm_len_eff;
          int na = nlin_relaxing_arm(n2, zeff);
          if (na != n2)
          { // zeff is beyond n2
            double zlen = arm_pool[n2].arm_len;
            int nb = arm_pool[n2].nxt_relax;
            while (nb != na)
            { // Check nb and assign diff const
              zlen += arm_pool[nb].arm_len;
              alt_taus_assign(i, nb, cur_time);
              nb = arm_pool[nb].nxt_relax;
            }
            zlen += arm_pool[na].arm_len;
            if ((zlen - zeff) / arm_pool[na].arm_len < 1.0e-2)
            {
              alt_taus_assign(i, na, cur_time);
            }
            else
            {
              alt_taus_assign2(i, na, cur_time);
            }
          }
        }

        n2 = arm_pool[n2].free_down;
      }
    } // branched_poly[i].alive
    else
    {
      if (br_copy[i].active == 0)
      {
        br_copy[i].active = -1;
        for (int j = 0; j < br_copy[i].narm; j++)
        {
          if (br_copy[i].assigned_taus[j] != 0)
          {
            if (br_copy[i].assigned_taus[j] == 1)
            {
              br_copy[i].assigned_taus[j] = 0;
            }
            else
            {
              br_copy[i].assigned_taus[j] = 0;
              br_copy[i].taus[j] = cur_time; // for now just put in suitable marker
            }
          }
        }
      }
    }
  } // end loop over polymers
}

void alt_taus_assign(int i, int n1, double tau_s)
{
  extern std::vector<polycopy> br_copy;
  extern std::vector<arm> arm_pool;
  int k = arm_pool[n1].copy_num;
  if (br_copy[i].assigned_taus[k] != 0)
  {
    br_copy[i].assigned_taus[k] = 0;
    br_copy[i].taus[k] = tau_s;
  }
}

void alt_taus_assign2(int i, int n1, double tau_s)
{
  extern std::vector<polycopy> br_copy;
  extern std::vector<arm> arm_pool;
  int k = arm_pool[n1].copy_num;
  if (br_copy[i].assigned_taus[k] != 0 && br_copy[i].assigned_taus[k] != 1)
  {
    br_copy[i].assigned_taus[k] = 1;
    br_copy[i].taus[k] = tau_s;
  }
}
