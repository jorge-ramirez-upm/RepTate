#include "../include/LP2R.h"
/**
  * \file
  * \brief Handle output in RepTate format
  */

/**
  * \brief Open files for Reptate format and add headers
  * \param[out] fRh : file for mechanical spectra output
  * \param[out] fDi : file for Dielectric spectra output
  */
void RepTateOpen(std::fstream &fRh, std::fstream &fDi)
{
using namespace LP2R_NS;
fRh.open(MechRelSpecFNM, std::ios::out);
fRh << "T=" <<reptate_temp <<";  " <<
"Mw=" << Sys_MW << ";  " << "PDI=" << Sys_PDI;
if(has_chem){fRh << ";  chem=" << reptate_chem; }
 if(has_label){fRh << "; label=" << reptate_label; }
 if(has_origin){fRh <<"; origin=" << reptate_origin; }
 fRh << std::endl;

if(CalcDielectric){
 fDi.open(DiRelSpecFNM, std::ios::out);
 fDi << "T=" <<reptate_temp <<";  " <<
        "Mw=" << Sys_MW << ";  " << "PDI=" << Sys_PDI;
 if(has_chem){fDi << ";  chem=" << reptate_chem; }
 if(has_label){fDi << "; label=" << reptate_label; }
 if(has_origin){fDi <<"; origin=" << reptate_origin; }
 fDi << std::endl;
                  }

}

/**
  * \brief write relaxation data in RepTate format
  *
  * \param[in] fRh : file for mechanical spectra output
  * \param[in] fDi : file for Dielectric spectra output
  * \param[in] res : fixed length array containing w, G', G", and possibly e', e"
  */

void RepTateWrite(std::fstream &fRh, std::fstream &fDi, const double(&res) [5])
{
if(fRh){fRh << res[0] << " " << res[1] " " << res[2] << std::endl;}
if(CalcDielectric){
if(fDi){fDi << res[0] << " " << res[3] << " " << res[4] << std::endl;}
                  }
}

/**
  * \brief Open file for CSV format and add headers
  * \param[out] fRh : file for mechanical spectra output
  */
void CSVOpen(std::fstream &fRh)
{
using namespace LP2R_NS;
fRh.open(MechRelSpecFNM, std::ios::out);
 if(Add_header){
  fRh << "w" << CSVdelimiter << " G'(w)" << CSVdelimiter << " G\"(w)" << CSVdelimiter << " eta(w)";
if(CalcDielectric){ fRh << CSVdelimiter  <<" e'(w)" << CSVdelimiter  << " e\"(w)"}
fRh << std::endl;
  fRh << "rad/s" << CSVdelimiter << " Pa" << CSVdelimiter << " Pa" << CSVdelimiter << " Pa-s";
if(CalcDielectric){ fRh << CSVdelimiter  <<" " << CSVdelimiter  << " "}
fRh << std::endl;
               }
}

/**
  * \brief write relaxation data in CSV file 
  *
  * \param[in] fRh : file for relaxation spectra output
  * \param[in] res : fixed length array containing w, G', G", and possibly e', e"
  */
void CSVWrite(std::fstream &fRh, const double(&res) [5])
{
if(fRh){fRh << res[0] << CSVdelimiter << " " << res[1]<< CSVdelimiter <<  " " 
    << res[2] << CSVdelimiter << " "  << sqrt(res[1]*res[1]+res[2]*res[2])/res[0]; 
if(CalcDielectric){
fRh << CSVdelimiter << " " << res[3] << CSVdelimiter << " " << res[4]; 
                  }
fRh << std::endl;
       }

}
