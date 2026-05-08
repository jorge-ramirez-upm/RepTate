#include "../include/LP2R.h"

/** 
  * \file
  * \brief
  * Read material parameters from the input file and call \c genPolyLin
  * \return nonzero integer in case input fails
  */
int ReadInput(void)
{
using namespace LP2R_NS;
// First try to read rc file
 ReadRCFL();

std::fstream f1;
f1.open(inpFNM, std::ios::in);
if(!f1){
if(GenLogFL){f_Log << "ERROR: Failed to open file " << inpFNM << " for input" << std::endl;}
  return 1;
       }
if(GenLogFL){f_Log << std::endl << "Opened " << inpFNM << " for input" << std::endl;}

std::string s1;
std::stringstream s1strm;
s1strm.str(std::string());

if(!safeGetline(f1, s1).eof()){
 s1strm << s1 << std::endl;
if(!(s1strm >> FreqMin)){
if(GenLogFL){f_Log << "ERROR: Failed to read minimum frequency in file " << inpFNM << std::endl;}
              return 2;}
if(!(s1strm >> FreqMax)){
if(GenLogFL){f_Log << "ERROR: Failed to read maximum frequency in file " << inpFNM << std::endl;
  f_Log << " (unintended line break? FreqMin, FreqMax, FreqRatio need to be in the same line)" << std::endl;}
              return 3;}
if(!(s1strm >> FreqRatio)){
if(GenLogFL){f_Log << "ERROR: Failed to read frequency ratio in file " << inpFNM << std::endl;
  f_Log << " (unintended line break? FreqMin, FreqMax, FreqRatio need to be in the same line)" << std::endl;}
                   return 4;}
                              }
else{
if(GenLogFL){f_Log << "ERROR: File " << inpFNM << " ended before reading frequency information for rheology response output" << std::endl;}
return 5;
    }
// Do basic checks on frequencies
if(FreqMin > FreqMax){
double tmp1=FreqMin; FreqMin=FreqMax; FreqMax=tmp1;
                     }
if(FreqMin < 1.0e-32){
if(GenLogFL){f_Log << "Minimum frequency is read as " << FreqMin << std::endl;
             f_Log << "   We need FreqMin to be greater than 1.0e-32" << std::endl;
             f_Log << "   Resetting FreqMin=1.0e-32" << std::endl; }
    FreqMin=1.0e-32;
                      }
if(FreqRatio < 1.000001){
if(GenLogFL){f_Log << "FreqRatio is read as " << FreqRatio << std::endl;
        f_Log << "    We need FreqRatio greater than 1.000001" << std::endl;
        f_Log << "    Resetting FreqRatio=1.01" << std::endl; }
FreqRatio=1.01;
                       }

if(GenLogFL){f_Log << "FreqMin=" << FreqMin <<"    FreqMax=" << FreqMax <<"    FreqRatio" << FreqRatio <<std::endl;}

if(!safeGetline(f1, s1).eof()){
s1strm.str(std::string());
s1strm << s1 << std::endl;
if(!(s1strm >> M_Kuhn)){
if(GenLogFL){f_Log << "ERROR: Failed to read M_Kuhn in file " << inpFNM << std::endl;}
             return 6;}
if(!(s1strm >> M_e)){
if(GenLogFL){f_Log << "ERROR: Failed to read M_e in file " << inpFNM << std::endl;
  f_Log << " (unintended line break? M_Kuhn, M_e, G_0, tau_e need to be in the same line)" << std::endl;}
             return 7;}
if(!(s1strm >> G_0)){
if(GenLogFL){f_Log << "ERROR: Failed to read G_0 in file " << inpFNM << std::endl;
  f_Log << " (unintended line break? M_Kuhn, M_e, G_0, tau_e need to be in the same line)" << std::endl;}
             return 8;}
if(!(s1strm >> tau_e)){
if(GenLogFL){f_Log << "ERROR: Failed to read tau_e in file " << inpFNM << std::endl;
  f_Log << " (unintended line break? M_Kuhn, M_e, G_0, tau_e need to be in the same line)" << std::endl;}
               return 9;}
                            }
else{
if(GenLogFL){f_Log << "ERROR: File " << inpFNM << " ended before reading  M_Kuhn" << std::endl;}
  return 10;
    }
if(GenLogFL){f_Log << "M_Kuhn="<<M_Kuhn <<"  M_e="<<M_e <<" G_0=" << G_0 << " tau_e=" << tau_e << std::endl;}
N_e=M_e/M_Kuhn;

if(!safeGetline(f1, s1).eof()){
s1strm.str(std::string());
s1strm << s1 << std::endl;
if(!(s1strm >> G_glass)){
if(GenLogFL){f_Log << "ERROR: Failed to read G_glass in file " << inpFNM << std::endl;}
             return 11;}
if(!(s1strm >> tau_glass )){
if(GenLogFL){f_Log << "ERROR: Failed to read tau_glass in file " << inpFNM << std::endl;
  f_Log << " (unintended line break? G_glass, tau_glass, beta_glass need to be in the same line)" << std::endl;}
                return 12;}
if(!(s1strm >> beta_glass)){
if(GenLogFL){f_Log << "ERROR: Failed to read beta_glass in file " << inpFNM << std::endl;
  f_Log << " (unintended line break? G_glass, tau_glass, beta_glass need to be in the same line)" << std::endl;}
                return 13;}
                            }
else{
if(GenLogFL){f_Log << "ERROR: File " << inpFNM << " ended before reading G_glass" << std::endl;}
return 14;}
if(GenLogFL){f_Log << "G_glass=" << G_glass << "  tau_glass="<< tau_glass << "  beta_glass=" << beta_glass <<std::endl;}

// rescale glassy modulus
tau_glass/=tau_e;
G_glass=(G_glass - 1.250*G_0)/G_0;

int errval=genPolyLin(f1);
f1.close();
return errval;
}
