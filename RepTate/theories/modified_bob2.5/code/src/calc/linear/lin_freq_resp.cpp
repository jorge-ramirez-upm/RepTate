/*
lin_freq_resp.cpp : This file is part bob-rheology (bob) 
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
 
// Calculate G'(omega), G''(omega)
#include <stdio.h>
#include <math.h>
#include "./lin_rheo.h"
void lin_freq_resp(int ndata, double * tp, double * phip, double * phip_ST)
{

double gpslow, g2pslow,gpfast,g2pfast, freq,tmpvar,tmpvar1;
bool calc_gt_fast;
extern int OutMode;
FILE * resfourfl;
switch(OutMode){
 case 1 : resfourfl=fopen("gtp.agr","w"); graceheadergtp(resfourfl); break;
 case 2 : resfourfl=fopen("gtp.osc","w"); reptateheadergtp(resfourfl); break;
 default : resfourfl=fopen("gtp.dat","w"); break;
               }
extern double FreqMax, FreqMin, FreqInterval, G_0_unit, unit_time, Alpha;
double phnow, phstnow, tnow;

// grace needs two sets of data one after another. So a trivial loop
for(int kxx=0; kxx<2; kxx++){
calc_gt_fast=true;
freq=FreqMax*FreqInterval;
while(freq > FreqMin){
  freq=freq/FreqInterval; gpslow=0.0; g2pslow=0.0;
 for (int j=1; j<ndata; j++) {
       phnow=0.50*(phip[j-1]+phip[j]); 
       phstnow=0.50*(phip_ST[j-1]+phip_ST[j]); tnow=tp[j];
   tmpvar=freq*tnow/(1.0 + freq*freq*tnow*tnow);
   tmpvar1=phnow*Alpha*pow(phstnow,Alpha)*(phip_ST[j-1]-phip_ST[j])/phstnow +
                  pow(phstnow,Alpha)*(phip[j-1]-phip[j]);
   gpslow+=tmpvar*freq*tnow*tmpvar1;
   g2pslow+=tmpvar*tmpvar1; }  
 if(calc_gt_fast) {
    fast_four_hist(freq,&gpfast,&g2pfast);
   if((gpfast < (0.010*gpslow)) && (g2pfast < (0.010*g2pslow)))
     calc_gt_fast=false; }
 else {gpfast=0.0; g2pfast=0.0; }
if(OutMode != 1){ if(kxx == 0){
 if(OutMode == 2){ 
    fprintf(resfourfl,"%e %e %e \n",freq/unit_time,
      (gpslow+gpfast)*G_0_unit, (g2pslow+g2pfast)*G_0_unit); }
  else{ 
    fprintf(resfourfl,"%e %e %e \n",freq/unit_time,
      (gpslow+gpfast)*G_0_unit, (g2pslow+g2pfast)*G_0_unit); }}
                            }
else{ if(kxx == 0){
    fprintf(resfourfl,"%e %e \n",freq/unit_time,(gpslow+gpfast)*G_0_unit);}
    else{
    fprintf(resfourfl,"%e %e \n",freq/unit_time,(g2pslow+g2pfast)*G_0_unit);}}

    }
if(OutMode == 1){fprintf(resfourfl,"&\n");
 if(kxx == 0){fprintf(resfourfl,"@target G0.S1 \n @type xy \n"); }}

                     }

fclose(resfourfl);
}
