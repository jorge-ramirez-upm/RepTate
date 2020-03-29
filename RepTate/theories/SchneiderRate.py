from scipy.integrate import ode, odeint
import numpy as np
from scipy.interpolate import interp1d

def intSchneider( t, Ndot, Ndot0, N_0, G_C):
    global N_dot_func

    N_scale = N_0  +  Ndot0 * t[-1]
    Ndot= Ndot/N_scale 

    #Prepend an initial datapoint at t=0
    t = np.append([0],t)
    Ndot = np.append(Ndot0,Ndot) 

    #Append a final data point
    t2 = np.append(t,t[-1]*5.0)
    Ndot = np.append(Ndot,Ndot[-1])

    N_dot_func = interp1d(t2, Ndot, kind='cubic') #Spline to interpolate Ndot
    
    #Solve Schneider ODEs
    phiSc0=([0.0,0.0,0.0,8*np.pi*N_0/N_scale])
    sol=odeint( Schneider, phiSc0, t, args=(G_C,))
    
    sol = np.delete(sol , 0, 0) #Remove row containing t=0
    sol = sol*N_scale
    return sol
    
def Schneider(phiSc,t,G_C):
    return  G_C*phiSc[1],  G_C*phiSc[2],  G_C*phiSc[3], \
      8*np.pi*abs(N_dot_func(t)) #When Ndot is small interpolation is sometimes negative!!
