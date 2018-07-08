/*
poly_stat.cpp : This file is part bob-rheology (bob) 
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

// Find out branching topology of the polymers in consideration
#include <stdio.h>
#include <string.h>
#include <math.h>
#include "../../../include/bob.h"
#include "../../RepTate/reptate_func.h"
extern bool reptate_flag;
extern bool flag_stop_bob;

double mass_poly(int n)
{
  extern std::vector<arm> arm_pool;
  extern std::vector<polymer> branched_poly;
  double mass_now = 0.0;
  int n1 = branched_poly[n].first_end;
  mass_now += arm_pool[n1].vol_fraction;
  int n2 = arm_pool[n1].down;
  while (n2 != n1)
  {
    mass_now += arm_pool[n2].vol_fraction;
    n2 = arm_pool[n2].down;
  }
  return (mass_now);
}

void poly_stat(void)
{
  extern std::vector<polymer> branched_poly;
  extern bool iscomb(int);
  int ncomb = 0;
  int nlin = 0;
  int nstar = 0;
  int ncombp = 0;
  double mcomb = 0.0;
  double mlin = 0.0;
  double mstar = 0.0;
  double mcombp = 0.0;
  double mtot = 0.0;
  double mtmp;
  double n_branch = 0.0;
  extern int num_poly;
  extern FILE *infofl;
  char table[1024];
  char line[256];

  if (reptate_flag)
    strcpy(table, "<b>Branching topology of the polymers:</b>");
  else
    fprintf(infofl, "Branching topology of the polymers\n");
  for (int i = 0; i < num_poly; i++)
  {
    if (flag_stop_bob)
    {
      my_abort((char *)"Calculations interrupted by user\n");
    }
    if (branched_poly[i].num_branch == 2)
    {
      nlin++;
      mtmp = mass_poly(i);
      mlin += mtmp;
      mtot += mtmp;
    }
    else
    {
      n_branch += (double)((branched_poly[i].num_branch - 1) / 2);
      if (branched_poly[i].num_branch == 3)
      {
        nstar++;
        mtmp = mass_poly(i);
        mstar += mtmp;
        mtot += mtmp;
      }
      else
      {
        if (iscomb(i))
        {
          ncomb++;
          mtmp = mass_poly(i);
          mcomb += mtmp;
          mtot += mtmp;
        }
        else
        {
          ncombp++;
          mtmp = mass_poly(i);
          mcombp += mtmp;
          mtot += mtmp;
        }
      }
    }
  }
  if (reptate_flag)
  {
    sprintf(line, "<tr><td>Number of branches per molecule</td><td>%9.4g</td></tr>", n_branch / ((double)num_poly));
    snprintf(table, sizeof table, "%s%s%s", table, "<table border=\"1\" width=\"100%\">", line);
    sprintf(line, "<tr><td>Number of linear molecules</td><td>%d</td></tr>", nlin);
    snprintf(table, sizeof table, "%s%s", table, line);
    sprintf(line, "<tr><td>Mass fraction of linear molecules</td><td>%9.4g</td></tr>", mlin / mtot);
    snprintf(table, sizeof table, "%s%s", table, line);
    sprintf(line, "<tr><td>Number of star molecules</td><td>%d</td></tr>", nstar);
    snprintf(table, sizeof table, "%s%s", table, line);
    sprintf(line, "<tr><td>Mass fraction of star molecules</td><td>%9.4g</td></tr>", mstar / mtot);
    snprintf(table, sizeof table, "%s%s", table, line);
    sprintf(line, "<tr><td>Number of comb molecules</td><td>%d</td></tr>", ncomb);
    snprintf(table, sizeof table, "%s%s", table, line);
    sprintf(line, "<tr><td>Mass fraction of comb molecules</td><td>%9.4g</td></tr>", mcomb / mtot);
    snprintf(table, sizeof table, "%s%s", table, line);
    sprintf(line, "<tr><td>Number of branch-on-branch molecules</td><td>%d</td></tr>", ncombp);
    snprintf(table, sizeof table, "%s%s", table, line);
    sprintf(line, "<tr><td>Mass fraction of branch-on-branch molecules</td><td>%9.4g</td></tr>", mcombp / mtot);
    snprintf(table, sizeof table, "%s%s%s", table, line, "</table>");
    print_to_python(table);
  }
  else
  {
    fprintf(infofl, "Number of branches per molecule = %le \n", n_branch / ((double)num_poly));
    fprintf(infofl, "number of linear molecules = %d \n", nlin);
    fprintf(infofl, "mass fraction of linear molecules = %e \n", mlin / mtot);
    fprintf(infofl, "number of star molecules = %d \n", nstar);
    fprintf(infofl, "mass fraction of star molecules = %e \n", mstar / mtot);
    fprintf(infofl, "number of comb molecules = %d \n", ncomb);
    fprintf(infofl, "mass fraction of comb molecules = %e \n", mcomb / mtot);
    fprintf(infofl, "number of branch-on-branch molecules = %d \n", ncombp);
    fprintf(infofl, "mass fraction of branch-on-branch molecules = %e \n", mcombp / mtot);
  }
}