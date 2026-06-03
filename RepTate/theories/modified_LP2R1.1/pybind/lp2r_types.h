#ifndef REPTATE_LP2R_TYPES_H
#define REPTATE_LP2R_TYPES_H

#include <vector>

namespace reptate_lp2r {

struct LP2RMaterial {
    double m_kuhn = 0.0;
    double m_e = 0.0;
    double g0 = 0.0;
    double tau_e = 0.0;
    double g_glass = 0.0;
    double tau_glass = 0.0;
    double beta_glass = 0.0;
};

struct LP2RControls {
    double alpha = 1.0;
    double t_cr_start = 1.0;
    double delta_cr = 0.30;
    double b_zeta = 2.0;
    double a_eq = 2.0;
    double b_eq = 10.0;
    double ret_pref = 0.189;
    double ret_pref_0 = 0.020;
    double ret_switch_exponent = 0.42;
    double rept_switch_factor = 1.664;
    double rouse_switch_factor = 1.5;
    double disentanglement_switch = 1.0;
    double start_time = 1.0e-3;
    double time_ratio = 1.02;
};

struct LP2RResult {
    std::vector<double> omega;
    std::vector<double> gp;
    std::vector<double> gpp;
    std::vector<double> eta;
    std::vector<double> epsilonp;
    std::vector<double> epsilonpp;
    double mn = 0.0;
    double mw = 0.0;
    double pdi = 1.0;
    double eta0 = 0.0;
};

struct LP2RRelaxationResult {
    std::vector<double> time;
    std::vector<double> gt;
    std::vector<double> mu;
    std::vector<double> r;
};

}  // namespace reptate_lp2r

#endif
