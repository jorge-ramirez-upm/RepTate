/*
time_step.cpp : This file is part of bob-rheology (bob) 
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

// relax for one time unit : first time called with zero
#include "../../include/bob.h"
#include "./relax.h"
#include <stdio.h>
int time_step(int indx)
{
  extern double cur_time, DtMult, phi, deltaphi;
  extern std::vector <arm> arm_pool;
  extern std::vector <polymer> branched_poly;
  extern int num_poly;
  int num_alive = 0;

#ifdef NBETA
  extern int CalcNlin;
  extern int nlin_num_data_av, nlin_collect_data;
  if (CalcNlin == 0)
  {
    if (nlin_collect_data == 0)
    {
      nlin_num_data_av++;
    }
  }
#endif

  if (indx != 0)
    cur_time = cur_time * DtMult;

  for (int i = 0; i < num_poly; i++)
  { // arm_retraction : collapse
    if (branched_poly[i].alive)
    {
      int n1 = branched_poly[i].first_free;
      int n2 = arm_pool[n1].free_down;
      arm_retraction(n1, indx);
#ifdef NBETA
      if (CalcNlin == 0)
      {
        if (nlin_collect_data == 0)
        {
          nlin_retraction(n1);
        }
        if (arm_pool[n1].compound)
        {
          sample_eff_arm_len(n1);
        }
      }
#endif
      while (n2 != n1)
      {
        arm_retraction(n2, indx);
#ifdef NBETA
        if (CalcNlin == 0)
        {
          if (nlin_collect_data == 0)
          {
            nlin_retraction(n2);
          }
          if (arm_pool[n2].compound)
          {
            sample_eff_arm_len(n2);
          }
        }
#endif
        n2 = arm_pool[n2].free_down;
      }

      n2 = arm_pool[n1].free_down; // extend_arm : calculate Z_eff : uncollapse
      if ((!arm_pool[n1].prune) && (!arm_pool[n1].ghost))
        extend_arm(i, n1);
      while (n2 != n1)
      {
        if ((!arm_pool[n2].prune) && (!arm_pool[n2].ghost))
          extend_arm(i, n2);
        n2 = arm_pool[n2].free_down;
      }
      del_ghost(i);
      if (branched_poly[i].alive)
        prune_chain(i);
    }
  } // end of arm_retraction

  for (int i = 0; i < num_poly; i++)
  { //check for reptation and count live number
    if (branched_poly[i].alive)
    {
      if (!branched_poly[i].linear_tag)
        check_linearity(i);
      if (branched_poly[i].linear_tag)
      {
        if (try_reptate(i))
        {
#ifdef NBETA
          if (CalcNlin == 0)
          {
            if (nlin_collect_data == 0)
            {
              reptate_nlin(i);
            }
          }
#endif
          rept_sv_mass(i);
          branched_poly[i].alive = false;
        }
        else
        {
          num_alive += 1;
        }
      }
      else
      {
        num_alive += 1;
      } // not yet linear
    }
  } // end checking for reptation.

  extern double phi_true, phi_ST;
  double phi_old = phi;
  double phi_true_old = phi_true;
  double phi_ST_old = phi_ST;

  phi = frac_unrelaxed(); //get currect phi
  deltaphi = phi - phi_old;
#ifdef NBETA
  if (CalcNlin == 0)
  {
    extern double nlin_phi_true, nlin_phi_ST, nlin_dphi_true, nlin_dphi_ST;
    if (nlin_collect_data == 0)
    {
      nlin_phi_true += phi_true;
      nlin_phi_ST += phi_ST;
      nlin_dphi_true += (phi_true_old - phi_true);
      nlin_dphi_ST += (phi_ST_old - phi_ST);
      calc_nlin_phi_held();
    }
  }
#endif
  return (num_alive);
}
