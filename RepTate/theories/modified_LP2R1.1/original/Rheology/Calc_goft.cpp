#include "../include/LP2R.h"
/** \file
  * \brief Calculate G(t)
  *
  * The span of time is hardcoded here between \f$ 10^{-4} \tau_e \f$ and \f$ 10^{4} \tau_d \f$ with
  * \f$ \tau_d \f$ being the longest relaxation time. 
  *
  * \param[in] fRh File handle for the output
  */

void Calc_goft(std::fstream &fRh)
{
using namespace LP2R_NS;
double t_min=1.0e-4;
double t_max=1.0e4;
if(Entangled_Dynamics){
  t_max=t_ar[t_ar.size() - 1]*1.0e4;
                      }
double t_ratio=1.1;


double tt=t_min/t_ratio;

while(tt < t_max){
tt*=t_ratio;
double muoft=0.0, Roft=0.0;
double gt_glass=G_glass*exp(-pow(tt/tau_glass, beta_glass));
double gt_FR=GoftRouse(tt);
double gt_Fast=GoftFast(tt);
double gt_Tube=GoftTube(tt, muoft, Roft);
double gt=G_0*(gt_glass+gt_FR+gt_Fast+gt_Tube);
if(OutputFormat == "RepTate"){
  fRh << tt*tau_e << " " << gt << std::endl;
                             }
else if(OutputFormat == "CSV"){
  fRh << tt*tau_e << CSVdelimiter << gt << CSVdelimiter << muoft << CSVdelimiter << Roft << std::endl; 
                              }
else{ fRh << tt*tau_e << " " << gt << " " << muoft << " " << Roft << std::endl;}
                 }
}
