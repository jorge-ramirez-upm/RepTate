/*
check_linearity.cpp : This file is part bob-rheology (bob) 
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
void check_linearity(int n) //check if n'th polymer is linear
{
 extern arm * arm_pool;
 extern polymer * branched_poly;
 int n1=branched_poly[n].first_free;
 int num_seg=1;
 int n2=arm_pool[n1].free_down;
 while(n2 != n1)
  {num_seg++; n2=arm_pool[n2].free_down;}
 if(num_seg <= 2) branched_poly[n].linear_tag=true; 

}
