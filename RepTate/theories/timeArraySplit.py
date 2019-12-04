import numpy as np

def timeArraySplit( t, Tend):
    lastPoint= np.nonzero(t >= Tend)[0][0]

    t1=t[:lastPoint]
    #t1=np.append([0],t[:lastPoint])
    t1=np.append(t1,[Tend])

    t2=np.append([Tend],t[lastPoint:])

    return t1,t2
    
