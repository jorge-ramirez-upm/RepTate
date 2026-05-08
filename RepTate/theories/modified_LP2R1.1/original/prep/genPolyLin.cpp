#include "../include/LP2R.h"
/**
  *\file
  *\brief
  * Read input for polymer components and generate/read polymers
  */

/**
  * Read input for polymer components and generate polymers
  * \param[in] f1 input file stream
  * \return status=0 if success, else non-zero
  */
int genPolyLin(std::fstream &f1)
{
using namespace LP2R_NS;

int num_comp;
std::string s1; std::stringstream s1strm;
if(!safeGetline(f1, s1).eof()){
s1strm.str(std::string());
s1strm << s1 << std::endl;
if(!(s1strm >> num_comp)){
if(GenLogFL){f_Log << "ERROR: Failed to read num_comp (Number of components) in file " << inpFNM << std::endl;}
              return 20;};
                            }
else{
if(GenLogFL){f_Log << "ERROR: File " << inpFNM << " ended before reading num_comp" << std::endl;}
 return 21;
    }

// make sure we have positive number of components
if(num_comp <= 0){
if(GenLogFL){f_Log << "Given number of components as num_comp=" << num_comp << std::endl;
             f_Log << " This must be a positive number! Will give up now." << std::endl;}
return 21;
                 }
if(GenLogFL){f_Log << "num_comp=" << num_comp << std::endl;}


std::vector<int> ptype;
std::vector<double> wtcomp;
std::vector<std::string> polyinfo;

for(int i=0; i<num_comp; i++){
 if(!safeGetline(f1, s1).eof()){
s1strm.str(std::string());
s1strm << s1 << std::endl;
  int a0; double b0;
if(!(s1strm >> a0)){
if(GenLogFL){f_Log << "ERROR: Failed to read ptype for component "<< i << " in file "<< inpFNM << std::endl;}
        return 22;}
if(!(s1strm >> b0)){
if(GenLogFL){f_Log << "ERROR: Failed to read wtfrac for component "<< i << " in file "<< inpFNM << std::endl;
f_Log <<" (unintended line break? ptype and wtfrac need to be in the same line) " << std::endl;}
        return 23;}
ptype.push_back(a0);
wtcomp.push_back(b0);
                               }
 else{
if(GenLogFL){f_Log << "ERROR: File " << inpFNM << " ended before reading information for component "<< i << std::endl;}
return 24;
     }

 if(!safeGetline(f1, s1).eof()){ polyinfo.push_back(s1); }
 else{
if(GenLogFL){f_Log << "ERROR: File " << inpFNM << " ended before reading information for component "<< i << std::endl;}
   return 25;}

                             }
// We have got all the information from input file; close it now
f1.close();
double wttot=0.0;
for(int i=0; i<num_comp; i++){wttot+=wtcomp[i];}
for(int i=0; i<num_comp; i++){wtcomp[i]/=wttot;}

int errval=0;
int na=0; double mwa=0.0, pdia=1.0;
for(int i=0; i<num_comp; i++){
if(errval == 0){
switch(ptype[i]){
 case 0: 
     s1strm.str(std::string());
     s1strm << polyinfo[i] << std::endl;
     s1strm >> na >> mwa >> pdia;
     if(s1strm.fail()){
       if(GenLogFL){
  f_Log << "Failed to process polymer information for component " << i+1 <<" (LogNormal distribution)." << std::endl
        << "We need number of component, weight averaged molar mass, and polydispersity index here." << std::endl
        << "The input ( " << s1 << " ) could not be read as one integer and two doubles. " << std::endl
        << "Will stop here." << std::endl; }

       errval=26; // return errval;
                     }
      GenLinLogNormal(na, mwa, pdia, wtcomp[i]);
      break;
 case 1: errval=GenLinGPC(polyinfo[i], wtcomp[i]); 
         if(errval != 0){return errval;}
         break;
 case 2: errval=GenLinWt(polyinfo[i], wtcomp[i]); 
         if(errval != 0){return errval;}
         break;
 default:
       if(GenLogFL){
  f_Log << "Unknown polymer type " << ptype[i] << " form component " << i+1 << std::endl
        << "Will stop here." << std::endl; }
       errval=28; return errval;
       break;
                }
                             }}
if(errval != 0){return errval;}
// ensure that total weight adds up to one
wttot=0.0;
for(int i=0; i<npoly; i++){ wttot+=LPoly[i]->wt; }
for(int i=0; i<npoly; i++){ LPoly[i]->wt/=wttot; }

// assign file names (and may be open output file for relaxation pathways
assign_FNMs();
// identify chains that should not get entangled dynamics
// Calculate molar mass moments

int num_entangled=0;
for(int i=0; i<npoly; i++){
  if(LPoly[i]->Z_chain< Rouse_Switch_Factor){
     LPoly[i]->relax_free_Rouse=true; LPoly[i]->alive=false; Rouse_wt+=LPoly[i]->wt;
if(OutTermRelaxPathways){
if(OutputFormat == "CSV"){
f_trelax << i<< CSVdelimiter << LPoly[i]->wt << CSVdelimiter << LPoly[i]->mass << CSVdelimiter  
         << LPoly[i]->t_FRouse*tau_e << CSVdelimiter << "0" << CSVdelimiter  
         << "1.0" << CSVdelimiter << "1.0" << std::endl;
                       }
else{ f_trelax << i << " " << LPoly[i]->mass << " " << LPoly[i]->wt << " " 
               << LPoly[i]->t_FRouse*tau_e << " " << "0  1.0 1.0" << std::endl;}
                        }
                                            }
  else{num_entangled++;}

  Sys_MN+= LPoly[i]->wt/LPoly[i]->mass;
  Sys_MW+=LPoly[i]->wt * LPoly[i]->mass;
                          }
Sys_MN=1.0/Sys_MN;
Sys_PDI=Sys_MW/Sys_MN;
if(GenLogFL){
  f_Log << "M_w = " << Sys_MW << ",   M_n = " << Sys_MN << ",   PDI = " << Sys_PDI << std::endl;
            }

if(num_entangled == 0){Entangled_Dynamics=false;
  if(GenLogFL){f_Log << "The polymer system is treated as unentangled Rouse melt. " << std::endl; }
                      }

// Add data for time zero
t_ar.push_back(0.0);
phi_ar.push_back(1.0);
phi_ST_ar.push_back(1.0);
t_eq_ar.push_back(0.0);
return 0;
}
