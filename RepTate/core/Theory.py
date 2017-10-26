import enum
import time
import getpass
from scipy.optimize import curve_fit
from scipy.stats.distributions import t

from CmdBase import *
from DataTable import *
from Parameter import *
from DraggableArtists import *

from tabulate import tabulate

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
        self.npoints=100
        self.dt=0.001
        self.dt_min=1e-6 
        self.eps=1e-4
        self.stop_steady=False
        self.fitting=False
        self.has_modes=False
        
        # XRANGE for FIT
        self.xmin=0.01
        self.xmax=1
        self.xrange = ax.axvspan(self.xmin, self.xmax, facecolor='yellow', alpha=0.3, visible=False)
        self.xminline = ax.axvline(self.xmin, color='black', linestyle='--', marker='o', visible=False)
        self.xmaxline = ax.axvline(self.xmax, color='black', linestyle='--', marker='o', visible=False)
        self.xminlinedrag=DraggableVLine(self.xminline, DragType.horizontal, self.change_xmin)
        self.xmaxlinedrag=DraggableVLine(self.xmaxline, DragType.horizontal, self.change_xmax)

        # YRANGE for FIT
        self.ymin=0.01
        self.ymax=1
        self.yrange = ax.axhspan(self.ymin, self.ymax, facecolor='pink', alpha=0.3, visible=False)
        self.yminline = ax.axhline(self.ymin, color='black', linestyle='--', marker='o', visible=False)
        self.ymaxline = ax.axhline(self.ymax, color='black', linestyle='--', marker='o', visible=False)
        self.yminlinedrag=DraggableHLine(self.yminline, DragType.vertical, self.change_ymin)
        self.ymaxlinedrag=DraggableHLine(self.ymaxline, DragType.vertical, self.change_ymax)
    
        # Pre-create as many tables as files in the dataset
        for f in parent_dataset.files:
            self.tables[f.file_name_short]=DataTable(ax)
            
        self.do_cite("")
            
    def precmd(self, line):
        """ 
        This method is called after the line has been input but before
        it has been interpreted. If you want to modifdy the input line
        before execution (for example, variable substitution) do it here.
        
        .. todo:: Substitute parameter values if symbol {param} is used
        """
        super(Theory,self).precmd(line)
        return line
        
    def do_calculate(self, line):
        """Calculate the theory"""
        for f in self.parent_dataset.files:
            self.function(f)
        if not self.fitting:
            self.do_plot(line)
            self.do_error(line)
    
    def do_error(self, line):
        """Report the error of the current theory on all the files, taking into account \
the current selected xrange and yrange.\n\
File error is calculated as the mean square of the residual, averaged over all points in the file.\n\
Total error is the mean square of the residual, averaged over all points in all files.
        """
        total_error=0
        npoints=0
        view = self.parent_dataset.parent_application.current_view
        print("%20s %10s (%10s)"%("File","Error","# Points"))
        print("=============================================")
        for f in self.parent_dataset.files:
            xexp, yexp, success = view.view_proc(f.data_table, f.file_parameters)
            xth, yth, success = view.view_proc(self.tables[f.file_name_short], f.file_parameters)
            if (self.xrange.get_visible()):
                conditionx=(xexp>self.xmin)*(xexp<self.xmax)
            else:
                conditionx=np.ones_like(xexp, dtype=np.bool)
            if (self.yrange.get_visible()):
                conditiony=(yexp>self.ymin)*(yexp<self.ymax)
            else:
                conditiony=np.ones_like(yexp, dtype=np.bool)
            yexp=np.extract(conditionx*conditiony, yexp)
            yth=np.extract(conditionx*conditiony, yth)
            f_error=np.mean((yth-yexp)**2)
            npt=len(yth)
            total_error+=f_error*npt
            npoints+=npt
            print("%20s %10.5g (%10d)"%(f.file_name_short,f_error,npt))
        print("%20s %10.5g (%10d)"%("TOTAL",total_error/npoints,npoints))

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
            xexp, yexp, success = view.view_proc(f.data_table, f.file_parameters)
            for i in range(view.n):
                if (self.xrange.get_visible()):
                    conditionx=(xexp[:,i]>self.xmin)*(xexp[:,i]<self.xmax)
                else:
                    conditionx=np.ones_like(xexp[:,i], dtype=np.bool)
                if (self.yrange.get_visible()):
                    conditiony=(yexp[:,i]>self.ymin)*(yexp[:,i]<self.ymax)
                else:
                    conditiony=np.ones_like(yexp[:,i], dtype=np.bool)
                ycond=np.extract(conditionx*conditiony, yth[:,i])
                y = np.append(y, ycond)
        return y

    def do_fit(self, line):
        """Minimize the error"""
        self.fitting = True
        view = self.parent_dataset.parent_application.current_view
        # Vectors that contain all X and Y in the files & view
        x = []
        y = []
        for f in self.parent_dataset.files:
            xexp, yexp, success = view.view_proc(f.data_table, f.file_parameters)
            for i in range(view.n):   
                if (self.xrange.get_visible()):
                    conditionx=(xexp[:,i]>self.xmin)*(xexp[:,i]<self.xmax)
                else:
                    conditionx=np.ones_like(xexp[:,i], dtype=np.bool)
                if (self.yrange.get_visible()):
                    conditiony=(yexp[:,i]>self.ymin)*(yexp[:,i]<self.ymax)
                else:
                    conditiony=np.ones_like(yexp[:,i], dtype=np.bool)
                xcond=np.extract(conditionx*conditiony, xexp[:,i])
                ycond=np.extract(conditionx*conditiony, yexp[:,i])

                x = np.append(x, xcond)
                y = np.append(y, ycond)      

        # Mount the vector of parameters (Active ones only)
        initial_guess = []
        param_min = []
        param_max = []
        for p in self.parameters.keys():
            par = self.parameters[p] 
            if par.min_flag: 
                initial_guess.append(par.value)
                param_min.append(par.min_value) #list of min values for fitting parameters
                param_max.append(par.max_value) #list of max values for fitting parameters

        opt = dict(return_full=True)
        try:
            #pars, pcov, infodict, errmsg, ier = curve_fit(self.func_fit, x, y, p0=initial_guess, full_output=1) 
            pars, pcov = curve_fit(self.func_fit, x, y, p0=initial_guess, method='trf', bounds=(param_min, param_max))
            #bounded parameter space 'bound=(0, np.inf)' triggers scipy.optimize.least_squares instead of scipy.optimize.leastsq
        except RuntimeError as e:
            print(e)
            return

        residuals = y - self.func_fit(x, *initial_guess)
        fres0 = sum(residuals**2)
        residuals = y - self.func_fit(x, *pars)
        fres1 = sum(residuals**2)
        print('Initial Error = %g --> Final Error = %g'%(fres0, fres1))

        # fiterror = np.mean((infodict['fvec'])**2)
        # funcev = infodict['nfev']
        # print("Solution found with %d function evaluations and error %g"%(funcev,fiterror))

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

        ind=0
        k=list(self.parameters.keys())
        k.sort()
        print("%10s   %10s +/- %10s (if it was optimized)"%("Parameter","Value","Error"))
        print("=============================================")
        for p in k:
            par = self.parameters[p] 
            if par.min_flag:
                par.error=par_error[ind]
                ind+=1
                print('%10s = %10.5g +/- %10.5g'%(par.name, par.value, par.error))
            else:
                print('%10s = %10.5g'%(par.name, par.value))
        self.fitting=False
        self.do_calculate(line)

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
        """View and switch the minimization state of the theory parameters
           parameters A B
           With no arguments, show the current values
        """
        if (line==""):
            plist = list(self.parameters.keys())
            plist.sort()
            print("%10s   %10s (with * = is optimized)"%("Parameter","Value"))
            print("=============================================")
            for p in plist:
                if self.parameters[p].min_flag: 
                    print("*%9s = %10.5g"%(self.parameters[p].name,self.parameters[p].value))
                else: 
                    print("%10s = %10.5g"%(self.parameters[p].name,self.parameters[p].value))
        else:
            for s in line.split():
                if (s in self.parameters):
                    self.parameters[s].min_flag=not self.parameters[s].min_flag
                else:
                    print("Parameter %s not found"%s)

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

# SAVE THEORY STUFF
    def do_save(self, line):
        """Save the results from all theory predictions to file"""
        print('Saving prediction of '+self.thname+' theory')
        for f in self.parent_dataset.files:
            fparam=f.file_parameters
            ttable=self.tables[f.file_name_short]
            ofilename=os.path.splitext(f.file_full_path)[0]+'_TH'+os.path.splitext(f.file_full_path)[1]
            print('File: '+f.file_name_short)
            fout=open(ofilename, 'w')
            k = list(f.file_parameters.keys())
            k.sort()
            for i in k:            
                fout.write(i + "=" + str(f.file_parameters[i])+ ";")
            fout.write('\n')
            fout.write('# Prediction of '+self.thname+' Theory\n')
            fout.write('# ')
            k = list(self.parameters.keys())
            k.sort()
            for i in k:
                fout.write(i + '=' + str(self.parameters[i].value) + '; ')
            fout.write('\n')
            fout.write('# Date: '+ time.strftime("%Y-%m-%d %H:%M:%S") + ' - User: ' + getpass.getuser() + '\n')
            k = f.file_type.col_names
            for i in k: 
                fout.write(i+'\t')
            fout.write('\n')
            for i in range(ttable.num_rows):
                for j in range(ttable.num_columns):
                    fout.write(str(ttable.data[i, j])+'\t')
                fout.write('\n')
            fout.close()


# SPAN STUFF
    def change_xmin(self, dx, dy):
        self.xmin+=dx                
        self.xminline.set_data([self.xmin,self.xmin],[0,1])
        self.xrange.set_xy([[self.xmin,0],[self.xmin,1],[self.xmax,1],[self.xmax,0],[self.xmin,0]])

    def change_xmax(self, dx, dy):
        self.xmax+=dx                
        self.xmaxline.set_data([self.xmax,self.xmax],[0,1])
        self.xrange.set_xy([[self.xmin,0],[self.xmin,1],[self.xmax,1],[self.xmax,0],[self.xmin,0]])

    def change_ymin(self, dx, dy):
        self.ymin+=dy     
        self.yminline.set_data([0, 1], [self.ymin, self.ymin])           
        self.yrange.set_xy([[0, self.ymin], [0, self.ymax], [1, self.ymax], [1 ,self.ymin], [0, self.ymin]])

    def change_ymax(self, dx, dy):
        self.ymax+=dy     
        self.ymaxline.set_data([0, 1], [self.ymax, self.ymax])           
        self.yrange.set_xy([[0, self.ymin], [0, self.ymax], [1, self.ymax], [1 ,self.ymin], [0, self.ymin]])

    def do_xrange(self, line):
        """Set/show xrange for fit and shows limits
           xrange  : switches ON/OFF the horizontal span
           xrange xmin xmax : Sets the limits of the span
        """
        if (line==""):
            self.xrange.set_visible(not self.xrange.get_visible()) 
            self.xminline.set_visible(not self.xminline.get_visible()) 
            self.xmaxline.set_visible(not self.xmaxline.get_visible()) 
            print("Xmin=%g Xmax=%g"%(self.xmin,self.xmax))
        else:
            items=line.split()
            if len(items)<2:
                print ("Not enough parameters")
            else:
                self.xmin=float(items[0])
                self.xmax=float(items[1])
                self.xminline.set_data([self.xmin,self.xmin],[0,1])
                self.xmaxline.set_data([self.xmax,self.xmax],[0,1])
                self.xrange.set_xy([[self.xmin,0],[self.xmin,1],[self.xmax,1],[self.xmax,0],[self.xmin,0]])
                if (not self.xrange.get_visible()):
                    self.xrange.set_visible(True) 
                    self.xminline.set_visible(True) 
                    self.xmaxline.set_visible(True) 
        self.do_plot(line)
            
    def do_yrange(self, line):
        """Set/show yrange for fit and shows limits
           yrange  : switches ON/OFF the vertical span
           yrange ymin ymax : Sets the limits of the span
        """
        if (line==""):
            self.yrange.set_visible(not self.yrange.get_visible()) 
            self.yminline.set_visible(not self.yminline.get_visible()) 
            self.ymaxline.set_visible(not self.ymaxline.get_visible()) 
            print("Ymin=%g Ymax=%g"%(self.ymin,self.ymax))
        else:
            items=line.split()
            if len(items)<2:
                print ("Not enough parameters")
            else:
                self.ymin=float(items[0])
                self.ymax=float(items[1])
                self.yminline.set_data([0, 1], [self.ymin, self.ymin])
                self.ymaxline.set_data([0, 1], [self.ymax, self.ymax])
                self.yrange.set_xy([[0, self.ymin], [0, self.ymax], [1, self.ymax], [1 ,self.ymin], [0, self.ymin]])
                if (not self.yrange.get_visible()):
                    self.yrange.set_visible(True) 
                    self.yminline.set_visible(True) 
                    self.ymaxline.set_visible(True) 
        self.do_plot(line)


# MODES STUFF
    def copy_modes(self):
        apmng=self.parent_dataset.parent_application.parent_manager
        L=apmng.list_theories_Maxwell()
        print("Found %d theories that provide modes"%len(L))
        for i, k in enumerate(L.keys()):
            print("%d: %s"%(i,k))
            print(tabulate([L[k][0][0],L[k][0][1]],tablefmt="grid"))
            print("")
        opt=int(input("Select theory (number between 0 and %d> "%(len(L)-1)))
        if (opt<0 or opt>=len(L)):
            print("Invalid option!")
        else:
            tt=L[list(L.keys())[opt]][0]
            self.set_modes(tt[0],tt[1])
    
    def do_copy_modes(self, line):
        self.copy_modes()
    
    def get_modes(self):
        tau=np.ones(1)
        G=np.ones(1)
        return tau, G
    
    def set_modes(self, tau, G):
        pass

    def do_cite(self, line):
        """Print citation information"""
        print(self.citations)

    def do_plot(self, line):
        """Call the plot from the parent Dataset"""
        self.parent_dataset.do_plot(line)

    def set_param_value(self, name, value):
        if (self.parameters[name].type==ParameterType.real):
            self.parameters[name].value=float(value)
        elif (self.parameters[name].type==ParameterType.integer):
            self.parameters[name].value=int(value)
        elif (self.parameters[name].type==ParameterType.discrete):
            pass
        else:
            pass

    def default(self, line):       
        """Called on an input line when the command prefix is not recognized.
           Check if there is an = sign in the line. If so, it is a parameter change.
           Else, we execute the line as Python code.
        """
        if "=" in line:
            par=line.split("=")
            if (par[0] in self.parameters):
                self.set_param_value(par[0],par[1])
            else:
                print("Parameter %s not found"%par[0])
        elif line in self.parameters.keys():
            print(self.parameters[line])
            print(self.parameters[line].__repr__())
        else:
            super(Theory, self).default(line)
