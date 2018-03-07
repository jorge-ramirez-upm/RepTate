/*
polygenUDF.cpp : This file is part bob-rheology (bob) 
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
#define UDF_segment_num 9
polymer polygenUDF(int * arm_type, double * mass, double * pdi)
{
extern arm * arm_pool;
polymer cur_poly;
int  nn[UDF_segment_num];
for(int i=0; i<UDF_segment_num; i++){
  nn[i]=request_arm(); 
  arm_pool[nn[i]].arm_len=poly_get_arm(arm_type[i], mass[i], pdi[i]);}

for(int i=1; i<(UDF_segment_num-1); i++){
 arm_pool[nn[i]].down=nn[i-1]; arm_pool[nn[i]].up=nn[i+1];}

arm_pool[nn[0]].down=nn[UDF_segment_num-1]; arm_pool[nn[0]].up=nn[1];
arm_pool[nn[UDF_segment_num-1]].down=nn[UDF_segment_num-2]; 
arm_pool[nn[UDF_segment_num-1]].up=nn[0];

cur_poly.first_end=nn[0];

attach_arm(nn[0],-1,-1,nn[1],nn[2]);
attach_arm(nn[1],-1,-1,nn[0],nn[2]);
attach_arm(nn[2],nn[0],nn[1],nn[3],nn[4]);
attach_arm(nn[3],nn[2],nn[6],nn[4],nn[5]);
attach_arm(nn[4],-1,-1,nn[3],nn[5]);
attach_arm(nn[5],-1,-1,nn[3],nn[4]);
attach_arm(nn[6],nn[2],nn[3],nn[7],nn[8]);
attach_arm(nn[7],-1,-1,nn[6],nn[8]);
attach_arm(nn[8],nn[6],nn[7],-1,-1);
poly_start(&cur_poly);
return(cur_poly);
}
