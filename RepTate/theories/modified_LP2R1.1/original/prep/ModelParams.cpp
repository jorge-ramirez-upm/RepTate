#include "../include/LinLin.h"

/** \file
  * \brief
  * Set default model parameters that are unlikely to be changed by most users
  */


void ModelParams(void)
{
using namespace LP2R_NS;
Alpha=1.0;
t_CR_START=1.0;
deltaCR=0.30;
B_zeta=2.0;
A_eq=2.0;
B_eq=10.0;
ret_pref=0.189;
Rept_Switch_Factor=1.664;

cur_time=1.0e-3;
DtMult=1.02;
}
