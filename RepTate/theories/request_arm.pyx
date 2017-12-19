def request_arm(arm_pool, bint arms_avail, int first_in_pool, int mmax, int arms_left):

    cdef int m = first_in_pool
    if arm_pool[m].R1 != 0:
        first_in_pool = arm_pool[m].R1
        mmax = mmax if mmax > m else m
        arm_pool[first_in_pool].L1 = 0
        arm_pool[m].L1 = 0
        arm_pool[m].L2 = 0
        arm_pool[m].R1 = 0
        arm_pool[m].R2 = 0
        arm_pool[m].up = 0
        arm_pool[m].down = 0
        arm_pool[m].ended = False
        arm_pool[m].endfin = False
        arm_pool[m].scission = False
        arms_left -= 1
        return m, arms_avail, first_in_pool, mmax, arms_left, True
    elif arm_pool[m].R1 == 0:
        # need to decide what to do if you run out of arms!
        arms_avail = False
        return m, arms_avail, first_in_pool, mmax, arms_left, False