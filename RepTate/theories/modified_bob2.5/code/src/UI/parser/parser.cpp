/*
parser.cpp : This file is part bob-rheology (bob) 
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

// here we decide what the command line wants us to do
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "../../../include/bob.h"
extern void print_short_license();
int parser(int argc, char *argv[])
{
  extern int runmode, CalcNlin, GenPolyOnly;
  extern FILE *inpfl;
  extern FILE *protofl;
  int cont_exec = 0;
  int defconf = 0;
  int definp = 0;
  char inpfname[256];
  char protofname[256];
  extern char conffname[256];
  extern void print_help(void);
  extern void print_version(void);
  extern void print_usage(void);

  // printf("\n %s : rheology of Branch-On-Branch polymers \n", bob_version);
  // print_short_license();
  if (argc == 1)
  { // no command line argument
    printf("Starting up interactive mode \n");
    runmode = 2;
  }
  else
  {
    if (argc == 2)
    { // expecting -b for batch mode, or --help, --version
      if (argv[1][0] == '-')
      {
        if (argv[1][1] == '-')
        {
          switch (argv[1][2])
          {
          case 'h':
            print_help();
            cont_exec = 2;
            break;
          case 'v':
            print_version();
            cont_exec = 2;
            break;
          default:
            print_usage();
            cont_exec = 1;
            break;
          }
        }
        else
        {
          switch (argv[1][1])
          {
          case 'b':
            printf("Entering batch mode with default filenames \n");
            runmode = 3;
            break;
          case 'n':
            CalcNlin = 0;
            runmode = 2;
            break;
          case 'h':
            print_help();
            cont_exec = 2;
            break;
          case 'v':
            print_version();
            cont_exec = 2;
            break;
          default:
            print_usage();
            cont_exec = 1;
            break;
          }
        }
      }
      else
      {
        printf("Looks like I found some command like argument without \"-\" \n\n");
        print_usage();
        cont_exec = 1;
      }
    }
    else
    { // Some argument to choose from
      for (int i = 1; i < argc; i++)
      {
        if (argv[i][0] == '-')
        {
          switch (argv[i][1])
          {
          case 'i':
            strcpy(inpfname, argv[++i]);
            definp = 1;
            break;
          case 'c':
            strcpy(conffname, argv[++i]);
            defconf = 1;
            break;
          case 'b':
            runmode = 3;
            break; //superficial. Allows -b along with -* fname
          case 'n':
            CalcNlin = 0;
            break;
          case 'p':
            GenPolyOnly = 0;
            break;
          case 'x':
            strcpy(protofname, argv[++i]);
            protofl = fopen(protofname, "r");
            break;
          default:
            print_usage();
            cont_exec = 1;
            break;
          }
        }
        else
        {
          print_usage();
          cont_exec = 1;
        }
      }
      if (cont_exec == 0)
      {
        runmode = 3;
        // printf("Entering batch mode \n");
      }
    }
  }

  if (cont_exec == 0)
  {

    if (runmode == 3)
    { // batch mode
      if (definp != 0)
      {
        // printf("Using input file as %s \n", inpfname);
      }
      else
      {
        strcpy(inpfname, "inp.dat");
        printf("Using default input file inp.dat \n");
      }
      inpfl = fopen(inpfname, "r");
      if (inpfl == NULL)
      {
        printf("Error opening input file %s \n", inpfname);
        abort();
      }

      if (defconf != 0)
      {
        // printf("Using configuration file as %s \n", conffname);
      }
      else
      {
        strcpy(conffname, "polyconf.dat");
        printf("Using default configuration file polyconf.dat \n");
      }
    }
    else
    {
      strcpy(inpfname, "inp.dat");
      strcpy(conffname, "polyconf.dat");
    }
  }

  return (cont_exec);
}
