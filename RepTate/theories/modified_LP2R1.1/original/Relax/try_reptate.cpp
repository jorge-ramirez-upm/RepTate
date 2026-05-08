#include "../include/LP2R.h"
/** \file
  * \brief Attempt relaxation by reptation
  * \param[in] np index of chain for which reptation is attempted
  */
void try_reptate(const int np)
{
using namespace LP2R_NS;
if( !LPoly[np]->rept_set){
double tcomp=Rept_Switch_Factor*3.0*LPoly[np]->Z_chain * LPoly[np]->z * LPoly[np]->z*Psi_rept ;
 if(tcomp < cur_time){
   LPoly[np]->rept_set=true;
   double len_to_rept=LPoly[np]->Z_chain - 2.0 * LPoly[np]->z;
   LPoly[np]->tau_d_0=3.0 *  LPoly[np]->Z_chain* len_to_rept * len_to_rept *Psi_rept ;

// For only linear polymer, the following ensures that reptation time for a given chain cannot be lower 
// than that of some shorter chain.
// May need rethinking when branched polymers are added in future.
   if(LPoly[np]->tau_d_0 < LastReptationTime){
    if(LPoly[np]->Z_chain < LastReptZ){ LPoly[np]->tau_d_0=LastReptationTime; }
                                             }
   else{LastReptationTime=LPoly[np]->tau_d_0; LastReptZ=LPoly[np]->Z_chain;}
   LPoly[np]->Z_rept=len_to_rept;
if(OutTermRelaxPathways){
 if(OutputFormat == "CSV"){
  f_trelax<< np << CSVdelimiter << LPoly[np]->wt << CSVdelimiter << LPoly[np]->mass << CSVdelimiter 
          << LPoly[np]->tau_d_0*tau_e << CSVdelimiter << "1" << CSVdelimiter 
          << phi_rept << CSVdelimiter << Psi_rept << std::endl;
                          }
 else{
  f_trelax<< np << " " << LPoly[np]->wt << " " << LPoly[np]->mass << " " 
                << LPoly[np]->tau_d_0*tau_e << " " << "1" 
                << " " << phi_rept << " " << Psi_rept << std::endl;
     }
                        } // OutTermRelaxPathways

if(LPoly[np]->tau_d_0 < cur_time){LPoly[np]->p_max=1;}
else{
     LPoly[np]->p_max=(int) floor(sqrt(LPoly[np]->tau_d_0/cur_time));
     if((LPoly[np]->p_max)%2 ==0){LPoly[np]->p_max=LPoly[np]->p_max-1;}
    }
if(LPoly[np]->p_max < 1){LPoly[np]->p_max=1;}
     LPoly[np]->p_next=LPoly[np]->p_max;
     LPoly[np]->rept_wt=0.0;
     for(int i=1; i<=LPoly[np]->p_max; i+=2){
                   LPoly[np]->rept_wt+=1.0/((double) (i*i));
                                            }

                     } // Set reptation
                         } // Check for reptation

if(LPoly[np]->rept_set){
double psq=(double) (LPoly[np]->p_next * LPoly[np]->p_next);
 if(cur_time > (LPoly[np]->tau_d_0/psq)){
   LPoly[np]->z+=0.50*LPoly[np]->Z_rept/(LPoly[np]->rept_wt*psq);
   if(LPoly[np]->p_next == 1){
     LPoly[np]->z=0.50*LPoly[np]->Z_chain;
     LPoly[np]->alive=false;
                            }
   else{LPoly[np]->p_next=LPoly[np]->p_next-2;}
                                                             }
                     }

}


