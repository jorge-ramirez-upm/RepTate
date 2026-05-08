#include "../include/LP2R.h"
/** \file
  * \brief Generate polymers with {molar mass, weight fraction} entries in a file
  * \param[in,out] fname file containing the weight fractions
  * \param[in] wtcomp weight fraction of the current component
  * \return zero if successful
  */
int GenLinWt(std::string &fname, const double wtcomp)
{
using namespace LP2R_NS;
typedef std::vector<double>::size_type vecint;
fname.erase(remove(fname.begin(), fname.end(), ' '), fname.end());
fname.erase(remove(fname.begin(), fname.end(), '\t'), fname.end());
std::fstream f1;
f1.open(fname, std::ios_base::in);
if(!f1){
if(GenLogFL){
  f_Log << "Failed to open weight fraction data file " << fname << " for input." << std::endl;
  f_Log << "Will stop here." << std::endl;
            }
return 1;}
std::vector<double> m_ar;
std::vector<double> wt_ar;
double wttot=0.0;
std::string s1;
std::stringstream s1strm;
double t1=0.0,t2=0.0;
while(!safeGetline(f1, s1).eof()){
s1strm.str(std::string());
s1strm << s1 << std::endl;
s1strm >> t1 >> t2;
if(s1strm.fail()){
if(GenLogFL){
  f_Log << "Failed to properly read data from weight fraction data file " << fname <<" :" << std::endl
        << "Found: " << s1 << " for entry " << m_ar.size()+1 <<std::endl
        << " We were expecting two floating point numbers here.. " << std::endl
        << " Will stop here." << std::endl; }
return 2;
                 }
if(t2 < 1.0e-12){t2=1.0e-12;} // guard against zero or negative weights
m_ar.push_back(t1);
wt_ar.push_back(t2);
wttot+=t2;
                                 }
f1.close();
if(GenLogFL){
  f_Log << "Read " << m_ar.size() << " weight fraction data set  from file " << fname << std::endl;}
for(vecint i=0; i<wt_ar.size(); i++){ wt_ar[i]=wt_ar[i]*wtcomp/wttot; }
C_LPoly * ptmp;
for(vecint i=0; i<m_ar.size(); i++){
  ptmp=new C_LPoly(m_ar[i], wt_ar[i], M_e);
  LPoly.push_back(ptmp); npoly++;
                                   }

return 0;
}
