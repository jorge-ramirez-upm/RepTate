/*
get_poly_component.cpp : This file is part of bob-rheology (bob) 
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

// polymer component n
#include <stdio.h>
#include <string.h>
#include <cstdlib>
#include "./../../include/bob.h"
void get_poly_component(int n, double blend_frac)
{
  extern int runmode, num_poly;
  int num_cur_comp;
  extern int CalcGPCLS;
  extern void gpcls(int, int, int, int);
  int polytype;
  extern char polycode[10];
  if (runmode == 2)
  {
    printf("\n Polymer component %d : \n", n + 1);
    printf("Number of polymers in current type?  ");
    scanf("%d", &num_cur_comp);
    printf("Select polymer type :\n");
    printf("Some (but not all) known polymer types follows: \n");
    printf("Look at manual for all possibilities \n");
    printf("    type \'0\' for linear \n");
    printf("         \'1\' for star \n");
    printf("         \'2\' for asymmetric star \n");
    printf("         \'3\' for H \n");
    printf("         \'4\' for Comb (number of side arms from Poisson dist.) \n");
    printf("         \'10\' for Cayley tree \n");
    printf("         \'20\' for metallocene-catalyzed polyethylene \n");
    //   printf("         \'30\' for Tubular LDPE \n");
    scanf("%d", &polytype);
  }
  else
  {
    extern FILE *inpfl;
    fscanf(inpfl, "%d %d", &num_cur_comp, &polytype);
  }
  num_cur_comp += num_poly;

  switch (polytype)
  {
  case 0:
    strcpy(polycode, "LINEAR");
    genLin(num_poly, num_cur_comp);
    break;
  case 1:
    strcpy(polycode, "Star");
    genStar(num_poly, num_cur_comp);
    break;
  case 2:
    strcpy(polycode, "asst");
    genStar_asym(num_poly, num_cur_comp);
    break;
  case 3:
    strcpy(polycode, "H");
    genH(num_poly, num_cur_comp);
    break;
  case 4:
    strcpy(polycode, "Comb");
    genComb(num_poly, num_cur_comp);
    break;
  case 5:
    strcpy(polycode, "Comb_fxd");
    genComb_fxd(num_poly, num_cur_comp);
    break;
  case 6:
    strcpy(polycode, "couplComb");
    gencoupledComb(num_poly, num_cur_comp);
    break;

  case 10:
    strcpy(polycode, "Cayley");
    genCayley(num_poly, num_cur_comp);
    break;
  case 11:
    strcpy(polycode, "CayLIN");
    genCayleyLIN(num_poly, num_cur_comp);
    break;
  case 12:
    strcpy(polycode, "CayST4");
    genCayley4(num_poly, num_cur_comp);
    break;

  case 20:
    strcpy(polycode, "MPE");
    genMPE(num_poly, num_cur_comp);
    break;
  case 21:
    strcpy(polycode, "MPEwtav");
    genMPE_wtav(num_poly, num_cur_comp);
    break;

  case 25:
    strcpy(polycode, "GELwtav");
    genGEL_wtav(num_poly, num_cur_comp);
    break;
  case 26:
    strcpy(polycode, "STGLWT");
    genstargel(num_poly, num_cur_comp);
    break;

  case 30:
    strcpy(polycode, "LDPE_TOB");
    genTobita(num_poly, num_cur_comp);
    break;
  case 40:
    strcpy(polycode, "prototype");
    genProto(num_poly, num_cur_comp);
    break;

  case 50:
    strcpy(polycode, "UDF");
    genUDF(num_poly, num_cur_comp);
    break;

  case 60:
    strcpy(polycode, "FromFile"); // correct num_cur_comp from file
    genfromfile(num_poly, &num_cur_comp, blend_frac);
    break;

  default:
    printf("Undefined polymer type %d \n", polytype);
    abort();
    break;
  }

  if ((polytype != 60))
  { // 60 sets own weight fraction

    if ((polytype == 21) || (polytype == 25) || (polytype == 26) || (polytype == 30))
    {
      set_vol_frac_wtav(num_poly, num_cur_comp, n, blend_frac);
    }
    else
    {
      set_vol_frac(num_poly, num_cur_comp, n, blend_frac);
    }
  }

  if (CalcGPCLS == 0)
  {
    gpcls(n, num_poly, num_cur_comp, 1);
  }
  num_poly = num_cur_comp;
}
