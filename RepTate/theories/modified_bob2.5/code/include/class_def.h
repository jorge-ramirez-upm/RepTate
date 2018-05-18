// class arm and polymer

#ifndef myclass_flag_
#define myclass_flag_

#include <vector>

class polycopy
{
public:
  int narm;
  int active;
  std::vector<int> armindx;
  std::vector<int> priority;
  std::vector<int> assigned_trelax;
  std::vector<double> trelax;
  std::vector<double> zeta;
  std::vector<int> relax_end;
  //int * assigned_Deff;     // * added by DJR * //
  //double * Deff;
  std::vector<int> assigned_taus; // * added by DJR * //
  std::vector<double> taus;
};
class arm
{
public:
  int L1, L2, R1, R2, up, down;
  double arm_len, vol_fraction;
  bool relaxing, free_end, compound, tmpflag;
  int relax_end, nxt_relax;
  int relaxend_cp;

  /* The following are used only for free ends */
  int free_up, free_down, nxtbranch1, nxtbranch2, next_friction;
  double z, dz, pot, gamma2, tau_K;
  double arm_len_eff, arm_len_end, deltazeff;
  double zeff_numer, zeff_denom;
  bool collapsed, ghost, prune, freeze_arm_len_eff;
  double tau_collapse, phi_collapse, extra_drag, pot_int;

  /* extra bits for nonlinear code */
  int priority, seniority;
  int compound_store_data_num, compound_store_data_del_indx;
  double compound_fit_time[10], compound_fit_zeff[10];

  /* Some more stuff */ /* last two added by DJR */
  //double pr_scl_z, str_time, alt_v_int, alt_D_end;
  double pr_scl_z, str_time, alt_v_int, armtaus, armzeta, alt_D_end;

  int copy_num;
};

class polymer
{
public:
  int first_end, first_free, num_branch;
  bool alive, linear_tag, rept_set;
  double relaxed_frac, ghost_contrib;
  double phi_rept;
  double gfac, molmass, wtfrac;
};

#endif
