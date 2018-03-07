/*
create_phi_hist.cpp : This file is part bob-rheology (bob) 
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
 
// create histogram of segments for use in fast modes
#include "../../../include/bob.h"
#include <stdio.h>
#include <math.h>
void create_phi_hist(void) {
extern arm * arm_pool; extern polymer * branched_poly;
extern int zintmin, zintmax, num_poly;
extern double  * phi_hist;
int phi_hist_max=0;
int n1,n2,zint;

for(int i=0; i<num_poly; i++){
   n1=branched_poly[i].first_end; n2=arm_pool[n1].down;
   zint=(int)floor(arm_pool[n1].arm_len);
   if(zint > phi_hist_max) {phi_hist_max=zint;}
     while(n2 != n1) { zint=(int)floor(arm_pool[n2].arm_len);
       if(zint > phi_hist_max) {phi_hist_max=zint;}
       n2=arm_pool[n2].down; } }
phi_hist_max+=4;



int * found_it=new int[phi_hist_max];
phi_hist = new double[phi_hist_max];

for (int i=0; i<phi_hist_max; i++) {
  phi_hist[i]=-1.0; // set to negative to imply nothing there
  found_it[i] = 0; }

zintmin=phi_hist_max; zintmax=0;
for (int i=0; i<num_poly; i++) {
   int n1=branched_poly[i].first_end;
   int n2=arm_pool[n1].down;
   int zint=(int)floor(arm_pool[n1].arm_len);
   if(zint < 0) {printf("Error : Negative arm! \n"); zint=0;}
   if(zint < zintmin) zintmin=zint;
   if(zint > zintmax) zintmax=zint;
    if(found_it[zint]==0)
       {phi_hist[zint]=0.0; found_it[zint]=1;}
   phi_hist[zint]+=arm_pool[n1].vol_fraction;

     while(n2 != n1)
      {
       zint=(int)floor(arm_pool[n2].arm_len);
   if(zint < 0) {printf("Error : Negative arm! \n"); zint=0;}
       if(zint < zintmin) zintmin=zint;
       if(zint > zintmax) zintmax=zint;
         if(found_it[zint]==0)
            {phi_hist[zint]=0.0; found_it[zint]=1;}
       phi_hist[zint]+=arm_pool[n2].vol_fraction;
       n2=arm_pool[n2].down;
      }
 }

if(zintmin == 0) zintmin=1;

delete [] found_it;
}
