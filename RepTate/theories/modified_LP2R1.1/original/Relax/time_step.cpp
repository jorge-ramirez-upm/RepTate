#include "../include/LP2R.h"
/** \file
  * \brief update relaxation by one time step
  * \param[in] indx set to zero for first call
  * \return number of chains still trapped in old tubes
  */
int time_step(const int indx)
{
using namespace LP2R_NS;
if(indx != 0){cur_time*=DtMult;}

for(int i=0; i<npoly; i++){
 if(LPoly[i]->alive){
   if(!LPoly[i]->rept_set){arm_retraction(i, indx);}
   if(LPoly[i]->alive && (cur_time > 1.0)){try_reptate(i);}
                    }
 if(LPoly[i]->alive){
 if( LPoly[i]->Z_chain*pow(phi_ST,Alpha) < Disentanglement_Switch){
      LPoly[i]->z=0.50*LPoly[i]->Z_chain; LPoly[i]->alive=false; 
if(OutTermRelaxPathways){
 if(OutputFormat == "CSV"){
  f_trelax << i << CSVdelimiter << LPoly[i]->wt << CSVdelimiter << LPoly[i]->mass << CSVdelimiter 
           << cur_time*tau_e << CSVdelimiter << "2" << CSVdelimiter << phi_ST << CSVdelimiter << Psi_rept << std::endl;
                          }
 else{
  f_trelax << i << " " << LPoly[i]->wt << " " << LPoly[i]->mass << " " << cur_time*tau_e << " " 
          << "2" << " " << phi_ST << " " << Psi_rept << std::endl;
     }
                        }
                                                                  }
                    }

                          }

frac_unrelaxed();
if(OutPhiPhiST){
  if(OutputFormat == "CSV"){
   f_phi << cur_time*tau_e << CSVdelimiter << phi_true << CSVdelimiter << phi_ST << CSVdelimiter 
         << phi_eq << CSVdelimiter << phi_rept << CSVdelimiter << Psi_rept << std::endl; }
  else{ f_phi << cur_time*tau_e << " " << phi_true << " " << phi_ST << " " 
              << phi_eq << " " << phi_rept << " " << Psi_rept << std::endl; }
               }

int nalive=0;
for(int i=0; i<npoly; i++){
 if(LPoly[i]->alive){nalive++;}}
return nalive;
}
