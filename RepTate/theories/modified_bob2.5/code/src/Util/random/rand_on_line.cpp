/*
rand_on_line.cpp : This file is part bob-rheology (bob) 
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
 
// pick up random n points over length [0,L] and return sorted
#include "../../../include/MersenneTwister.h"
#include <math.h>
void rand_on_line(double L, int n, double * junc)
{
extern MTRand mtrand1;
for(int i=0; i< n; i++)
 {
  junc[i]=L*mtrand1();
 }

//NR: piksrt
double a;
int i;
for (int j=1; j< n; j++)
 {
  a=junc[j]; i=j;
  while(i >0 && junc[i-1] > a){ junc[i]=junc[i-1]; i--;}
  junc[i]=a;
 }
}
