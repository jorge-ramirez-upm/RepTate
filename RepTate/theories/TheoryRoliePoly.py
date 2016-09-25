from Theory import *
import numpy as np
from scipy.integrate import ode, odeint

class TheoryRoliePoly(Theory, CmdBase):
    """Rolie-Poly"""
    thname="RoliePoly"
    description="RoliePoly"
    citations="Likhtman, A.E. & Graham, R.S.\n\
Simple constitutive equation for linear polymer melts derived from molecular theory: Rolie-Poly equation\n\
J. Non-Newtonian Fluid Mech., 2003, 114, 1-12"

    def __init__(self, name="ThRoliePoly", parent_dataset=None, ax=None):
        super(TheoryRoliePoly, self).__init__(name, parent_dataset, ax)
        self.function = self.RoliePoly
        self.has_modes = True
        self.parameters["beta"]=Parameter("beta", 0.5, "CCR coefficient", ParameterType.real, False)
        self.parameters["delta"]=Parameter("deta", -0.5, "CCR exponent", ParameterType.real, False)
        self.parameters["lmax"]=Parameter("lmax", 10.0, "Maximum extensibility", ParameterType.real, False)
        self.parameters["nmodes"]=Parameter("nmodes", 2, "Number of modes", ParameterType.integer, False)
        for i in range(self.parameters["nmodes"].value):
            self.parameters["G%d"%i]=Parameter("G%d"%i, 1000.0, "Modulus of mode %d"%i, ParameterType.real, False)
            self.parameters["tauD%d"%i]=Parameter("tauD%d"%i, 10.0, "Terminal time of mode %d"%i, ParameterType.real, False)
            self.parameters["tauR%d"%i]=Parameter("tauR%d"%i, 0.5, "Rouse time of mode %d"%i, ParameterType.real, True)

    def set_param_value(self, name, value):
        if (name=="nmodes"):
            oldn=self.parameters["nmodes"].value
        super(TheoryRoliePoly, self).set_param_value(name, value)
        if (name=="nmodes"):
            for i in range(self.parameters["nmodes"].value):
                self.parameters["G%d"%i]=Parameter("G%d"%i, 1000.0, "Modulus of mode %d"%i, ParameterType.real, False)
                self.parameters["tauD%d"%i]=Parameter("tauD%d"%i, 10.0, "Terminal time of mode %d"%i, ParameterType.real, False)
                self.parameters["tauR%d"%i]=Parameter("tauR%d"%i, 0.5, "Rouse time of mode %d"%i, ParameterType.real, True)
            if (oldn>self.parameters["nmodes"].value):
                for i in range(self.parameters["nmodes"].value,oldn):
                    del self.parameters["G%d"%i]
                    del self.parameters["tauD%d"%i]
                    del self.parameters["tauR%d"%i]

    def get_modes(self):
        nmodes=self.parameters["nmodes"].value
        tau=np.zeros(nmodes)
        G=np.zeros(nmodes)
        for i in range(nmodes):
            tau[i]=self.parameters["tauD%d"%i].value
            G[i]=self.parameters["G%d"%i].value
        return tau, G

    def set_modes(self, tau, G):
        nmodes=len(tau)
        self.set_param_value("nmodes", nmodes)
        for i in range(nmodes):
            self.set_param_value("tauD%d"%i,tau[i])
            self.set_param_value("G%d"%i,G[i])

    def sigmadotshear(self, sigma, t, p):
        """Rolie-Poly differential equation under shear flow
    
        Arguments:
            sigma: vector of state variables (only xx and xy components are relevant)
                    sigma = [sxx, sxy]
            t : time
            p : vector of the parameters:
                    p = [tauD, tauR, beta, delta, gammadot]
        """ 
        sxx, sxy = sigma
        tauD, tauR, beta, delta, gammadot = p
    
        # Create the vector with the time derivative of sigma
        trace_sigma = sxx + 2
        aux1 = 2*(1-np.sqrt(3/trace_sigma))/tauR
        aux2 = beta*(trace_sigma/3)**delta
        return [2*gammadot*sxy-(sxx-1)/tauD-aux1*(sxx+aux2*(sxx-1)), gammadot*1-sxy/tauD-aux1*(sxy+aux2*sxy)]

        
    def RoliePoly(self, f=None):
        ft=f.data_table
        tt=self.tables[f.file_name_short]
        tt.num_columns=ft.num_columns
        tt.num_rows=ft.num_rows
        tt.data=np.zeros((tt.num_rows, tt.num_columns))
        tt.data[:,0]=ft.data[:,0]
        
        # ODE solver parameters
        abserr = 1.0e-8
        relerr = 1.0e-6
        t = ft.data[:,0]
        t = np.concatenate([[0],t])
        sigma0=[1, 0]
        beta=self.parameters["beta"].value
        delta=self.parameters["delta"].value
        gammadot=float(f.file_parameters["gdot"])
        nmodes=self.parameters["nmodes"].value
        for i in range(nmodes):
            tauD=self.parameters["tauD%d"%i].value
            tauR=self.parameters["tauR%d"%i].value
            p = [tauD, tauR, beta, delta, gammadot]
            sig = odeint(self.sigmadotshear, sigma0, t, args=(p,), atol=abserr, rtol=relerr)
            tt.data[:,1]+=self.parameters["G%d"%i].value*np.delete(sig[:,1],[0])
       
       