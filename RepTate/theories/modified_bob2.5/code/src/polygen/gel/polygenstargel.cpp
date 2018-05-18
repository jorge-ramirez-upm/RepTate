/*
polygenstargel.cpp : This file is part bob-rheology (bob) 
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
#include "../../../include/MersenneTwister.h"

polymer polygenstargel(double p, int arm_type, double mn_arm, double pdi)
{
  extern std::vector<arm> arm_pool;
  polymer cur_poly;

  int n1 = request_arm();
  int n2 = request_arm();
  int n3 = request_arm();
  arm_pool[n1].arm_len = poly_get_arm(arm_type, mn_arm, pdi);
  arm_pool[n2].arm_len = poly_get_arm(arm_type, mn_arm, pdi);
  arm_pool[n3].arm_len = poly_get_arm(arm_type, mn_arm, pdi);
  cur_poly.first_end = n1;
  attach_arm(n1, -1, -1, n2, n3);
  attach_arm(n2, n1, n3, -1, -1);
  attach_arm(n3, n1, n2, -1, -1);
  arm_pool[n1].up = n2;
  arm_pool[n1].down = n3;
  arm_pool[n2].up = n3;
  arm_pool[n2].down = n1;
  arm_pool[n3].up = n1;
  arm_pool[n3].down = n2;

  extern void stargel_internal(double, int, double, double, polymer *, int);
  stargel_internal(p, arm_type, mn_arm, pdi, &cur_poly, n1);
  stargel_internal(p, arm_type, mn_arm, pdi, &cur_poly, n2);
  stargel_internal(p, arm_type, mn_arm, pdi, &cur_poly, n3);

  poly_start(&cur_poly);
  return (cur_poly);
}

void stargel_internal(double p, int arm_type, double mn_arm, double pdi, polymer *cur_poly, int n0)
{
  extern std::vector<arm> arm_pool;
  extern MTRand mtrand1;
  double randnum = mtrand1();
  if (randnum < p)
  {
    int n1 = request_arm();
    int n2 = request_arm();
    arm_pool[n1].arm_len = poly_get_arm(arm_type, mn_arm, pdi);
    arm_pool[n2].arm_len = poly_get_arm(arm_type, mn_arm, pdi);
    arm_pool[n0].arm_len += poly_get_arm(arm_type, mn_arm, pdi);

    int nd = arm_pool[n0].down;
    arm_pool[n0].down = n1;
    arm_pool[n1].up = n0;
    arm_pool[n1].down = n2;
    arm_pool[n2].up = n1;
    arm_pool[n2].down = nd;
    arm_pool[nd].up = n2;

    if (arm_pool[n0].L1 == -1)
    {
      arm_pool[n0].L1 = n1;
      arm_pool[n0].L2 = n2;
      attach_arm(n1, -1, -1, n0, n2);
      attach_arm(n2, -1, -1, n0, n1);
    }
    else
    {
      arm_pool[n0].R1 = n1;
      arm_pool[n0].R2 = n2;
      attach_arm(n1, n0, n2, -1, -1);
      attach_arm(n2, n0, n1, -1, -1);
    }

    stargel_internal(p, arm_type, mn_arm, pdi, cur_poly, n1);
    stargel_internal(p, arm_type, mn_arm, pdi, cur_poly, n2);
  }
}
