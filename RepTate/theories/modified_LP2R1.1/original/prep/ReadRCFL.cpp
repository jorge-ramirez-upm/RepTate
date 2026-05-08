#include "../include/LP2R.h"

/** 
  * \file
  * \brief
  * Read options given as option=value pair in a file
  */

/**
  * return \c true if string sR=="yes"
  */
bool assign_RHS_bool(std::string &sR)
{
if(sR == "yes"){return true;}
else{return false;}
}


/**
   * Try to assign double equivalent value of sR to param (repeated as string sprm). 
   * If it fails, it will assign the default value val (repeated as string sval).
   *
   * \param[out] param parameter value represented in string sR
   * \param[in] sR string object representing some double
   * \param[in] sprm Name of the parameter we are trying to assign
   * \param[in] val default value of the parameter
   */

void assign_RC_dbl(double &param, const std::string &sR, const std::string sprm, const double val)
{
    try{param=std::stod(sR);}
    catch(...){param=val; 
if(LP2R_NS::GenLogFL){
LP2R_NS::f_Log << "Could not make sense of value of " << sprm << " as " << sR << " in file " << LP2R_NS::rcFNM <<std::endl;
LP2R_NS::f_Log << "     Will proceed with default value of " << sprm << "=" << val << std::endl << std::endl; }
              } 
}

/**
  * (If present) read resource file
  * Ignore anything that does not make sense
  */

void ReadRCFL(void)
{
using namespace LP2R_NS;

std::fstream f1;
f1.open(rcFNM, std::ios_base::in);

if(f1){
if(GenLogFL){
f_Log << std::endl << "Found resource file " << rcFNM <<  std::endl;
            }
std::string sL,sR;
while(!readEquality(f1,sL,sR).eof()){
  if(sL == "Alpha"){ assign_RC_dbl(Alpha, sR, "Alpha", 1.0);}
  else if(sL=="t_CR_START"){assign_RC_dbl(t_CR_START, sR, "t_CR_START", 1.0);}
  else if(sL=="deltaCR"){assign_RC_dbl(deltaCR, sR, "deltaCR", 0.30);}
  else if(sL=="B_zeta"){assign_RC_dbl(B_zeta, sR, "B_zeta", 2.0);}
  else if(sL=="A_eq"){assign_RC_dbl(A_eq, sR,"A_eq", 2.0);}
  else if(sL=="B_eq"){assign_RC_dbl(B_eq, sR, "B_eq", 10.0);}
  else if(sL=="ret_pref"){assign_RC_dbl(ret_pref, sR, "ret_pref", 0.189); }
  else if(sL=="Rept_Switch_Factor"){assign_RC_dbl(Rept_Switch_Factor, sR, "Rept_Switch_Factor",1.664); }
  else if(sL=="Rouse_Switch_Factor"){assign_RC_dbl(Rouse_Switch_Factor, sR, "Rouse_Switch_Factor", 1.50);}
  else if(sL=="Start_time"){assign_RC_dbl(cur_time, sR, "Start_time",1.0e-3);
   if(cur_time < 1.0e-8){
        if(GenLogFL){ f_Log << "Found Start_time = "<< cur_time<< " in rc file " << rcFNM << std::endl;
     f_Log << "Logarithmically spaced time intervals is used (Start_time should be greater than 0)" << std::endl;
     f_Log << "Using Start_time = 1.0e-3 (anything below 1.0e-8 will give this message)" << std::endl << std::endl;}
        cur_time=1.0e-3;
                         }
                           }
  else if(sL=="Time_ratio"){assign_RC_dbl(DtMult, sR, "Time_ratio", 1.02);
   if(DtMult <= 1.000001){
   if(GenLogFL){ f_Log << "Found Time_ratio = " << DtMult << " in rc file " << rcFNM << std::endl;
                 f_Log << "Time ratio is ratio of successive discretized times, hence greater than 1.0" << std::endl;
              f_Log << "Using Time_ratio = 1.02 (anything below 1.000001 will give this message)" << std::endl << std::endl;}
              DtMult=1.02;
                         }
                           }
  else if(sL=="CalcDielectric"){
     if(!CalcDielectric){if(assign_RHS_bool(sR)){CalcDielectric=true;} } }
  else if(sL=="OutputFormat"){OutputFormat=sR;}
  else if(sL=="OutTermRelaxPathways"){if(assign_RHS_bool(sR)){OutTermRelaxPathways=true;} }
  else if(sL=="OutPhiPhiST"){if(assign_RHS_bool(sR)){OutPhiPhiST=true;}}
  else if(sL=="Output_G_of_t"){if(assign_RHS_bool(sR)){Output_G_of_t=true;}}
  else if(sL=="CSVdelimiter"){
   if(sR.size() > 0){CSVdelimiter=sR;}
                             }
  else if(sL=="Add_header"){Add_header=assign_RHS_bool(sR);}
  else if(sL=="label"){
  if(sR.size() > 0){ has_label=true; reptate_label=sR;}
                      }
  else if(sL=="origin"){
   if(sR.size() > 0){ has_origin=true; reptate_origin=sR;}
                       }
  else if(sL=="chem"){
   if(sR.size() > 0){has_chem=true; reptate_chem=sR;}
                     }
  else if(sL=="Temp"){has_temp=true; assign_RC_dbl(reptate_temp, sR, "Temperature", 0.0);}
  else if(sL=="ret_pref_0"){assign_RC_dbl(ret_pref_0, sR, "ret_pref_0", 0.020);}
  else if(sL=="ret_switch_exponent"){assign_RC_dbl(ret_switch_exponent, sR, "ret_switch_exponent", 0.42);}
  else if(sL=="Disentanglement_Switch"){assign_RC_dbl(Disentanglement_Switch, sR, "Disentanglement_Switch", 1.0);}
 else{
  if(GenLogFL){ f_Log << std::endl << "Ignoring unresolved statement in rc file " 
          << rcFNM << ":" << std::endl;
          f_Log << "          " << sL << " = " << sR << std::endl << std::endl; } }


                                    }
f1.close();
  }
else{
if(GenLogFL){
 f_Log << std::endl << "Did not find resource file " << rcFNM << std::endl;
 f_Log << "    (will proceed will default parameters)" << std::endl;
            }
           } // no resource file, proceed with default
CSVdelimiter+=" "; // Add a space here 
// Long time maximum allowed drop in phi_ST during one time-step
STmaxDrop=exp(-log(DtMult)/(2.0*Alpha));
// logarithm of DtMult
Log_DtMult=log(DtMult);
}
