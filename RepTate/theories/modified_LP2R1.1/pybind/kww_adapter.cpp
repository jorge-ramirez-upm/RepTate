#include "kww_adapter.h"

#include <cmath>
#include <limits>
#include <stdexcept>

extern "C" {
double kwws(const double, const double);
double kwwc(const double, const double);
}

namespace reptate_lp2r {
namespace {

constexpr long double PI = 3.141592653589793238462643383279502884L;
constexpr long double KWW_DELTA = 2.2e-12L;
constexpr long double KWW_EPS = 5.5e-20L;
constexpr int KWW_MAX_ITER = 16;

double kww_lim_low_storage(double beta)
{
    if (beta > 1.024) {
        return -1.68725 * beta + 4.8108 * beta * beta -
               2.561 * beta * beta * beta + 0.442 * beta * beta * beta * beta;
    }
    return std::exp(-0.03208 / beta / beta - 4.314 / beta + 3.516200 -
                    0.50287 * beta + 1.240 * beta * beta);
}

double kww_lim_low_loss(double beta)
{
    if (beta > 1.024) {
        return -0.8774954 * beta + 3.5873 * beta * beta -
               2.083 * beta * beta * beta + 0.3796 * beta * beta * beta * beta;
    }
    return std::exp(-0.02194 / beta / beta - 4.130 / beta + 2.966189 +
                    0.030104 * beta + 1.062 * beta * beta);
}

double square(double value)
{
    return value * value;
}

double kww_lim_high_storage(double beta)
{
    if (beta < 0.82) {
        return std::exp(0.07847516 / beta / beta - 2.585876 / beta + 4.999414 -
                        8.460926 * beta + 6.289183 * beta * beta);
    }
    return std::exp(-0.962597724393 + 5.818057 * (beta - 0.82) -
                    3.026212 * square(beta - 0.82) +
                    0.5485754 * std::pow(beta - 0.82, 3));
}

double kww_lim_high_loss(double beta)
{
    if (beta < 0.82) {
        return std::exp(0.006923209 / beta / beta - 1.321692 / beta - 1.44582 +
                        2.516339 * beta + 0.2973773 * beta * beta);
    }
    return std::exp(-0.746496154631 + 6.057558 * (beta - 0.82) -
                    3.41052 * square(beta - 0.82) +
                    0.7932314 * std::pow(beta - 0.82, 3));
}

double kww_mid_safe(double omega, double beta, bool storage)
{
    if (omega <= 0.0 || beta < 0.1 || beta > 2.0) {
        throw std::invalid_argument("invalid KWW arguments");
    }

    long double p = 1.8L;
    long double q = 0.2L;
    if (beta < 0.15) {
        p = 1.8L;
        q = 0.2L;
    } else if (beta < 0.25) {
        p = 1.6L;
        q = 0.4L;
    } else if (beta < 1.0) {
        p = 1.4L;
        q = 0.6L;
    } else if (beta < 1.75) {
        p = 1.0L;
        q = 0.2L;
    } else if (beta < 1.95) {
        p = 0.75L;
        q = 0.2L;
    } else {
        p = 0.15L;
        q = 0.4L;
    }

    const int kind = storage ? 1 : 0;
    const long double w = omega;
    const long double b = beta;
    const long double smin = 0.01L;
    int n = 40;
    long double previous = std::numeric_limits<long double>::quiet_NaN();
    long double best = std::numeric_limits<long double>::quiet_NaN();

    for (int iter = 0; iter < KWW_MAX_ITER; ++iter) {
        if (n > 1000000) {
            break;
        }
        const long double h =
            std::log(std::log(42.0L * n / KWW_DELTA / smin) / p) / n;
        int alternating_sign = 1 - 2 * (n & 1);
        long double sum = 0.0L;
        long double total_abs = 0.0L;

        for (int kaux = -n; kaux <= n; ++kaux) {
            long double k = static_cast<long double>(kaux);
            if (!kind) {
                k -= 0.5L;
            }
            const long double u = k * h;
            const long double chi = 2.0L * p * std::sinhl(u) + 2.0L * q * u;
            const long double dchi = 2.0L * p * std::coshl(u) + 2.0L * q;

            long double ahk = 0.0L;
            long double dhk = 0.0L;
            long double chk = 0.0L;
            if (u == 0.0L) {
                ahk = PI / h / dchi;
                dhk = 0.5L;
                chk = std::sin(ahk);
            } else {
                if (-chi > std::numeric_limits<double>::max_exponent / 2) {
                    continue;
                }
                const long double e = std::expl(-chi);
                ahk = PI / h * u / (1.0L - e);
                dhk = 1.0L / (1.0L - e) -
                      u * e * dchi / ((1.0L - e) * (1.0L - e));
                if (e > 1.0L) {
                    chk = kind ? std::sinl(PI * k / (1.0L - e)) :
                                 std::cosl(PI * k / (1.0L - e));
                } else {
                    chk = alternating_sign * std::sinl(PI * k * e / (1.0L - e));
                }
            }

            const long double tk = ahk / w;
            const long double f = std::expl(-std::powl(tk, b));
            const long double term = dhk * chk * f;
            sum += term;
            total_abs += std::fabsl(term);
            alternating_sign = -alternating_sign;
        }

        if (sum > 0.0L) {
            best = sum * PI / w;
        }
        if (iter > 0 && sum > 0.0L && std::isfinite(static_cast<double>(sum))) {
            const long double change = std::fabsl(sum - previous);
            const long double threshold = KWW_DELTA * std::fabsl(sum);
            if (change + KWW_EPS * total_abs < threshold) {
                return static_cast<double>(sum * PI / w);
            }
            if (std::isfinite(static_cast<double>(best)) &&
                change < 1.0e-10L * std::fabsl(sum)) {
                return static_cast<double>(best);
            }
        }
        previous = sum;
        n *= 2;
    }

    if (std::isfinite(static_cast<double>(best)) && best > 0.0L) {
        return static_cast<double>(best);
    }
    throw std::runtime_error("KWW fallback integration failed");
}

bool use_safe_midrange(double omega, double beta, bool storage)
{
    const double low_limit =
        storage ? kww_lim_low_storage(beta) : kww_lim_low_loss(beta);
    const double high_limit =
        storage ? kww_lim_high_storage(beta) : kww_lim_high_loss(beta);
    return omega >= low_limit && omega <= high_limit;
}

}  // namespace

double kww_storage(double omega, double beta)
{
    if (use_safe_midrange(std::fabs(omega), beta, true)) {
        const double value = kww_mid_safe(std::fabs(omega), beta, true);
        return omega < 0.0 ? -value : value;
    }
    return kwws(omega, beta);
}

double kww_loss(double omega, double beta)
{
    if (use_safe_midrange(std::fabs(omega), beta, false)) {
        return kww_mid_safe(std::fabs(omega), beta, false);
    }
    return kwwc(omega, beta);
}

}  // namespace reptate_lp2r
