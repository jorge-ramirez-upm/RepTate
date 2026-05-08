#include "../include/LP2R.h"
/** \file
  * \brief add appropriate header to time domain relaxation output file
  * 
  * \param[in] fRh File handle for G(t) output
  */
void add_goft_headers(std::fstream &fRh)
{
using namespace LP2R_NS;
if(OutputFormat == "RepTate"){
 fRh << "Mw=" << Sys_MW << ";gamma=1; " << std::endl;
 fRh << "t sxy" << std::endl;
                             }
else{ 
 if(Add_header){
   if(OutputFormat == "CSV"){
     fRh << "t" << CSVdelimiter << "G(t)"  << CSVdelimiter << "mu(t)" << CSVdelimiter << "R(t)"<< std::endl;
                            }
   else if(OutputFormat == "Text"){
     fRh << "t  G(t) mu(t) R(t)" << std::endl;
                                  }
   else{
     fRh << "#t  G(t) mu(t) R(t)" << std::endl;
       }
               }
    }
}
