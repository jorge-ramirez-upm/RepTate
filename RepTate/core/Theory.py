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
from PyQt5.QtCore import pyqtSignal

from collections import OrderedDict
from math import log

class EndComputationRequested(Exception):
    """Exception class to end computations"""
    pass

class Theory(CmdBase):
    """Abstract class to describe a theory
    
    [description]
    """
    thname = ""
    """ thname {str} -- Theory name """
    description = ""
    """ description {str} -- Description of theory """
    citations = ""
    """ citations {str} -- Articles that should be cited """
    doi = ""
    """ doicode {str} -- Doi code of the article """
    nfev = 0
    """ nfev {int} -- Number of function evaluations """

    print_signal = pyqtSignal(str)

    def __init__(self, name="Theory", parent_dataset=None, axarr=None):
        """
        **Constructor**
        
        The following variables should be set by the particular realization of the theory:
            - parameters     (dict): Parameters of the theory
            - function       (func): Function that calculates the theory
            - min            (real): min for integration/calculation
            - max            (real): max
            - npoints         (int): Number of points to calculate
            - point_distribution   : all_points, linear, log
            - dt             (real): default time step
            - dt_min         (real): minimum time step for adaptive algorithms
            - eps            (real): precision for adaptive algorithms
            - integration_method   : Euler, RungeKutta5, AdaptiveDt
            - stop_steady    (bool): Stop calculation if steady state of component 0 is attained
        
        Keyword Arguments:
            - name {str} -- Name of theory (default: {"Theory"})
            - parent_dataset {DataSet} -- DataSet that contains the Theory (default: {None})
            - ax {matplotlib axes} -- matplotlib graph (default: {None})
        """
        super().__init__()

        self.name = name
        self.parent_dataset = parent_dataset
        self.axarr = axarr
        self.ax = axarr[0]  #theory calculation only on this plot
        self.parameters = OrderedDict(
        )  # keep the dictionary key in order for the parameter table
        self.tables = {}
        self.function = None
        self.active = True  #defines if the theorie is plotted
        self.calculate_is_busy = False
        self.axarr[0].autoscale(False)
        self.autocalculate = True

        # THEORY OPTIONS
        self.npoints = 100
        self.dt = 0.001
        self.dt_min = 1e-6
        self.eps = 1e-4
        self.stop_steady = False
        self.is_fitting = False
        self.has_modes = False

        ax = self.ax

        # XRANGE for FIT
        self.xmin = 0.01
        self.xmax = 1
        self.xrange = ax.axvspan(
            self.xmin, self.xmax, facecolor='yellow', alpha=0.3, visible=False)
        self.xminline = ax.axvline(
            self.xmin,
            color='black',
            linestyle='--',
            marker='o',
            visible=False)
        self.xmaxline = ax.axvline(
            self.xmax,
            color='black',
            linestyle='--',
            marker='o',
            visible=False)
        self.xminlinedrag = DraggableVLine(self.xminline, DragType.horizontal,
                                           self.change_xmin, self)
        self.xmaxlinedrag = DraggableVLine(self.xmaxline, DragType.horizontal,
                                           self.change_xmax, self)
        self.is_xrange_visible = False

        # YRANGE for FIT
        self.ymin = 0.01
        self.ymax = 1
        self.yrange = ax.axhspan(
            self.ymin, self.ymax, facecolor='pink', alpha=0.3, visible=False)
        self.yminline = ax.axhline(
            self.ymin,
            color='black',
            linestyle='--',
            marker='o',
            visible=False)
        self.ymaxline = ax.axhline(
            self.ymax,
            color='black',
            linestyle='--',
            marker='o',
            visible=False)
        self.yminlinedrag = DraggableHLine(self.yminline, DragType.vertical,
                                           self.change_ymin, self)
        self.ymaxlinedrag = DraggableHLine(self.ymaxline, DragType.vertical,
                                           self.change_ymax, self)
        self.is_yrange_visible = False

        # Pre-create as many tables as files in the dataset
        for f in parent_dataset.files:
            self.tables[f.file_name_short] = DataTable(
                axarr, "TH-" + f.file_name_short)
            #initiallize theory table: important for 'single_file' theories
            ft = f.data_table
            tt = self.tables[f.file_name_short]
            tt.num_columns = ft.num_columns
            tt.num_rows = ft.num_rows
            tt.data = np.zeros((tt.num_rows, tt.num_columns))

        self.do_cite("")

        if CmdBase.mode == CmdMode.GUI:
            self.print_signal.connect(self.print_qtextbox)  # Asynchronous print when using multithread
        # flag for requesting end of computations
        self.stop_theory_flag = False

    def precmd(self, line):
        """Calculations before the theory is calculated
        
        This function could be erased
        This method is called after the line has been input but before
        it has been interpreted. If you want to modifdy the input line
        before execution (for example, variable substitution) do it here.
        
        Arguments:
            - line {[type]} -- [description]
        
        Returns:
            - [type] -- [description]
        """
        super(Theory, self).precmd(line)
        return line

    def update_parameter_table(self):
        """
        Added so that Maxwell modes works in CL
        """
        pass
    def handle_actionCalculate_Theory(self):
        """Used only in non GUI mode"""
        self.do_calculate("")

    def request_stop_computations(self):
        """Called when user wants to terminate the current computation"""
        self.Qprint("Stop current calculation requested")
        self.stop_theory_flag = True

    def do_calculate(self, line, timing=True):
        """Calculate the theory"""
        if self.calculate_is_busy:
            return
        if not self.tables:
            return

        self.calculate_is_busy = True
        self.start_time_cal = time.time()
        for f in self.theory_files():
            self.function(f)
        if not self.is_fitting:
            self.do_plot(line)
            self.do_error(line)
        if timing:
            self.Qprint('''<i>---Calculated in %.3g seconds---</i><br>''' % (time.time() - self.start_time_cal))
            self.do_cite("")
        self.calculate_is_busy = False

    def theory_files(self):
        if not self.single_file:
            return self.parent_dataset.files
        f_list = []
        selected_file = self.parent_dataset.selected_file
        if selected_file:
            if selected_file.active:
                f_list.append(self.parent_dataset.selected_file
                              )  #use the selected/highlighted file if active
        if not f_list:  #there is no selected file or it is inactive
            for f in self.parent_dataset.files:
                if f.active:
                    f_list.append(f)
                    break
        return f_list

    def do_error(self, line):
        """Report the error of the current theory
        
        Report the error of the current theory on all the files, taking into account
        the current selected xrange and yrange.

        File error is calculated as the mean square of the residual, averaged over all points in the file.
        Total error is the mean square of the residual, averaged over all points in all files.
        
        Arguments:
            - line {[type]} -- [description]
        """
        total_error = 0
        npoints = 0
        view = self.parent_dataset.parent_application.current_view
        tools = self.parent_dataset.parent_application.tools       
        table='''<table border="1" width="100%">'''
        table+='''<tr><th>File</th><th>Error (RSS)</th><th># Pts</th></tr>'''
        #msg = "\n%14s %10s (%5s)\n" % ("File", "Err (RSS)", "# Pts")
        #msg += "=================================="
        #self.Qprint(msg)

        for f in self.theory_files():
            xexp, yexp, success = view.view_proc(f.data_table,
                                                 f.file_parameters)
            xth, yth, success = view.view_proc(self.tables[f.file_name_short],
                                               f.file_parameters)
            if (self.xrange.get_visible()):
                conditionx = (xexp > self.xmin) * (xexp < self.xmax)
            else:
                conditionx = np.ones_like(xexp, dtype=np.bool)
            if (self.yrange.get_visible()):
                conditiony = (yexp > self.ymin) * (yexp < self.ymax)
            else:
                conditiony = np.ones_like(yexp, dtype=np.bool)
            conditionnaninf = (~np.isnan(xexp)) * (~np.isnan(yexp)) * (
                ~np.isnan(xth)) * (~np.isnan(yth)) * (~np.isinf(xexp)) * (
                    ~np.isinf(yexp)) * (~np.isinf(xth)) * (~np.isinf(yth))
            yexp = np.extract(conditionx * conditiony * conditionnaninf, yexp)
            yth = np.extract(conditionx * conditiony * conditionnaninf, yth)
            f_error = np.mean((yth - yexp)**2)
            npt = len(yth)
            total_error += f_error * npt
            npoints += npt
            #self.Qprint("%.14s %10.4g (%5d)" % (f.file_name_short, f_error, npt))
            table+= '''<tr><td>%14s</td><td>%10.4g</td><td>%5d</td></tr>'''% (f.file_name_short, f_error, npt)
        table+='''</table><br>'''
        self.Qprint(table)

        #count number of fitting parameters
        free_p = 0
        for p in self.parameters.values():
            if p.opt_type == OptType.opt:
                free_p += 1

        if npoints != 0:
            self.Qprint("<b>TOTAL ERROR</b>: %12.5g (%6d)" % (total_error / npoints, npoints))
            # Bayesian information criterion (BIC) penalise free parametters (overfitting)
            # Model with lowest BIC number is prefered
            self.Qprint("<b>Bayesian IC</b>: %12.5g<br>" % (npoints * log(total_error / npoints) + free_p * log(npoints)))
        else:
            self.Qprint("<b>TOTAL ERROR</b>: %12s (%6d)<br>" % ("N/A", npoints))

    def func_fit(self, x, *param_in):
        """[summary]
        
        [description]
        
        Arguments:
            - x {[type]} -- [description]
            - \*param_in {[type]} -- [description]
        
        Returns:
            - [type] -- [description]
        """
        ind = 0
        k = list(self.parameters.keys())
        k.sort()
        for p in k:
            par = self.parameters[p]
            if par.opt_type == OptType.opt:
                par.value = param_in[ind]
                ind += 1
        self.do_calculate("", timing=False)
        y = []
        view = self.parent_dataset.parent_application.current_view

        for f in self.theory_files():
            if f.active:
                xth, yth, success = view.view_proc(
                    self.tables[f.file_name_short], f.file_parameters)
                xexp, yexp, success = view.view_proc(f.data_table,
                                                     f.file_parameters)
                for i in range(view.n):
                    if (self.xrange.get_visible()):
                        conditionx = (xexp[:, i] > self.xmin) * (
                            xexp[:, i] < self.xmax)
                    else:
                        conditionx = np.ones_like(xexp[:, i], dtype=np.bool)
                    if (self.yrange.get_visible()):
                        conditiony = (yexp[:, i] > self.ymin) * (
                            yexp[:, i] < self.ymax)
                    else:
                        conditiony = np.ones_like(yexp[:, i], dtype=np.bool)
                    conditionnaninf = (~np.isnan(xexp)[:, 0]) * (
                        ~np.isnan(yexp)[:, 0]) * (~np.isinf(xexp)[:, 0]) * (
                            ~np.isinf(yexp)[:, 0])
                    ycond = np.extract(
                        conditionx * conditiony * conditionnaninf, yth[:, i])
                    y = np.append(y, ycond)
        self.nfev += 1
        return y

    def do_fit(self, line):
        """Minimize the error
        
        [description]
        
        Arguments:
            - line {[type]} -- [description]
        """
        if not self.tables:
            self.is_fitting = False
            return
        if len(self.parent_dataset.inactive_files) == len(
                self.parent_dataset.files):  #all files hidden
            self.is_fitting = False
            return
        th_files = self.theory_files()
        if not th_files:
            self.is_fitting = False
            return

        self.is_fitting = True
        start_time = time.time()
        view = self.parent_dataset.parent_application.current_view
        self.Qprint('''<h2>Parameter Fitting</h2>''')
        # Vectors that contain all X and Y in the files & view
        x = []
        y = []

        if self.xrange.get_visible():
            if self.xmin > self.xmax:
                temp = self.xmin
                self.xmin = self.xmax
                self.xmax = temp
            self.Qprint("<b>xrange</b>=[%0.3g, %0.3g]" % (self.xmin, self.xmax))
        if self.yrange.get_visible():
            if self.ymin > self.ymax:
                temp = self.ymin
                self.ymin = self.ymax
                self.ymax = temp
            self.Qprint("<b>yrange</b>=[%.03g, %0.3g]" % (self.ymin, self.ymax))

        for f in th_files:
            if f.active:
                xexp, yexp, success = view.view_proc(f.data_table,
                                                     f.file_parameters)
                for i in range(view.n):
                    if (self.xrange.get_visible()):
                        conditionx = (xexp[:, i] > self.xmin) * (
                            xexp[:, i] < self.xmax)
                    else:
                        conditionx = np.ones_like(xexp[:, i], dtype=np.bool)
                    if (self.yrange.get_visible()):
                        conditiony = (yexp[:, i] > self.ymin) * (
                            yexp[:, i] < self.ymax)
                    else:
                        conditiony = np.ones_like(yexp[:, i], dtype=np.bool)
                    conditionnaninf = (~np.isnan(xexp)[:, 0]) * (
                        ~np.isnan(yexp)[:, 0]) * (~np.isinf(xexp)[:, 0]) * (
                            ~np.isinf(yexp)[:, 0])
                    xcond = np.extract(
                        conditionx * conditiony * conditionnaninf, xexp[:, i])
                    ycond = np.extract(
                        conditionx * conditiony * conditionnaninf, yexp[:, i])

                    x = np.append(x, xcond)
                    y = np.append(y, ycond)

        # Mount the vector of parameters (Active ones only)
        initial_guess = []
        param_min = []
        param_max = []
        k = list(self.parameters.keys())
        k.sort()
        for p in k:
            par = self.parameters[p]
            if par.opt_type == OptType.opt:
                initial_guess.append(par.value)
                param_min.append(
                    par.min_value)  #list of min values for fitting parameters
                param_max.append(
                    par.max_value)  #list of max values for fitting parameters
        if (not param_min) or (not param_max):
            self.Qprint("No parameter to minimize")
            self.is_fitting = False
            return
        opt = dict(return_full=True)
        self.nfev = 0
        try:
            #pars, pcov, infodict, errmsg, ier = curve_fit(self.func_fit, x, y, p0=initial_guess, full_output=1)
            pars, pcov = curve_fit(
                self.func_fit,
                x,
                y,
                p0=initial_guess,
                bounds=(param_min, param_max),
                method='trf')
            #bounded parameter space 'bound=(0, np.inf)' triggers scipy.optimize.least_squares instead of scipy.optimize.leastsq
        except Exception as e:
            print("In do_fit()", e)
            self.Qprint("%s" % e)
            self.is_fitting = False
            return

        residuals = y - self.func_fit(x, *initial_guess)
        fres0 = sum(residuals**2)
        residuals = y - self.func_fit(x, *pars)
        fres1 = sum(residuals**2)

        table='''<table border="1" width="100%">'''
        table+='''<tr><th>Initial Error</th><th>Final Error</th></tr>'''
        table+='''<tr><td>%g</td><td>%g</td></tr>'''%(fres0, fres1)
        table+='''</table><br>'''
        self.Qprint(table)

        self.Qprint('<b>%g</b> function evaluations' % (self.nfev))

        alpha = 0.05  # 95% confidence interval = 100*(1-alpha)
        n = len(y)  # number of data points
        p = len(pars)  # number of parameters
        dof = max(0, n - p)  # number of degrees of freedom
        # student-t value for the dof and confidence level
        tval = t.ppf(1.0 - alpha / 2., dof)

        par_error = []
        #for i, p, var in zip(range(p), pars, np.diag(pcov)):
        for var in np.diag(pcov):
            sigma = var**0.5
            par_error.append(sigma * tval)

        ind = 0
        table='''<table border="1" width="100%">'''
        table+='''<tr><th>Parameter</th><th>Value ± Error</th></tr>'''
        #self.Qprint("\n%9s = %10s ± %-9s" % ("Parameter", "Value", "Error"))
        #self.Qprint("==================================")
        for p in k:
            par = self.parameters[p]
            if par.opt_type == OptType.opt:
                par.error = par_error[ind]
                ind += 1
                table+='''<tr><td>%s</td><td>%10.4g ± %-9.4g</td></tr>'''%(par.name, par.value, par.error)
                #self.Qprint('%9s = %10.4g ± %-9.4g' % (par.name, par.value, par.error))
            else:
                table+='''<tr><td>%s</td><td>%10.4g</td></tr>'''%(par.name, par.value)
                #self.Qprint('%9s = %10.4g' % (par.name, par.value))
        table+='''</table><br>'''
        self.Qprint(table)        
        self.is_fitting = False
        self.do_calculate(line, timing=False)
        self.Qprint('''<i>---Fitted in %.3g seconds---</i><br>''' % (time.time() - start_time))
        #self.Qprint("\n---Fitting in %.3g seconds---" % (time.time() - start_time))
        self.do_cite("")

    def do_print(self, line):
        """Print the theory table associated with the given file name
        
        [description]
        
        Arguments:
            - line {[type]} -- [description]
        """
        if line in self.tables:
            print(self.tables[line].data)
        else:
            print("Theory table for \"%s\" not found" % line)

    def complete_print(self, text, line, begidx, endidx):
        """[summary]
        
        [description]
        
        Arguments:
            - text {[type]} -- [description]
            - line {[type]} -- [description]
            - begidx {[type]} -- [description]
            - endidx {[type]} -- [description]
        
        Returns:
            [type] -- [description]
        """
        file_names = list(self.tables.keys())
        if not text:
            completions = file_names[:]
        else:
            completions = [f for f in file_names if f.startswith(text)]
        return completions

    def do_parameters(self, line):
        """View and switch the minimization state of the theory parameters
           parameters A B
        
        Several parameters are allowed
        With no arguments, show the current values
        
        Arguments:
            line {[type]} -- [description]
        """
        if (line == ""):
            plist = list(self.parameters.keys())
            plist.sort()
            print("%9s   %10s (with * = is optimized)" % ("Parameter",
                                                          "Value"))
            print("==================================")
            for p in plist:
                if self.parameters[p].opt_type == OptType.opt:
                    print("*%8s = %10.5g" % (self.parameters[p].name,
                                             self.parameters[p].value))
                elif self.parameters[p].opt_type == OptType.nopt:
                    print("%8s = %10.5g" % (self.parameters[p].name,
                                            self.parameters[p].value))
                elif self.parameters[p].opt_type == OptType.const:
                    print("%8s = %10.5g" % (self.parameters[p].name,
                                            self.parameters[p].value))
        else:
            for s in line.split():
                if (s in self.parameters):
                    if self.parameters[s].opt_type == OptType.opt:
                        self.parameters[s].opt_type == OptType.nopt
                    elif self.parameters[s].opt_type == OptType.nopt:
                        self.parameters[s].opt_type == OptType.opt
                    elif self.parameters[s].opt_type == OptType.const:
                        print("Parameter %s is not optimized" % s)
                else:
                    print("Parameter %s not found" % s)

    def complete_parameters(self, text, line, begidx, endidx):
        """[summary]
        
        [description]
        
        Arguments:
            - text {[type]} -- [description]
            - line {[type]} -- [description]
            - begidx {[type]} -- [description]
            - endidx {[type]} -- [description]
        
        Returns:
            - [type] -- [description]
        """
        parameter_names = list(self.parameters.keys())
        if not text:
            completions = parameter_names[:]
        else:
            completions = [f for f in parameter_names if f.startswith(text)]
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
            - line {[type]} -- [description]
        """
        self.Qprint('Saving prediction(s) of ' + self.name + ' theory')
        for f in self.parent_dataset.files:
            fparam = f.file_parameters
            ttable = self.tables[f.file_name_short]
            if line == '':
                ofilename = os.path.splitext(
                    f.file_full_path)[0] + '_TH' + os.path.splitext(
                        f.file_full_path)[1]
            else:
                ofilename = os.path.join(line, f.file_name_short + '_TH' + os.path.splitext(
                        f.file_full_path)[1])
            # print("ofilename", ofilename)
            # print('File: ' + f.file_name_short)
            fout = open(ofilename, 'w')
            k = list(f.file_parameters.keys())
            k.sort()
            for i in k:
                fout.write(i + "=" + str(f.file_parameters[i]) + ";")
            fout.write('\n')
            fout.write('# Prediction of ' + self.thname + ' Theory\n')
            fout.write('# ')
            k = list(self.parameters.keys())
            k.sort()
            for i in k:
                fout.write(i + '=' + str(self.parameters[i].value) + '; ')
            fout.write('\n')
            fout.write('# Date: ' + time.strftime("%Y-%m-%d %H:%M:%S") +
                       ' - User: ' + getpass.getuser() + '\n')
            k = f.file_type.col_names
            for i in k:
                fout.write(i + '\t')
            fout.write('\n')
            for i in range(ttable.num_rows):
                for j in range(ttable.num_columns):
                    fout.write(str(ttable.data[i, j]) + '\t')
                fout.write('\n')
            fout.close()

# SPAN STUFF

    def change_xmin(self, dx, dy):
        """[summary]
        
        [description]
        
        Arguments:
            - dx {[type]} -- [description]
            - dy {[type]} -- [description]
        """
        try:
            self.xmin += dx
            self.xminline.set_data([self.xmin, self.xmin], [0, 1])
            self.xrange.set_xy([[self.xmin, 0], [self.xmin, 1], [self.xmax, 1],
                                [self.xmax, 0], [self.xmin, 0]])
        except:
            pass

    def change_xmax(self, dx, dy):
        """[summary]
        
        [description]
        
        Arguments:
            - dx {[type]} -- [description]
            - dy {[type]} -- [description]
        """
        try:
            self.xmax += dx
            self.xmaxline.set_data([self.xmax, self.xmax], [0, 1])
            self.xrange.set_xy([[self.xmin, 0], [self.xmin, 1], [self.xmax, 1],
                                [self.xmax, 0], [self.xmin, 0]])
        except:
            pass

    def change_ymin(self, dx, dy):
        """[summary]
        
        [description]
        
        Arguments:
            - dx {[type]} -- [description]
            - dy {[type]} -- [description]
        """
        self.ymin += dy
        self.yminline.set_data([0, 1], [self.ymin, self.ymin])
        self.yrange.set_xy([[0, self.ymin], [0, self.ymax], [1, self.ymax],
                            [1, self.ymin], [0, self.ymin]])

    def change_ymax(self, dx, dy):
        """[summary]
        
        [description]
        
        Arguments:
            - dx {[type]} -- [description]
            - dy {[type]} -- [description]
        """
        self.ymax += dy
        self.ymaxline.set_data([0, 1], [self.ymax, self.ymax])
        self.yrange.set_xy([[0, self.ymin], [0, self.ymax], [1, self.ymax],
                            [1, self.ymin], [0, self.ymin]])

    def do_xrange(self, line):
        """Set/show xrange for fit and shows limits
        
        With no arguments: switches ON/OFF the horizontal span
        
        Arguments:
            - line {[xmin xmax]} -- Sets the limits of the span
        """
        if (line == ""):
            """.. todo:: Set range to current view limits"""
            self.xmin, self.xmax = self.ax.get_xlim()
            self.xminline.set_data([self.xmin, self.xmin], [0, 1])
            self.xmaxline.set_data([self.xmax, self.xmax], [0, 1])
            self.xrange.set_xy([[self.xmin, 0], [self.xmin, 1], [self.xmax, 1],
                                [self.xmax, 0], [self.xmin, 0]])
            self.xrange.set_visible(not self.xrange.get_visible())
            self.xminline.set_visible(not self.xminline.get_visible())
            self.xmaxline.set_visible(not self.xmaxline.get_visible())
        else:
            items = line.split()
            if len(items) < 2:
                print("Not enough parameters")
            else:
                self.xmin = float(items[0])
                self.xmax = float(items[1])
                self.xminline.set_data([self.xmin, self.xmin], [0, 1])
                self.xmaxline.set_data([self.xmax, self.xmax], [0, 1])
                self.xrange.set_xy([[self.xmin, 0], [self.xmin, 1],
                                    [self.xmax, 1], [self.xmax,
                                                     0], [self.xmin, 0]])
                if (not self.xrange.get_visible()):
                    self.xrange.set_visible(True)
                    self.xminline.set_visible(True)
                    self.xmaxline.set_visible(True)
        self.do_plot(line)

    def do_yrange(self, line):
        """Set/show yrange for fit and shows limits
        
        With no arguments: switches ON/OFF the vertical span
        
        Arguments:
            - line {[ymin ymax]} -- Sets the limits of the span
        """
        if (line == ""):
            self.ymin, self.ymax = self.ax.get_ylim()
            self.yminline.set_data([0, 1], [self.ymin, self.ymin])
            self.ymaxline.set_data([0, 1], [self.ymax, self.ymax])
            self.yrange.set_xy([[0, self.ymin], [1, self.ymin], [1, self.ymax],
                                [0, self.ymax], [0, self.ymin]])
            self.yrange.set_visible(not self.yrange.get_visible())
            self.yminline.set_visible(not self.yminline.get_visible())
            self.ymaxline.set_visible(not self.ymaxline.get_visible())
            print("Ymin=%g Ymax=%g" % (self.ymin, self.ymax))
        else:
            items = line.split()
            if len(items) < 2:
                print("Not enough parameters")
            else:
                self.ymin = float(items[0])
                self.ymax = float(items[1])
                self.yminline.set_data([0, 1], [self.ymin, self.ymin])
                self.ymaxline.set_data([0, 1], [self.ymax, self.ymax])
                self.yrange.set_xy([[0, self.ymin], [0, self.ymax],
                                    [1, self.ymax], [1, self.ymin],
                                    [0, self.ymin]])
                if (not self.yrange.get_visible()):
                    self.yrange.set_visible(True)
                    self.yminline.set_visible(True)
                    self.ymaxline.set_visible(True)
        self.do_plot(line)

    def set_xy_limits_visible(self, xstate=False, ystate=False):
        """Hide the x- and y-range selectors
        
        [description]
        """
        self.xrange.set_visible(xstate)
        self.xminline.set_visible(xstate)
        self.xmaxline.set_visible(xstate)

        self.yrange.set_visible(ystate)
        self.yminline.set_visible(ystate)
        self.ymaxline.set_visible(ystate)

        self.parent_dataset.actionVertical_Limits.setChecked(xstate)
        self.parent_dataset.actionHorizontal_Limits.setChecked(ystate)
        self.parent_dataset.set_limit_icon()


# MODES STUFF

    def copy_modes(self):
        """[summary]
        
        [description]
        """
        apmng = self.parent_dataset.parent_application.parent_manager
        L, S= apmng.list_theories_Maxwell(th_exclude=self)
        print("Found %d theories that provide modes" % len(L))
        kys = list(L.keys())
        kys.sort()
        for i, k in enumerate(kys):
            print("%d: %s" % (i, k))
        opt = int(
            input("Select theory (number between 0 and %d> " % (len(L) - 1)))
        if (opt < 0 or opt >= len(L)):
            print("Invalid option!")
        else:
            tau, G0 = L[kys[opt]]()
            tauinds = (-tau).argsort()
            tau = tau[tauinds]
            G0 = G0[tauinds]
            self.set_modes(tau, G0)

    def do_copy_modes(self, line):
        """[summary]
        
        [description]
        
        Arguments:
            - line {[type]} -- [description]
        """
        self.copy_modes()

    def get_modes(self):
        """[summary]
        
        [description]
        
        Returns:
            - [type] -- [description]
        """
        tau = np.ones(1)
        G = np.ones(1)
        return tau, G

    def set_modes(self, tau, G):
        """[summary]
        
        [description]
        
        Arguments:
            - tau {[type]} -- [description]
            - G {[type]} -- [description]
        """
        pass

    def do_cite(self, line):
        """Print citation information
        
        [description]
        
        Arguments:
            - line {[type]} -- [description]
        """
        if (self.citations != ""):
            self.Qprint('''\n<b><font color=red>CITE</font>:</b> <a href="%s">%s</a><p>'''%(self.doi, self.citations))

    def do_plot(self, line):
        """Call the plot from the parent Dataset
        
        [description]
        
        Arguments:
            - line {[type]} -- [description]
        """
        self.parent_dataset.do_plot(line)
        #self.plot_theory_stuff()

    def set_param_value(self, name, value):
        """[summary]
        
        [description]
        
        Arguments:
            - name {[type]} -- [description]
            - value {[type]} -- [description]

        Returns:
            - Success{bool} -- True if the operation was successful
        """
        p = self.parameters[name]
        try:
            if (p.type == ParameterType.real):
                try:
                    val = float(value)
                except ValueError:
                    return "Value must be a float", False
                if val < p.min_value:
                    p.value = p.min_value
                    return 'Value must be greater than %.4g' % p.min_value, False
                elif val > p.max_value:
                    p.value = p.max_value
                    return 'Value must be smaller than %.4g' % p.max_value, False
                else:
                    p.value = val
                    return '', True

            elif (p.type == ParameterType.integer):
                try:
                    val = int(value)  #convert to int
                except ValueError:
                    return "Value must be an integer", False
                if val < p.min_value:
                    p.value = p.min_value
                    return 'Value must be greater than %d' % p.min_value, False
                elif val > p.max_value:
                    p.value = p.max_value
                    return 'Value must be smaller than %d' % p.max_value, False
                else:
                    p.value = val
                    return '', True

            elif (p.type == ParameterType.discrete_integer):
                try:
                    val = int(value)  #convert to int
                except ValueError:
                    return "Value must be an integer", False
                if val in p.discrete_values:
                    p.value = val
                    return '', True
                else:
                    message = "Values allowed: " + ', '.join(
                        [str(s) for s in p.discrete_values])
                    print(message)
                    return message, False

            elif (p.type == ParameterType.discrete_real):
                try:
                    val = float(value)
                except ValueError:
                    return "Value must be a float", False
                if val in p.discrete_values:
                    p.value = val
                    return '', True
                else:
                    message = "Values allowed: " + ', '.join(
                        [str(s) for s in p.discrete_values])
                    print(message)
                    return message, False

            elif (p.type == ParameterType.boolean):
                if value in [True, 'true', 'True', '1', 't', 'T', 'y', 'yes']:
                    p.value = True
                else:
                    p.value = False
                return '', True

            elif (p.type == ParameterType.string):
                p.value = value
                return '' , True

            else:
                return '', False

        except ValueError as e:
            print("In set_param_value:", e)
            return '', False

    def default(self, line):
        """Called when the input command is not recognized
        
        Called on an input line when the command prefix is not recognized.
        Check if there is an = sign in the line. If so, it is a parameter change.
        Else, we execute the line as Python code.
        
        Arguments:
            - line {[type]} -- [description]
        """
        if "=" in line:
            par = line.split("=")
            if (par[0] in self.parameters):
                self.set_param_value(par[0], par[1])
            else:
                print("Parameter %s not found" % par[0])
        elif line in self.parameters.keys():
            print(self.parameters[line])
            print(self.parameters[line].__repr__())
        else:
            super(Theory, self).default(line)

    def do_hide(self, line=''):
        """Hide the theory artists and associated tools
        
        [description]
        """
        self.active = False
        self.set_xy_limits_visible(False, False)  # hide xrange and yrange
        for table in self.tables.values():
            for i in range(table.MAX_NUM_SERIES):
                for nx in range(self.parent_dataset.nplots):
                    table.series[nx][i].set_visible(False)
        try:
            self.show_theory_extras(False)
        except:  # current theory has no extras
            # print("current theory has no extras to hide")
            pass

    def set_th_table_visible(self, fname, state):
        """Show/Hide all theory lines related to the file "fname" """
        tt = self.tables[fname]
        for i in range(tt.MAX_NUM_SERIES):
            for nx in range(self.parent_dataset.nplots):
                tt.series[nx][i].set_visible(state)

    def do_show(self, line=''):
        """[summary]
        
        [description]
        """
        self.active = True
        self.set_xy_limits_visible(self.is_xrange_visible,
                                   self.is_yrange_visible)
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
        except:  # current theory has no extras
            # print("current theory has no extras to show")
            pass
        self.parent_dataset.do_plot("")

    def Qprint(self, msg, end='<br>'):
        """[summary]
        
        [description]
        
        Arguments:
            - msg {[type]} -- [description]
        """
        if CmdBase.mode == CmdMode.GUI:
            self.print_signal.emit(msg + end)
        else:
            print(msg, end=end)

    def print_qtextbox(self, msg):
        """Print message in the GUI log text box"""
        self.thTextBox.insertHtml(msg)
        self.thTextBox.verticalScrollBar().setValue(
            self.thTextBox.verticalScrollBar().maximum())
        self.thTextBox.moveCursor(QTextCursor.End)