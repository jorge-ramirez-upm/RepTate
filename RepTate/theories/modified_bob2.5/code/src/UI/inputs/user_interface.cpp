/*
user_interface.cpp : This file is part bob-rheology (bob) 
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

#include <stdio.h>
#include <math.h>
#include "../../RepTate/reptate_func.h"

void user_interface(void)
{
  //First initialize a few things
  extern double gamma1, phi, phi_true, phi_ST;
  double pi = 4.0 * atan(1.0);
  gamma1 = 9.0 * pow(pi, (double)3) / 16.0;
  phi = 1.0;
  phi_true = 1.0;
  phi_ST = 1.0;

  // Now time for input

  extern void get_sys_size(void); // allocate arm and polymers
  get_sys_size();

  extern void get_dyn_mode(void); // assumptions and parameters about relaxation
  get_dyn_mode();

  extern void get_material(void); // chemistry : M_e, \tau_e ...
  get_material();

  // extern bool reptate_flag;
  if (reptate_flag){
    extern void print_io_to_reptate(void); // dump input to output
    print_io_to_reptate();
  }
  else{
    extern void print_io(void); // dump input to output
    print_io();
  }

  // Ready to generate /read polymer configuration

  extern void get_poly(void); // find out the polymer to use
  get_poly();

  extern void create_phi_hist(void);
  create_phi_hist();
  extern void topoan(void);
  topoan();
}
