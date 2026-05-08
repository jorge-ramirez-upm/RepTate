#include "../include/LP2R.h"
#include <algorithm>
/** \file
  * \brief Generate polymers based on GPC data from a file
  */

/**
  * sort paired vectors in ascending order of the first
  * \param[in,out] m molar mass
  * \param[in,out] p dwdm associated with m
  */
void aa_sort2_minmax( std::vector<double> &m, std::vector<double> &p)
{
double tmpval=0.0;
int i_min=0;
int n=m.size();

for(int i=0; i<n; i++){
  i_min=i;
  for(int j=i; j<n; j++){
    if(m[i_min] > m[j]){i_min=j;}
                        }
 if(i_min != i){
   tmpval=m[i]; m[i]=m[i_min]; m[i_min]=tmpval;
   tmpval=p[i]; p[i]=p[i_min]; p[i_min]=tmpval;
               }
                      }
}

/**
  * GPC data in {M, dw/dlog_10(M)} format in the specified file
  * As with all other files, comments are allowed with a "%" symbol
  *
  * \param[inout] fname string containing the filename
  * \param[in] wtcomp weight fraction assigned to the current component
  * \return zero if successful
  */

int GenLinGPC(std::string &fname, const double wtcomp)
{
using namespace LP2R_NS;
typedef std::vector<double>::size_type vecint;
// Remove any whitespace from fname
fname.erase(remove(fname.begin(), fname.end(), ' '), fname.end());
fname.erase(remove(fname.begin(), fname.end(), '\t'), fname.end());
std::fstream f1;
f1.open(fname, std::ios_base::in);
if(!f1){
if(GenLogFL){
  f_Log << "Failed to open GPC data file " << fname << " for input." << std::endl;
  f_Log << "Will stop here." << std::endl;
            }
return 1;}
std::vector<double> m_ar;
std::vector<double> p_ar;
std::string s1;
std::stringstream s1strm;
double t1=0.0,t2=0.0;
while(!safeGetline(f1, s1).eof()){
s1strm.str(std::string());
s1strm << s1 << std::endl;
s1strm >> t1 >> t2;
if(s1strm.fail()){
if(GenLogFL){
  f_Log << "Failed to read data from GPC data file " << fname <<" :" << std::endl
        << "Found: " << s1 << " for entry " << m_ar.size()+1 <<std::endl
        << " We were expecting two floating point numbers here.. " << std::endl
        << " Will stop here." << std::endl; }
 return 2;
                 }
if(t2 < 1.0e-12){t2=1.0e-12;} // guard against zero or negative weights
m_ar.push_back(t1);
p_ar.push_back(t2);
                                 }
f1.close();

// Guard against empty file
if(m_ar.size() == 0){
if(GenLogFL){
  f_Log << "Did not find any valid data in GPC data file " << fname << std::endl 
        << "Will stop here. " << std::endl; }
return 3;
                    }
if(GenLogFL){
  f_Log << "Read " << m_ar.size() << " GPC data set  from file " << fname << std::endl;}


C_LPoly * ptmp;
// Guard against single data set
if(m_ar.size() == 1){ ptmp=new C_LPoly(m_ar[0], wtcomp, M_e); 
                      LPoly.push_back(ptmp); npoly++;
          return 0; }

aa_sort2_minmax(m_ar, p_ar);

std::vector<double> wt_ar;
double tot_wt=0.0;
for(vecint i=0; i< (m_ar.size() -1); i++){
double dlm=log10(m_ar[i+1]) - log10(m_ar[i]);
wt_ar.push_back(dlm*p_ar[i]);
tot_wt+=wt_ar[i];
                                      }
double dlm=log10(m_ar[m_ar.size()-1]) - log10(m_ar[m_ar.size()-2]);
wt_ar.push_back(dlm*p_ar[m_ar.size()-1]);
tot_wt+=wt_ar[m_ar.size()-1];
for(vecint i=0; i<m_ar.size(); i++){
  ptmp=new C_LPoly(m_ar[i], wt_ar[i]*wtcomp/tot_wt, M_e);
  LPoly.push_back(ptmp); npoly++;
                                }
return 0;
}
