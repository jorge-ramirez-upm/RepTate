/*
output_nlin.cpp : This file is part bob-rheology (bob) 
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

#include <stdio.h>
#include <math.h>
#include <vector>
#include "../../RepTate/reptate_func.h"

void output_nlin(void)
{
  extern FILE *nlin_outfl;
  extern double nlin_phi_true, nlin_phi_ST, nlin_dphi_true, nlin_dphi_ST, Alpha;
  extern int nlin_num_data_av, NumNlinStretch;
  extern int nlin_collect_data;
  extern int num_maxwell, nlin_nxt_data;
  extern double nlin_t_min, nlin_t_max, NlinAvDt;
  extern std::vector<double> t_maxwell;

  nlin_phi_true = nlin_phi_true / ((double)nlin_num_data_av);
  nlin_phi_ST = nlin_phi_ST / ((double)nlin_num_data_av);

  double w_split = nlin_dphi_true * exp(Alpha * log(nlin_phi_ST));
  double tmpvar = nlin_dphi_true * exp(Alpha * log(nlin_phi_ST));
  tmpvar += Alpha * nlin_phi_true * exp((Alpha - 1.0) * log(nlin_phi_ST)) * nlin_dphi_ST;
  w_split = w_split / tmpvar;

  int num_modes = 0;
  extern int max_prio_var;
  extern std::vector<std::vector<double> > nlin_prio_phi_relax;
  extern std::vector<std::vector<double> > nlin_prio_phi_held;


  double tot_phi_relax, tot_phi_held;
  tot_phi_relax = 0.0;
  tot_phi_held = 0.0;

  for (int i = 0; i < max_prio_var; i++)
  {
    for (int j = 0; j < NumNlinStretch; j++)
    {
      if (nlin_prio_phi_relax[i][j] > 1.0e-16)
      {
        tot_phi_relax += nlin_prio_phi_relax[i][j];
        num_modes++;
      }
      if (nlin_prio_phi_held[i][j] > 1.0e-16)
      {
        tot_phi_held += nlin_prio_phi_held[i][j];
        num_modes++;
      }
    }
  }

  extern double StretchBinWidth;
  extern double unit_time;
  double cur_t_maxwell = t_maxwell[nlin_nxt_data] * unit_time;
  // fprintf(nlin_outfl, "%e %d \n", cur_t_maxwell, num_modes);
  std::vector<double> temp;
  temp.resize(2);
  temp[0] = cur_t_maxwell;
  temp[1] = num_modes;
  vector_nlin_outfl.push_back(temp);
  double cur_rate;


  temp.resize(3);
  for (int i = 0; i < max_prio_var; i++)
  {
    cur_rate = 1.0;
    for (int j = 0; j < NumNlinStretch; j++)
    {
      if (nlin_prio_phi_relax[i][j] > 1.0e-16)
      {
        // fprintf(nlin_outfl, "%d %e %e \n", i + 1,
                // (1.0 - w_split) * nlin_prio_phi_relax[i][j] / tot_phi_relax, cur_rate);
      temp[0] = i + 1;
      temp[1] = (1.0 - w_split) * nlin_prio_phi_relax[i][j] / tot_phi_relax;
      temp[2] = cur_rate;
      vector_nlin_outfl.push_back(temp);
      }
      if (nlin_prio_phi_held[i][j] > 1.0e-16)
      {
        // fprintf(nlin_outfl, "%d %e %e \n", i + 1,
                // w_split * nlin_prio_phi_held[i][j] / tot_phi_held, cur_rate);
        temp[0] = i + 1;
        temp[1] = w_split * nlin_prio_phi_held[i][j] / tot_phi_held;
        temp[2] = cur_rate;
        vector_nlin_outfl.push_back(temp);
      }
      cur_rate = cur_rate * StretchBinWidth;
    }
  }

  extern int nlin_collect_data;
  extern int num_maxwell, nlin_nxt_data;
  extern double nlin_t_min, nlin_t_max, NlinAvDt;
  extern std::vector<double> t_maxwell;
  nlin_collect_data = -1;
  nlin_nxt_data++;
  if (nlin_nxt_data < num_maxwell)
  {
    nlin_t_min = t_maxwell[nlin_nxt_data] / NlinAvDt;
    nlin_t_max = t_maxwell[nlin_nxt_data] * NlinAvDt;
  }
  else
  {
    nlin_t_min = nlin_t_max = 1.0e32;
  }
}
