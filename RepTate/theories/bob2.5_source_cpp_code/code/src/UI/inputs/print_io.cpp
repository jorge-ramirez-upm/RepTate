/*
print_io.cpp : This file is part bob-rheology (bob) 
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
 
// dump input to info file. Open info strem out here.
#include <stdio.h>
void print_io(void)
{
extern FILE * infofl;
fprintf(infofl,"\n parameters after reading inputs: \n");

extern double Alpha, RetLim, PSquare, mass_mono, N_e, G_0_unit, temp; 
extern double unit_time,rho_poly,ReptAmount;
extern int  PrefMode, ReptScheme;
fprintf(infofl,"alpha  = %e \n",Alpha);
fprintf(infofl,"R_L  = %e \n",RetLim);
fprintf(infofl,"p^2  = %e \n",2.0*PSquare);
fprintf(infofl,"Mass of monomer  = %e \n",mass_mono);
fprintf(infofl,"N_e  = %e \n",N_e);
G_0_unit = 6651.58 * (rho_poly*temp/(N_e*mass_mono)); //Pa
fprintf(infofl,"Temperature (input) = %e \n",temp);
fprintf(infofl,"G_0 = %e \n", G_0_unit);
fprintf(infofl,"tau_e = %e sec \n \n",unit_time);

switch(PrefMode){
case 0 : 
fprintf(infofl,"compound arm prefactor same as outermost arm.\n"); break;
case 1 : 
fprintf(infofl,"compound arm prefactor includes effective armlen.\n"); break;
case 2 : 
fprintf(infofl,"compound arm prefactor includes effective friction.\n");break;
                 }

switch(ReptScheme){
case 1:fprintf(infofl,"Reptation in thin tube.\n"); break;
case 2:fprintf(infofl,"Reptation in current tube.\n"); break;
case 3:fprintf(infofl,"Rept in tube from time at which %le lengh chain reptate \n",ReptAmount); break;
case 4:fprintf(infofl,"Rept in tube from time at which %le fraction chain reptate \n",ReptAmount); break;
                   }
fprintf(infofl,"\n End of input parameters \n");
}
