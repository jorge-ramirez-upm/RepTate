// RepTate: Rheology of Entangled Polymers: Toolkit for the Analysis of Theory and Experiments
// --------------------------------------------------------------------------------------------------------

// Authors:
//     Jorge Ramirez, jorge.ramirez@upm.es
//     Victor Boudara, victor.boudara@gmail.com
//     Daniel Read, d.j.read@leeds.ac.uk

// Useful links:
//     http://blogs.upm.es/compsoftmatter/software/reptate/
//     https://github.com/jorge-ramirez-upm/RepTate
//     http://reptate.readthedocs.io

// --------------------------------------------------------------------------------------------------------

// Copyright (2017): Jorge Ramirez, Victor Boudara, Universidad Politécnica de Madrid, University of Leeds

// This file is part of RepTate.

// RepTate is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.

// RepTate is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.

// You should have received a copy of the GNU General Public License
// along with RepTate.  If not, see <http://www.gnu.org/licenses/>.

// --------------------------------------------------------------------------------------------------------
#include <stdlib.h>
#include "polybits.h"
#include "calc_architecture.h"

int calc_seniority(int n)
{
    int first, m, sen_level, mL1, mL2, mR1, mR2, senL1, senL2, senR1, senR2, maxL, maxR, nassigned, armnum;
    first = br_poly[n].first_end;
    m = first;
    nassigned = 0;
    armnum = br_poly[n].armnum;
    while (true)
    {
        // loop over all arms and determine if free end (seniority=1)
        // if not, assign 0 (not determined)
        if ((arm_pool[m].L1 == 0 && arm_pool[m].L2 == 0) || (arm_pool[m].R1 == 0 && arm_pool[m].R2))
        {
            // it is a free end
            arm_pool[m].senio = 1;
            nassigned++;
            if (nassigned == armnum)
            {
                br_poly[n].max_senio = 1;
                return 1;
            }
        }
        else
        {
            arm_pool[m].senio = 0;
        }
        m = arm_pool[m].down;
        if (m == first)
            break;
    }

    m = first;
    sen_level = 2;
    while (true)
    {
        if (arm_pool[m].senio == 0)
        {
            // seniority not yet determined
            mL1 = arm_pool[m].L1;
            mL2 = arm_pool[m].L2;
            mR1 = arm_pool[m].R1;
            mR2 = arm_pool[m].R2;

            senL1 = arm_pool[mL1].senio;
            senL2 = arm_pool[mL2].senio;
            maxL = senL1 > senL2 ? senL1 : senL2;

            senR1 = arm_pool[mR1].senio;
            senR2 = arm_pool[mR2].senio;
            maxR = senR1 > senR2 ? senR1 : senR2;

            if ((senL1 != 0 && senL2 != 0 && maxL == sen_level - 1) || (senR1 != 0 && senR2 != 0 && maxR == sen_level - 1))
            {
                arm_pool[m].senio = sen_level;
                nassigned++;
                if (nassigned == armnum)
                {
                    br_poly[n].max_senio = 1;
                    return sen_level;
                }
            }
        }
        m = arm_pool[m].down;
        if (m == first)
        {
            sen_level++;
        }
    }
}