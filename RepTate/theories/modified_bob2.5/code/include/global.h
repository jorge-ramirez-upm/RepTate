#ifndef GLOBAL_H
#define GLOBAL_H
#include <vector>
#include "class_def.h"

/* Variables controlled by bob.rc or input file or parser */
int max_poly, max_arm;

int GenPolyOnly, OutMode, PrefMode, ReptScheme, CalcNlin, PrioMode;
int NumNlinStretch, DefinedMaxwellModes, CalcGPCLS, GPCNumBin, GPCPolyMult;
int ForceGPCTrace;
int LateRouse, LtRsActivated;
double LtRsFactor;
int SlavePhiToPhiST;

double Alpha, PSquare, TStart, DtMult, RetLim, FreqMax, FreqMin, FreqInterval;
double StretchBinWidth, NlinAvDt, MaxwellInterval, NlinAvInterval, ReptAmount;

/* other variables */

int num_poly, first_avail_in_pool;
std::vector<arm> arm_pool;
std::vector<polymer> branched_poly;
std::vector<double> phi_hist;

char polycode[10];

double N_e, temp, mass_mono, rho_poly;
double gamma1, phi, phi_true, phi_ST, deltaphi;
double cur_time, unit_time, G_0_unit;
int zintmin, zintmax, runmode;
char conffname[256];
FILE *infofl;
FILE *inpfl;
FILE *errfl;
FILE *conffl;
FILE *debugfl;
FILE *protofl;
MTRand mtrand1;

/* specific to nonlinear part */
std::vector<std::vector<double> > nlin_prio_phi_relax;
std::vector<std::vector<double> > nlin_prio_phi_held;
double nlin_phi_true, nlin_phi_ST, nlin_dphi_true, nlin_dphi_ST;
int max_prio_var, max_senio_var;

int num_maxwell, nlin_nxt_data;
std::vector<double> t_maxwell;
double nlin_t_min, nlin_t_max;
int nlin_collect_data, nlin_num_data_av;

FILE *nlin_outfl;

/* addition for snipping */
int Snipping;
int NlinPrep; // Copy to Snipping
double SnipTime;
std::vector<polycopy> br_copy;
int FlowPriority;
double FlowTime; // FlowTime is immediately copied to SnipTime
                 // to retain old codes

/* static to global */
bool supertube_activated;
double phi_ST_0;
double ST_activ_time;

#endif