#include "../include/LP2R.h"
/**
  * \file
  * \brief Zero shear viscosity
  */


/**
  * \brief Viscosity contribution from internal Rouse modes, Longitudinal modes, and Free Rouse chains
  *
  * Return viscosity in units of G_0*tau_e
  */
double viscRouseModes(void)
{
using namespace LP2R_NS;
double etaL=0.0; // Longitudinal
double etaIR=0.0; // Internal Rouse
double etaFR=0.0; // Unentangled chains

InvSqSum pInvSqSum;
for(int i1=0; i1<npoly; i1++){
 double zz=LPoly[i1]->Z_chain;
int zi=(int) ceil(zz);
int zm=(int) ceil(zz*N_e);

  if(!LPoly[i1]->relax_free_Rouse){

  etaL+=LPoly[i1]->wt*pInvSqSum(zi-1)*zz;
  etaIR+=LPoly[i1]->wt*pInvSqSum(zi,zm)*zz;
                                 }
  else{
   etaFR+=LPoly[i1]->wt*pInvSqSum(zm)*zz;
      }
                              }
double eta=0.25*(etaL+2.5*(etaIR+etaFR));
return eta;
}


/**
  * \brief zero-shear contribution from glassy modes
  */
double viscGlass(void)
{
using namespace LP2R_NS;
return G_glass*(tau_glass/beta_glass)*tgamma(1.0/beta_glass);
}



/**
  * \brief zero-shear viscosity from tube relaxation
  * in units of [G_0 * tau_e]
  */
double viscTubeRelax(void)
{
using namespace LP2R_NS;
double eta0=0.0;
int nd=t_ar.size();
double td=t_ar[nd-1];
double phiSTattd=phi_ST_ar[nd-1];
double tk, tm, dphi, dphiST, tv;
for(int k=1; k<nd; k++){
 dphi=phi_ar[k-1]-phi_ar[k]; tk=t_ar[k];
 tv=0.0;
  for(int m=1; m<nd; m++){
   dphiST=pow(phi_ST_ar[m-1], Alpha) - pow(phi_ST_ar[m], Alpha); tm=t_ar[m];
   tv+=dphiST*tm/(tk+tm);
                            }
   tv+=pow(phiSTattd, Alpha)*sqrt(td/tk)*(1.57079632679489661922 - atan(sqrt(td/tk)));
   eta0+=dphi*tk*tv;
                          }
return eta0;
}



/**
  * Return zero-shear viscosity as Pa-s
  */
double CalcVisc(void)
{
using namespace LP2R_NS;
double eta0=0.0;
if(t_ar.size() > 0){eta0=(1.0 - Rouse_wt)*viscTubeRelax();}
eta0+=viscRouseModes();
eta0+=viscGlass();

return eta0*G_0*tau_e;
}

