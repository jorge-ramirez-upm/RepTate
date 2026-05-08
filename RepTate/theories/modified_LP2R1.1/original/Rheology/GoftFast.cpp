#include "../include/LP2R.h"
/** \file
  * \brief G(t) contribution from in-tube Rouse modes
  *
  * \param[in] t time in units of tau_e
  * \return G(t) in units of G_0
  */
double GoftFast(const double t)
{
using namespace LP2R_NS;
double gt=0.0, gR=0.0;
int zi=1;
for(int i1=0; i1<npoly; i1++){
if(!LPoly[i1]->relax_free_Rouse){
double zz=LPoly[i1]->Z_chain;
double tauR=LPoly[i1]->t_FRouse; // Z^2 \tau_e
zi=(int) ceil(zz);
gR=0.0;
  for(int p=1; p<zi; p++){ // longitudinal contribution
   double psq=(double) (p*p);
   gR+=exp(-psq*t/tauR);
                         }
int max_term=(int)ceil(N_e * zz);
  for(int p=zi; p<max_term; p++){ // internal Rouse modes
    double psq2=(double) (2*p*p);
    gR+=5.0*exp(-psq2*t/tauR);
                                }
gt+= gR*LPoly[i1]->wt/(4.0*zz);
                                }
                             }
return gt;
}
