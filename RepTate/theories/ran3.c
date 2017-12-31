#include <math.h>
#include "ran3.h"

double ran3(int *idum)
{
    const double mbig = 4.0e6;
    const double mseed = 1618033.0;
    const double mz = 0.0;
    const double fac = 2.5e-7;

    static int Ran3Inext;
    static int Ran3Inextp;
    static double Ran3Ma[56]; //[1..55]

    int i, ii, k;
    double mj, mk;

    if (idum < 0)
    {
        mj = mseed + *idum;
        if (mj >= 0.0)
        {
            mj = mj - mbig * trunc(mj / mbig);
        }
        else
        {
            mj = mbig - fabs(mj) + mbig * trunc(fabs(mj) / mbig);
        }
        Ran3Ma[55] = mj;
        mk = 1;
        for (i = 1; i <= 54; i++)
        {
            ii = (21 * i) % 55;
            Ran3Ma[ii] = mk;
            mk = mj - mk;
            if (mk < mz)
            {
                mk = mk + mbig;
            }
            mj = Ran3Ma[ii];
        }
        for (k = 1; k <= 4; k++)
        {
            for (i = 1; i <= 55; i++)
            {
                Ran3Ma[i] = Ran3Ma[i] - Ran3Ma[1 + ((i + 30) % 55)];
                if (Ran3Ma[i] < mz)
                {
                    Ran3Ma[i] = Ran3Ma[i] + mbig;
                }
            }
        }
        Ran3Inext = 0;
        Ran3Inextp = 31;
        *idum = 1;
    }
    Ran3Inext = Ran3Inext + 1;
    if (Ran3Inext == 56)
    {
        Ran3Inext = 1;
    }
    Ran3Inextp = Ran3Inextp + 1;
    if (Ran3Inextp == 56)
    {
        Ran3Inextp = 1;
    }
    mj = Ran3Ma[Ran3Inext] - Ran3Ma[Ran3Inextp];
    if (mj < mz)
    {
        mj = mj + mbig;
    }
    Ran3Ma[Ran3Inext] = mj;
    return mj * fac;
}