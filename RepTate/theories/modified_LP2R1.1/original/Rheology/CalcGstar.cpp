#include "../include/LP2R.h"
/** \file
  * \breif Calculate and output frequency responses
  *
  * \param[in] fRh File handle for mechanical response
  * \param[in] fDi File handle for dielectric response
  */

void CalcGstar(std::fstream &fRh, std::fstream &fDi)
{
using namespace LP2R_NS;

FreqMin=FreqMin*tau_e;
FreqMax=FreqMax*tau_e;
double freq=FreqMin/FreqRatio;
while(freq < FreqMax){
 freq*=FreqRatio;
 double gp=0.0, g2p=0.0, ep=0.0, e2p=0.0;
 double gptmp=0.0, g2ptmp=0.0, eptmp=0.0, e2ptmp=0.0;
  GStarGlass(freq, gptmp, g2ptmp); // glassy response
  gp=gptmp; g2p=g2ptmp;

  GStarRouse(freq, gptmp, g2ptmp, eptmp, e2ptmp); // unentangled Rouse
  gp+=gptmp; g2p+=g2ptmp; ep+=eptmp; e2p+=e2ptmp;

  if(Entangled_Dynamics){
    GStarFastRouse(freq, gptmp, g2ptmp); // In tube Rouse modes
     gp+=gptmp; g2p+=g2ptmp;

    GStarSlow(freq, gptmp, g2ptmp, eptmp, e2ptmp);
    gp+=(1.0 - Rouse_wt)*gptmp; g2p+=(1.0 - Rouse_wt)*g2ptmp;
    ep+=(1.0 - Rouse_wt)*eptmp; e2p+=(1.0 - Rouse_wt)*e2ptmp;
                        }

double visc=G_0*tau_e*sqrt(gp*gp+g2p*g2p)/freq;
if(OutputFormat == "CSV"){
 fRh << freq/tau_e << CSVdelimiter << gp*G_0 << CSVdelimiter << g2p*G_0 
     << CSVdelimiter << visc;
 if(CalcDielectric){ fRh << CSVdelimiter << ep << CSVdelimiter << e2p;}
 fRh << std::endl;
                         }
 else if(OutputFormat == "RepTate"){
 fRh << freq/tau_e << " " << gp*G_0 << " " << g2p*G_0 << std::endl;
 if(CalcDielectric){
 fDi << freq/tau_e << " " << ep << " " << e2p << std::endl;
                   }
                                   }
 else{
 fRh << freq/tau_e << " " << gp*G_0 << " " << g2p*G_0 << " " << visc;
 if(CalcDielectric){ fRh << " " << ep << " " << e2p;}
 fRh << std::endl;
     }

                     }
}
