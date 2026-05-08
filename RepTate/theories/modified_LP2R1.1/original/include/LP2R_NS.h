#ifndef _LP2R_NS_
#define _LP2R_NS_
/** \file
  * \brief
  * global namespaces
  *
  */

/**
  * Global variables
  */
namespace LP2R_NS{

// Model parameters

extern double M_Kuhn; /**< Kuhn Molar mass */
extern double M_e; /**< Entanglement molar mass  */
extern double G_0; /**< Plateau modulus */
extern double tau_e; /**< Entanglement time */
extern double N_e; /**< N_e == M_e/M_Kuhn; Number of Kuhn beads in one entanglement */

extern double G_glass; /**< Glassy modulus */
extern double tau_glass; /**< Glassy relaxation time */
extern double beta_glass; /**< stretching exponent for glassy relaxation */

extern double Alpha; /**< Dilution exponent */
extern double t_CR_START; /**< Time (units of tau_e) below which no CR events are included 
                            * in the tube model.
                            * (faster events are accounted in the bare tube picture itself.) */
extern double deltaCR; /**< Fractional drop in tube constraints at CR events (in long polymers)*/
extern double B_zeta; /**< Proportionality constant relating friction coefficient to supertube fraction */
extern double A_eq; /**< Proportionality constant connecting "effective equilibrium time" and time to locally
                       equiilbiate in a certain supertube */
extern double B_eq; /**< Constant delaying equilibrium for fast CR events */
extern double ret_pref; /**< Constant in arm retraction formula ( \f$ \mathcal{C}_{a,\infty} \f$ )*/
extern double ret_pref_0; /**< Short-time prefactor for CLF (\f$ \mathcal{C}_{a,0} \f$ ) */
extern double ret_switch_exponent; /**< Exponent \f$ \epsilon_{a} \f$ determining how steeply
           CLF switches to long-time strength */
extern double Rept_Switch_Factor; /**< Constant deciding transition from CLF to reptation */
extern double Rouse_Switch_Factor; /**< Minimum number of bare entanglements to be considered entangled  ( \f$ Z_u \f$ )*/
extern double Disentanglement_Switch; /**< Number of entanglement in the supertube  below which chains relax by "disentanglement". */ 

extern double cur_time; /**< Read as Start_time from resource file, start of integration time */
extern double DtMult; /**< Read as Time_ratio from resource file, ratio of consecutive discrete times */
extern double Log_DtMult; /**< Log(DtMult) */

// Files
extern std::string inpFNM; /**< Input file name */
extern std::string rcFNM; /**< resource file name */

// control output
extern bool CalcDielectric; /**< (false) If \c true, output dielectric loss (assuming type-A dipoles)\n
                                 Commad line flag -d takes precedence over resource file instruction.  */
extern std::string OutputFormat; /**< Output format in result files:\n
                                *  Default (.dat extension, space as dilimiter, header as comment with hash) \n
                                *  Text (.txt extension, space as dilimiter, header as string) \n
                                *  CSV (.csv extension, comma as (default) dilimiter) \n
                                *  RepTate (various extensions, see https://reptate.readthedocs.io ) */
extern std::string CSVdelimiter; /**< Allow for non-standard delimiter (ex. some european locale uses semicolon) */
extern bool Add_header; /**< (true) Add appropriate headers in the output files */
extern bool OutTermRelaxPathways; /**< (false) If \c true, terminal relaxation of each chain triggers detailed output */
extern bool Output_G_of_t; /**< (false) If \c true, output mechanical relaxation in the time domain. */
extern bool GenLogFL; /**< (false) If \c true, create a log file to output each step */
extern std::fstream f_Log; /**< File stream for log */
extern std::fstream f_trelax; /**< File stream for detailed relaxation information */
extern std::fstream f_phi; /**< File stream for tube diameters as a function of time */

extern bool OutPhiPhiST; /**< (false) If \c true, time evolution of different phi (can be mapped to tube diameters) 
                           * as a function of time is written in a file */
extern double FreqMin; /**< Minimum frequency for dynamic rheology output */
extern double FreqMax; /**< Maximum frequency for dynamic rheology output */
extern double FreqRatio; /**< Multiplier ( >1 ) between subsequent freqencies for output */

// relaxation data
extern double phi_true; /**< current unrelaxed fraction */
extern double phi_ST; /**< current unrelaxed supertube fraction */
extern double phi_rept; /**< related to the tube in which reptation is preferred currently*/
extern double phi_eq; /**< related to tube in which CLF is possible */
extern double Psi_rept; /**< Speed up factor for reptation by accessing fatter tube */

extern bool supertube_activated; /**< (false) set to true during supertube relaxation */
extern double phi_ST_0; /**< phi_ST just before supertube relaxation is activated */
extern double ST_activ_time; /**< time at which current supertube relaxation is activated */
extern bool AboveTauEFirst; /**< Start with false and set to true once t > t_CR_START */
extern double STmaxDrop; /**< Long time maximum drop in phi_ST druing one time step. \n
                                 STmaxDrop = exp(-log(DtMult)/(2.0*Alpha)) */

// Reptate software specific input
extern bool has_temp; /**< flag to note if reptate header variables have been set */
extern bool has_origin;  /**< flag to note if reptate header variables have been set */
extern bool has_label;  /**< flag to note if reptate header variables have been set */
extern bool has_chem; /**< flag to note if reptate header variables have been set */
extern std::string reptate_origin; /**< reptate header string */
extern std::string reptate_label; /**< reptate header string */
extern std::string reptate_chem; /**< reptate header string */
extern double reptate_temp; /**< temperature for reptate header */

// Output file names 
extern std::string RelSpecFNM; /**< Output filename for relaxation spectra in default mode */
extern std::string MechRelSpecFNM; /**< Output file name for Mechanical relaxation (Reptate mode) */
extern std::string DiRelSpecFNM; /**< Output file name for  Dielectric relaxation (reptate mode) */
extern std::string MechRelFNM; /**< Output file name for G(t) */
extern std::string OutTermRelaxFNM; /**< File in which terminal relaxation information should be written to */
extern std::string OutPhiPhiSTFNM; /**< File in which different phi are written to */

extern std::vector<double> t_ar; /**< Discrete times at which relaxation is tracked */
extern std::vector<double> phi_ar; /**< unrelaxed fraction (as function of time) */
extern std::vector<double> phi_ST_ar; /**< unrelaxed supertube fraction (as function of time) */
extern std::vector<double> t_eq_ar; /**< equilibration time in current supertube */
extern int phi_eq_indx; /**< index in \c t_eq_ar closest to the current time */
extern double LastReptationTime; /**< Keep track of time at which some chain switched to reptation. \n
                                       Any subsequent molecules may not have reptation time smaller than this. */
extern double LastReptZ; /**< Z_chain corresponding to the largest reptation time assigned so far */

extern std::vector<C_LPoly *> LPoly; /**< Polymer objects */
extern int npoly; /**< Number of polymers */
extern double Rouse_wt; /**< Weight fraction of chains that relax by free Rouse */
extern double Sys_MN; /**< Number averaged molar mass of the blend */
extern double Sys_MW; /**< Weight averaged molar mass of the blend */
extern double Sys_PDI; /**< polydispersity index of the blend */
extern bool Entangled_Dynamics; /**< true if polymers are entangled to begin with */
                      };

#endif
