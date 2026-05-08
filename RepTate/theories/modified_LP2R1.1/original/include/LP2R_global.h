// Define global namespace objects
namespace LP2R_NS{
// Model parameters
double  M_Kuhn, M_e, N_e, G_0, tau_e;
double G_glass, tau_glass, beta_glass;

double Alpha=1.0, t_CR_START=1.0, deltaCR=0.30;
double B_zeta=2.0, A_eq=2.0, B_eq=10.0;
double ret_pref=0.189, Rept_Switch_Factor=1.664;
double Rouse_Switch_Factor=1.5, Disentanglement_Switch=1.0;
double ret_pref_0=0.020, ret_switch_exponent=0.42;

// discrete time evolution control
double cur_time=1.0e-3, DtMult=1.02, Log_DtMult;

// Output control
double FreqMin=1.0e-3, FreqMax=1.0e3, FreqRatio=1.1;
bool CalcDielectric=false, OutTermRelaxPathways=false, OutPhiPhiST=false;
bool Output_G_of_t=false;
std::string OutputFormat="Default", CSVdelimiter=","; bool Add_header=true;
bool has_temp=false, has_origin=false, has_label=false, has_chem=false;
double reptate_temp=0.0;
std::string reptate_origin, reptate_label, reptate_chem;
bool GenLogFL=false;

// input filenames and file handles
std::string inpFNM="inp.dat", rcFNM="LP2R.rc";
std::fstream f_Log;

// output filenames 
std::string RelSpecFNM="RelSpec", MechRelSpecFNM, DiRelSpecFNM;
std::string MechRelFNM="MechRel";
std::string OutTermRelaxFNM="TermRelax", OutPhiPhiSTFNM="STube";
std::fstream f_trelax;
std::fstream f_phi;

// Polymer collection
int npoly=0;
std::vector<C_LPoly *> LPoly;
double Rouse_wt=0.0;
double Sys_MN=0.0, Sys_MW=0.0, Sys_PDI=1.0;
bool Entangled_Dynamics=true;

// time dependent relaxation variables
double phi_true=1.0, phi_ST=1.0, phi_rept=1.0, phi_eq=1.0, Psi_rept=1.0;
double LastReptationTime=1.0, LastReptZ=1.0;

bool supertube_activated=false, AboveTauEFirst=false; 
double phi_ST_0=1.0, ST_activ_time=1.0, STmaxDrop=1.0; 

// Storage of relaxation data
std::vector<double> t_ar, phi_ar, phi_ST_ar, t_eq_ar;
int phi_eq_indx=0;
                 };
