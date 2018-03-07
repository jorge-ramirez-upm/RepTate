/*
genH.cpp : This file is part bob-rheology (bob) 
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
void genH(int ni, int nf)
{
 extern FILE* infofl; extern FILE * inpfl;
 extern double mass_mono;
 extern polymer * branched_poly;

extern int runmode;
 double m_arm, m_cross, pdi_arm, pdi_cross;
 int arm_type1, arm_type2;

if(runmode == 2){
printf("First we need information about the four side arms. \n");
user_get_arm_type(&arm_type1,&m_arm,&pdi_arm);
printf("Now information about the backbone. \n");
user_get_arm_type(&arm_type2,&m_cross,&pdi_cross);
                }
else{
   fscanf(inpfl, "%d", &arm_type1);
   fscanf(inpfl, "%le %le", &m_arm, &pdi_arm);
   fscanf(inpfl, "%d", &arm_type2);
   fscanf(inpfl, "%le %le", &m_cross, &pdi_cross);
    }

 fprintf(infofl,"Selected H polymer\n");
 fprintf(infofl,"Side arms : ");
 print_arm_type(arm_type1, m_arm, pdi_arm);
 fprintf(infofl,"Backbone : ");
 print_arm_type(arm_type2, m_cross, pdi_cross);

  m_arm=m_arm/mass_mono; if(arm_type1 != 0) {m_arm=m_arm/pdi_arm;}
 m_cross=m_cross/mass_mono; if(arm_type2 != 0) {m_cross = m_cross/pdi_cross;}
 for (int i=ni; i<nf; i++)
  {
branched_poly[i]=polygenH(arm_type1,m_arm,pdi_arm,arm_type2,m_cross,pdi_cross);
  }

 fprintf(infofl,"Created %d H  polymers \n", nf-ni);
}




