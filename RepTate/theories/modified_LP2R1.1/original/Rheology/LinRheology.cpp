#include "../include/LP2R.h"
/**
  * \file
  * \brief Calculate relaxation spectra (and possibly time relaxation)
  * 
  */

void LinRheology(void)
{
using namespace LP2R_NS;

std::fstream fRh;
std::fstream fDi;
fRh.open(MechRelSpecFNM, std::ios::out); 
if(CalcDielectric){
if(OutputFormat == "RepTate"){ // only RepTate format uses two different files
   fDi.open(DiRelSpecFNM, std::ios::out);}
                  }
add_spectra_headers(fRh, fDi);
CalcGstar(fRh, fDi);
fRh.close(); if(fDi){fDi.close();}

if(GenLogFL){double eta0=CalcVisc(); f_Log << "Zero-shear viscosity = " << eta0 << std::endl;}

if(Output_G_of_t){
 fRh.open(MechRelFNM, std::ios::out);
 add_goft_headers(fRh);
 Calc_goft(fRh);
 fRh.close();
                 } 

}
