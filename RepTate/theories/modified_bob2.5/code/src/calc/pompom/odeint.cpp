/*
odeint.cpp : This file is part bob-rheology (bob) 
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

#include "./pompom.h"
#include <math.h>

void odeint(double ystart, double x1, double x2, double eps, double h1, double hmin,
            double tauS, double tauB, double gdot, int q, int kmax,
            double *xp, double *yp,
            void (*derivs)(double, double *, double *, double, double, double, int))
{
  double dydx, yscal, hlast, hdid, hnext;
  double x = x1;
  double tiny = 1.0e-30;
  double h;
  extern void warnmsgs(int);
  if ((x2 - x1) > 0.0)
  {
    h = fabs(h1);
  }
  else
  {
    h = -fabs(h1);
  }
  int kount, nok, nbad;
  kount = nok = nbad = 0;
  double y = ystart;
  int flag;

  hlast = h;
  for (int i = 0; i < kmax; i++)
  {
    flag = 0;
    h = hlast;
    while ((x < (xp[i] - tiny)) && (flag == 0))
    {
      if ((xp[i] - x) < fabs(h))
      {
        h = xp[i] - x + tiny;
        flag = 1;
      }
      (*derivs)(x, &y, &dydx, tauS, tauB, gdot, q);
      yscal = fabs(y) + fabs(h * dydx) + tiny;
      rkqs(&y, dydx, &x, h, eps, yscal, &hdid, &hnext, tauS, tauB, gdot, q, derivs);
      if (hdid == h)
      {
        nok++;
      }
      else
      {
        nbad++;
      }
      if (fabs(hnext) < hmin)
      {
        h = hmin;
      }
      else
      {
        h = hnext;
      }
      if ((xp[i] - x) < fabs(h))
      {
        h = xp[i] - x + tiny;
        flag = 1;
      }
    }
    yp[i] = y;
  }

  /*
hlast=hmin;

for(int nstp=0; nstp<=10000; nstp++){flag=0;
       (*derivs) (x,&y,&dydx,tauS, tauB, gdot, q);
       yscal=fabs(y)+fabs(h*dydx) + tiny;	

 if(kount < (kmax-1)){
    if ((x-xp[kount])*(xp[kount]-x1) >= 0.0){yp[kount]=y; kount++;}
   if ((x+h-xp[kount])*(x+h-x1) > 0.0){hlast=h; h=xp[kount]-x; flag=1;} }
 if ((x+h-x2)*(x+h-x1) > 0.0){ h=x2-x;};

 rkqs(&y,dydx,&x,h,eps,yscal,&hdid,&hnext,tauS, tauB, gdot, q, derivs);
  if(hdid == h){nok++;}
  else{nbad++;}
  if ((x-x2)*(x2-x1) >= 0.0){ystart=y;
	   yp[kount]=y;kount++; return; }
if(flag == 0){if(fabs(hnext) < hmin){
//        warnmsgs(401);
	h=hlast;}
	else{h=hnext;}} 
                 }
//warnmsgs(402); 
return;
*/
}
