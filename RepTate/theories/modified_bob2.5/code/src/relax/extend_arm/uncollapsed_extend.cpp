/*
uncollapsed_extend.cpp : This file is part bob-rheology (bob) 
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
 
//arm_pool[n] is not collapsed and not frozen : extend it
#include <math.h>
#include "../../../include/bob.h"
#include "../relax.h"
#include <iostream>
#include <cstdlib>
using namespace std;
void uncollapsed_extend(int m, int n)
{ 
 extern std::vector <arm> arm_pool;
 extern double phi,Alpha,cur_time,PSquare;

// Changes 10 May 2007
// For simple arm check if it can gobble up another arm to become compound 
 if(!arm_pool[n].compound) {
// change  20 June 2007
// Do this only if current time > z^2 (we are taking care of backbone
// Rouse time for the outermost arm
if(cur_time > (arm_pool[n].z * arm_pool[n].z)){
            int n1=arm_pool[n].nxtbranch1; int n2=arm_pool[n].nxtbranch2;
            if((n1 == -1) || (n2==-1))
              arm_pool[n].freeze_arm_len_eff=true;
            else
              {
                if(arm_pool[n1].relaxing && arm_pool[n2].relaxing)
                 arm_pool[n].freeze_arm_len_eff=true;
                else
                 {
                  if(arm_pool[n1].relaxing && (!arm_pool[n2].relaxing))
                   arm_len_end_extend(m,n,n1,n2);
                  else
                   {
                    if(arm_pool[n2].relaxing && (!arm_pool[n1].relaxing))
                     arm_len_end_extend(m,n,n2,n1);
                   }
                 }
              }

                        } }

// end changes on 10 May 2007

  if(arm_pool[n].compound)
    {
      double tmpvar;
      if(arm_pool[n].zeff_denom > tiny)
       {tmpvar=arm_pool[n].zeff_numer/arm_pool[n].zeff_denom +
           3.0*PSquare*pow(phi,Alpha)*cur_time/arm_pool[n].zeff_denom;}
      else
       {tmpvar=arm_pool[n].arm_len_end + tiny;}

        if(tmpvar > arm_pool[n].arm_len_end)  //end of current compound arm
          {
            tmpvar=arm_pool[n].arm_len_end;
            int n1=arm_pool[n].nxtbranch1; int n2=arm_pool[n].nxtbranch2;
            if((n1 == -1) || (n2==-1))
              arm_pool[n].freeze_arm_len_eff=true;
            else
              {
                if(arm_pool[n1].relaxing && arm_pool[n2].relaxing)
                 arm_pool[n].freeze_arm_len_eff=true;
                else
                 {
                  if(arm_pool[n1].relaxing && (!arm_pool[n2].relaxing))
                   arm_len_end_extend(m,n,n1,n2);
                  else
                   {
                    if(arm_pool[n2].relaxing && (!arm_pool[n1].relaxing))
                     arm_len_end_extend(m,n,n2,n1);
                   }
                 }
              }

          }

        arm_pool[n].deltazeff=(tmpvar - arm_pool[n].arm_len_eff);
        arm_pool[n].arm_len_eff=tmpvar;
    }
  else
    arm_pool[n].deltazeff=0.0;
  
}
