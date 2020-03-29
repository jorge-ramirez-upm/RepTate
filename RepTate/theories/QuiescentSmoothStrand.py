# -*- coding: utf-8 -*-
"""
Created on Fri Nov 30 13:15:57 2018

@author: phydjr
"""

import math
import scipy
from scipy import optimize
import numpy as np


def wholeLandscape(NT, E0_param, mus_param, Kappa0_param):
    global E0, mus, Kappa0, thetaMin, arsq,ar

    E0=E0_param
    mus=mus_param
    Kappa0=Kappa0_param
    
    thetaMin=1e-300

    #a_r
    arsq=9.0/16.0*math.pi
    ar=math.sqrt(arsq)

    return Freeflucqui(NT)


def Freequi(NS,NT):
    LL=NT/NS  
    kappa=Kappa0+1.0/LL**2
    
    FF=-0.5*(NS-1)*math.log(2.0*math.pi/kappa) + 0.5*math.log(NS) - NT*E0
    #surface terms
    aspect=NS**3/NT**2/arsq
    if aspect<1:
        ep=math.sqrt(1.0-aspect)
        Stil=2.0*NS+2.0*ar*NT*math.asin(ep)/ep/math.sqrt(NS)
    elif aspect>1:
        eps0=math.sqrt(1.0-1.0/aspect)
        Stil=2.0*NS+arsq*NT**2*math.log((1.0+eps0)/(1.0-eps0))/eps0/NS**2
    else:
        Stil=2.0*NS+2.0*ar*NT/math.sqrt(NS)
    FF+=mus*Stil
    return FF


def Free1qui(NT):
    res=scipy.optimize.minimize_scalar(Freequi, bounds=(0.00001,0.999999*NT), args=(NT), method='bounded')
    #print res
    return res.fun
    
def Freeflucqui(NT):
    res=scipy.optimize.minimize_scalar(Freequi, bounds=(0.0000001,0.999999*NT), args=(NT), method='bounded')
    nsmid=res.x
    ##second derivative
    d2fdn2=(Freequi(nsmid+0.1,NT)+Freequi(nsmid-0.1,NT)-2*Freequi(nsmid,NT))/0.01
    fNT=res.fun+math.log(d2fdn2/2/math.pi)
    return fNT

