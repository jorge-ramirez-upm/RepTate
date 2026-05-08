#include "lp2r_solver.h"

#include "kww_adapter.h"

#include <algorithm>
#include <cmath>
#include <stdexcept>

namespace reptate_lp2r {
namespace {

constexpr double kPiOver2 = 1.57079632679489661922;
constexpr double kSqrtPi = 1.77245385090551602729;

class InvSqSum {
public:
    InvSqSum()
    {
        psum_[0] = 0.0;
        psum_[1] = 1.0;
        for (int i = 2; i < 500; ++i) {
            psum_[i] = psum_[i - 1] + 1.0 / static_cast<double>(i * i);
        }
    }

    double operator()(int z) const
    {
        if (z <= 0) {
            return 0.0;
        }
        if (z < 500) {
            return psum_[z];
        }
        return psum_[499] + intg_psum(500, z);
    }

    double operator()(int z1, int z2) const
    {
        if (z2 < z1) {
            return 0.0;
        }
        const double s1 = z1 <= 500 ? psum_[std::max(0, z1 - 1)]
                                    : psum_[499] + intg_psum(500, z1 - 1);
        const double s2 = z2 < 500 ? psum_[z2] : psum_[499] + intg_psum(500, z2);
        return s2 - s1;
    }

private:
    static double intg_psum(int n1, int n2)
    {
        const double n1d = static_cast<double>(n1);
        const double n2d = static_cast<double>(n2);
        const double n1dsq = n1d * n1d;
        const double n2dsq = n2d * n2d;
        double val = 1.0 / n1d - 1.0 / n2d + 0.50 * (1.0 / n1dsq + 1.0 / n2dsq);
        val += (1.0 / (n1d * n1dsq) - 1.0 / (n2d * n2dsq)) / 6.0;
        return val;
    }

    double psum_[500]{};
};

void validate_positive(double value, const char* name)
{
    if (!(value > 0.0) || !std::isfinite(value)) {
        throw std::invalid_argument(std::string(name) + " must be a positive finite value");
    }
}

void symbint(double tk, double td, double w, double& rint1, double& rint2)
{
    const double a = tk / td;
    const double b = w * w * tk * tk;
    const double alpha = std::sqrt(1.0 + b);
    const double beta = std::sqrt(1.0 + alpha);
    const double gamma = std::sqrt(a * (alpha - 1.0));
    const double delta = std::sqrt(a * (alpha + 1.0));
    const double rt2 = std::sqrt(2.0);

    const double t1 = std::log((rt2 * gamma + a + alpha) / (a + alpha - rt2 * gamma));
    const double t2 = std::atan(2.0 * rt2 * alpha * delta /
                                (delta * delta + gamma * gamma - 2.0 * alpha * alpha));

    rint1 = -gamma * beta * t1 - 2.0 * std::sqrt(a) * (1.0 + alpha) * t2;
    rint2 = beta * gamma * (1.0 + alpha) * t1 / b - 2.0 * std::sqrt(a) * t2;
    const double factor = 1.0 / (2.0 * rt2 * alpha * beta * a);
    rint1 *= factor;
    rint2 *= factor;
}

}  // namespace

LP2RSolver::LPoly::LPoly(double m, double w, double me)
    : mass(m), wt(w), z_chain(m / me), t_frouse(z_chain * z_chain)
{
}

LP2RSolver::LP2RSolver(LP2RMaterial material, LP2RControls controls)
    : material_(material), controls_(controls)
{
    validate_positive(material_.m_kuhn, "m_kuhn");
    validate_positive(material_.m_e, "m_e");
    validate_positive(material_.g0, "g0");
    validate_positive(material_.tau_e, "tau_e");
    validate_positive(material_.tau_glass, "tau_glass");
    validate_positive(material_.beta_glass, "beta_glass");
    validate_positive(controls_.time_ratio, "time_ratio");
    validate_positive(controls_.start_time, "start_time");
    if (controls_.time_ratio <= 1.000001) {
        throw std::invalid_argument("time_ratio must be greater than 1.000001");
    }
    if (material_.beta_glass < 0.1 || material_.beta_glass > 2.0) {
        throw std::invalid_argument("beta_glass must be in the range supported by kww.c: [0.1, 2.0]");
    }
}

void LP2RSolver::add_lognormal_component(double weight, int n, double mw, double pdi)
{
    validate_positive(weight, "weight");
    validate_positive(mw, "mw");
    validate_positive(pdi, "pdi");
    if (n <= 1 || pdi <= 1.0) {
        polymers_.emplace_back(mw, weight, material_.m_e);
        prepared_ = false;
        return;
    }

    const double mu = std::log(mw) - 1.50 * std::log(pdi);
    const double sigma = std::sqrt(std::log(pdi));
    const double ln_m_low = mu + sigma * sigma - 2.63 * std::sqrt(2.0) * sigma;
    const double ln_m_high = mu + sigma * sigma + 2.63 * std::sqrt(2.0) * sigma;

    double mw_bin = 0.0;
    double m2 = std::exp(ln_m_low);
    double wt_bin = lognormal_weight(mw, pdi, -1.0, m2, mw_bin);
    polymers_.emplace_back(mw_bin, wt_bin * weight, material_.m_e);

    const double delta_ln_m = (ln_m_high - ln_m_low) / static_cast<double>(n - 2);
    for (int i = 0; i < n - 2; ++i) {
        const double m1 = std::exp(ln_m_low + static_cast<double>(i) * delta_ln_m);
        m2 = std::exp(ln_m_low + static_cast<double>(i + 1) * delta_ln_m);
        wt_bin = lognormal_weight(mw, pdi, m1, m2, mw_bin);
        polymers_.emplace_back(mw_bin, wt_bin * weight, material_.m_e);
    }

    const double m1 = std::exp(ln_m_high);
    wt_bin = lognormal_weight(mw, pdi, m1, -1.0, mw_bin);
    polymers_.emplace_back(mw_bin, wt_bin * weight, material_.m_e);
    prepared_ = false;
}

void LP2RSolver::add_discrete_component(const std::vector<double>& mass,
                                        const std::vector<double>& weight,
                                        double component_weight)
{
    validate_positive(component_weight, "component_weight");
    if (mass.size() != weight.size() || mass.empty()) {
        throw std::invalid_argument("mass and weight arrays must be non-empty and have the same length");
    }
    double total_weight = 0.0;
    for (std::size_t i = 0; i < mass.size(); ++i) {
        validate_positive(mass[i], "mass");
        validate_positive(weight[i], "weight");
        total_weight += weight[i];
    }
    for (std::size_t i = 0; i < mass.size(); ++i) {
        polymers_.emplace_back(mass[i], component_weight * weight[i] / total_weight, material_.m_e);
    }
    prepared_ = false;
}

void LP2RSolver::prepare()
{
    if (polymers_.empty()) {
        throw std::runtime_error("at least one polymer component is required");
    }
    cancel_requested_.store(false);
    reset_runtime_state();

    n_e_ = material_.m_e / material_.m_kuhn;
    tau_glass_scaled_ = material_.tau_glass / material_.tau_e;
    g_glass_scaled_ = (material_.g_glass - 1.250 * material_.g0) / material_.g0;
    log_dt_mult_ = std::log(controls_.time_ratio);
    st_max_drop_ = std::exp(-std::log(controls_.time_ratio) / (2.0 * controls_.alpha));

    double total_weight = 0.0;
    for (const auto& polymer : polymers_) {
        total_weight += polymer.wt;
    }
    validate_positive(total_weight, "total polymer weight");
    for (auto& polymer : polymers_) {
        polymer.wt /= total_weight;
        polymer.z_chain = polymer.mass / material_.m_e;
        polymer.t_frouse = polymer.z_chain * polymer.z_chain;
    }

    int num_entangled = 0;
    for (auto& polymer : polymers_) {
        if (polymer.z_chain < controls_.rouse_switch_factor) {
            polymer.relax_free_rouse = true;
            polymer.alive = false;
            rouse_wt_ += polymer.wt;
        } else {
            ++num_entangled;
        }
        sys_mn_ += polymer.wt / polymer.mass;
        sys_mw_ += polymer.wt * polymer.mass;
    }
    sys_mn_ = 1.0 / sys_mn_;
    sys_pdi_ = sys_mw_ / sys_mn_;
    entangled_dynamics_ = num_entangled > 0;

    t_ar_.push_back(0.0);
    phi_ar_.push_back(1.0);
    phi_st_ar_.push_back(1.0);
    t_eq_ar_.push_back(0.0);
    prepared_ = true;
}

bool LP2RSolver::step()
{
    if (!prepared_) {
        throw std::runtime_error("prepare() must be called before step()");
    }
    if (cancel_requested_.load() || !entangled_dynamics_) {
        return false;
    }
    const int nalive = time_step(step_index_ == 0 ? 0 : 1);
    ++step_index_;
    return nalive > 0 && !cancel_requested_.load();
}

void LP2RSolver::run_relaxation()
{
    if (!prepared_) {
        prepare();
    }
    while (step()) {
    }
}

LP2RResult LP2RSolver::run(double freq_min, double freq_max, double freq_ratio)
{
    prepare();
    run_relaxation();
    return calculate_spectra(freq_min, freq_max, freq_ratio);
}

void LP2RSolver::cancel()
{
    cancel_requested_.store(true);
}

bool LP2RSolver::cancelled() const
{
    return cancel_requested_.load();
}

double LP2RSolver::progress() const
{
    return std::max(0.0, std::min(1.0, 1.0 - phi_true_));
}

bool LP2RSolver::prepared() const
{
    return prepared_;
}

LP2RResult LP2RSolver::calculate_spectra(double freq_min, double freq_max, double freq_ratio) const
{
    if (!prepared_) {
        throw std::runtime_error("prepare() must be called before calculate_spectra()");
    }
    validate_positive(freq_min, "freq_min");
    validate_positive(freq_max, "freq_max");
    validate_positive(freq_ratio, "freq_ratio");
    if (freq_ratio <= 1.000001) {
        throw std::invalid_argument("freq_ratio must be greater than 1.000001");
    }
    if (freq_min > freq_max) {
        std::swap(freq_min, freq_max);
    }
    freq_min = std::max(freq_min, 1.0e-32);

    LP2RResult result;
    const double freq_min_scaled = freq_min * material_.tau_e;
    const double freq_max_scaled = freq_max * material_.tau_e;
    double freq = freq_min_scaled / freq_ratio;

    while (freq < freq_max_scaled) {
        freq *= freq_ratio;
        double gp = 0.0;
        double gpp = 0.0;
        double ep = 0.0;
        double epp = 0.0;
        double gp_tmp = 0.0;
        double gpp_tmp = 0.0;
        double ep_tmp = 0.0;
        double epp_tmp = 0.0;

        gstar_glass(freq, gp_tmp, gpp_tmp);
        gp += gp_tmp;
        gpp += gpp_tmp;

        gstar_rouse(freq, gp_tmp, gpp_tmp, ep_tmp, epp_tmp);
        gp += gp_tmp;
        gpp += gpp_tmp;
        ep += ep_tmp;
        epp += epp_tmp;

        if (entangled_dynamics_) {
            gstar_fast_rouse(freq, gp_tmp, gpp_tmp);
            gp += gp_tmp;
            gpp += gpp_tmp;

            gstar_slow(freq, gp_tmp, gpp_tmp, ep_tmp, epp_tmp);
            gp += (1.0 - rouse_wt_) * gp_tmp;
            gpp += (1.0 - rouse_wt_) * gpp_tmp;
        }

        result.omega.push_back(freq / material_.tau_e);
        result.gp.push_back(gp * material_.g0);
        result.gpp.push_back(gpp * material_.g0);
        result.eta.push_back(material_.g0 * material_.tau_e * std::sqrt(gp * gp + gpp * gpp) / freq);
    }

    result.mn = sys_mn_;
    result.mw = sys_mw_;
    result.pdi = sys_pdi_;
    result.eta0 = calc_visc();
    return result;
}

void LP2RSolver::reset_runtime_state()
{
    prepared_ = false;
    entangled_dynamics_ = true;
    step_index_ = 0;
    cur_time_ = controls_.start_time;
    log_dt_mult_ = 0.0;
    st_max_drop_ = 1.0;
    rouse_wt_ = 0.0;
    sys_mn_ = 0.0;
    sys_mw_ = 0.0;
    sys_pdi_ = 1.0;
    phi_true_ = 1.0;
    phi_st_ = 1.0;
    phi_rept_ = 1.0;
    phi_eq_ = 1.0;
    psi_rept_ = 1.0;
    last_reptation_time_ = 1.0;
    last_rept_z_ = 1.0;
    supertube_activated_ = false;
    above_tau_e_first_ = false;
    phi_st_0_ = 1.0;
    st_activ_time_ = 1.0;
    phi_eq_indx_ = 0;
    t_ar_.clear();
    phi_ar_.clear();
    phi_st_ar_.clear();
    t_eq_ar_.clear();

    for (auto& polymer : polymers_) {
        polymer.z = 0.0;
        polymer.alive = true;
        polymer.relax_free_rouse = false;
        polymer.rept_set = false;
        polymer.tau_d_0 = 1.0e22;
        polymer.z_rept = 0.0;
        polymer.rept_wt = 0.0;
        polymer.p_max = 0;
        polymer.p_next = 0;
    }
}

double LP2RSolver::lognormal_weight(double mw, double pdi, double m1, double m2, double& mw_bin) const
{
    const double mu = std::log(mw) - 1.50 * std::log(pdi);
    const double sigma = std::sqrt(std::log(pdi));
    double wt_bin = 0.0;
    if (m1 < 0.0) {
        wt_bin = 0.5 * std::erfc((mu + sigma * sigma - std::log(m2)) / (std::sqrt(2.0) * sigma));
        const double t2 = std::erfc((mu + 2.0 * sigma * sigma - std::log(m2)) /
                                    (std::sqrt(2.0) * sigma));
        mw_bin = 0.50 * mw * t2 / wt_bin;
    } else if (m2 < 0.0) {
        wt_bin = 1.0 - 0.5 * std::erfc((mu + sigma * sigma - std::log(m1)) /
                                       (std::sqrt(2.0) * sigma));
        const double t1 = std::erfc((mu + 2.0 * sigma * sigma - std::log(m1)) /
                                    (std::sqrt(2.0) * sigma));
        mw_bin = 0.50 * mw * (2.0 - t1) / wt_bin;
    } else {
        const double w1 = 0.5 * std::erfc((mu + sigma * sigma - std::log(m1)) /
                                          (std::sqrt(2.0) * sigma));
        const double w2 = 0.5 * std::erfc((mu + sigma * sigma - std::log(m2)) /
                                          (std::sqrt(2.0) * sigma));
        wt_bin = w2 - w1;
        const double t1 = std::erfc((mu + 2.0 * sigma * sigma - std::log(m1)) /
                                    (std::sqrt(2.0) * sigma));
        const double t2 = std::erfc((mu + 2.0 * sigma * sigma - std::log(m2)) /
                                    (std::sqrt(2.0) * sigma));
        mw_bin = 0.50 * mw * (t2 - t1) / wt_bin;
    }
    return wt_bin;
}

double LP2RSolver::get_phi_eq()
{
    double phi_eq = 1.0;
    int n1 = phi_eq_indx_;
    const int n = static_cast<int>(t_ar_.size());
    for (int i = n1; i < n; ++i) {
        if (t_eq_ar_[i] > cur_time_) {
            n1 = i - 1;
            break;
        }
    }
    if (n1 < n - 1) {
        const double deltat = cur_time_ - t_eq_ar_[n1];
        const double phidel = phi_ar_[n1 + 1] - phi_ar_[n1];
        phi_eq = phi_ar_[n1] + phidel * deltat / (t_eq_ar_[n1 + 1] - t_eq_ar_[n1]);
        phi_eq_indx_ = n1;
    } else {
        phi_eq = phi_ar_[n - 1];
    }
    return phi_eq;
}

void LP2RSolver::frac_unrelaxed()
{
    const double phit_sv = phi_true_;
    phi_true_ = 0.0;
    for (const auto& polymer : polymers_) {
        if (polymer.alive) {
            phi_true_ += polymer.wt * (1.0 - 2.0 * polymer.z / polymer.z_chain);
        }
    }

    if (cur_time_ > controls_.t_cr_start) {
        const double a_zeta_inv = 1.0 / ((1.0 - controls_.delta_cr) * (1.0 - controls_.delta_cr)) - 1.0;
        double delta_cr_now = 1.0 - (1.0 - controls_.delta_cr) * std::sqrt(1.0 + a_zeta_inv / cur_time_);
        if (delta_cr_now < 0.0) {
            delta_cr_now = 0.0;
        }

        double delta_phi = 0.0;
        if (above_tau_e_first_) {
            above_tau_e_first_ = false;
            delta_phi = 1.0 - phi_true_;
        } else {
            delta_phi = phit_sv - phi_true_;
        }

        const double st_max_drop_now = (1.0 - st_max_drop_) / (1.0 - delta_cr_now * st_max_drop_);
        const double dphi_max = phi_st_ * st_max_drop_now;
        if (!supertube_activated_) {
            if (delta_phi <= dphi_max) {
                phi_st_ = phi_true_;
            } else {
                supertube_activated_ = true;
                phi_st_0_ = phi_st_ - delta_cr_now * delta_phi;
                st_activ_time_ = cur_time_;
                phi_st_ -= dphi_max;
            }
        } else {
            const double tv = phi_st_0_ * std::exp(std::log(st_activ_time_ / cur_time_) /
                                                  (2.0 * controls_.alpha));
            if (tv < phi_true_) {
                phi_st_ = phi_true_;
                supertube_activated_ = false;
            } else if (delta_phi <= dphi_max) {
                phi_st_ = tv;
            } else {
                phi_st_0_ -= delta_cr_now * delta_phi;
                phi_st_ = phi_st_0_ * std::exp(std::log(st_activ_time_ / cur_time_) /
                                               (2.0 * controls_.alpha));
            }
        }
    }

    const double t_equil_cur_tube = controls_.a_eq * cur_time_ * (1.0 + controls_.b_eq / std::sqrt(cur_time_));
    t_ar_.push_back(cur_time_);
    phi_ar_.push_back(phi_true_);
    phi_st_ar_.push_back(phi_st_);
    t_eq_ar_.push_back(t_equil_cur_tube);
    phi_eq_ = get_phi_eq();

    if (!supertube_activated_ && cur_time_ > 1.0) {
        double tpast = -controls_.b_eq + std::sqrt(controls_.b_eq * controls_.b_eq +
                                                  4.0 * cur_time_ / controls_.a_eq);
        tpast = 0.25 * tpast * tpast;
        if (phi_eq_ < 0.999999) {
            const double tv = controls_.b_zeta * std::pow(phi_eq_, 3.0 * controls_.alpha) * tpast;
            if (tv < psi_rept_) {
                psi_rept_ = tv;
                phi_rept_ = phi_eq_;
            }
        }
    }
}

void LP2RSolver::arm_retraction(int np, int indx)
{
    auto& polymer = polymers_[np];
    const double clf_pref = controls_.ret_pref_0 +
                            (controls_.ret_pref - controls_.ret_pref_0) /
                                (1.0 + std::exp(-controls_.ret_switch_exponent * std::log(cur_time_)));
    if (indx == 0) {
        polymer.z = std::sqrt(2.0 * clf_pref * std::sqrt(cur_time_));
        return;
    }

    const double z0 = polymer.z;
    double dz = 0.50 * clf_pref * std::sqrt(cur_time_ / std::pow(phi_eq_, controls_.alpha)) *
                log_dt_mult_ / (z0 * std::sqrt(psi_rept_));
    if (dz > 0.50 * polymer.z_chain - polymer.z) {
        dz = 0.50 * polymer.z_chain - polymer.z;
        polymer.alive = false;
    }
    polymer.z = z0 + dz;
}

void LP2RSolver::try_reptate(int np)
{
    auto& polymer = polymers_[np];
    if (!polymer.rept_set) {
        const double tcomp = controls_.rept_switch_factor * 3.0 * polymer.z_chain *
                             polymer.z * polymer.z * psi_rept_;
        if (tcomp < cur_time_) {
            polymer.rept_set = true;
            const double len_to_rept = polymer.z_chain - 2.0 * polymer.z;
            polymer.tau_d_0 = 3.0 * polymer.z_chain * len_to_rept * len_to_rept * psi_rept_;
            if (polymer.tau_d_0 < last_reptation_time_) {
                if (polymer.z_chain < last_rept_z_) {
                    polymer.tau_d_0 = last_reptation_time_;
                }
            } else {
                last_reptation_time_ = polymer.tau_d_0;
                last_rept_z_ = polymer.z_chain;
            }
            polymer.z_rept = len_to_rept;
            if (polymer.tau_d_0 < cur_time_) {
                polymer.p_max = 1;
            } else {
                polymer.p_max = static_cast<int>(std::floor(std::sqrt(polymer.tau_d_0 / cur_time_)));
                if (polymer.p_max % 2 == 0) {
                    --polymer.p_max;
                }
            }
            if (polymer.p_max < 1) {
                polymer.p_max = 1;
            }
            polymer.p_next = polymer.p_max;
            polymer.rept_wt = 0.0;
            for (int i = 1; i <= polymer.p_max; i += 2) {
                polymer.rept_wt += 1.0 / static_cast<double>(i * i);
            }
        }
    }

    if (polymer.rept_set) {
        const double psq = static_cast<double>(polymer.p_next * polymer.p_next);
        if (cur_time_ > polymer.tau_d_0 / psq) {
            polymer.z += 0.50 * polymer.z_rept / (polymer.rept_wt * psq);
            if (polymer.p_next == 1) {
                polymer.z = 0.50 * polymer.z_chain;
                polymer.alive = false;
            } else {
                polymer.p_next -= 2;
            }
        }
    }
}

int LP2RSolver::time_step(int indx)
{
    if (indx != 0) {
        cur_time_ *= controls_.time_ratio;
    }

    for (int i = 0; i < static_cast<int>(polymers_.size()); ++i) {
        auto& polymer = polymers_[i];
        if (polymer.alive) {
            if (!polymer.rept_set) {
                arm_retraction(i, indx);
            }
            if (polymer.alive && cur_time_ > 1.0) {
                try_reptate(i);
            }
        }
        if (polymer.alive &&
            polymer.z_chain * std::pow(phi_st_, controls_.alpha) < controls_.disentanglement_switch) {
            polymer.z = 0.50 * polymer.z_chain;
            polymer.alive = false;
        }
    }

    frac_unrelaxed();

    int nalive = 0;
    for (const auto& polymer : polymers_) {
        if (polymer.alive) {
            ++nalive;
        }
    }
    return nalive;
}

void LP2RSolver::gstar_glass(double w, double& gp, double& gpp) const
{
    const double omega = w * tau_glass_scaled_;
    gp = g_glass_scaled_ * omega * kww_storage(omega, material_.beta_glass);
    gpp = g_glass_scaled_ * omega * kww_loss(omega, material_.beta_glass);
}

void LP2RSolver::gstar_rouse(double w, double& gp, double& gpp, double& ep, double& epp) const
{
    gp = gpp = ep = epp = 0.0;
    for (const auto& polymer : polymers_) {
        if (!polymer.relax_free_rouse) {
            continue;
        }
        double gr = 0.0;
        double g2r = 0.0;
        double er = 0.0;
        double e2r = 0.0;
        const double tau1 = polymer.t_frouse;
        const int pmax = static_cast<int>(std::ceil(polymer.z_chain * n_e_));
        for (int p = 1; p <= pmax; ++p) {
            const double psq = static_cast<double>(p * p);
            double taup = tau1 / (2.0 * psq);
            double tv = w * taup;
            double tv2 = tv * tv;
            gr += tv2 / (1.0 + tv2);
            g2r += tv / (1.0 + tv2);
            if (p % 2 != 0) {
                taup = tau1 / psq;
                tv = w * taup;
                tv2 = tv * tv;
                er += tv2 / (psq * (1.0 + tv2));
                e2r += tv / (psq * (1.0 + tv2));
            }
        }
        gr = gr * 5.0 * polymer.wt / (4.0 * polymer.z_chain);
        g2r = g2r * 5.0 * polymer.wt / (4.0 * polymer.z_chain);
        gp += gr;
        gpp += g2r;
        ep += polymer.wt * er;
        epp += polymer.wt * e2r;
    }
}

void LP2RSolver::gstar_fast_rouse(double w, double& gp, double& gpp) const
{
    gp = gpp = 0.0;
    const double w2 = w * w;
    for (const auto& polymer : polymers_) {
        if (polymer.relax_free_rouse) {
            continue;
        }
        const double zz = polymer.z_chain;
        const int zi = static_cast<int>(std::ceil(zz));
        double gp_poly = 0.0;
        double gpp_poly = 0.0;
        for (int i = 1; i < zi; ++i) {
            double tv = static_cast<double>(i) / zz;
            const double tv2 = tv * tv;
            const double tv4 = tv2 * tv2;
            gp_poly += 1.0 / (w2 + tv4);
            gpp_poly += tv2 / (w2 + tv4);
        }
        const int max_term = static_cast<int>(std::ceil(n_e_ * zz));
        for (int i = zi; i < max_term; ++i) {
            double tv = static_cast<double>(i) / zz;
            const double tv2 = tv * tv;
            const double tv4 = tv2 * tv2;
            tv = 1.0 / (w2 + 4.0 * tv4);
            gp_poly += 5.0 * tv;
            gpp_poly += 10.0 * tv2 * tv;
        }
        gp += w2 * gp_poly * polymer.wt / (4.0 * zz);
        gpp += w * gpp_poly * polymer.wt / (4.0 * zz);
    }
}

void LP2RSolver::gstar_slow(double w, double& gp, double& gpp, double& ep, double& epp) const
{
    gp = gpp = ep = epp = 0.0;
    const double wsq = w * w;
    const int n = static_cast<int>(t_ar_.size());
    for (int k = 1; k < n; ++k) {
        const double dphi = phi_ar_[k - 1] - phi_ar_[k];
        const double tk = t_ar_[k];
        for (int m = 1; m < n; ++m) {
            const double dphi_st = std::pow(phi_st_ar_[m - 1], controls_.alpha) -
                                   std::pow(phi_st_ar_[m], controls_.alpha);
            const double tm = t_ar_[m];
            const double tkm = tk * tm / (tk + tm);
            const double tv = tkm / (1.0 + wsq * tkm * tkm);
            gp += tv * tkm * dphi * dphi_st;
            gpp += tv * dphi * dphi_st;
        }
        double rint1 = 0.0;
        double rint2 = 0.0;
        symbint(tk, t_ar_[n - 1], w, rint1, rint2);
        rint1 *= 0.50 * std::pow(phi_st_ar_[n - 1], controls_.alpha);
        rint2 *= 0.50 * std::pow(phi_st_ar_[n - 1], controls_.alpha);
        gp += rint2 * tk * tk * dphi;
        gpp += rint1 * tk * dphi;
        const double tv = tk / (1.0 + wsq * tk * tk);
        ep += tv * tk * dphi;
        epp += tv * dphi;
    }
    gp *= wsq;
    gpp *= w;
    ep *= wsq;
    epp *= w;
}

double LP2RSolver::calc_visc() const
{
    InvSqSum p_inv_sq_sum;
    double eta_l = 0.0;
    double eta_ir = 0.0;
    double eta_fr = 0.0;
    for (const auto& polymer : polymers_) {
        const double zz = polymer.z_chain;
        const int zi = static_cast<int>(std::ceil(zz));
        const int zm = static_cast<int>(std::ceil(zz * n_e_));
        if (!polymer.relax_free_rouse) {
            eta_l += polymer.wt * p_inv_sq_sum(zi - 1) * zz;
            eta_ir += polymer.wt * p_inv_sq_sum(zi, zm) * zz;
        } else {
            eta_fr += polymer.wt * p_inv_sq_sum(zm) * zz;
        }
    }
    double eta0 = 0.25 * (eta_l + 2.5 * (eta_ir + eta_fr));

    eta0 += g_glass_scaled_ * (tau_glass_scaled_ / material_.beta_glass) *
            std::tgamma(1.0 / material_.beta_glass);

    if (t_ar_.size() > 1) {
        double eta_tube = 0.0;
        const int nd = static_cast<int>(t_ar_.size());
        const double td = t_ar_[nd - 1];
        const double phi_st_at_td = phi_st_ar_[nd - 1];
        for (int k = 1; k < nd; ++k) {
            const double dphi = phi_ar_[k - 1] - phi_ar_[k];
            const double tk = t_ar_[k];
            double tv = 0.0;
            for (int m = 1; m < nd; ++m) {
                const double dphi_st = std::pow(phi_st_ar_[m - 1], controls_.alpha) -
                                       std::pow(phi_st_ar_[m], controls_.alpha);
                const double tm = t_ar_[m];
                tv += dphi_st * tm / (tk + tm);
            }
            tv += std::pow(phi_st_at_td, controls_.alpha) * std::sqrt(td / tk) *
                  (kPiOver2 - std::atan(std::sqrt(td / tk)));
            eta_tube += dphi * tk * tv;
        }
        eta0 += (1.0 - rouse_wt_) * eta_tube;
    }

    return eta0 * material_.g0 * material_.tau_e;
}

}  // namespace reptate_lp2r
