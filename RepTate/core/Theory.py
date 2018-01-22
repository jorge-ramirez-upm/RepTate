# RepTate: Rheology of Entangled Polymers: Toolkit for the Analysis of Theory and Experiments
# http://blogs.upm.es/compsoftmatter/software/reptate/
# https://github.com/jorge-ramirez-upm/RepTate
# http://reptate.readthedocs.io
# Jorge Ramirez, jorge.ramirez@upm.es
# Victor Boudara, mmvahb@leeds.ac.uk
# Copyright (2017) Universidad Politécnica de Madrid, University of Leeds
# This software is distributed under the GNU General Public License. 
"""Module Theory

Module that defines the basic structure and properties of a theory.

"""
import os
import enum
import time
import getpass
import numpy as np
from scipy.optimize import curve_fit
from scipy.stats.distributions import t

from CmdBase import CmdBase, CmdMode
from DataTable import DataTable
from Parameter import Parameter, ParameterType, OptType
from DraggableArtists import DraggableVLine, DraggableHLine, DragType
from PyQt5.QtGui import QTextCursor

from tabulate import tabulate


class Theory(CmdBase):
    """Abstract class to describe a theory
    
    [description]
    """
    thname=""
    """ thname {str} -- Theory name """
    description=""
    """ description {str} -- Description of theory """
    citations=""
    """ citations {str} -- Articles that should be cited """
    nfev = 0
    """ nfev {int} -- Number of function evaluations """    

    def __init__(self, name="Theory", parent_dataset=None, axarr=None):
        """Constructor
        
        The following variables should be set by the particular realization of the theory:
        parameters     (dict): Parameters of the theory
        function       (func): Function that calculates the theory
        min            (real): min for integration/calculation
        max            (real): max
        npoints         (int): Number of points to calculate
        point_distribution   : all_points, linear, log
        dt             (real): default time step
        dt_min         (real): minimum time step for adaptive algorithms
        eps            (real): precision for adaptive algorithms
        integration_method   : Euler, RungeKutta5, AdaptiveDt
        stop_steady    (bool): Stop calculation if steady state of component 0 is attained
        
        Keyword Arguments:
            name {str} -- Name of theory (default: {"Theory"})
            parent_dataset {DataSet} -- DataSet that contains the Theory (default: {None})
            ax {matplotlib axes} -- matplotlib graph (default: {None})
        """
        super(Theory, self).__init__() 
        self.name=name
        self.parent_dataset = parent_dataset
        self.axarr = axarr
        self.ax = axarr[0] #theory calculation only on this plot
        self.parameters={}
        self.tables={}
        self.function=None
        self.active = True #defines if the theorie is plotted
        self.calculate_is_busy = False
        

        # THEORY OPTIONS
        self.npoints=100
        self.dt=0.001
        self.dt_min=1e-6 
        self.eps=1e-4
        self.stop_steady=False
        self.is_fitting=False
        self.has_modes=False
        
        ax = self.ax
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
            self.tables[f.file_name_short] = DataTable(axarr, "TH-" + f.file_name_short)

        self.do_cite("")
            
    def precmd(self, line):
        """Calculations before the theory is calculated
        
        This function could be erased
        This method is called after the line has been input but before
        it has been interpreted. If you want to modifdy the input line
        before execution (for example, variable substitution) do it here.
        
        Arguments:
            line {[type]} -- [description]
        
        Returns:
            [type] -- [description]
        """
        super(Theory,self).precmd(line)
        return line

    def update_parameter_table(self):
        """
        Added so that Maxwell modes works in CL
        """
        pass
        
    def do_calculate(self, line, timing=True):
        """Calculate the theory"""
        if self.calculate_is_busy:
            return
        if not self.tables:
            return

        self.calculate_is_busy = True
        start_time = time.time()
        if self.single_file: #find the first active file in dataset
            if len(self.parent_dataset.inactive_files) == len(self.parent_dataset.files): #all files hidden
                self.function(self.parent_dataset.files[0])
            else: #find first visible file
                for f in self.parent_dataset.files:
                    if f.file_name_short not in self.parent_dataset.inactive_files:
                        self.function(f)
                        break
        else:
            for f in self.parent_dataset.files:
                self.function(f)
        if not self.is_fitting:
            self.do_plot(line)
            self.do_error(line)
        if timing:
            self.Qprint("")
            self.Qprint("---Calculated in %.3g seconds---" % (time.time() - start_time))
        self.calculate_is_busy = False

    def do_error(self, line):
        """Report the error of the current theory
        
        Report the error of the current theory on all the files, taking into account \
        the current selected xrange and yrange.\n\
        File error is calculated as the mean square of the residual, averaged over all points in the file.\n\
        Total error is the mean square of the residual, averaged over all points in all files.
        
        Arguments:
            line {[type]} -- [description]
        """
        total_error=0
        npoints=0
        view = self.parent_dataset.parent_application.current_view
        self.Qprint("")
        self.Qprint("%14s %10s (%6s)"%("File","Error","# Pts."))
        self.Qprint("==================================")
        for f in self.parent_dataset.files:
            if f.active:
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
                conditionnaninf=(~np.isnan(xexp))*(~np.isnan(yexp))*(~np.isnan(xth))*(~np.isnan(yth))*(~np.isinf(xexp))*(~np.isinf(yexp))*(~np.isinf(xth))*(~np.isinf(yth))
                yexp=np.extract(conditionx*conditiony*conditionnaninf, yexp)
                yth=np.extract(conditionx*conditiony*conditionnaninf, yth)
                f_error=np.mean((yth-yexp)**2)
                npt=len(yth)
                total_error+=f_error*npt
                npoints+=npt
                self.Qprint("%14s %10.5g (%6d)"%(f.file_name_short,f_error,npt))
        if npoints != 0:
            self.Qprint("%14s %10.5g (%6d)"%("TOTAL",total_error/npoints,npoints))
        else:
            self.Qprint("%14s %10s (%6d)"%("TOTAL", "N/A", npoints))

    def func_fit(self, x, *param_in):
        """[summary]
        
        [description]
        
        Arguments:
            x {[type]} -- [description]
            *param_in {[type]} -- [description]
        
        Returns:
            [type] -- [description]
        """
        ind=0
        k=list(self.parameters.keys())
        k.sort()
        for p in k:
            par = self.parameters[p] 
            if par.opt_type == OptType.opt: 
                par.value=param_in[ind]
                ind+=1
        self.do_calculate("", timing=False)
        y = []
        view = self.parent_dataset.parent_application.current_view
        for f in self.parent_dataset.files:
            if f.active:
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
                    conditionnaninf=(~np.isnan(xexp)[:,0])*(~np.isnan(yexp)[:,0])*(~np.isinf(xexp)[:,0])*(~np.isinf(yexp)[:,0])
                    ycond=np.extract(conditionx*conditiony*conditionnaninf, yth[:,i])
                    y = np.append(y, ycond)
        self.nfev += 1
        return y

    def do_fit(self, line):
        """Minimize the error
        
        [description]
        
        Arguments:
            line {[type]} -- [description]
        """
        if not self.tables:
            return
        if len(self.parent_dataset.inactive_files) == len(self.parent_dataset.files): #all files hidden
            return
        self.is_fitting = True
        start_time = time.time()
        view = self.parent_dataset.parent_application.current_view
        self.Qprint("")
        self.Qprint("==================================")
        self.Qprint("PARAMETER FITTING")
        self.Qprint("==================================")
        # Vectors that contain all X and Y in the files & view
        x = []
        y = []

        if self.xrange.get_visible():
            if self.xmin < self.xmax:
                self.Qprint("xrange=[%0.3g, %0.3g]"%(self.xmin, self.xmax))
            else:
                temp = self.xmin
                self.xmin = self.xmax
                self.xmax = xmin
        if self.yrange.get_visible():
            if self.ymin < self.ymax:
                self.Qprint("yrange=[%.03g, %0.3g]"%(self.ymin, self.ymax))
            else:
                temp = self.ymin
                self.ymin = self.ymax
                self.ymax = temp
                
        for f in self.parent_dataset.files:
            if f.active:
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
                    conditionnaninf=(~np.isnan(xexp)[:,0])*(~np.isnan(yexp)[:,0])*(~np.isinf(xexp)[:,0])*(~np.isinf(yexp)[:,0])
                    xcond=np.extract(conditionx*conditiony*conditionnaninf, xexp[:,i])
                    ycond=np.extract(conditionx*conditiony*conditionnaninf, yexp[:,i])

                    x = np.append(x, xcond)
                    y = np.append(y, ycond)      

        # Mount the vector of parameters (Active ones only)
        initial_guess = []
        param_min = []
        param_max = []
        k=list(self.parameters.keys())
        k.sort()
        for p in k:
            par = self.parameters[p] 
            if par.opt_type == OptType.opt:
                initial_guess.append(par.value)
                param_min.append(par.min_value) #list of min values for fitting parameters
                param_max.append(par.max_value) #list of max values for fitting parameters
        if (not param_min) or (not param_max):
            self.Qprint("No parameter to minimize")
            self.is_fitting = False
            return
        opt = dict(return_full=True)
        self.nfev = 0
        try:
            #pars, pcov, infodict, errmsg, ier = curve_fit(self.func_fit, x, y, p0=initial_guess, full_output=1) 
            pars, pcov = curve_fit(self.func_fit, x, y, p0=initial_guess, method='trf', bounds=(param_min, param_max))
            #bounded parameter space 'bound=(0, np.inf)' triggers scipy.optimize.least_squares instead of scipy.optimize.leastsq
        except Exception as e:
            print("In do_fit()", e)
            return

        residuals = y - self.func_fit(x, *initial_guess)
        fres0 = sum(residuals**2)
        residuals = y - self.func_fit(x, *pars)
        fres1 = sum(residuals**2)
        self.Qprint('Initial Error = %g -->'%(fres0))
        self.Qprint('Final Error   = %g'%(fres1))
        self.Qprint('%g function evaluations'%(self.nfev))
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
        self.Qprint("")
        self.Qprint("%9s = %10s ± %-9s"%("Parameter","Value","Error"))
        self.Qprint("==================================")
        for p in k:
            par = self.parameters[p] 
            if par.opt_type == OptType.opt:
                par.error=par_error[ind]
                ind+=1
                self.Qprint('%9s = %10.4g ± %-9.4g'%(par.name, par.value, par.error))
            else:
                self.Qprint('%9s = %10.4g'%(par.name, par.value))
        self.is_fitting=False
        self.do_calculate(line, timing=False)
        self.Qprint("")
        self.Qprint("---Fitting in %.3g seconds---" % (time.time() - start_time))


    def do_print(self, line):
        """Print the theory table associated with the given file name
        
        [description]
        
        Arguments:
            line {[type]} -- [description]
        """
        if line in self.tables:
            print(self.tables[line].data)
        else:
            print("Theory table for \"%s\" not found"%line)

    def complete_print(self, text, line, begidx, endidx):
        """[summary]
        
        [description]
        
        Arguments:
            text {[type]} -- [description]
            line {[type]} -- [description]
            begidx {[type]} -- [description]
            endidx {[type]} -- [description]
        
        Returns:
            [type] -- [description]
        """
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
        
        Several parameters are allowed
        With no arguments, show the current values
        
        Arguments:
            line {[type]} -- [description]
        """
        if (line==""):
            plist = list(self.parameters.keys())
            plist.sort()
            print("%9s   %10s (with * = is optimized)"%("Parameter","Value"))
            print("==================================")
            for p in plist:
                if self.parameters[p].opt_type == OptType.opt: 
                    print("*%8s = %10.5g"%(self.parameters[p].name,self.parameters[p].value))
                elif self.parameters[p].opt_type == OptType.nopt: 
                    print("%8s = %10.5g"%(self.parameters[p].name,self.parameters[p].value))
        else:
            for s in line.split():
                if (s in self.parameters):
                    if self.parameters[s].opt_type == OptType.opt:
                        self.parameters[s].opt_type == OptType.nopt
                    elif self.parameters[s].opt_type == OptType.nopt:
                        self.parameters[s].opt_type == OptType.opt
                else:
                    print("Parameter %s not found"%s)

    def complete_parameters(self, text, line, begidx, endidx):
        """[summary]
        
        [description]
        
        Arguments:
            text {[type]} -- [description]
            line {[type]} -- [description]
            begidx {[type]} -- [description]
            endidx {[type]} -- [description]
        
        Returns:
            [type] -- [description]
        """
        parameter_names=list(self.parameters.keys())
        if not text:
            completions = parameter_names[:]
        else:
            completions = [ f
                            for f in parameter_names
                            if f.startswith(text)
                            ]
        return completions

    def plot_theory_stuff(self):
        """[summary]
        
        [description]
        """
        pass

# SAVE THEORY STUFF
    def do_save(self, line):
        """Save the results from all theory predictions to file
        
        [description]
        
        Arguments:
            line {[type]} -- [description]
        """
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
        """[summary]
        
        [description]
        
        Arguments:
            dx {[type]} -- [description]
            dy {[type]} -- [description]
        """
        try:
            self.xmin+=dx                
            self.xminline.set_data([self.xmin,self.xmin],[0,1])
            self.xrange.set_xy([[self.xmin,0],[self.xmin,1],[self.xmax,1],[self.xmax,0],[self.xmin,0]])
        except:
            pass

    def change_xmax(self, dx, dy):
        """[summary]
        
        [description]
        
        Arguments:
            dx {[type]} -- [description]
            dy {[type]} -- [description]
        """
        try:
            self.xmax+=dx                
            self.xmaxline.set_data([self.xmax,self.xmax],[0,1])
            self.xrange.set_xy([[self.xmin,0],[self.xmin,1],[self.xmax,1],[self.xmax,0],[self.xmin,0]])
        except:
            pass

    def change_ymin(self, dx, dy):
        """[summary]
        
        [description]
        
        Arguments:
            dx {[type]} -- [description]
            dy {[type]} -- [description]
        """
        self.ymin+=dy     
        self.yminline.set_data([0, 1], [self.ymin, self.ymin])           
        self.yrange.set_xy([[0, self.ymin], [0, self.ymax], [1, self.ymax], [1 ,self.ymin], [0, self.ymin]])

    def change_ymax(self, dx, dy):
        """[summary]
        
        [description]
        
        Arguments:
            dx {[type]} -- [description]
            dy {[type]} -- [description]
        """
        self.ymax+=dy     
        self.ymaxline.set_data([0, 1], [self.ymax, self.ymax])           
        self.yrange.set_xy([[0, self.ymin], [0, self.ymax], [1, self.ymax], [1 ,self.ymin], [0, self.ymin]])

    def do_xrange(self, line):
        """Set/show xrange for fit and shows limits
        
        With no arguments: switches ON/OFF the horizontal span
        
        Arguments:
            line {[xmin xmax]} -- Sets the limits of the span
        """
        if (line==""):
            """.. todo:: Set range to current view limits"""
            self.xmin, self.xmax = self.ax.get_xlim()
            self.xminline.set_data([self.xmin,self.xmin],[0,1])
            self.xmaxline.set_data([self.xmax,self.xmax],[0,1])
            self.xrange.set_xy([[self.xmin,0],[self.xmin,1],[self.xmax,1],[self.xmax,0],[self.xmin,0]])
            self.xrange.set_visible(not self.xrange.get_visible()) 
            self.xminline.set_visible(not self.xminline.get_visible()) 
            self.xmaxline.set_visible(not self.xmaxline.get_visible()) 
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
        
        With no arguments: switches ON/OFF the vertical span
        
        Arguments:
            line {[ymin ymax]} -- Sets the limits of the span
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
        """[summary]
        
        [description]
        """
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
        """[summary]
        
        [description]
        
        Arguments:
            line {[type]} -- [description]
        """
        self.copy_modes()
    
    def get_modes(self):
        """[summary]
        
        [description]
        
        Returns:
            [type] -- [description]
        """
        tau=np.ones(1)
        G=np.ones(1)
        return tau, G
    
    def set_modes(self, tau, G):
        """[summary]
        
        [description]
        
        Arguments:
            tau {[type]} -- [description]
            G {[type]} -- [description]
        """
        pass

    def do_cite(self, line):
        """Print citation information
        
        [description]
        
        Arguments:
            line {[type]} -- [description]
        """
        print(self.citations)

    def do_plot(self, line):
        """Call the plot from the parent Dataset
        
        [description]
        
        Arguments:
            line {[type]} -- [description]
        """
        self.parent_dataset.do_plot(line)
        #self.plot_theory_stuff()

    def set_param_value(self, name, value):
        """[summary]
        
        [description]
        
        Arguments:
            name {[type]} -- [description]
            value {[type]} -- [description]

        Returns:
            Success{bool} -- True if the operation was successful
        """
        if (self.parameters[name].type==ParameterType.real):
            self.parameters[name].value=float(value)
            return True
        elif (self.parameters[name].type==ParameterType.integer):
            self.parameters[name].value=int(value)
            return True
        elif (self.parameters[name].type==ParameterType.discrete_integer):
            if int(value) in self.parameters[name].discrete_values:
                self.parameters[name].value=int(value)
                return True
            else:
                print("Values allowed=", self.parameters[name].discrete_values)
                return False
        elif (self.parameters[name].type==ParameterType.discrete_real):
            if float(value) in self.parameters[name].discrete_values:
                self.parameters[name].value=float(value)
                return True
            else:
                print("Values allowed=", self.parameters[name].discrete_values)
                return False
        elif (self.parameters[name].type==ParameterType.boolean):
            if value in [True, 'true', 'True', '1', 't', 'T', 'y', 'yes']:
                self.parameters[name].value=True
            else:
                self.parameters[name].value=False
        else:
            pass


    def default(self, line):
        """Called when the input command is not recognized
        
        Called on an input line when the command prefix is not recognized.
        Check if there is an = sign in the line. If so, it is a parameter change.
        Else, we execute the line as Python code.
        
        Arguments:
            line {[type]} -- [description]
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
    
    def do_hide(self):
        """[summary]
        
        [description]
        """
        self.active = False
        for table in self.tables.values():
            for i in range(table.MAX_NUM_SERIES):
                for nx in range(self.parent_dataset.nplots):
                    table.series[nx][i].set_visible(False)
        try:
            self.show_theory_extras(False)
        except: # current theory has no extras
            # print("current theory has no extras to hide")
            pass
    
    def set_th_table_visible(self, fname, state):
        """Show/Hide all theory lines related to the file "fname" """
        tt = self.tables[fname]
        for i in range(tt.MAX_NUM_SERIES):
            for nx in range(self.parent_dataset.nplots):
                tt.series[nx][i].set_visible(state)

    def do_show(self):
        """[summary]
        
        [description]
        """
        self.active = True
        for fname in self.tables:
            if fname in self.parent_dataset.inactive_files:
                return
            else:
                tt = self.tables[fname]
                for i in range(tt.MAX_NUM_SERIES):
                    for nx in range(self.parent_dataset.nplots):
                        tt.series[nx][i].set_visible(True)
        try:
            self.show_theory_extras(True)
        except: # current theory has no extras
            # print("current theory has no extras to show")
            pass
        self.parent_dataset.do_plot("")

    def Qprint(self, msg):
        """[summary]
        
        [description]
        
        Arguments:
            msg {[type]} -- [description]
        """
        if CmdBase.mode == CmdMode.GUI:
            self.thTextBox.append(msg)
            self.thTextBox.verticalScrollBar().setValue(self.thTextBox.verticalScrollBar().maximum())
            self.thTextBox.moveCursor(QTextCursor.End)
        else:
            print(msg)
