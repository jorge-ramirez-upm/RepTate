#include <stdlib.h>
#include "polybits.h"
#include "polymassrg.h"

void mass_segs(int first, double *lentot_out, int *segtot_out)
{
    int next;
    *lentot_out = arm_pool[first].arm_len;
    *segtot_out = 1;
    next = arm_pool[first].down;
    while (next != first)
    {
        *lentot_out = *lentot_out + arm_pool[next].arm_len;
        *segtot_out = *segtot_out + 1;
        next = arm_pool[next].down;
        if (next == 0)
        {
            next = first;
            // ('issues here');
        }
    }
}

void mass_rg1(int m, double cur_c, double *lentot_out, double *htot_out, double *jtot_out)
{

    int mc, m1, m2;
    double h1, h2, j1, j2, len1, len2, lenc, hc, jc;

    mc = abs(m); // sign of m gives direction
    if (mc == 0)
    { // do not count current segment
        *lentot_out = 0.0;
        *htot_out = 0.0;
        *jtot_out = 0.0;
        return;
    }
    if (m > 0)
    { //positive direction
        m1 = arm_pool[mc].R1;
        m2 = arm_pool[mc].R2;
    }
    else
    {
        m1 = arm_pool[mc].L1;
        m2 = arm_pool[mc].L2;
    }
    mass_rg1(m1, cur_c, &len1, &h1, &j1);
    mass_rg1(m2, cur_c, &len2, &h2, &j2);
    lenc = arm_pool[mc].arm_len;
    hc = lenc / 2.0;
    jc = lenc / 3.0;
    *lentot_out = lenc + len1 + len2;
    *htot_out = (lenc * hc + lenc * (len1 + len2) + len1 * h1 + len2 * h2) / (*lentot_out);
    *jtot_out = (lenc * lenc * jc + len1 * len1 * j1 + len2 * len2 * j2 + 2.0 * (len1 * len2 * (h1 + h2) + len1 * lenc * (h1 + hc) + len2 * lenc * (h2 + hc))) / ((*lentot_out) * (*lentot_out));
}

void mass_rg2(int m, double cur_c, double *lentot_out, double *jtot_out, double *gfact_out)
{
    int mc, m1, m2;
    double h1, h2, j1, j2, len1, len2, lenc, hc, jc;

    mc = abs(m); //sign of m gives direction
    if (mc == 0)
    { //do not count current segment
        *lentot_out = 0.0;
        *jtot_out = 0.0;
        *gfact_out = 0.0;
        return;
    }
    m1 = arm_pool[mc].L1;
    m2 = arm_pool[mc].L2;
    mass_rg1(m1, cur_c, &len1, &h1, &j1);
    mass_rg1(m2, cur_c, &len2, &h2, &j2);
    mass_rg1(mc, cur_c, &lenc, &hc, &jc);
    *lentot_out = lenc + len1 + len2;
    *jtot_out = (lenc * lenc * jc + len1 * len1 * j1 + len2 * len2 * j2 + 2.0 * (len1 * len2 * (h1 + h2) + len1 * lenc * (h1 + hc) + len2 * lenc * (h2 + hc))) / ((*lentot_out) * (*lentot_out));
    *gfact_out = 3 * (*jtot_out) / (*lentot_out);
}
