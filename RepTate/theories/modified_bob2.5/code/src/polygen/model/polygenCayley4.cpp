/*
polygenCayley4.cpp : This file is part bob-rheology (bob) 
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
#include <math.h>
#include <stdio.h>
polymer polygenCayley4(int levl, int* arm_type, double* mn_arm, double* pdi)
{
extern std::vector <arm> arm_pool;
polymer cur_poly;
cur_poly=polygenH(arm_type[0], mn_arm[0], pdi[0],0,0.0,pdi[0]);

for (int i=1; i<=levl; i++)
 {
      int n1=cur_poly.first_free; int n2=n1;
      int m1=request_arm(); int m2=request_arm();
      int k1=cur_poly.first_end; int k2=arm_pool[k1].down;
      arm_pool[k1].down=m1; arm_pool[m1].up=k1; arm_pool[m1].down=m2;
      arm_pool[m2].up=m1; arm_pool[m2].down=k2; arm_pool[k2].up=m2;
 
      arm_pool[m1].arm_len=poly_get_arm(arm_type[i], mn_arm[i], pdi[i]);
      arm_pool[m2].arm_len=poly_get_arm(arm_type[i], mn_arm[i], pdi[i]);
      if((arm_pool[n2].L1== -1) && (arm_pool[n2].L2 == -1)){
arm_pool[n2].L1=m1; arm_pool[n2].L2=m2; arm_pool[m1].R1=n2; arm_pool[m1].R2=m2;
arm_pool[m2].R1=m1; arm_pool[m2].R2=n2;
        }
      else{
arm_pool[n2].R1=m1; arm_pool[n2].R2=m2; arm_pool[m1].L1=n2; arm_pool[m1].L2=m2;
arm_pool[m2].L1=m1; arm_pool[m2].L2=n2;
          }

 n2=arm_pool[n1].free_down;
   while(n2 != n1){
      int m1=request_arm(); int m2=request_arm();
      int k1=cur_poly.first_end; int k2=arm_pool[k1].down;
      arm_pool[k1].down=m1; arm_pool[m1].up=k1; arm_pool[m1].down=m2;
      arm_pool[m2].up=m1; arm_pool[m2].down=k2; arm_pool[k2].up=m2;
      arm_pool[m1].arm_len=poly_get_arm(arm_type[i], mn_arm[i], pdi[i]);
      arm_pool[m2].arm_len=poly_get_arm(arm_type[i], mn_arm[i], pdi[i]);
      if((arm_pool[n2].L1== -1) && (arm_pool[n2].L2 == -1)){
arm_pool[n2].L1=m1; arm_pool[n2].L2=m2; arm_pool[m1].R1=n2; arm_pool[m1].R2=m2;
arm_pool[m2].R1=m1; arm_pool[m2].R2=n2;
        }
      else{
arm_pool[n2].R1=m1; arm_pool[n2].R2=m2; arm_pool[m1].L1=n2; arm_pool[m1].L2=m2;
arm_pool[m2].L1=m1; arm_pool[m2].L2=n2;
          }
 n2=arm_pool[n2].free_down;
                  }
poly_start(&cur_poly);
 }

poly_start(&cur_poly);
return(cur_poly);
}
