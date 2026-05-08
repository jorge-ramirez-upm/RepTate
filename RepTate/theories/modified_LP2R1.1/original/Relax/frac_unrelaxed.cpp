#include "../include/LP2R.h"
/**
  *\file
  *\brief Decide on supertube relaxation based on material relaxed in the current time interval
  */
void frac_unrelaxed(void)
{
using namespace LP2R_NS;

double deltaphi, dphi_max;
double phit_sv=phi_true;

phi_true=0.0;
for(int i=0; i<npoly; i++){
  if(LPoly[i]->alive){
    phi_true+=LPoly[i]->wt * (1.0 - 2.0*LPoly[i]->z/LPoly[i]->Z_chain);
                     }
                          }

if(cur_time > t_CR_START){ // only thin tube available before this time
double A_zeta_inv= (1.0/((1.0 - deltaCR)*(1.0 - deltaCR))) - 1.0;
double deltaCRnow= 1.0 - (1.0 - deltaCR)*sqrt(1.0 + A_zeta_inv/cur_time);
if(deltaCRnow < 0.0){deltaCRnow=0.0;}

if(AboveTauEFirst){AboveTauEFirst=false;
 deltaphi=1.0-phi_true; // tube relaxation starts now
                    }
else{deltaphi=phit_sv - phi_true;}
double STmaxDropnow=(1.0 - STmaxDrop)/(1.0 - deltaCRnow*STmaxDrop);
dphi_max=phi_ST*STmaxDropnow;
// ********************************************
if(!supertube_activated){
 if(deltaphi <= dphi_max){phi_ST=phi_true;}
 else{ //start of new CR Rouse region
   supertube_activated=true;
   phi_ST_0=phi_ST - deltaCRnow*deltaphi;
   ST_activ_time=cur_time;
   phi_ST-=dphi_max; // this much can relax in one time step
     }
                        }
else{ // already in CR Rouse
 double tv=phi_ST_0*exp(log(ST_activ_time/cur_time)/(2.0*Alpha));
 if(tv < phi_true){phi_ST=phi_true; supertube_activated=false;}
 else{ // continue in CR Rouse
   if(deltaphi <= dphi_max){ // normal power-law
                      phi_ST=tv;
                           }
   else{ // additional CR; add extra drop to phi_ST_0
     phi_ST_0-=deltaCRnow*deltaphi;

     phi_ST=phi_ST_0*exp(log(ST_activ_time/cur_time)/(2.0*Alpha));
       }
     }
    }
// ********************************************
                         } // cur_time > t_CR_START condition

// store data and calculate t_eq, a_eq
double t_equil_cur_tube=A_eq*cur_time*(1.0 + B_eq/sqrt(cur_time));
t_ar.push_back(cur_time); phi_ar.push_back(phi_true);
phi_ST_ar.push_back(phi_ST);
t_eq_ar.push_back(t_equil_cur_tube);
phi_eq=GetPhiEq();
double tpast;
if(!supertube_activated){
 if(cur_time > 1.0){
tpast=-B_eq + sqrt(B_eq*B_eq + 4.0 *cur_time/A_eq);
tpast=0.25*tpast*tpast;
if(phi_eq < 0.999999){
   double tv=B_zeta*pow(phi_eq, 3.0*Alpha)*tpast;
   if(tv < Psi_rept){Psi_rept=tv; phi_rept=phi_eq;}
                     }
                   }
                        }
}
