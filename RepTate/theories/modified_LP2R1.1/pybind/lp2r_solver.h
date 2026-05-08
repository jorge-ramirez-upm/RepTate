#ifndef REPTATE_LP2R_SOLVER_H
#define REPTATE_LP2R_SOLVER_H

#include "lp2r_types.h"

#include <atomic>
#include <vector>

namespace reptate_lp2r {

class LP2RSolver {
public:
    LP2RSolver(LP2RMaterial material, LP2RControls controls);

    void add_lognormal_component(double weight, int n, double mw, double pdi);
    void add_discrete_component(const std::vector<double>& mass,
                                const std::vector<double>& weight,
                                double component_weight = 1.0);

    void prepare();
    bool step();
    void run_relaxation();
    LP2RResult calculate_spectra(double freq_min, double freq_max, double freq_ratio) const;
    LP2RResult run(double freq_min, double freq_max, double freq_ratio);

    void cancel();
    bool cancelled() const;
    double progress() const;
    bool prepared() const;

private:
    struct LPoly {
        double mass = 0.0;
        double wt = 0.0;
        double z_chain = 0.0;
        double z = 0.0;
        bool alive = true;
        bool relax_free_rouse = false;
        bool rept_set = false;
        double tau_d_0 = 1.0e22;
        double z_rept = 0.0;
        double rept_wt = 0.0;
        int p_max = 0;
        int p_next = 0;
        double t_frouse = 0.0;

        LPoly(double m, double w, double me);
    };

    void reset_runtime_state();
    double lognormal_weight(double mw, double pdi, double m1, double m2, double& mw_bin) const;
    double get_phi_eq();
    void frac_unrelaxed();
    void arm_retraction(int np, int indx);
    void try_reptate(int np);
    int time_step(int indx);

    void gstar_glass(double w, double& gp, double& gpp) const;
    void gstar_rouse(double w, double& gp, double& gpp, double& ep, double& epp) const;
    void gstar_fast_rouse(double w, double& gp, double& gpp) const;
    void gstar_slow(double w, double& gp, double& gpp, double& ep, double& epp) const;
    double calc_visc() const;

    LP2RMaterial material_;
    LP2RControls controls_;
    std::vector<LPoly> polymers_;

    double n_e_ = 0.0;
    double g_glass_scaled_ = 0.0;
    double tau_glass_scaled_ = 0.0;

    bool prepared_ = false;
    bool entangled_dynamics_ = true;
    int step_index_ = 0;
    double cur_time_ = 1.0e-3;
    double log_dt_mult_ = 0.0;
    double st_max_drop_ = 1.0;
    double rouse_wt_ = 0.0;
    double sys_mn_ = 0.0;
    double sys_mw_ = 0.0;
    double sys_pdi_ = 1.0;

    double phi_true_ = 1.0;
    double phi_st_ = 1.0;
    double phi_rept_ = 1.0;
    double phi_eq_ = 1.0;
    double psi_rept_ = 1.0;
    double last_reptation_time_ = 1.0;
    double last_rept_z_ = 1.0;
    bool supertube_activated_ = false;
    bool above_tau_e_first_ = false;
    double phi_st_0_ = 1.0;
    double st_activ_time_ = 1.0;
    int phi_eq_indx_ = 0;

    std::vector<double> t_ar_;
    std::vector<double> phi_ar_;
    std::vector<double> phi_st_ar_;
    std::vector<double> t_eq_ar_;

    std::atomic_bool cancel_requested_{false};
};

}  // namespace reptate_lp2r

#endif
