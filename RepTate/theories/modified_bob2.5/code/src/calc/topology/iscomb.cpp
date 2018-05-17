/*
iscomb.cpp : This file is part bob-rheology (bob) 
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
 
// Returns false in m'th polymer is not comb
// for a comb, each inner segment has atleast one left and atleast one right
// neighbour segment which are free.

#include "../../../include/bob.h"
bool iscomb(int m)
{
extern std::vector <polymer> branched_poly;
extern std::vector <arm> arm_pool;
bool isitcomb=true;

if(branched_poly[m].num_branch > 3)
{
int n1=branched_poly[m].first_end;
if(!arm_pool[n1].free_end)
 {
if(!((arm_pool[arm_pool[n1].L1].free_end || arm_pool[arm_pool[n1].L2].free_end)
&& (arm_pool[arm_pool[n1].R1].free_end || arm_pool[arm_pool[n1].R2].free_end)))
{isitcomb=false;}
 }
int n2=arm_pool[n1].down;
while(n2 != n1)
{
if(!arm_pool[n2].free_end)
 {
if(!((arm_pool[arm_pool[n2].L1].free_end || arm_pool[arm_pool[n2].L2].free_end)
&& (arm_pool[arm_pool[n2].R1].free_end || arm_pool[arm_pool[n2].R2].free_end)))
{isitcomb=false;}
 }
n2=arm_pool[n2].down;
}
}

return isitcomb;
}

