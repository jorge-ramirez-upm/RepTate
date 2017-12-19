import numpy as np

def brlength(double conv, double Cb, double fin_conv):
    """Calculate length between branch-points of a segment grown at conversion "conv" """
    # var
    # rnd,rho :double
    cdef double rnd, cdrho, r

    rnd = np.random.random()
    if rnd == 0.0:
        rnd = 1.0
    rho = Cb * np.log((1.0 - conv) / (1.0 - fin_conv))
    r = -np.log(rnd)/rho
    return r