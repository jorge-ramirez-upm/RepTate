#include "../include/LP2R.h"
void add_spectra_headers(std::fstream &fRh, std::fstream &fDi)
{
using namespace LP2R_NS;
if(OutputFormat == "RepTate"){ // Separate files; always header
  fRh << "T=" <<reptate_temp <<";" 
      << "Mw=" << Sys_MW << ";" << "PDI=" << Sys_PDI <<";";
 if(has_chem){fRh << "chem=" << reptate_chem <<";";}
 if(has_label){fRh << "label=" << reptate_label<<";"; }
 if(has_origin){fRh <<"origin=" << reptate_origin<<";"; }
 fRh << std::endl;
if(CalcDielectric){
fDi << "T=" <<reptate_temp <<";" 
    << "Mw=" << Sys_MW << ";" << "PDI=" << Sys_PDI<<";";
if(has_chem){fDi << "chem=" << reptate_chem<<";"; }
if(has_label){fDi << "label=" <<reptate_label<<";"; }
if(has_origin){fDi <<"origin=" << reptate_origin<<";"; }
fDi << std::endl;
                  }
                             }
else{ // Single file
if(Add_header){
 if(OutputFormat == "CSV"){
 fRh << "w" << CSVdelimiter << "G\'(w)" << CSVdelimiter 
     << "G\"(w)" << CSVdelimiter << "eta(w)" ;
 if(CalcDielectric){fRh << CSVdelimiter << "e\'(w)/Delta_e" 
                        << CSVdelimiter << "e\"(w)/Delta_e";}
                          }
 else if(OutputFormat == "Text"){
  fRh << "w  G\'(w)  G\"(w) eta(w)";
  if(CalcDielectric){fRh << " e\'(w)/Delta_e e\"(w)/Delta_e"; }
                                }
 else{
  fRh << "#w  G\'(w)  G\"(w) eta(w)";
  if(CalcDielectric){fRh << " e\'(w)/Delta_e e\"(w)/Delta_e"; }
     }

 fRh << std::endl;
              }
    }
}
