/*
polygenasH.cpp : This file is part bob-rheology (bob) 
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
polymer polygenasH(int arm_type, double m_arm1, double pdi_arm1,
                   double m_arm2, double pdi_arm2, double m_cross, double pdi_cross)
{
  extern double N_e;
  extern std::vector<arm> arm_pool;
  polymer cur_poly;
  int n1 = request_arm();
  int n2 = request_arm();
  int n3 = request_arm();
  int n4 = request_arm();
  int n5 = request_arm();

  if (arm_type == 0)
  {
    arm_pool[n1].arm_len = armlen_gaussian(m_arm1, pdi_arm1) / N_e;
    arm_pool[n2].arm_len = armlen_gaussian(m_arm2, pdi_arm2) / N_e;
    arm_pool[n3].arm_len = armlen_gaussian(m_cross, pdi_cross) / N_e;
    arm_pool[n4].arm_len = armlen_gaussian(m_arm1, pdi_arm1) / N_e;
    arm_pool[n5].arm_len = armlen_gaussian(m_arm2, pdi_arm2) / N_e;
  }
  else
  {
    if (arm_type == 1)
    {
      arm_pool[n1].arm_len = armlen_lognormal(m_arm1, pdi_arm1) / N_e;
      arm_pool[n2].arm_len = armlen_lognormal(m_arm2, pdi_arm2) / N_e;
      arm_pool[n3].arm_len = armlen_lognormal(m_cross, pdi_cross) / N_e;
      arm_pool[n4].arm_len = armlen_lognormal(m_arm1, pdi_arm1) / N_e;
      arm_pool[n5].arm_len = armlen_lognormal(m_arm2, pdi_arm2) / N_e;
    }
    else
    {
      arm_pool[n1].arm_len = armlen_semiliving(m_arm1, pdi_arm1) / N_e;
      arm_pool[n2].arm_len = armlen_semiliving(m_arm2, pdi_arm2) / N_e;
      arm_pool[n3].arm_len = armlen_semiliving(m_cross, pdi_cross) / N_e;
      arm_pool[n4].arm_len = armlen_semiliving(m_arm1, pdi_arm1) / N_e;
      arm_pool[n5].arm_len = armlen_semiliving(m_arm2, pdi_arm2) / N_e;
    }
  }

  arm_pool[n1].R1 = n2;
  arm_pool[n1].R2 = n3;
  arm_pool[n2].R1 = n1;
  arm_pool[n2].R2 = n3;
  arm_pool[n3].L1 = n1;
  arm_pool[n3].L2 = n2;
  arm_pool[n3].R1 = n4;
  arm_pool[n3].R2 = n5;
  arm_pool[n4].L1 = n3;
  arm_pool[n4].L2 = n5;
  arm_pool[n5].L1 = n3;
  arm_pool[n5].L2 = n4;

  arm_pool[n1].up = n5;
  arm_pool[n1].down = n2;
  arm_pool[n2].up = n1;
  arm_pool[n2].down = n3;
  arm_pool[n3].up = n2;
  arm_pool[n3].down = n4;
  arm_pool[n4].up = n3;
  arm_pool[n4].down = n5;
  arm_pool[n5].up = n4;
  arm_pool[n5].down = n1;
  cur_poly.first_end = n1;
  poly_start(&cur_poly);
  return (cur_poly);
}
