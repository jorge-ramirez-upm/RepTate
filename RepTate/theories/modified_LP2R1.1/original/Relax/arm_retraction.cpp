#include "../include/LP2R.h"
/** \file
  *\brief relaxation from contour length fluctuation
  *
  * \param[in] np Index for polymer relaxing by CLF
  * \param[in] indx Set to zero at first call when z=0 (avoid division by zero)
  */
void arm_retraction(const int np, const int indx)
{
using namespace LP2R_NS;

double CLFpref=ret_pref_0 + (ret_pref - ret_pref_0)/
    (1.0 + exp(-ret_switch_exponent*(log(cur_time))) );
double dz=0.0;
if(indx == 0){ // first call; z=0
 dz=sqrt(2.0*CLFpref*sqrt(cur_time));
 LPoly[np]->z=dz;
             }
else{
 double z0=LPoly[np]->z;
 dz=0.50*CLFpref*sqrt(cur_time/pow(phi_eq, Alpha))*Log_DtMult/(z0*sqrt(Psi_rept));
if(dz > (0.50*LPoly[np]->Z_chain - LPoly[np]->z))
{ // Some chains may end up here at the interface of reptation and disentanglement
dz=0.50*LPoly[np]->Z_chain - LPoly[np]->z;
LPoly[np]->alive=false;
if(OutTermRelaxPathways){ // Treat them as disentanglement
 if(OutputFormat == "CSV"){
  f_trelax<< np << CSVdelimiter << LPoly[np]->wt << CSVdelimiter << LPoly[np]->mass << CSVdelimiter 
          << cur_time*tau_e << CSVdelimiter 
          << "2" << CSVdelimiter << phi_ST << CSVdelimiter << Psi_rept << std::endl;
                          }
 else{
  f_trelax<< np << " " << LPoly[np]->wt << " " << LPoly[np]->mass << " " << cur_time*tau_e << " " 
          << "2" << " " << phi_ST << " " << Psi_rept << std::endl;
     }
                        } // OutTermRelaxPathways

}
LPoly[np]->z=z0+dz;
    }

}

