import numpy as np

def scilength(double conv, double Cs, double fin_conv):
    """Calculate length between scission-points of a segment grown at conversion "conv" """
    # var
    # rnd,eta  :double
    cdef double rnd, eta, r

    rnd = np.random.random()
    if rnd == 0.0:
        rnd = 1.0
    eta = Cs * np.log((1.0 - conv) / (1.0 - fin_conv)) + 1.0e-80
    r = -np.log(rnd)/eta
    if r < 1000.0:
        r = np.trunc(r) + 1
    return r
