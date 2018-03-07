/*
lin_time_resp.cpp : This file is part bob-rheology (bob) 
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
#include "./lin_rheo.h"
void lin_time_resp(int ndata, double * tp, double * phip, double * phip_ST)
{
FILE * resfl;
extern int OutMode;
switch(OutMode){
case 1 : resfl=fopen("gt.agr","w"); graceheadergt(resfl); break;
case 2 : resfl=fopen("goft.gt","w"); break;
default : resfl=fopen("gt.dat","w"); break;
               }
double tt, goft_slow, goft_fast, phnow, phstnow; tt=0.00010;
bool calc_gt_fast=true;
extern double Alpha, unit_time, G_0_unit;

for (int i1=0; i1 < 300; i1++) {
   if(i1==0) {tt=0.00010;}
   else      {tt=tt*1.20;}
   goft_slow=0.0;
     for (int j=1; j<ndata; j++) {
phnow=0.50*(phip[j-1]+phip[j]); phstnow=0.50*(phip_ST[j-1]+phip_ST[j]);
goft_slow+=exp(-tt/tp[j-1])*
   (Alpha*phnow*pow(phstnow,Alpha)*(phip_ST[j-1]-phip_ST[j])/phstnow
 + pow(phstnow,Alpha)*(phip[j-1]-phip[j])); }
   if(calc_gt_fast) {
      goft_fast=fast_real_hist(tt);
      if(goft_fast < (0.01 * goft_slow)) calc_gt_fast=false; }
   else   {goft_fast=0.0;}
fprintf(resfl,"%e %e \n",tt*unit_time, (goft_slow+goft_fast)*G_0_unit);
 }
if(OutMode == 2){fprintf(resfl,"& \n");}
fclose(resfl);

}
