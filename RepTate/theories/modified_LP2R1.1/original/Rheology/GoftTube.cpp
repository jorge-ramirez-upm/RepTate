#include "../include/LP2R.h"
/** \file
  * \brief G(t) contribution from tube constraints: \f$ mu(t)*R(t) \f$
  *
  * \param[in] t time in units of tau_e
  * \param[out] muoft Tube survival probability \f$ \mu(t) \f$
  * \param[out] Roft Constraint release contribution \f$ R(t) \f$
  * \return G(t) in units of G_0
  */
double GoftTube(const double t, double &muoft, double &Roft)
{
using namespace LP2R_NS;
muoft=0.0; Roft=0.0;
int n=t_ar.size();
double goft=0.0;
if(Entangled_Dynamics){
 for(int k=1; k<n; k++){ // loop over time slices
   double dphi=phi_ar[k-1] - phi_ar[k]; double tk=t_ar[k];
   muoft+=dphi*exp(-t/tk);
   double dphiST=pow(phi_ST_ar[k-1], Alpha) -pow(phi_ST_ar[k], Alpha);
   Roft+=dphiST*exp(-t/tk);
                       }
  double taud=t_ar[n-1];
  double rint=0.50*pow(phi_ST_ar[n-1], Alpha)*1.77245385090551602729*sqrt(taud/t)*
    (1.0 - erfc(sqrt(t/taud))); // integral beyond when muoft goes to zero
  Roft+=rint;
  goft=muoft*Roft;
                      }
return goft;
}
