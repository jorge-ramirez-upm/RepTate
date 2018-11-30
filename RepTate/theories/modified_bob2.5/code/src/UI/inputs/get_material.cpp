/*
get_material.cpp : This file is part bob-rheology (bob) 
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
#include "../../../include/bob.h"
void get_material(void)
{
  extern double N_e, unit_time, temp, mass_mono, rho_poly;
  extern int runmode;
  if (runmode == 2)
  {
    printf("\n");
    printf("Mass of a monomer (in atomic unit, ex.:PE->28.0) ?  ");
    scanf("%le", &mass_mono);
    printf("Number of monomers in an entanglement length ?  ");
    scanf("%le", &N_e);
    printf("mass-density of the polymer (in g/cc) ?  ");
    scanf("%le", &rho_poly);
    printf("Entanglement time tau_e (s) ?  ");
    scanf("%le", &unit_time);
    printf("Temperature (Kelvin) ? ");
    scanf("%le", &temp);
    printf("\n");
  }
  else
  {
    extern FILE *inpfl;
    // fscanf(inpfl, "%le %le %le", &mass_mono, &N_e, &rho_poly);
    // fscanf(inpfl, "%le %le ", &unit_time, &temp);
    mass_mono = get_next_inp();
    N_e = get_next_inp();
    rho_poly = get_next_inp();
    unit_time = get_next_inp();
    temp = get_next_inp();

  }

  if (rho_poly < 2.0)
  { // the input is in g/cc : convert to kg/m^3
    rho_poly = 1000.0 * rho_poly;
  }

  extern double FreqMin, FreqMax;
  FreqMin = FreqMin * unit_time;
  FreqMax = FreqMax * unit_time;
}
