import numpy as np

MBIG = 4.0e6
MSEED = 1618033.0
MZ = 0.0
FAC = 2.5e-7

Ran3Ma = [0.0] * 56 #ARRAY [1..55] OF real
Ran3Inext = 0
Ran3Inextp = 0

def abs(x):
    return x if x >= 0 else -x

def ran3(idum):
    global Ran3Inext, Ran3Inextp
# (* CONST
#       MBIG = 1000000000  MSEED=161803398  MZ=0  FAC=1.0e-9
# VAR
#       i,ii,k,mj,mk: longint *)

    # VAR
    # i,ii,k: integer
    # mj,mk: real
    if idum < 0:
        mj = MSEED + idum
        if mj >= 0.0:
            mj = mj - MBIG * np.trunc(mj / MBIG)
        else:
            mj = MBIG - abs(mj) + MBIG * np.trunc(abs(mj) / MBIG)
    # (*    mj = mj MOD MBIG *)
        Ran3Ma[55] = mj
        mk = 1
        for i in range(1, 55): #[1..54]
            ii = 21*i % 55
            Ran3Ma[ii] = mk
            mk = mj - mk
            if mk < MZ: 
                mk = mk + MBIG
            mj = Ran3Ma[ii]

        for k in range(1, 5):
            for i in range(1, 56): # [1..55]
                Ran3Ma[i] = Ran3Ma[i] - Ran3Ma[1 + ((i + 30) % 55)]
                if Ran3Ma[i] < MZ:
                    Ran3Ma[i] = Ran3Ma[i] + MBIG
        Ran3Inext = 0
        Ran3Inextp = 31
        idum = 1
    
    Ran3Inext = Ran3Inext + 1
    if Ran3Inext == 56:
        Ran3Inext = 1
    
    Ran3Inextp = Ran3Inextp + 1
    if Ran3Inextp == 56:
        Ran3Inextp = 1
    
    mj = Ran3Ma[Ran3Inext] - Ran3Ma[Ran3Inextp]
    if mj < MZ:
        mj = mj + MBIG
    Ran3Ma[Ran3Inext] = mj
    return mj * FAC, idum
