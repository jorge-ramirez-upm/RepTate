# -*- coding: utf-8 -*-
"""
Created on Fri Nov 30 13:15:57 2018

@author: phydjr
"""

import math
import scipy
#import matplotlib.pyplot as plt
from scipy import optimize
#import pandas as pa
import numpy as np
import re
import sys
import os



def afun(A,LL):
    sum1=0.0
    sum2=0.0
    for i in range(numc):
        tem=1.0-A*edf[i]
        sum1+=phi[i]*edf[i]/tem
        sum2+=phi[i]*edf[i]/tem**2
    tem=LL*sum1/sum2-1.0
    return tem

def Free2(NS,NT):
    LL=NT/NS
    A=scipy.optimize.brenth(afun,0,iedfmax,args=(LL))
    sum1=0.0
    for i in range(numc):
        tem=1.0-A*edf[i]
        sum1+=phi[i]*edf[i]/tem
    AB=1.0/sum1
    w=[]
    v=[]
    for i in range(numc):
        tem=1.0-A*edf[i]
        w.append(AB*phi[i]*edf[i]/tem)
        v.append(w[i]/tem/LL)
    # now, put together free energy terms
    sum1=0.0
    for i in range(numc):
        logw=math.log(w[i])
        logv=math.log(v[i])
        logc=math.log(v[i]-w[i]/LL)
        sum1+=w[i]*(2*logw-logphi[i])/LL-v[i]*logv+(v[i]-w[i]/LL)*logc-v[i]*df[i]    
    FF=NT*sum1-NS*math.log(LL)-NT*E0
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
        
def Freequi(NS,NT):
    LL=NT/NS    
    FF=-NS*math.log(LL)-NT*E0+(NT-NS)*math.log(1.0-1.0/LL)
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

def Free1(NT):
    res=scipy.optimize.minimize_scalar(Free2, bounds=(1,0.999999*NT), args=(NT), method='bounded')
    return res.fun
    
def Freefluc(NT):
    res=scipy.optimize.minimize_scalar(Free2, bounds=(1,0.999999*NT), args=(NT), method='bounded')
    nsmid=res.x
    ##second derivative
    d2fdn2=(Free2(nsmid+0.1,NT)+Free2(nsmid-0.1,NT)-2*Free2(nsmid,NT))/0.01
    fNT=res.fun+math.log(d2fdn2/2/math.pi)
    return fNT


def Free1qui(NT):
    res=scipy.optimize.minimize_scalar(Freequi, bounds=(1,0.999999*NT), args=(NT), method='bounded')
    return res.fun
    
def Freeflucqui(NT):
    res=scipy.optimize.minimize_scalar(Freequi, bounds=(1,0.999999*NT), args=(NT), method='bounded')
    nsmid=res.x
    ##second derivative
    d2fdn2=(Freequi(nsmid+0.1,NT)+Freequi(nsmid-0.1,NT)-2*Freequi(nsmid,NT))/0.01
    fNT=res.fun+math.log(d2fdn2/2/math.pi)
    return fNT

def Freesum(NT):
    sum=0.0
    NS=1
    while NS<NT:
        sum=sum+math.exp(-Free2(NS,NT))
        NS=NS+1
    fren=-math.log(sum)
    return fren

def Freesumqui(NT):
    sum=0.0
    NS=1
    while NS<NT:
        sum=sum+math.exp(-Freequi(NS,NT))
        NS=NS+1
    fren=-math.log(sum)
    return fren


def findDfStar( params):
    #Extract params
    global E0, mus, phi, df, edf, edfmax, logphi, iedfmax, arsq, ar,numc, trueQuiescent
    
    trueQuiescent = params['landscape']
    phi = params['phi']
    df = params['df']
    numc=phi.size
    E0 = params['epsilonB']
    mus = params['muS']
    maxNT=trueQuiescent.size

    

    #a_r
    arsq=9.0/16.0*math.pi
    ar=math.sqrt(arsq)

    #setting up some parameters
    edf = [0] * numc
    edfmax=0
    logphi=[]

    for i in range(numc):
        edf[i]=math.exp(df[i])
        logphi.append(math.log(phi[i]))
        edfmax=max(edfmax,edf[i])
    iedfmax=0.999999999999999/edfmax


    res=scipy.optimize.minimize_scalar(FreeTrue, bounds=(3.0,maxNT), method='bounded')
    return -res.fun
    
def FreeTrue(NT):
    NTlow = math.floor(NT)
    NThigh = NTlow +1
    trueQ = trueQuiescent[NTlow] + \
      (trueQuiescent[NThigh]-trueQuiescent[NTlow])*(NT-NTlow)
    #!3return -(Freefluc(NT)-Freeflucqui(NT))
    return -(trueQ+Freefluc(NT)-Freeflucqui(NT))
