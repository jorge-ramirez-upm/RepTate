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

// Copyright (2017-2023): Jorge Ramirez, Victor Boudara, Universidad Politécnica de Madrid, University of Leeds


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
#include "polycleanup.h"

void polyclean(int n)
{
    int seg1;
    seg1 = br_poly[n].first_end;
    armclean(seg1);
    seg1 = -seg1;
    armclean(seg1);
}

void armclean(int m)
{
    int mc, m1, m2, mc1, mc2, t1, t2, tc1, tc2, tup, tdown;
    mc = abs(m);
    if (m > 0)
    { //positive direction
        m1 = arm_pool[mc].R1;
        m2 = arm_pool[mc].R2;
    }
    else //negative direction
    {
        m1 = arm_pool[mc].L1;
        m2 = arm_pool[mc].L2;
    }
    if ((m1 != 0) && (m2 != 0))
    { //branchpoint - no need for cleaning
        armclean(m1);
        armclean(m2);
    }
    else if ((m1 != 0) && (m2 == 0)) // < changed to <> by DJR
    {

        mc1 = abs(m1);
        // add lengths together
        arm_pool[mc].arm_len = arm_pool[mc].arm_len + arm_pool[mc1].arm_len;
        // reconnect current segment to opposite side of next segment
        if (m1 > 0)
        {
            t1 = arm_pool[mc1].R1;
            t2 = arm_pool[mc1].R2;
        }
        else
        {
            t1 = arm_pool[mc1].L1;
            t2 = arm_pool[mc1].L2;
        }
        tc1 = abs(t1);
        tc2 = abs(t2);
        //if (tc1=mc) or (tc2=mc) then writeln('error');
        if (m > 0)
        {
            arm_pool[mc].R1 = t1;
            arm_pool[mc].R2 = t2;
        }
        else
        {
            arm_pool[mc].L1 = t1;
            arm_pool[mc].L2 = t2;
        }
        if (t1 > 0)
        {
            arm_pool[tc1].L2 = -m; // as viewed from this segment, the sign of the current segment
                                   // is the opposite of its sign from where suroutine was originally called
            arm_pool[tc1].L1 = t2; // this should already be so!!
        }
        else if (t1 < 0)
        { //specifically exclude case where t1=0
            arm_pool[tc1].R2 = -m;
            arm_pool[tc1].R1 = t2; //this should already be so!!
        }
        if (t2 > 0)
        {
            arm_pool[tc2].L1 = -m;
            arm_pool[tc2].L2 = t1; //this should already be so!!
        }
        else if (t2 < 0)
        { //specifically exclude case where t1=0
            arm_pool[tc2].R1 = -m;
            arm_pool[tc2].R2 = t1; //this should already be so!!
        }
        // reconnect up and down of removed segment
        tup = arm_pool[mc1].up;
        tdown = arm_pool[mc1].down;
        arm_pool[tup].down = tdown;
        arm_pool[tdown].up = tup;
        // return to pool
        return_arm(mc1);
        // re-call clean-up on m
        armclean(m);
    }
    else if ((m1 == 0) && (m2 != 0))
    {
        mc2 = abs(m2);
        // add lengths together
        arm_pool[mc].arm_len = arm_pool[mc].arm_len + arm_pool[mc2].arm_len;
        // reconnect current segment to opposite side of next segment
        if (m2 > 0)
        {
            t1 = arm_pool[mc2].R1;
            t2 = arm_pool[mc2].R2;
        }
        else
        {
            t1 = arm_pool[mc2].L1;
            t2 = arm_pool[mc2].L2;
        }
        tc1 = abs(t1);
        tc2 = abs(t2);
        //if (tc1=mc) or (tc2=mc) then writeln('error');
        if (m > 0)
        {
            arm_pool[mc].R1 = t1;
            arm_pool[mc].R2 = t2;
        }
        else
        {
            arm_pool[mc].L1 = t1;
            arm_pool[mc].L2 = t2;
        }
        if (t1 > 0)
        {
            arm_pool[tc1].L2 = -m; // as viewed from this segment, the sign of the current segment
                                   // is the opposite of its sign from where suroutine was originally called
            arm_pool[tc1].L1 = t2; // this should already be so!!
        }
        else if (t1 < 0)
        { //specifically exclude case where t1=0
            arm_pool[tc1].R2 = -m;
            arm_pool[tc1].R1 = t2; //!this should already be so!!
        }
        if (t2 > 0)
        {
            arm_pool[tc2].L1 = -m;
            arm_pool[tc2].L2 = t1; // this should already be so!!
        }
        else if (t2 < 0)
        { // specifically exclude case where t1=0
            arm_pool[tc2].R1 = -m;
            arm_pool[tc2].R2 = t1; // !this should already be so!!
        }
        // reconnect up and down of removed segment
        tup = arm_pool[mc2].up;
        tdown = arm_pool[mc2].down;
        arm_pool[tup].down = tdown;
        arm_pool[tdown].up = tup;
        // return to pool
        return_arm(mc2);
        // recall clean-up on m
        armclean(m);
    }
}
