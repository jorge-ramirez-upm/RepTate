/*
topoan.cpp : This file is part bob-rheology (bob) 
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
#include "../../RepTate/reptate_func.h"
#include <stdio.h>
void topoan(void)
{
  extern std::vector<arm> arm_pool;
  extern std::vector<polymer> branched_poly;
  extern int num_poly;
  extern void calc_priority(int);
  extern void calc_seniority(int);
  for (int i = 0; i < num_poly; i++)
  {
    calc_priority(i);
    calc_seniority(i);
  }
  extern int max_prio_var, max_senio_var;
  int n1, n2;
  max_prio_var = 0;
  max_senio_var = 0;

  for (int i = 0; i < num_poly; i++)
  {
    n1 = branched_poly[i].first_end;
    arm_pool[n1].compound_store_data_num = 0;
    arm_pool[n1].compound_store_data_del_indx = 1;
    if (arm_pool[n1].priority > max_prio_var)
    {
      max_prio_var = arm_pool[n1].priority;
    }
    if (arm_pool[n1].seniority > max_senio_var)
    {
      max_senio_var = arm_pool[n1].seniority;
    }
    n2 = arm_pool[n1].down;
    while (n2 != n1)
    {
      arm_pool[n2].compound_store_data_num = 0;
      arm_pool[n2].compound_store_data_del_indx = 1;
      if (arm_pool[n2].priority > max_prio_var)
      {
        max_prio_var = arm_pool[n2].priority;
      }
      if (arm_pool[n2].seniority > max_senio_var)
      {
        max_senio_var = arm_pool[n2].seniority;
      }
      n2 = arm_pool[n2].down;
    }
  }
  // *** NOW redefine priority and seniority to start from 0 to conform with C array
  for (int i = 0; i < num_poly; i++)
  {
    n1 = branched_poly[i].first_end;
    arm_pool[n1].seniority -= 1;
    arm_pool[n1].priority -= 1;
    n2 = arm_pool[n1].down;
    while (n2 != n1)
    {
      arm_pool[n2].seniority -= 1;
      arm_pool[n2].priority -= 1;
      n2 = arm_pool[n2].down;
    }
  }

  extern FILE *infofl;
  extern bool reptate_flag;
  if (reptate_flag)
  {
    char line[128];
    sprintf(line, "<b>Maximum priority=%d<b><br><b>Maximum seniority=%d</b><br>", max_prio_var, max_senio_var);
    print_to_python(line);
  }
  fprintf(infofl, "maximum priority = %d \n maximum seniority = %d \n", max_prio_var, max_senio_var);
}
