#include <stdio.h>
#include <stdbool.h>

#include "my_structs.h"

double scilength(double cur_conv, double Cs, double fin_conv){
    return 0;
}

double brlength(double cur_conv, double Cb, double fin_conv){
    return 0;
}
void tobita_grow(bool arms_avail, 
        int dir, int m, double cur_conv, bool sc_tag,
        double Cs, double Cb, double fin_conv,
        double tau, double beta,
         int rlevel, int bcount, bool tobitabatcherrorflag
         ){
        //"""dir,m:integer cur_conv: double sc_tag: boolean"""
        // var
        // m1,m2 :integer
        // seg_len,new_conv,rnd :double
        // sigma,lambd,pref,Psigma,Plambd,Pbeta :double

        rlevel += 1;  //recursion level
        if (rlevel > 5000 || tobitabatcherrorflag){
            //  need to decide what to do if you make molecules too big
            tobitabatcherrorflag = true;
            rlevel = 100000;
            return;
        }
        if (arms_avail == false)   // don't do anything if arms aren't available
            return;

        double seg_len = scilength(cur_conv, Cs, fin_conv);
        if (sc_tag && (seg_len < polybits.arm_pool[m].arm_len)){
            polybits.arm_pool[m].arm_len = seg_len;  // scission event
            polybits.arm_pool[m].scission = true;
        }
        /*
        Make a list od the arm_pool attribute and convert it into a list
        arm_pool[m].arm_len => arm_pool[m][0]

        */
        seg_len = brlength(cur_conv, Cb, fin_conv);

        if seg_len < polybits.arm_pool[m].arm_len: // a branch point
            bcount += 1
            m1, success = polybits.request_arm() // return success=False if arms not available
            if success: 
                polybits.armupdown(m, m1)
                m2, success = polybits.request_arm()
                if success:
                    polybits.armupdown(m,m2)
                    if (dir > 0): //going to the right
                        polybits.arm_pool[m].R1 = m1
                        polybits.arm_pool[m1].L2 = -m    //I think it might be useful if
                                                      //1 is connected to 2 all the time
                                                      // sign(L1) etc indicates direction of subsequent segment.
                        polybits.arm_pool[m1].arm_len = polybits.arm_pool[m].arm_len - seg_len
                        polybits.arm_pool[m].arm_len = seg_len
                        polybits.arm_pool[m1].arm_conv = cur_conv
                        polybits.arm_pool[m1].scission = polybits.arm_pool[m].scission
                        polybits.arm_pool[m].scission = False
                        new_conv = self.getconv2(cur_conv)
                        seg_len = self.calclength(new_conv)
                        polybits.arm_pool[m2].arm_len = seg_len
                        polybits.arm_pool[m2].arm_conv = new_conv
                        polybits.arm_pool[m1].L1 = m2
                        polybits.arm_pool[m2].L2 = m1
                        polybits.arm_pool[m].R2 = m2
                        polybits.arm_pool[m2].L1 = -m
                        self.tobita_grow(1, m2, new_conv, True)
                        self.tobita_grow(dir, m1, cur_conv, False)
                    else:  //going to the left
                        polybits.arm_pool[m].L1 = -m1
                        polybits.arm_pool[m1].R2 = m
                        polybits.arm_pool[m1].arm_len = polybits.arm_pool[m].arm_len - seg_len
                        polybits.arm_pool[m].arm_len = seg_len
                        polybits.arm_pool[m1].arm_conv = cur_conv
                        polybits.arm_pool[m1].scission = polybits.arm_pool[m].scission
                        polybits.arm_pool[m].scission = False
                        new_conv = self.getconv2(cur_conv)
                        seg_len = self.calclength(new_conv)
                        polybits.arm_pool[m2].arm_len = seg_len
                        polybits.arm_pool[m2].arm_conv = new_conv
                        polybits.arm_pool[m1].R1 = m2
                        polybits.arm_pool[m2].L2 = -m1
                        polybits.arm_pool[m].L2 = m2
                        polybits.arm_pool[m2].L1 = m
                        self.tobita_grow(1, m2, new_conv, True)
                        self.tobita_grow(dir, m1, cur_conv, False)
                    // end of arm m2 available
                // end of arm m1 available
            // end of it's a branchpoint
        else: // non side-branching condition - deal with end of chain
            if polybits.arm_pool[m].scission: // the end of the chain is a scission point
                rnd, polybits.iy3 = ran3(polybits.iy3)
                if rnd < 0.50: // and there is more growth at the scission point
                    new_conv = self.getconv2(cur_conv)
                    m1, success = polybits.request_arm() // success=False if arm not available
                    if success: 
                        polybits.armupdown(m, m1)
                        seg_len = self.calclength(new_conv)
                        polybits.arm_pool[m1].arm_len = seg_len
                        polybits.arm_pool[m1].arm_conv = new_conv
                        if dir > 0:
                            polybits.arm_pool[m].R1 = m1
                            polybits.arm_pool[m1].L2 = -m
                        else:
                            polybits.arm_pool[m].L1 = m1
                            polybits.arm_pool[m1].L2 = m
                        self.tobita_grow(1, m1, new_conv, True)
                    // end check for arm available
                // end of more growth from scission point
            // end of scission at chain end
            // chain end possibilities depend on the direction
            elif dir > 0:  //  growing to the right
                sigma = Cs * cur_conv / (1.0 - cur_conv) // calculate scission event population
                lambd = Cb * cur_conv / (1.0 - cur_conv)  // calculate branching population
                pref = tau + beta + sigma + lambd
                Pbeta = beta/pref         // prob termination by combination
                rnd, polybits.iy3 = ran3(polybits.iy3)
                if rnd < Pbeta: //prob for termination by combination
                    m1, success = polybits.request_arm() // success=False if arm not available
                    if success:
                        polybits.armupdown(m, m1)
                        seg_len = self.calclength(cur_conv)
                        polybits.arm_pool[m1].arm_len = seg_len
                        polybits.arm_pool[m1].arm_conv = cur_conv
                        polybits.arm_pool[m].R1 = -m1
                        polybits.arm_pool[m1].R2 = -m
                        self.tobita_grow(-1, m1, cur_conv, True)
                    // end polybits.request_arm check
                // otherwise, end of chain: do nothing
            // end of right growth
            else: // must be left growth
                sigma = Cs * cur_conv / (1.0 - cur_conv) // calculate scission event population
                lambd = Cb * cur_conv / (1.0 - cur_conv)  // calculate branching population
                pref = tau + beta + sigma + lambd
                Plambd = lambd/pref     // prob reaction from polymer transfer (branching)
                Psigma = sigma/pref // prob reaction from scission site
                rnd, polybits.iy3 = ran3(polybits.iy3)
                if rnd < Plambd: // grew from a branch
                    bcount += 1
                    new_conv = self.getconv1(cur_conv)
                    m1, success = polybits.request_arm()
                    if success: // check arm availability
                        polybits.armupdown(m, m1)
                        m2, success = polybits.request_arm()
                        if success:
                            polybits.armupdown(m, m2)
                            seg_len = self.calclength(new_conv)
                            polybits.arm_pool[m1].arm_len = seg_len
                            polybits.arm_pool[m1].arm_conv = new_conv
                            polybits.arm_pool[m].L1 = m1
                            polybits.arm_pool[m1].L2 = m
                            self.tobita_grow(1, m1, new_conv, True)
                            seg_len = self.calclength(new_conv)
                            polybits.arm_pool[m2].arm_len = seg_len
                            polybits.arm_pool[m2].arm_conv = new_conv
                            polybits.arm_pool[m].L2 = -m2
                            polybits.arm_pool[m2].R1 = m
                            polybits.arm_pool[m1].L1 = -m2
                            polybits.arm_pool[m2].R2 = m1
                            self.tobita_grow(-1, m2, new_conv, True)
                        // end polybits.request_arm m2 check
                    // end polybits.request_arm m1 check
                elif rnd < (Psigma + Plambd): // grew from scission
                    new_conv = self.getconv1(cur_conv)
                    rnd2, polybits.iy3 = ran3(polybits.iy3)
                    if rnd2 <= 0.50:
                        m1, success = polybits.request_arm()
                        if success: // check arm availability
                            polybits.armupdown(m, m1)
                            seg_len = self.calclength(new_conv)
                            polybits.arm_pool[m1].arm_len = seg_len
                            polybits.arm_pool[m1].arm_conv = new_conv
                            polybits.arm_pool[m].L1 = m1
                            polybits.arm_pool[m1].L2 = m
                            self.tobita_grow(1, m1, new_conv, True)
                        // end polybits.request_arm check
                    else:
                        m2, success = polybits.request_arm()
                        if success: // check arm availability
                            polybits.armupdown(m, m2)
                            seg_len = self.calclength(new_conv)
                            polybits.arm_pool[m2].arm_len = seg_len
                            polybits.arm_pool[m2].arm_conv = new_conv
                            polybits.arm_pool[m].L2 = -m2
                            polybits.arm_pool[m2].R1 = m
                            self.tobita_grow(-1, m2, new_conv, True)
                        // end polybits.request_arm check
                // grew from initiation : do nothing
            // end of left-growth chain end possibilities
        // end of all chain-end possibilities
        rlevel -= 1
         }