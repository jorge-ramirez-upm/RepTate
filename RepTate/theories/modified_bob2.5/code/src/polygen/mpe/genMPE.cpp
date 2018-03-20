/*
genMPE.cpp : This file is part bob-rheology (bob) 
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
void genMPE(int ni, int nf)
{
extern FILE* infofl; extern FILE* inpfl;
extern polymer * branched_poly;
double mass,beta;
extern int runmode;
if(runmode == 2)
{
printf("M_W ? .."); scanf("%le", &mass);
printf("Av. number of branch per molecule, b_m ? .."); scanf("%le", &beta);
}
else
{
fscanf(inpfl, "%le %le", &mass, &beta);
}
fprintf(infofl, "Selected metallocene PE \n");

  mass=mass/(2.0*(beta + 1.0));

  fprintf(infofl, "b_m = %e \n",beta);
  fprintf(infofl, "M_n = %e \n",mass);
  fprintf(infofl, "lambda = %e \n", 14.0e3 * beta/mass);
  fprintf(infofl, "P_B = %e \n", beta/(1.0+2.0*beta));
  fprintf(infofl, "M_w = %e \n", 2.0*(beta+1.0)*mass);

  double prop_prob = 1.0 - 28.0 *(beta+1.0)/mass;
  double mono_prob = (1.0 - 28.0 * (2.0*beta + 1.0)/mass)/prop_prob;

  fprintf(infofl, "Propagation probability = %e \n", prop_prob);
  fprintf(infofl, "Monomer addition probability = %e \n", mono_prob);

  for (int i=ni; i<nf; i++)
   {
    branched_poly[i]=polygenMPE(prop_prob,mono_prob);
   }

  fprintf(infofl, "created %d metallocene-PE polymers. \n",nf-ni);

}
