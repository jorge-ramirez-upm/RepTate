/*
arm_retraction.cpp : This file is part bob-rheology (bob) 
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

// retract n'th arm : first time step : indx=0
#include <math.h>
#include <stdio.h>
#include "../../../include/bob.h"
#include "../relax.h"
void arm_retraction(int n, int indx)
{
  double dz;
  extern double cur_time, gamma1, phi, DtMult, deltaphi, Alpha, RetLim, PSquare;
  extern arm *arm_pool;
  extern int PrefMode;
  extern int LtRsActivated;

  if (indx == 0)
  { //first time step : use only Rouse dynamics
    arm_pool[n].z = exp(log(cur_time / gamma1) * 0.250);
    arm_pool[n].pot = 1.50 * pow(phi, Alpha) * (arm_pool[n].z * arm_pool[n].z) /
                      arm_pool[n].arm_len;
    arm_pool[n].tau_K = arm_pool[n].gamma2 * arm_pool[n].z;
    dz = arm_pool[n].z;
    arm_pool[n].deltazeff = 0.0;
    if (dz > (arm_pool[n].arm_len_end - RetLim / pow(phi, Alpha)))
    {
      dz = arm_pool[n].arm_len_end;
      arm_pool[n].collapsed = true;
      arm_pool[n].tau_collapse = cur_time;
      arm_pool[n].phi_collapse = phi;
    }
    arm_pool[n].z = dz;
    arm_pool[n].dz = dz;
    arm_pool[n].pot_int = dz * (1.0 + 0.50 * dz * dz / arm_pool[n].arm_len);
  }
  else
  { // interpolation scheme
    double z0 = arm_pool[n].z;
    double dphidz, dzeffdz;
    if (arm_pool[n].dz > tiny)
    {
      dphidz = deltaphi / arm_pool[n].dz;
      dzeffdz = arm_pool[n].deltazeff / arm_pool[n].dz;
    }
    else
    {
      dphidz = 0.0;
      dzeffdz = 0.0;
    }

    double u0 = arm_pool[n].pot;
    double t0 = arm_pool[n].tau_K;
    double up = 3.0 * z0 * pow(phi, Alpha) / arm_pool[n].arm_len_eff;
    double u2p = ((3.0 * pow(phi, Alpha)) / arm_pool[n].arm_len_eff) *
                 (1.0 + Alpha * z0 * dphidz / phi - z0 * dzeffdz / arm_pool[n].arm_len_eff);
    double g1 = gamma1;
    double g2 = arm_pool[n].gamma2;
    double aa, bb, cc;
    double expp = exp(u0);
    double expm = exp(-u0);

    if (!arm_pool[n].compound)
    { // simple arm
      if (u0 < 15.0)
      {
        cc = -log(DtMult);
        bb = up;
        aa = 0.50 * up;
        double delta1 = t0 * expm / (g1 * pow(z0, 4.0));
        double delta2 = 1.0 / (1.0 + delta1);
        double delta4 = g2 * expp / t0;
        double delta3 = 4.0 / z0 + up - delta4;
        bb += 4.0 / z0 - delta2 * delta3;
        aa += -2.0 / (z0 * z0) - 0.50 * (delta1 * delta2 * delta2 * delta3 * delta3);
        aa -= 0.50 * delta2 * (u2p - 4.0 / (z0 * z0) + delta4 * (delta4 - up));
      }
      else
      { // assume only Kramers' term contributes
        if (fabs(up) >= 1e-6)
        {
          aa = 1.0;
          bb = 2.0 / up;
          cc = -2.0 * exp(log(cur_time * (1.0 - 1.0 / DtMult)) - u0) / (g2 * up);
        }
        else
        {
          aa = 0.0;
          bb = 1.0;
          cc = -exp(log(cur_time * (1.0 - 1.0 / DtMult)) - u0) / g2;
        }
      }
      dz = quad_solve_spl(aa, bb, cc);

      if (LtRsActivated == 0)
      {
        dz = sqrt(cur_time) - z0;
        if ((z0 + dz) > arm_pool[n].arm_len_end)
        {
          dz = arm_pool[n].arm_len_end - z0;
        }
      }

      if ((z0 + dz) > (arm_pool[n].arm_len_end - RetLim / phi))
      {
        dz = arm_pool[n].arm_len_end - z0;
        if (dz < 0.0)
          dz = 0.0;
        if (!arm_pool[n].collapsed)
        {
          arm_pool[n].collapsed = true;
          arm_pool[n].tau_collapse = cur_time;
          arm_pool[n].phi_collapse = phi;
        }
      }

      arm_pool[n].z = z0 + dz;
      arm_pool[n].pot = u0 + up * dz + 0.50 * u2p * dz * dz;
      arm_pool[n].tau_K = t0 + g2 * expp * (dz + 0.50 * up * dz * dz);
      arm_pool[n].dz = dz;
      arm_pool[n].pot_int += expp * dz * (1.0 + 0.50 * up * dz + (u2p + up * up) * dz * dz / 6.0);
    } // end work on simple arm
    else
    { // compound arm
      double drag;
      if (PrefMode == 0)
      {
        drag = arm_pool[n].gamma2;
      } //drag from outer most arm
      else
      {
        if (PrefMode == 1)
        { // replace arm_len by arm_len_eff
          drag = arm_pool[n].arm_len_eff * sqrt(1.50 * pi_pow_5 * arm_pool[n].arm_len_eff);
        }
        else
        {
          drag = calc_eff_fric(n) / PSquare;
          drag += 1.50 * pi_pow_2 * arm_pool[n].arm_len_eff;        // backbone contribution
          drag = drag * sqrt(2.0 * pi * arm_pool[n].arm_len / 3.0); // only outer arm in curveture
        }
      }

      double tk = drag * arm_pool[n].pot_int;
      double tf;
      if (u0 < 15.0)
      {
        double te = g1 * pow(z0, 4.0);
        tf = te / (expm + te / tk);
      }
      else
      {
        tf = tk;
      }
      if (tf >= (cur_time - 1.0e-6))
      {
        arm_pool[n].dz = 0.0;
      } // safety factor 1e-6
      else
      {            // the arm can retract
        g2 = drag; // approximate g2 almost constant.
        // should be ok since we `correct' our estimate in next step.
        if (u0 < 15)
        { // u0 not too large
          cc = -log(cur_time / tf);
          bb = up;
          aa = 0.50 * up;
          double delta1 = t0 * expm / (g1 * pow(z0, 4.0));
          double delta2 = 1.0 / (1.0 + delta1);
          double delta4 = g2 * expp / t0;
          double delta3 = 4.0 / z0 + up - delta4;
          bb += 4.0 / z0 - delta2 * delta3;
          aa += -2.0 / (z0 * z0) - 0.50 * (delta1 * delta2 * delta2 * delta3 * delta3);
          aa -= 0.50 * delta2 * (u2p - 4.0 / (z0 * z0) + delta4 * (delta4 - up));
        }
        else
        { // u0 large
          if (fabs(up) >= 1e-6)
          {
            aa = 1.0;
            bb = 2.0 / up;
            cc = -2.0 * exp(log((cur_time - tf)) - u0) / (g2 * up);
          }
          else
          {
            aa = 0.0;
            bb = 1.0;
            cc = -exp(log((cur_time - tf)) - u0) / g2;
          }
        }
        dz = quad_solve_spl(aa, bb, cc);
        if (LtRsActivated == 0)
        {
          dz = arm_pool[n].arm_len_eff - z0;
        }

        // *** Change here to make sure z is always smaller than z_eff
        // 25 April 2007
        if (arm_pool[n].compound)
        {
          if ((z0 + dz) > arm_pool[n].arm_len_eff)
          {
            dz = arm_pool[n].arm_len_eff - z0 + tiny;
          }
        }
        // *** end of change
        if ((z0 + dz) > (arm_pool[n].arm_len_end - RetLim / phi))
        {
          dz = arm_pool[n].arm_len_end - z0;
          if (dz < 0.0)
            dz = 0.0;
          if (!arm_pool[n].collapsed)
          {
            arm_pool[n].collapsed = true;
            arm_pool[n].tau_collapse = cur_time;
            arm_pool[n].phi_collapse = phi;
          }
        }
        arm_pool[n].z = z0 + dz;
        arm_pool[n].pot = u0 + up * dz + 0.50 * u2p * dz * dz;
        arm_pool[n].tau_K = t0 + g2 * expp * (dz + 0.50 * up * dz * dz);
        arm_pool[n].dz = dz;
        arm_pool[n].pot_int += expp * dz * (1.0 + 0.50 * up * dz + (u2p + up * up) * dz * dz / 6.0);
      }

    } // end work on compound arm
  }   // end interpolation scheme
}
