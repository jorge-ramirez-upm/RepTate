/*
polywrite.cpp : This file is part bob-rheology (bob) 
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
#include "../../../include/bob.h"

void polywrite(void)
{
 extern FILE *conffl;
 extern int num_poly;
 extern arm * arm_pool;
 extern polymer * branched_poly;
 extern char polycode[10];
 extern double N_e;

 int n1;
  fprintf(conffl,"%s \n", polycode);
  fprintf(conffl,"%le \n", N_e);
  fprintf(conffl,"%d \n", num_poly);
  for (int i=0; i < num_poly; i++)
   {
  int numseg=branched_poly[i].num_branch;
  fprintf(conffl,"%d \n",numseg);
   int nsv=branched_poly[i].first_end;
   int inmin=nsv;
   n1=arm_pool[nsv].down;
      while(n1 != nsv)
       {
        n1=arm_pool[n1].down;
        if(n1 < inmin)
           inmin=n1;
       }
// Changing here : 22 Sept
for(int n1=inmin; n1 < (inmin+numseg); n1++){
  fprintf(conffl,"%d %d %d %d %e %e\n", fold_wrt(arm_pool[n1].L1,inmin),
    fold_wrt(arm_pool[n1].L2,inmin), fold_wrt(arm_pool[n1].R1,inmin), 
    fold_wrt(arm_pool[n1].R2,inmin), arm_pool[n1].arm_len,arm_pool[n1].vol_fraction);
}
/* old code
  fprintf(conffl,"%d %d %d %d %e %e \n", fold_wrt(arm_pool[inmin].L1,inmin),
fold_wrt(arm_pool[inmin].L2,inmin),fold_wrt(arm_pool[inmin].R1,inmin), 
  fold_wrt(arm_pool[inmin].R2,inmin), arm_pool[inmin].arm_len, arm_pool[inmin].vol_fraction);
    n1=arm_pool[inmin].down;
      while(n1 != inmin)
       {
  fprintf(conffl,"%d %d %d %d %e %e\n", fold_wrt(arm_pool[n1].L1,inmin),
    fold_wrt(arm_pool[n1].L2,inmin), fold_wrt(arm_pool[n1].R1,inmin), 
    fold_wrt(arm_pool[n1].R2,inmin), arm_pool[n1].arm_len,arm_pool[n1].vol_fraction);
         n1=arm_pool[n1].down;
 
       }
 End old code */ 

   }

}
   
