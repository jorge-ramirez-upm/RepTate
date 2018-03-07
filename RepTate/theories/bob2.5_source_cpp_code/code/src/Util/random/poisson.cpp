/*
poisson.cpp : This file is part bob-rheology (bob) 
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
 
// Poisson distribution : Numerical Recipes
#include "../../../include/MersenneTwister.h"
#include "./bob_random.h"
#include <math.h>
#define pi 3.14159265358979323844
double gammln(double xx)
 {
	int j;
	double x,y,tmp,ser;
	static const double cof[6]={76.18009172947146,-86.50532032941677,
		24.01409824083091,-1.231739572450155,0.1208650973866179e-2,
		-0.5395239384953e-5};

	y=x=xx;
	tmp=x+5.5;
	tmp -= (x+0.5)*log(tmp);
	ser=1.000000000190015;
	for (j=0;j<6;j++) ser += cof[j]/++y;
	return -tmp+log(2.5066282746310005*ser/x);
 }

double poisson(double xm)
{
extern MTRand mtrand1;
double g, em, t, y;
if(xm < 12.0)
{
  g=exp(-xm); em=0.0; t=mtrand1();
  while (t > g)
   {
    em=em+1.0; t=t*mtrand1() ;
   }
}
else
{
double sq=sqrt(2.0 * xm); double alxm=log(xm);
g=xm*alxm - gammln(xm + 1.0);
int cont=1;
    while(cont != 0)
    {
    em=-1.0;
        while(em < 0.0)
        {
        y=tan(pi * mtrand1() );
        em=sq*y + xm;
        }
    em=floor(em);
    t=0.90 * (1.0 + y*y) * exp(em*alxm - gammln(em+1.0) -g);
    if(mtrand1() <= t) cont = 0;
    }
}
return(em);
}
