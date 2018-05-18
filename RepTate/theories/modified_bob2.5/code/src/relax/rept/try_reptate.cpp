/*
try_reptate.cpp : This file is part bob-rheology (bob) 
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
bool try_reptate(int n)
{
  extern std::vector<arm> arm_pool;
  extern std::vector<polymer> branched_poly;
  extern double phi, cur_time, Alpha, PSquare, RetLim;
  extern int ReptScheme;
  double drag_sidebranch, bbonelen, len_to_rep;
  double drag_tot, tau_d;

  int n1 = branched_poly[n].first_free;
  int n2 = arm_pool[n1].free_down;
  if (n1 == n2) //dealing with one arm linear
  {
    drag_sidebranch = arm_pool[n1].extra_drag;
    bbonelen = arm_pool[n1].arm_len_end;
    len_to_rep = arm_pool[n1].arm_len_end - arm_pool[n1].z;
  }
  else //two arm linear
  {
    drag_sidebranch = arm_pool[n1].extra_drag + arm_pool[n2].extra_drag;
    bbonelen = arm_pool[n1].arm_len_end + arm_pool[n2].arm_len_end;
    len_to_rep = arm_pool[n1].arm_len_end - arm_pool[n1].z +
                 arm_pool[n2].arm_len_end - arm_pool[n2].z;
  }

  n1 = branched_poly[n].first_end;
  n2 = arm_pool[n1].down;
  if (!arm_pool[n1].relaxing)
  {
    bbonelen += arm_pool[n1].arm_len;
    len_to_rep += arm_pool[n1].arm_len;
  }
  while (n2 != n1)
  {
    if (!arm_pool[n2].relaxing)
    {
      bbonelen += arm_pool[n2].arm_len;
      len_to_rep += arm_pool[n2].arm_len;
    }
    n2 = arm_pool[n2].down;
  }
  drag_sidebranch += branched_poly[n].ghost_contrib;

  if (ReptScheme == 1) // bare tube
  {
    drag_tot = drag_sidebranch / PSquare +
               3.0 * pi_pow_2 * bbonelen;
    tau_d = drag_tot * len_to_rep * len_to_rep / pi_pow_2;
  }
  else if (ReptScheme == 2) // final dilated tube
  {
    drag_tot = drag_sidebranch / (PSquare * pow(phi, Alpha)) +
               3.0 * pi_pow_2 * bbonelen;
    tau_d = drag_tot * len_to_rep * len_to_rep * pow(phi, Alpha) / pi_pow_2;
  }
  else // inbetween tube
  {
    if (branched_poly[n].rept_set)
    {
      double phi_rept = branched_poly[n].phi_rept;
      drag_tot = drag_sidebranch / (PSquare * pow(phi_rept, Alpha)) +
                 3.0 * pi_pow_2 * bbonelen;
      tau_d = drag_tot * len_to_rep * len_to_rep * pow(phi_rept, Alpha) / pi_pow_2;
    }
    else
    {
      extern double ReptAmount; // Rept_scheme == 3/4
      drag_tot = drag_sidebranch / (PSquare * pow(phi, Alpha)) +
                 3.0 * pi_pow_2 * bbonelen;
      if (ReptScheme == 3)
      {
        tau_d = drag_tot * ReptAmount * ReptAmount * pow(phi, Alpha) / pi_pow_2;
      }
      else
      {
        tau_d = drag_tot * pow((ReptAmount * bbonelen), (double)2) * pow(phi, Alpha) / pi_pow_2;
      }
      if (cur_time > tau_d)
      {
        branched_poly[n].rept_set = true;
        branched_poly[n].phi_rept = phi;
      }
      if (cur_time > 0.001)
        tau_d = 2.0 * cur_time;
      else
        tau_d = 1.0;
    }
  }
  if (len_to_rep < (2.0 * RetLim / phi))
  {
    tau_d = cur_time - 1.0e-6;
  }

  return (cur_time > tau_d);
}
