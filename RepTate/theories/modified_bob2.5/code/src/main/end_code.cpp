/*
end_code.cpp : This file is part of bob-rheology (bob) 
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

// deallocate memory; close open files;

#include <stdio.h>
#include <stdlib.h>
#include "../../include/bob.h"

void end_code(void)
{
  extern FILE *infofl;
  extern FILE *errfl;
  extern FILE *debugfl;
  if (infofl != NULL)
  {
    fclose(infofl);
  }
  if (errfl != NULL)
  {
    fclose(errfl);
  }
  if (debugfl != NULL)
  {
    fclose(debugfl);
  }

  extern int GenPolyOnly;
  if (GenPolyOnly != 0)
  {
    extern polycopy *br_copy;
    extern int num_poly;
    for (int i = 0; i < num_poly; i++)
    {
      delete[] br_copy[i].armindx;
      delete[] br_copy[i].priority;
      delete[] br_copy[i].assigned_trelax;
      delete[] br_copy[i].trelax;
      delete[] br_copy[i].zeta;
      delete[] br_copy[i].relax_end;
      delete[] br_copy[i].assigned_taus;
      delete[] br_copy[i].taus;
    }

    extern double *t_maxwell;
    delete[] t_maxwell;

    extern int CalcNlin;
    if (CalcNlin == 0)
    {
      extern double **nlin_prio_phi_relax;
      extern double **nlin_prio_phi_held;
      extern int max_prio_var;
      extern void delete_ar_2d_double(double **ar, int m);
      delete_ar_2d_double(nlin_prio_phi_relax, max_prio_var);
      delete_ar_2d_double(nlin_prio_phi_held, max_prio_var);
    }

    extern double *omega, *g_p, *g_pp;
    delete[] omega;
    delete[] g_p;
    delete[] g_pp;
  }
  extern arm *arm_pool;
  extern polymer *branched_poly;
  extern double *phi_hist;
  delete[] phi_hist;
  delete[] arm_pool;
  delete[] branched_poly;
}
