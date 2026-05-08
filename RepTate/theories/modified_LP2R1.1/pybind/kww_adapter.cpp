#include "kww_adapter.h"

extern "C" {
double kwws(const double, const double);
double kwwc(const double, const double);
}

namespace reptate_lp2r {

double kww_storage(double omega, double beta)
{
    return kwws(omega, beta);
}

double kww_loss(double omega, double beta)
{
    return kwwc(omega, beta);
}

}  // namespace reptate_lp2r
