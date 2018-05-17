/*
genLin.cpp : This file is part bob-rheology (bob) 
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
void genLin(int ni, int nf)
{
extern FILE* infofl; extern FILE * inpfl;
extern int  runmode;
extern std::vector <polymer> branched_poly;
extern double mass_mono;
double seglen, mass,pdi;
int arm_type;

if(runmode == 3){ //batch mode
fscanf(inpfl, "%d", &arm_type);
fscanf(inpfl, "%lf %lf", &mass, &pdi);
                }
else{ user_get_arm_type(&arm_type,&mass,&pdi); }

fprintf(infofl,"Selected linear polymer ");
print_arm_type(arm_type, mass, pdi);


 mass=mass/mass_mono; if(arm_type != 0) {mass=mass/pdi;} 

for (int i=ni; i<nf; i++)
 {
  seglen=poly_get_arm(arm_type,mass, pdi);
  branched_poly[i]=polygenLin(seglen);
 }
 

fprintf(infofl, "created %d Linear polymers. \n",nf-ni); 
}

