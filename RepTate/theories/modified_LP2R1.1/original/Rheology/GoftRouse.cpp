#include "../include/LP2R.h"
/** \file
  * \brief G(t) contribution from unentangled chains
  *
  * \param[in] t time in units of tau_e
  * \return G(t) in units of G_0
  */
double GoftRouse(const double t)
{
using namespace LP2R_NS;
double gt=0.0, gR=0.0;
for(int i1=0; i1<npoly; i1++){
if(LPoly[i1]->relax_free_Rouse){
gR=0.0;
double tau1=LPoly[i1]->t_FRouse;
int pmax=(int) ceil(LPoly[i1]->Z_chain*N_e);
for(int p=1; p<= pmax; p++){
 double psq=(double) (p*p);
 double taup=tau1/(2.0*psq);
 gR+=exp(-t/taup);
                           }
gt+=gR*5.0*LPoly[i1]->wt/(4.0*LPoly[i1]->Z_chain);
                               }
                             }
return gt;
}
