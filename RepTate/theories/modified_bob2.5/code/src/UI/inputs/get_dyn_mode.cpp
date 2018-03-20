/*
get_dyn_mode.cpp : This file is part bob-rheology (bob) 
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

// Get assumptions and parameters about the relaxation dynamics
#include <stdio.h>
void get_dyn_mode(void)
{
    extern int runmode, ReptScheme, PrefMode;
    extern double Alpha, RetLim, PSquare, TStart, cur_time, DtMult, ReptAmount;
    bool stored_values = false;
    if (runmode == 2)
    {
        printf("\nPlease enter dilation exponent alpha : ");
        scanf("%le", &Alpha);
        printf("\n");
        printf("We need assumptions/parameters re. branch point hops and reptation \n");
        printf("Type 1 if you want me to choose for you else type 0 ?? ... ");
        int tint;
        scanf("%d", &tint);
        printf("\n");
        if (tint == 1)
            stored_values = true;
        if (!stored_values)
        {
            printf("A side arm is considered to have retracted when the (dilated) length \n");
            printf("    still to retract is less than a certain  value R_L.\n");
            printf("       Please enter R_L : ");
            scanf("%le", &RetLim);
            printf("\n");
            printf("Beyond retraction time, branch point diffuses with hop size \"p.a\" \n");
            printf("Value of p^2 ?  ");
            scanf("%le", &PSquare);
            printf("\n");

            printf("For branch-on-branch compound arm, prefactor in retraction time \n");
            printf("  is not handled quite correctly. \n");
            printf("Type in 0 if you want prefactor same as outermost arm \n");
            printf("        1 if the prefactor involves effective arm length \n");
            printf("        2 if full effective friction goes in the prefactor ... ");
            scanf("%d", &PrefMode);
            if ((PrefMode < 0) || (PrefMode > 2))
            {
                printf("Illegal choice, continuing with mode 1 \n");
            }
            printf("\n");
            printf("Type in 1 if you want to consider reptation in thin tube \n");
            printf("        2 if you want to consider reptation in current tube \n");
            printf("        3 for tube diameter associated with the time at which linears \n");
            printf("          reptate by a fixed amount \n");
            printf("        4 for tube diameter associated with the time at which linears \n");
            printf("          reptate by a fixed fraction of the length it needs to reptate \n");
            printf("Your choice (1/2/3/4) ? ...  ");
            scanf("%d", &ReptScheme);
            if ((ReptScheme < 1) || (PrefMode > 4))
            {
                printf("Illegal choice : continuing with thin tube \n");
                ReptScheme = 1;
            }
            if (ReptScheme == 3)
            {
                printf("\nHow much of chain reptate by the time involved in reptation dilation? ...");
                scanf("%le", &ReptAmount);
            }
            else
            {
                if (ReptScheme == 4)
                {
                    printf("\nWhat fraction of chain reptate by the time involved in reptation dilation? ...");
                    scanf("%le", &ReptAmount);
                }
            }
            printf("\n");
            printf("We follow relaxation starting at time t_0 after a small strain,\n");
            printf("  and take snapshots of relaxation at times m*t_0 till everything relax.\n");
            printf("\n");
            printf("Starting time t_0 (a small number, typically 1e-4)  ? ... ");
            scanf("%le", &cur_time);
            printf("The multiplicative time step, m (>1, typically 1.002) ? ... ");
            scanf("%le", &DtMult);
        }
    }
    else
    {
        extern FILE *inpfl;
        fscanf(inpfl, "%le", &Alpha);
        int tmpint;
        fscanf(inpfl, "%d", &tmpint);
        if (tmpint != 1)
        {
            fscanf(inpfl, "%le %le  %d %d", &RetLim, &PSquare, &PrefMode, &ReptScheme);
            if ((ReptScheme == 3) || (ReptScheme == 4))
            {
                fscanf(inpfl, "%le", &ReptAmount);
            }
            fscanf(inpfl, "%le %le", &cur_time, &DtMult);
            printf("DtMult = %le \n", DtMult);
        }
        else
        {
            stored_values = true;
        }
    }

    if (RetLim < 1e-8)
    {
        RetLim = 1e-8;
    }
    PSquare = 0.50 * PSquare; // equations involving p^2 does not include factor 2
                              // from 1-d diffusion in the code implementation.
    TStart = cur_time;
}
