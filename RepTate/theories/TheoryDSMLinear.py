# RepTate: Rheology of Entangled Polymers: Toolkit for the Analysis of Theory and Experiments
# --------------------------------------------------------------------------------------------------------
#
# Authors:
#     Jorge Ramirez, jorge.ramirez@upm.es
#     Victor Boudara, victor.boudara@gmail.com
#
# Useful links:
#     http://blogs.upm.es/compsoftmatter/software/reptate/
#     https://github.com/jorge-ramirez-upm/RepTate
#     http://reptate.readthedocs.io
#
# --------------------------------------------------------------------------------------------------------
#
# Copyright (2017): Jorge Ramirez, Victor Boudara, Universidad Politécnica de Madrid, University of Leeds
#
# This file is part of RepTate.
#
# RepTate is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# RepTate is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with RepTate.  If not, see <http://www.gnu.org/licenses/>.
#
# --------------------------------------------------------------------------------------------------------
"""Module TheoryDSMLinear"""
import numpy as np
from CmdBase import CmdBase, CmdMode
from Parameter import Parameter, ParameterType, OptType
from Theory import Theory
from QTheory import QTheory
from DataTable import DataTable
from scipy import interpolate, special, optimize 

class TheoryDSMLinear(CmdBase):
    """Calculate the Discrete Slip Link theory for the linear rheology of linear entangled polymers.
        
    * **Parameters**"""

    thname = "CFSM+Rouse"
    description = "Clustered Fixed Slip Link theory for linear entangled polymers"
    citations = ["Katzarova, M. et al, Rheol Acta 2015, 54(3), 169-183.", "Andreev, M. et al., J. Rheol. 2014, 58(3), 723-736"]
    doi = ["https://doi.org/10.1007/s00397-015-0836-0", "https://doi.org/10.1122%2F1.4869252"]

    def __new__(cls, name='', parent_dataset=None, axarr=None):
        """**Constructor**"""
        return GUITheoryDSMLinear(
            name, parent_dataset,
            axarr) if (CmdBase.mode == CmdMode.GUI) else CLTheoryDSMLinear(
                name, parent_dataset, axarr)


class BaseTheoryDSMLinear:
    """Base theory DSM"""
    #help_file = ''
    single_file = False  # False if the theory can be applied to multiple files simultaneously
    thname = TheoryDSMLinear.thname
    citations = TheoryDSMLinear.citations
    doi = TheoryDSMLinear.doi

    def __init__(self, name='', parent_dataset=None, axarr=None):
        """**Constructor**"""
        super().__init__(name, parent_dataset, axarr)
        self.function = self.calculate  # main theory function
        self.has_modes = False  # True if the theory has modes

        # Declare theory parameters and Material parameters
        self.parameters["MK"] = Parameter(
            name=r'MK',
            value=300,
            description="Molecular weight of Kuhn step (Da)",
            type=ParameterType.real,
            opt_type=OptType.const,
            display_flag=True)

        self.parameters["rho0"] = Parameter(
            name=r'rho0',
            value=1.0,
            description="Density (g/cc)",
            type=ParameterType.real,
            opt_type=OptType.const,
            display_flag=True)

        self.parameters["Mc"] = Parameter(
            name=r'Mc',
            value=2000,
            description="Molecular weight of a cluster in Da",
            type=ParameterType.real,
            opt_type=OptType.opt,
            display_flag=True)

        self.parameters["tau_c"] = Parameter(
            name=r'tau_c',
            value=0.1,
            description="Time constant used to fit CFSM results (beta = 1) to experimental data",
            type=ParameterType.real,
            opt_type=OptType.opt,
            display_flag=True)

        self.parameters["beta"] = Parameter(
            name=r'beta',
            value=30,
            description="Entanglement activity parameter for input to DSM simulations",
            type=ParameterType.real,
            opt_type=OptType.opt,
            display_flag=True)

        # self.parameters["tau_K"] = Parameter(
        #     name=r'tau_K',
        #     value=tau_K,
        #     description="Time constant for comparing DSM results to experimental data",
        #     type=ParameterType.real,
        #     opt_type=OptType.const,
        #     display_flag=True)

        # self.parameters["Nc"] = Parameter(
        #     name=r'N_c',
        #     value=Nc,
        #     description="Number of entanglement clusters",
        #     type=ParameterType.real,
        #     opt_type=OptType.const,
        #     display_flag=True)

        self.get_material_parameters()

        ft = self.parent_dataset.files[0].data_table
        Mw = float(parent_dataset.files[0].file_parameters["Mw"])*1000.0 # units of Da
        T = float(parent_dataset.files[0].file_parameters["T"]) + 273.15 # In units of K
        R = 8.314462*10**3 #units of L Pa K^-1 mol^-1
        rho0 = self.parameters["rho0"].value
        MK = self.parameters["MK"].value
        #---------------------------------------------
        # CALCULATE DSM PARAMETERS FROM CROSSOVER FREQUENCY
        crossover_limits = self.find_crossover_limits(data=ft.data)
        [omega_x, Gx] = self.Gslfx(crossover_limits,data=ft.data)
        solNc = optimize.brentq(self.solveNc,a=1,b=1000,args=(Gx,Mw,rho0,R,T))
        if solNc>0:
            self.Nc = solNc
            self.Mc = Mw/self.Nc
            self.set_param_value("Mc", self.Mc)
            self.tau_c = 151.148/(omega_x*self.Nc**3.50)
            self.set_param_value("tau_c", self.tau_c)
            self.beta = Mw/(0.56*self.Nc*MK) - 1
            self.set_param_value("beta", self.beta)
            self.tau_K = self.tau_c/(0.265*self.beta**(8.0/3.0))
            self.N_K = Mw/MK

    def tandelta(self, omega, data):
        """Calculate the interpolated tan(delta)"""

        wGp = data[:,0]
        wGdp = data[:,0]
        Gp = data[:,1]
        Gdp = data[:,2]

        return (np.interp(omega,wGdp,Gdp)/np.interp(omega,wGp,Gp) - 1)
    
    def solveNc(self, x,  Gx, Mw, rho, R, T):
        """Function to solve for Nc from frequency crossover data (linear chains only)"""

        GxGN0 = [9.191488, 2336.3116, 14232.0515, 33.81303697, 13102.47993, 1068.7744]

        G0 = rho*R*T/(2*Mw)*(x-3) #from our definition of R, G0 will have units of kPa

        func = (GxGN0[0] + GxGN0[1]*(1/x) + GxGN0[2]*((1/x)**2))\
                    /(GxGN0[3] + GxGN0[4]*(1/x) + GxGN0[5]*((1/x)**2))

        return func*G0 - Gx/1000 #Gx has units of Pa


    def Gslfx(self,crossover_limits,data):
        """Function to find crossover frequency from limits"""

        sol = optimize.brentq(self.tandelta,crossover_limits[0],crossover_limits[1],args=(data))
        return sol, np.interp(sol,data[:,0],data[:,1])


    def find_crossover_limits(self,data):
        """Find the lower and upper limits of the crossover frequency"""

        omega = data[:,0]
        Gp = data[:,1]
        Gdp = data[:,2]

        for j in range(0,len(omega)):
            if Gdp[j]-Gp[j] < 0:
                if j<10:
                    ind1 = 0
                else:
                    ind1 = j-10
                if j+10>=len(omega):
                    ind2 = len(omega)-1
                else:
                    ind2 = j+10

                omega_range = [omega[ind1],omega[ind2]]
                    
                break

        return omega_range

    def set_linear_params(self, Nc):
        """Returns fixed parameters for calculating linear chain G* data"""

        alpha1 = [-0.00051, -0.0205]
        alpha2 = [0.00029, 0.109957]
        alpha3 = [17.69589, 1.04026, -0.00095677]
        tau1 = [0.6288876, 0.119458]
        tau2 = [1.52508156, 0.02996758796795]
        tau3 = [3.110954, 0.022615]
        tau4 = [3.4840295, 0.0142809]

        alpha = [alpha1[0]*Nc + alpha1[1], alpha2[0]*Nc + alpha2[1], \
                 alpha3[0]/Nc + alpha3[1] + alpha3[2]*Nc]
        tau = [tau1[1]*Nc**tau1[0], tau2[1]*Nc**tau2[0], \
               tau3[1]*Nc**tau3[0], tau4[1]*Nc**tau4[0]]

        alphaR = [0.64635, -0.4959, -1.2716]
        tauR = [6.313268381616272*(10**-9), 2.181509372282138*(10**-7), 0.797317365925168, 18.201382525250114]

        GR = 1942.29

        return [alpha, tau, alphaR, tauR, GR]
    
    def supp_prod(self, tau, alpha, i):
        """Returns the product operator used in the G* calculation"""
        result = 1
        for j in range (1, i+1):
            result *= tau[j]**(alpha[j - 1] - alpha[j])
    
        return result
   
    def Gstar(self, omega, params, Rouse=False):
        """Calculates G* using DSM or Rouse parameters"""

        if Rouse:
            alpha = params[2]
            tau = params[3]
            G0 = params[4]
        else:
            alpha = params[0]
            tau = params[1]
            G0 = params[5]

        sumGp1 = 0
        sumGp2 = 0
        sumGdp1 = 0
        sumGdp2 = 0
        for i in range(0, len(alpha)):

            sumGp1 += (self.supp_prod(tau,alpha,i)/(alpha[i]+2))*(tau[i+1]**(alpha[i]+2)*special.hyp2f1(1, (alpha[i]+2)/2, (alpha[i]+4)/2, -omega**2*tau[i+1]**2)\
                        - tau[i]**(alpha[i]+2)*special.hyp2f1(1, (alpha[i]+2)/2, (alpha[i]+4)/2, -omega**2*tau[i]**2))

            sumGp2 += self.supp_prod(tau,alpha,i)*(tau[i+1]**alpha[i] - tau[i]**alpha[i])/alpha[i]

            sumGdp1 += (self.supp_prod(tau,alpha,i)/(alpha[i]+1))*(tau[i+1]**(alpha[i]+1)*special.hyp2f1(1, (alpha[i]+1)/2, (alpha[i]+3)/2, -omega**2*tau[i+1]**2)\
                        - tau[i]**(alpha[i]+1)*special.hyp2f1(1, (alpha[i]+1)/2, (alpha[i]+3)/2, -omega**2*tau[i]**2))

            sumGdp2 += self.supp_prod(tau,alpha,i)*(tau[i+1]**alpha[i] - tau[i]**alpha[i])/alpha[i]

        return G0*omega**2*sumGp1/sumGp2 + 1j*(G0*omega*sumGdp1/sumGdp2) 


    def do_error(self, line):
        super().do_error(line)
        self.print_DSM_params()

    def print_DSM_params(self):
        """Print out parameters for DSM simulations"""

        Mc = self.parameters["Mc"].value
        tau_c = self.parameters["tau_c"].value
        beta = self.parameters["beta"].value
        tau_K = tau_c/(0.265*beta**(8.0/3.0))
        MK = self.parameters["MK"].value

        self.Qprint("<b>Additional DSM Parameters:</b>")
        tab_data = [['%-18s' % 'Name', '%-18s' % 'Value']]
        tab_data.append(['%-18s'%'<b>tau_K</b>', '%18.4g' % tau_K])
        self.Qprint(tab_data)

        tab_data = [['%-18s' % 'File', '%-18s' % 'NK', '%-18s' % 'Nc']]
        for f in self.theory_files():
            Mw = float(f.file_parameters["Mw"])*1000
            NK = Mw/MK
            Nc = Mw/Mc
            tab_data.append(['%-18s'% f.file_name_short, '%18.4g' % NK,  '%18.4g' % Nc])
        self.Qprint(tab_data)

    def calculate(self, f=None):
        """ 
        CLUSTERED FIXED SLIP-LINK (CFSM) + ROUSE MODEL FOR LINEAR VISCOELASTICITY

          PARAMETERS:
          > Mc    - molecular weight of cluster
          > Nc    - number of clusters
          > tau_c - time constant to compare CFSM results to experimental data
          > beta  - entanglement activity parameter for input to DSM simulations
          > NK    - number of Kuhn steps for input into DSM simulation
          > tau_K - time constant to compare DSM results to experimental data
        """

        #---------------------------------------------
        # FUNCTION INPUT
        ft = f.data_table
        tt = self.tables[f.file_name_short]
        tt.num_columns = ft.num_columns
        tt.num_rows = ft.num_rows
        tt.data = np.zeros((tt.num_rows, tt.num_columns))
        tt.data[:, 0] = ft.data[:, 0]

        MK = self.parameters["MK"].value
        rho0 = self.parameters["rho0"].value
        Mw = float(f.file_parameters["Mw"])*1000.0 #units of Da
        T = float(f.file_parameters["T"]) + 273.15 #units of K
        R = 8.314462*10**3 #units of L Pa K^-1 mol^-1

        Mc = self.parameters["Mc"].value
        tau_c = self.parameters["tau_c"].value
        beta = self.parameters["beta"].value
        Nc = Mw/Mc
        tau_K = tau_c/(0.265*beta**(8.0/3.0))
        N_K = Mw/MK
        # END FUNCTION INPUT
        #---------------------------------------------


        # #---------------------------------------------
        # # CALCULATE DSM PARAMETERS FROM CROSSOVER FREQUENCY
        # crossover_limits = self.find_crossover_limits(data=ft.data)
        # [omega_x, Gx] = self.Gslfx(crossover_limits,data=ft.data)
        # solNc = optimize.brentq(self.solveNc,a=1,b=1000,args=(Gx,Mw,rho0,R,T))
        # if solNc>0:
        #     self.Nc = solNc
        #     self.Mc = Mw/self.Nc
        # self.tau_c = 151.148/(omega_x*self.Nc**3.50)
        # self.beta = Mw/(0.56*self.Nc*MK) - 1
        # self.tau_K = self.tau_c/(0.265*self.beta**(8.0/3.0))
        # self.N_K = Mw/MK

        #- - - - - - - - - - - - - - - - - - - - - - -
        # CALCULATE CFSM AND HIGH FREQUENCY ROUSE RELAXATION MODULUS
        params=self.set_linear_params(Nc)

        G0 = rho0*R*T/Mw
        params.append(G0)

        Gstar_vec = np.vectorize(self.Gstar,excluded=['Rouse','params']) 

        CFSM = 0.5*(Nc-3)*Gstar_vec(omega=tt.data[:,0]*tau_c, params=params, Rouse=False)
        prefactor = G0*((N_K+beta)/(beta+1))
        Rouse = prefactor*Gstar_vec(omega=(tt.data[:,0]*tau_K*(beta**2)), params=params, Rouse=True)

        Gstar = CFSM + Rouse #G* has units of kPa

        tt.data[:,1] = Gstar.real*1000 #convert to Pa
        tt.data[:,2] = Gstar.imag*1000



class CLTheoryDSMLinear(BaseTheoryDSMLinear, Theory):
    """CL Version"""

    def __init__(self, name='', parent_dataset=None, axarr=None):
        """**Constructor**"""
        super().__init__(name, parent_dataset, axarr)

    # This class usually stays empty


class GUITheoryDSMLinear(BaseTheoryDSMLinear, QTheory):
    """GUI Version"""

    def __init__(self, name='', parent_dataset=None, axarr=None):
        """**Constructor**"""
        super().__init__(name, parent_dataset, axarr)

    # add widgets specific to the theory here:
