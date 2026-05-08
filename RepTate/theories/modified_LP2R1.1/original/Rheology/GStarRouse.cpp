/**
  * \file
  * \brief Rouse spectra for unentangled chains
  *
  * \param[in] freq Frequency
  * \param[out] gRs G'
  * \param[out] g2Rs G"
  * \param[out] eRs epsilon'
  * \param[out] e2Rs epsilon"
  */

#include "../include/LP2R.h"
void GStarRouse(double freq, double &gRs, double &g2Rs, double &eRs, double &e2Rs)
{
using namespace LP2R_NS;
gRs=0.0; g2Rs=0.0; eRs=0.0; e2Rs=0.0;

double gR, g2R, eR, e2R, taup, tv, tv2;
for(int i1=0; i1<npoly; i1++){
if(LPoly[i1]->relax_free_Rouse){
gR=g2R=eR=e2R=0.0;
double tau1=LPoly[i1]->t_FRouse; // Z^2 * tau_e
int pmax=(int) ceil(LPoly[i1]->Z_chain*N_e);

for(int p=1; p<= pmax; p++){
 double psq=(double) (p*p);
 taup=tau1/(2.0*psq); // stress relaxation time
 tv=freq*taup;
 tv2=tv*tv;
 gR+=tv2/(1.0+tv2);
 g2R+=tv/(1.0+tv2);
if(p%2 != 0){
 taup=tau1/psq;
  tv=freq*taup;
  tv2=tv*tv;
  eR+=tv2/(psq*(1.0 + tv2));
  e2R+=tv/(psq*(1.0 + tv2));
            }

                           }
gR=gR*5.0*LPoly[i1]->wt/(4.0*LPoly[i1]->Z_chain); 
g2R=g2R*5.0*LPoly[i1]->wt/(4.0*LPoly[i1]->Z_chain);
gRs+=gR; g2Rs+=g2R;
eRs+=LPoly[i1]->wt*eR;
e2Rs+=LPoly[i1]->wt*e2R;
                          }
                           }

}
