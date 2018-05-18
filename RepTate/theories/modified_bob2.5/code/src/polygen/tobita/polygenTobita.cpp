/*
polygenTobita.cpp : This file is part bob-rheology (bob) 
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

// checked 3 Oct 2008
#include "../../../include/bob.h"
#include "./tobita.h"
#include <stdio.h>
#include <math.h>
polymer polygenTobita(double tau, double beta, double cs, double cb,
                      double fin_conv)
{
  extern std::vector<arm> arm_pool;
  double cur_conv, seg_len;
  polymer cur_poly;
  bool sc_tag;
  int m, m1;

  cur_conv = getconv1(fin_conv);
  m = request_arm();
  cur_poly.first_end = m;
  arm_pool[m].up = m;
  arm_pool[m].down = m;
  seg_len = calclength(cur_conv, cs, cb, tau, beta);
  arm_pool[m].arm_len = seg_len;
  arm_pool[m].z = cur_conv;     // use to store arm_conv of DJR
  arm_pool[m].relaxing = false; // scission
  sc_tag = true;

  int rlevel = 0;
  int bcount = 0;

  tobita_grow(1, m, cur_conv, sc_tag, &rlevel,
              cs, cb, fin_conv, tau, beta, &bcount);

  m1 = request_attached_arm(m);
  arm_pool[m].L1 = m1;
  arm_pool[m1].R2 = m;

  seg_len = calclength(cur_conv, cs, cb, tau, beta);
  arm_pool[m1].arm_len = seg_len;
  arm_pool[m1].z = cur_conv;
  arm_pool[m1].relaxing = false; //scission
  rlevel = 0;

  sc_tag = true;
  tobita_grow(-1, m1, cur_conv, sc_tag, &rlevel,
              cs, cb, fin_conv, tau, beta, &bcount);

  /* double mass_old=0.0; int nk0=cur_poly.first_end;
mass_old+=arm_pool[nk0].arm_len;
int nk1=arm_pool[nk0].down;
while(nk1 != nk0){mass_old+=arm_pool[nk1].arm_len; nk1=arm_pool[nk1].down;}
*/

  tobita_clean(&cur_poly);

  /*
double mass_new=0.0;  nk0=cur_poly.first_end;
mass_new+=arm_pool[nk0].arm_len;
nk1=arm_pool[nk0].down;
while(nk1 != nk0){mass_new+=arm_pool[nk1].arm_len; nk1=arm_pool[nk1].down;}
extern double N_e;
if((fabs(mass_old - mass_new*N_e)/mass_old ) > 0.001){
printf("Tobita : %e  %e \n",mass_old, mass_new*N_e); }
printf("Tobita: %e  \n",mass_new*N_e); 
*/

  poly_start(&cur_poly);
  return cur_poly;
}
