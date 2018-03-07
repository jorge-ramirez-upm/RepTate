/*
sample_eff_arm_len.cpp : This file is part bob-rheology (bob) 
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
 
// Store data for extrapolation to get Rouse time of compound arm
#include "../../../include/bob.h"
#include "./nlin.h"
void sample_eff_arm_len(int nnn){
extern arm * arm_pool; extern double cur_time;
int n=nlin_relaxing_arm(nnn, arm_pool[nnn].arm_len_eff);

int ndt=arm_pool[n].compound_store_data_num;
double ddz=arm_pool[n].arm_len/50.0;

if(ndt < 10) {
if(ndt > 0){
 if((arm_pool[nnn].arm_len_eff - arm_pool[n].compound_fit_zeff[ndt-1]) > ddz){
   arm_pool[n].compound_fit_time[ndt]=cur_time;
   arm_pool[n].compound_fit_zeff[ndt]=arm_pool[nnn].arm_len_eff;
   arm_pool[n].compound_store_data_num=ndt+1;}
}
else{
   arm_pool[n].compound_fit_time[ndt]=cur_time;
   arm_pool[n].compound_fit_zeff[ndt]=arm_pool[nnn].arm_len_eff;
   arm_pool[n].compound_store_data_num=ndt+1;
} }
else{ // move data around to create space
if((arm_pool[nnn].arm_len_eff - arm_pool[n].compound_fit_zeff[ndt-1]) > ddz ){

 if(arm_pool[nnn].z > arm_pool[n].compound_fit_zeff[0]){
   for(int j=0; j<9; j++) {
    arm_pool[n].compound_fit_time[j]=arm_pool[n].compound_fit_time[j+1];
    arm_pool[n].compound_fit_zeff[j]=arm_pool[n].compound_fit_zeff[j+1];
                           }
   arm_pool[n].compound_fit_time[9]=cur_time;
   arm_pool[n].compound_fit_zeff[9]=arm_pool[nnn].arm_len_eff; }
else{
   for(int j=1; j<5; j++){
    arm_pool[n].compound_fit_time[j]=arm_pool[n].compound_fit_time[2*j];
    arm_pool[n].compound_fit_zeff[j]=arm_pool[n].compound_fit_zeff[2*j]; }
   arm_pool[n].compound_fit_time[5]=cur_time;
   arm_pool[n].compound_fit_zeff[5]=arm_pool[nnn].arm_len_eff;
  arm_pool[n].compound_store_data_num=6; }

    } }
}

