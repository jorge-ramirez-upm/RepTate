/*
gpclsutil.cpp : This file is part bob-rheology (bob) 
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

/* Calculate GPC LS data for component ncomp with polymers from ni to nf */
/* Utility codes that are needed */

#include "../../../include/bob.h"

double gpc_calc_mass(int i)
{
  extern std::vector <polymer> branched_poly;
  extern std::vector <arm> arm_pool;
  int n0 = branched_poly[i].first_end;
  double mass = arm_pool[n0].arm_len;
  int nd = arm_pool[n0].down;
  while (nd != n0)
  {
    mass += arm_pool[nd].arm_len;
    nd = arm_pool[nd].down;
  }
  extern double N_e, mass_mono;
  mass = mass * N_e * mass_mono;
  return mass;
}

double gpc_calc_wtfrac(int i)
{
  extern std::vector <polymer> branched_poly;
  extern std::vector <arm> arm_pool;
  int n0 = branched_poly[i].first_end;
  double mass = arm_pool[n0].vol_fraction;
  int nd = arm_pool[n0].down;
  while (nd != n0)
  {
    mass += arm_pool[nd].vol_fraction;
    nd = arm_pool[nd].down;
  }
  return mass;
}

int gpc_num_br(int i)
{
  extern std::vector <polymer> branched_poly;
  extern std::vector <arm> arm_pool;
  int n0 = branched_poly[i].first_end;
  int nn = 1;
  int nd = arm_pool[n0].down;
  while (nd != n0)
  {
    nn++;
    nd = arm_pool[nd].down;
  }
  nn = (nn - 1) / 2;
  return nn;
}

// Calculate ideal g factor.
// Use Kramer's decomposition for branched Rg
double gpc_calc_gfac(int m)
{
  extern std::vector <arm> arm_pool;
  extern std::vector <polymer> branched_poly;
  extern double left_mass(int);
  double rg_br = 0.0;
  double ntot = 0.0;
  int nbr = 1;
  int n1 = branched_poly[m].first_end;
  ntot += arm_pool[n1].arm_len;
  int n2 = arm_pool[n1].down;
  while (n2 != n1)
  {
    nbr++;
    ntot += arm_pool[n2].arm_len;
    n2 = arm_pool[n2].down;
  }

  if (nbr == 2)
  {
    return 1.0;
  }
  else
  {
    double n_left;
    n1 = branched_poly[m].first_end;
    double n_cur = arm_pool[n1].arm_len;
    n_left = left_mass(n1);
    rg_br += n_cur * (n_left * (ntot - n_left) + n_cur * ((0.50 * ntot - n_left) - n_cur / 3.0));
    n2 = arm_pool[n1].down;
    while (n2 != n1)
    {
      n_cur = arm_pool[n2].arm_len;
      n_left = left_mass(n2);
      rg_br += n_cur * (n_left * (ntot - n_left) + n_cur * ((0.50 * ntot - n_left) - n_cur / 3.0));
      n2 = arm_pool[n2].down;
    }

    rg_br = rg_br / (ntot * ntot);
    double g_fac = rg_br * 6.0 / ntot;
    return g_fac;
  }
}

double left_mass(int i)
{
  extern std::vector <arm> arm_pool;
  extern double recur_left_mass(int, int);
  int nL1, nL2;
  double mass = 0.0;
  if ((arm_pool[i].L1 == -1) && (arm_pool[i].L2 == -1))
  {
    return mass;
  }
  else
  {
    if ((nL1 = arm_pool[i].L1) != -1)
    {
      mass += recur_left_mass(nL1, i);
    }
    if ((nL2 = arm_pool[i].L2) != -1)
    {
      mass += recur_left_mass(nL2, i);
    }

    return mass;
  }
}

double recur_left_mass(int n1, int i)
{
  extern std::vector <arm> arm_pool;
  double mass = arm_pool[n1].arm_len;
  if ((arm_pool[n1].L1 == i) || (arm_pool[n1].L2 == i))
  { // travel right
    int nR1 = arm_pool[n1].R1;
    if (nR1 != -1)
    {
      mass += recur_left_mass(nR1, n1);
    }
    int nR2 = arm_pool[n1].R2;
    if (nR2 != -1)
    {
      mass += recur_left_mass(nR2, n1);
    }
  }
  else
  { // travel left
    int nL1 = arm_pool[n1].L1;
    if (nL1 != -1)
    {
      mass += recur_left_mass(nL1, n1);
    }
    int nL2 = arm_pool[n1].L2;
    if (nL2 != -1)
    {
      mass += recur_left_mass(nL2, n1);
    }
  }
  return mass;
}
