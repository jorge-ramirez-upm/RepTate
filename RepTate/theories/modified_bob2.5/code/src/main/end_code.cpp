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

void close_files(void)
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
  if (debugfl != NULL)
  {
    fclose(debugfl);
  }
}

void end_code(void)
{

  close_files();
  extern int GenPolyOnly;
  if (GenPolyOnly != 0)
  {
    extern std::vector <polycopy> br_copy;
    extern int num_poly;
    for (int i = 0; i < br_copy.size(); i++)
    {
      br_copy[i].armindx.clear();
      br_copy[i].priority.clear();
      br_copy[i].assigned_trelax.clear();
      br_copy[i].trelax.clear();
      br_copy[i].zeta.clear();
      br_copy[i].relax_end.clear();
      br_copy[i].assigned_taus.clear();
      br_copy[i].taus.clear();
 
      // hopefully deallocate the memory
      br_copy[i].armindx.shrink_to_fit();
      br_copy[i].priority.shrink_to_fit();
      br_copy[i].assigned_trelax.shrink_to_fit();
      br_copy[i].trelax.shrink_to_fit();
      br_copy[i].zeta.shrink_to_fit();
      br_copy[i].relax_end.shrink_to_fit();
      br_copy[i].assigned_taus.shrink_to_fit();
      br_copy[i].taus.shrink_to_fit();
    }
    br_copy.clear();
    br_copy.shrink_to_fit();

    extern std::vector <double> t_maxwell;
    t_maxwell.clear();
    t_maxwell.shrink_to_fit();

    extern int CalcNlin;
    if (CalcNlin == 0)
    {
      extern std::vector< std::vector <double> > nlin_prio_phi_relax;
      extern std::vector< std::vector <double> > nlin_prio_phi_held;
      for (int i=0; i<nlin_prio_phi_relax.size(); i++){
        nlin_prio_phi_relax[i].clear();
        nlin_prio_phi_held[i].clear();
        nlin_prio_phi_relax[i].shrink_to_fit();
        nlin_prio_phi_held[i].shrink_to_fit();
      }
        nlin_prio_phi_relax.clear();
        nlin_prio_phi_held.clear();
        nlin_prio_phi_relax.shrink_to_fit();
        nlin_prio_phi_held.shrink_to_fit();
    }

    extern std::vector <double> omega, g_p, g_pp;
    omega.clear();
    g_p.clear();
    g_pp.clear();
  }
  extern std::vector <arm> arm_pool;
  extern std::vector <polymer> branched_poly;
  extern std::vector <double> phi_hist;

  phi_hist.clear();
  arm_pool.clear();
  branched_poly.clear();
  // hopefully deallocate the memory
  phi_hist.shrink_to_fit();
  arm_pool.shrink_to_fit();
  branched_poly.shrink_to_fit();

}
