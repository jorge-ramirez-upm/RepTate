/*
init_var_nlin.cpp : This file is part bob-rheology (bob) 
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
#include <vector> 

void init_var_nlin(void)
{
extern std::vector< std::vector <double> > nlin_prio_phi_relax;
extern std::vector< std::vector <double> > nlin_prio_phi_held;
extern int max_prio_var, NumNlinStretch;

for(int i=0; i< max_prio_var; i++){ for(int j=0; j<NumNlinStretch; j++){
 nlin_prio_phi_relax[i][j]=0.0; nlin_prio_phi_held[i][j]=0.0; }}

extern int nlin_collect_data; nlin_collect_data=0;
extern int nlin_num_data_av; nlin_num_data_av=0;
extern double nlin_phi_true, nlin_phi_ST, nlin_dphi_true, nlin_dphi_ST;
nlin_phi_true=0.0; nlin_phi_ST=0.0; nlin_dphi_true=0.0; nlin_dphi_ST=0.0;

}

