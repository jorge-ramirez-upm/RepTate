import enum
from scipy.optimize import curve_fit
from scipy.stats.distributions import t

from CmdBase import *
from DataTable import *
from Parameter import *

class Theory(CmdBase):
    """Abstract class to describe a theory
            thname            (str): Theory name
            description     (str): Description of theory
    """
    thname=""
    description=""
    citations=""

    def __init__(self, name="Theory", parent_dataset=None, ax=None):
        """Constructor:
        Args:
            name            (str): Name used internally by the dataset
            type           (enum): Type of theory (point, line, user)
            parameters     (dict): Parameters of the theory
            point_function (func): Calculation for point theory
            line_function  (func): Calculation for line theory
            user_function  (func): Calculation for user theory
            citations       (str): Articles that should be cited
       Theory Options:
            min            (real): min for integration/calculation
            max            (real): max
            npoints         (int): Number of points to calculate
            point_distribution   : all_points, linear, log
            dt             (real): default time step
            dt_min         (real): minimum time step for adaptive algorithms
            eps            (real): precision for adaptive algorithms
            integration_method   : Euler, RungeKutta5, AdaptiveDt
            stop_steady    (bool): Stop calculation if steady state of component 0 is attained
        """
        super(Theory, self).__init__() 
        self.name=name
        self.parent_dataset = parent_dataset
        self.ax = ax
        self.parameters={}
        self.tables={}
        self.function=None

        # THEORY OPTIONS
        self.min=0.01
        self.max=1
        self.npoints=100
        self.dt=0.001
        self.dt_min=1e-6 
        self.eps=1e-4
        self.stop_steady=False
        
        self.xspan = ax.axvspan(self.min, self.max, facecolor='yellow', alpha=0.5)
        self.xminline = ax.axvline(self.min, color='black', linestyle='--', marker='o')
        self.xmaxline = ax.axvline(self.max, color='black', linestyle='--', marker='o')
        #self.xminline.visible = False # DOESN'T WORK

        # Pre-create as many tables as files in the dataset
        for f in parent_dataset.files:
            self.tables[f.file_name_short]=DataTable(ax)
            
        self.do_cite("")
            
    def precmd(self, line):
        """ This method is called after the line has been input but before
            it has been interpreted. If you want to modifdy the input line
            before execution (for example, variable substitution) do it here.
            TODO: Substitute parameter values if symbol {param} is used
        """
        super(Theory,self).precmd(line)
        return line
        
    def do_calculate(self, line):
        """Calculate the theory"""
        for f in self.parent_dataset.files:
            self.function(f)
    
    def do_error(self, line):
        """Report the error of the current theory on the given filename
           The error is calculated with least-squares
        """
        total_error=0
        view = self.parent_dataset.parent_application.current_view
        for f in self.parent_dataset.files:
            xexp, yexp, success = view.view_proc(f.data_table, f.file_parameters)
            xth, yth, success = view.view_proc(self.tables[f.file_name_short], f.file_parameters)
            f_error=np.mean((yth-yexp)**2)
            total_error+=f_error
            print("%s\t%g"%(f.file_name_short,f_error))
        print("TOTAL\t%g"%total_error)

    def func_fit(self, x, *param_in):
        ind=0
        for p in self.parameters.keys():
            par = self.parameters[p] 
            if par.min_flag: 
                par.value=param_in[ind]
                ind+=1
        self.do_calculate("")
        y = []
        view = self.parent_dataset.parent_application.current_view
        for f in self.parent_dataset.files:
            xth, yth, success = view.view_proc(self.tables[f.file_name_short], f.file_parameters)
            for i in range(view.n):
                y = np.append(y, yth[:,i])
        return y

    def do_fit(self, line):
        """Minimize the error"""
        view = self.parent_dataset.parent_application.current_view
        # Vectors that contain all X and Y in the files & view
        x = []
        y = []
        for f in self.parent_dataset.files:
            xexp, yexp, success = view.view_proc(f.data_table, f.file_parameters)
            for i in range(view.n):
                x = np.append(x, xexp[:,i])
                y = np.append(y, yexp[:,i])      

        # Mount the vector of parameters (Active ones only)
        initial_guess=[]
        for p in self.parameters.keys():
            par = self.parameters[p] 
            if par.min_flag: 
                initial_guess.append(par.value)

        pars, pcov = curve_fit(self.func_fit, x, y, p0=initial_guess)

        alpha = 0.05 # 95% confidence interval = 100*(1-alpha)
        n = len(y)    # number of data points
        p = len(pars) # number of parameters
        dof = max(0, n - p) # number of degrees of freedom
        # student-t value for the dof and confidence level
        tval = t.ppf(1.0-alpha/2., dof) 

        par_error=[]
        #for i, p, var in zip(range(p), pars, np.diag(pcov)):
        for var in np.diag(pcov):
            sigma = var**0.5
            par_error.append(sigma*tval)
            #print ('p{0}: {1} ± {2}'.format(i, p, sigma*tval))

        ind=0
        for p in self.parameters.keys():
            par = self.parameters[p] 
            if par.min_flag:
                par.error=par_error[ind]
                ind+=1
                print('{0} = {1} ± {2}'.format(par.name, par.value, par.error))

    def do_print(self, line):
        """Print the theory table associated with the given file name"""
        if line in self.tables:
            print(self.tables[line].data)
        else:
            print("Theory table for \"%s\" not found"%line)

    def complete_print(self, text, line, begidx, endidx):
        file_names=list(self.tables.keys())
        if not text:
            completions = file_names[:]
        else:
            completions = [ f
                            for f in file_names
                            if f.startswith(text)
                            ]
        return completions
        
    def do_parameters(self, line):
        """View and/or change the values of the theory parameters
           parameters A=0.4 B=0.3
           With no arguments, show the current values
        """
        if (line==""):
            for p in self.parameters.keys():
                print("%s=%g"%(self.parameters[p].name,self.parameters[p].value))
        else:
            for s in line.split():
                par=s.split("=")
                if (par[0] in self.parameters):
                    self.parameters[par[0]].value=float(par[1])
                else:
                    print("Parameter %s not found"%par[0])

    def complete_parameters(self, text, line, begidx, endidx):
        parameter_names=list(self.parameters.keys())
        if not text:
            completions = parameter_names[:]
        else:
            completions = [ f
                            for f in parameter_names
                            if f.startswith(text)
                            ]
        return completions
        
    def do_cite(self, line):
        """Print citation information"""
        print(self.citations)

    def do_plot(self, line):
        """Call the plot from the parent Dataset"""
        self.parent_dataset.do_plot(line)

    def default(self, line):       
        """Called on an input line when the command prefix is not recognized.
           In that case we execute the line as Python code.
        """
        if "=" in line:
            par=line.split("=")
            if (par[0] in self.parameters):
                self.parameters[par[0]].value=float(par[1])
            else:
                print("Parameter %s not found"%par[0])
        elif line in self.parameters.keys():
            print(self.parameters[line])
            print(self.parameters[line].__repr__())
        else:
            super(Theory, self).default(line)
