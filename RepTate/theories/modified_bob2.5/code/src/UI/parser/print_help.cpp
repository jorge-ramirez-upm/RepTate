/*
print_help.cpp : This file is part bob-rheology (bob) 
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
extern void print_short_license();
void print_help(void)
{
  printf("bob calculates rheological response of general branched polymers, \n");
  printf("  including, but not limited to Branch-On-Branch architecture.\n \n");
  printf("For occational usage, use bob with out any arguments \n");
  printf("    for  a text based user interface. \n\n");

  printf("\"bob --version\" prints the version information and known issues. \n");
  printf("\"bob --help\" prints this page. \n\n");

  printf("For extensive and repetitive usage, batch mode might be more useful. \n");
  printf("\"-b\" flag runs bob in batch mode. \n");
  printf("In batch mode you can also specify some filenames: \n");
  printf("You can supply input filename as \"-i inputfilename\" \n");
  printf("and/or polymer configuration filename as \"-c configurationfile\" \n\n");

  printf("Some parameters are set through a file bob.rc \n");

  printf("For details of the input, resource and configuration file format : \n");
  printf("see the relevant pages of the manual. \n");

  printf("To find details about the method of the computation: \n");
  printf("Look at: J. Rheo, 50, 207-234 (2006). \n");
  printf("         Science, 333, 1871-1874 (2011). \n");

  printf("Details of non-linear computation will be communicated to J. Rheo. \n");
}
