/*
bob.cpp : This file is part of bob-rheology (bob), Modified verison for RepTate compatibility
bob-2.5 : rheology of Branch-On-Branch polymers
Copyright (C) 2006-2011, 2012 C. Das, D.J. Read, T.C.B. McLeish, V. Boudara

 
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
#include <stdbool.h>
#include <exception>
#include <math.h>
#include <stdlib.h>
#include "../../include/bob.h"
#include "../../include/MersenneTwister.h"
#include "../../include/global.h"

#include "../RepTate/reptate_func.h"

int bob_main(int, char **);
void init_static(void);
bool reptate_flag = true; // if false, "end_code()" is called at the end of bob_main()
int nnp_size;

bool reptate_save_polyconf_and_return_gpc(int argc, char **argv, int nbin, int ncomp, int ni, int nf, double *mn_out, double *mw_out, double *lgmid_out, double *wtbin_out, double *brbin_out, double *gbin_out)
{
  try
  {
    infofl = fopen("info.txt", "w");
    rcread();
    set_flag_stop_bob(false);
    bob_main(argc, argv);
    return_gpcls(nbin, ncomp, ni, nf, lgmid_out, wtbin_out, brbin_out, gbin_out);
    get_mn_mw(mn_out, mw_out);
    // close_files();
    end_code();
    return true;
  }
  catch (const std::exception &)
  {
    // close_files();
    end_code();
    return false;
  }
}

bool get_bob_lve(double *omega_out, double *gp_out, double *gpp_out)
{
  try
  {
    for (int i = 0; i < n_lve_out; i++)
    {
      omega_out[i] = omega[i];
      gp_out[i] = g_p[i];
      gpp_out[i] = g_pp[i];
    }
    // close_files();
    end_code();
    return true;
  }
  catch (const std::exception &)
  {
    // close_files();
    end_code();
    return false;
  }
}

bool run_bob_lve(int argc, char **argv, int *n)
{
  try
  {
    infofl = fopen("info.txt", "w");
    rcread();
    extern int OutMode;
    OutMode = 3;
    set_flag_stop_bob(false);
    bob_main(argc, argv);
    *n = n_lve_out;
    return true;
  }
  catch (const std::exception &)
  {
    return false;
  }
}

void init_static()
{
  // These variables were static in "origanal BoB"
  extern bool supertube_activated;
  extern double phi_ST_0;
  extern double ST_activ_time;
  supertube_activated = false;
  phi_ST_0 = 1.0;
  ST_activ_time = 1.0;
}

int bob_main(int argc, char *argv[])
{
  init_static();
  int cont_exec = parser(argc, argv);
  if (cont_exec == 1)
  {
    my_abort((char *)"Parser failed \n");
  }

  if (cont_exec == 0)
  {
    user_interface();
    poly_stat();
    if (GenPolyOnly != 0)
    {
      if ((Snipping != 0) && (CalcNlin != 0))
      {
        fprintf(infofl, "Following relaxation to calculate linear rheology\n");
      }
      if ((Snipping == 0) && (CalcNlin != 0))
      {
        fprintf(infofl, "Following relaxation to calculate linear rheology\n");
        fprintf(infofl, "and saving segment relaxation times for nonlinear flow \n");
      }
      if (CalcNlin == 0)
      {
        fprintf(infofl, "Following relaxation to calculate nonlinear flow predictions\n");
      }

/* ******************** Snipping  ********************  */
#ifdef NBETA
      if ((Snipping == 0) || (CalcNlin == 0))
      {
        SnipTime = SnipTime / unit_time;
        fprintf(infofl, "SnipTime (Sim unit ) = %e \n", SnipTime);
      }
      if (CalcNlin == 0)
      {
        FILE *fprio = fopen("savedprio.dat", "r"); //reading in previous savedprio.dat
        if (fprio == NULL)
        {
          my_abort((char *)"Was expecting file savedprio.dat here \nPlease run with CalcNlin=no  first. \n");
        }
        for (int i = 0; i < num_poly; i++)
        {
          int n1 = branched_poly[i].first_end;
          int n2 = arm_pool[n1].down;
          fscanf(fprio, "%d %lf %lf %lf", &arm_pool[n1].priority, &arm_pool[n1].str_time,
                 &arm_pool[n1].armtaus, &arm_pool[n1].armzeta);
          arm_pool[n1].priority -= 1;
          while (n2 != n1)
          {
            fscanf(fprio, "%d %lf %lf %lf", &arm_pool[n2].priority, &arm_pool[n2].str_time,
                   &arm_pool[n2].armtaus, &arm_pool[n2].armzeta);
            arm_pool[n2].priority -= 1;
            n2 = arm_pool[n2].down;
          }
        }
        fclose(fprio);

        if (FlowPriority == 0)
        {
          for (int i = 0; i < num_poly; i++)
          {
            extern void calc_flow_priority(int);
            calc_flow_priority(i);
          }
        }
        fprio = fopen("savedprio.dat", "w"); // re-writing the savedprio.dat file after altitude
        for (int i = 0; i < num_poly; i++)
        {
          int n1 = branched_poly[i].first_end;
          int n2 = arm_pool[n1].down;
          fprintf(fprio, "%d %e %e %e\n", arm_pool[n1].priority + 1, arm_pool[n1].str_time,
                  arm_pool[n1].armtaus, arm_pool[n1].armzeta);
          while (n2 != n1)
          {
            fprintf(fprio, "%d %e %e %e\n", arm_pool[n2].priority + 1, arm_pool[n2].str_time,
                    arm_pool[n2].armtaus, arm_pool[n2].armzeta);
            n2 = arm_pool[n2].down;
          }
        }
        fclose(fprio);
      }
      br_copy.resize(num_poly);
      for (int i = 0; i < num_poly; i++)
      {
        int nnp = 1;
        int n1 = branched_poly[i].first_end;
        int n2 = arm_pool[n1].down;
        while (n2 != n1)
        {
          nnp++;
          n2 = arm_pool[n2].down;
        }
        nnp_size = nnp;
        br_copy[i].narm = nnp;
        br_copy[i].active = 0;
        br_copy[i].armindx.resize(nnp);
        br_copy[i].priority.resize(nnp);
        br_copy[i].assigned_trelax.resize(nnp);
        br_copy[i].trelax.resize(nnp);
        br_copy[i].zeta.resize(nnp);
        br_copy[i].relax_end.resize(nnp);
        br_copy[i].assigned_taus.resize(nnp);
        br_copy[i].taus.resize(nnp);

        nnp = 0;
        br_copy[i].armindx[nnp] = n1;
        arm_pool[n1].copy_num = nnp;
        br_copy[i].priority[nnp] = 1;
        br_copy[i].assigned_trelax[nnp] = -1;
        br_copy[i].trelax[nnp] = 0.0;
        br_copy[i].relax_end[nnp] = -200;
        br_copy[i].assigned_taus[nnp] = -1;
        br_copy[i].taus[nnp] = 0.0;
        br_copy[i].zeta[nnp] = 0.0;
        // br_copy[i].relax_end[nnp]=n1;
        n2 = arm_pool[n1].down;
        while (n2 != n1)
        {
          nnp++;
          br_copy[i].armindx[nnp] = n2;
          arm_pool[n2].copy_num = nnp;
          br_copy[i].assigned_trelax[nnp] = -1;
          br_copy[i].trelax[nnp] = 0.0;
          br_copy[i].relax_end[nnp] = -300;
          br_copy[i].assigned_taus[nnp] = -1;
          br_copy[i].taus[nnp] = 0.0;
          br_copy[i].zeta[nnp] = 0.0;
          //  br_copy[i].relax_end[nnp]=n2;
          br_copy[i].priority[nnp] = 1;
          n2 = arm_pool[n2].down;
        }
      }

      if (CalcNlin == 0)
      {
        startup_nlin();
      }

#endif
      /* ******************** Snipping  ********************  */
      FILE *phifl = fopen("supertube.dat", "w");

      fprintf(phifl, "%e %e %e  %e \n", 0.0, 1.0, 1.0, 1.0);
      int ndata = 2;
      int num_alive = time_step(0);
      fprintf(phifl, "%e %e %e  %e \n", cur_time, phi, phi_ST, phi_true);

      if ((CalcNlin != 0) && (Snipping == 0))
      {
        extern void sample_alt_time(void);
        sample_alt_time();
        extern void sample_alt_taus(void);
        sample_alt_taus();
      }

      double progres = 1;
      char info_progres[256];
      while (num_alive > 0)
      {
        if ((phi_ST + 0.05) <= progres)
        {
          sprintf(info_progres, "%3g%% done\n", (1 - progres) * 100);
          print_to_python(info_progres);
          progres -= 0.1;
        }
        if (flag_stop_bob){
          my_abort((char *)"Calculations interrupted by user\n");
        }

#ifdef NBETA
        if (CalcNlin == 0)
        {
          if (nlin_collect_data == -1)
          {
            if (cur_time > nlin_t_min)
            {
              init_var_nlin();
            }
          }
          else
          {
            if (cur_time > nlin_t_max)
            {
              output_nlin();
            }
          }
        }
#endif
        num_alive = time_step(1);
        ndata++;

        if ((CalcNlin != 0) && (Snipping == 0))
        {
          extern void sample_alt_time(void);
          sample_alt_time();
          extern void sample_alt_taus(void);
          sample_alt_taus();
        }

        if (cur_time > 1e30)
        {
          printf("in if (cur_time > 1e30) \n");

          warnmsgs(101);
          for (int i = 0; i < num_poly; i++)
          {
            if (branched_poly[i].alive)
            {
              polyout(i);
            }
          }
          num_alive = 0;
        }
        if (phi_true < 0.0)
        { // numerical precision can give small negative phi
          phi_true = 0.0;
          if ((num_alive > 0) && (phi_true < -1.0e-6))
          {
            warnmsgs(102);
            for (int i = 0; i < num_poly; i++)
            {
              if (branched_poly[i].alive)
              {
                polyout(i);
              }
            }
            num_alive = 0;
          }
        }
        if ((num_alive > 0) && (phi_true > 0.0))
        {
          fprintf(phifl, "%e %e %e %e  \n", cur_time, phi, phi_ST, phi_true);
        }
        else
        {
          num_alive = 0;
          fprintf(phifl, "%e %e %e %e  \n", cur_time, 0.0, 0.0, 0.0);
        }
      }
      print_to_python((char *)"100% done\n");

      if ((CalcNlin != 0) && (Snipping == 0))
      {
        extern void calcsnipprio(void);
        calcsnipprio();
      }
      fclose(phifl);
      lin_rheology(ndata);
#ifdef NBETA
      if ((CalcNlin != 0) && (Snipping == 0))
      {
        extern void dumpsnipprio(void);
        dumpsnipprio();
      }
      if (CalcNlin == 0)
      {
        fclose(nlin_outfl);
        pompom();
      }
#endif
    }
  }
  if (!reptate_flag)
  {
    end_code();
  }
  return 0;
}
