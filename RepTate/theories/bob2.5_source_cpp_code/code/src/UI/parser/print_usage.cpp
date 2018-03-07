/*
print_usage.cpp : This file is part bob-rheology (bob) 
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
 
#include<stdio.h>
void print_usage(void)
{
printf(" Incorrect usage \n\n");

printf("use bob without any arguments for interactive mode. \n\n");

printf("bob --version prints version \n");
printf("bob --help gives help page and tells you how to get more help. \n\n");

printf("bob -b goes to batch mode \n");
printf("In batch mode, you can give input and configuration filenames as \n");
printf(" -i input_filename -c configuration_filename \n");
printf("Default input filename for batch mode is inp.dat \n");
printf(" and default configuration filename is polyconf.dat \n");
printf(" Some parameters are set through bob.rc \n");
printf(" For details look at the manual \n");
printf(" use -n to switch on non-linear flow calculation \n");
}
