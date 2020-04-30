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
# Copyright (2017-2020): Jorge Ramirez, Victor Boudara, Universidad Politécnica de Madrid, University of Leeds
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
"""Module TheoryTTS_Automatic

Module for the pseudo theory for Time-Temperature superposition shift of LVE data.

"""
import os
import time
import getpass
import numpy as np
from os.path import dirname, join, abspath, isfile, isdir
from scipy import interp
from scipy.optimize import minimize, curve_fit
from scipy.stats import distributions
from RepTate.core.CmdBase import CmdBase, CmdMode
from RepTate.core.Parameter import Parameter, ParameterType, OptType
from RepTate.core.Theory import Theory
from RepTate.gui.QTheory import QTheory
from PyQt5.QtWidgets import QWidget, QToolBar, QAction, QStyle, QFileDialog, QComboBox, QMessageBox
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon



class TheoryTTSShiftAutomatic(CmdBase):
    """Automatic Time-temperature superposition of experimental data.

    * **Parameters**
       - This theory has no parameters.

    """
    thname = "Automatic TTS Shift"
    description = "Shift data automatically for best overlap"
    citations = []
    doi = []

    def __new__(cls, name="", parent_dataset=None, ax=None):
        """[summary]

        [description]

        Keyword Arguments:
            - name {[type]} -- [description] (default: {""})
            - parent_dataset {[type]} -- [description] (default: {None})
            - ax {[type]} -- [description] (default: {None})

        Returns:
            - [type] -- [description]
        """
        return GUITheoryTTSShiftAutomatic(name, parent_dataset, ax) if (
            CmdBase.mode == CmdMode.GUI) else CLTheoryTTSShiftAutomatic(
                name, parent_dataset, ax)


class BaseTheoryTTSShiftAutomatic:
    """[summary]

    [description]
    """
    help_file = 'http://reptate.readthedocs.io/manual/Applications/TTS/Theory/theory.html#automatic-tts-shift'
    single_file = False
    thname = TheoryTTSShiftAutomatic.thname
    citations = TheoryTTSShiftAutomatic.citations
    doi = TheoryTTSShiftAutomatic.doi

    def __init__(self, name="", parent_dataset=None, ax=None):
        """
        **Constructor**

        Keyword Arguments:
            - name {[type]} -- [description] (default: {""})
            - parent_dataset {[type]} -- [description] (default: {None})
            - ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, ax)
        self.function = self.TheoryTTSShiftAutomatic

        self.parameters["T"] = Parameter(
            name="T",
            value=25,
            description="Temperature to shift to, in °C",
            type=ParameterType.real,
            opt_type=OptType.const,
            display_flag=False)
        self.parameters["vert"] = Parameter(
            name="vert",
            value=True,
            description="Shift vertically",
            type=ParameterType.boolean,
            opt_type=OptType.const,
            display_flag=False)
        self.Mwset, self.Mw, self.Tdict = self.get_cases()
        self.current_master_curve = None
        self.current_table = None
        self.current_file_min = None
        self.shiftParameters = {}
        self.aT_vs_T = {}
        for k in self.tables.keys():
            self.shiftParameters[k] = (
                0.0, 0.0)  # log10 of horizontal, then vertical

    def TheoryTTSShiftAutomatic(self, f=None):
        """[summary]

        [description]

        Keyword Arguments:
            - f {[type]} -- [description] (default: {None})
        """
        ft = f.data_table
        tt = self.tables[f.file_name_short]
        tt.num_columns = ft.num_columns
        tt.num_rows = ft.num_rows
        tt.data = np.zeros((tt.num_rows, tt.num_columns))

        try:
            H, V = self.shiftParameters[f.file_name_short]
        except KeyError:
            # table did not exixt when the TH was opened
            H, V = self.shiftParameters[f.file_name_short] = (0, 0)

        tt.data[:, 0] = ft.data[:, 0] * np.power(10.0, H)
        tt.data[:, 1] = ft.data[:, 1] * np.power(10.0, V)
        tt.data[:, 2] = ft.data[:, 2] * np.power(10.0, V)

    def get_cases(self):
        """Get all different samples in the dataset

           Samples are different if Mw, Mw2, phi, phi2 are different
        """
        nfiles = len(self.parent_dataset.files)
        Mw = []
        Tlist = []

        for i in range(nfiles):
            Filei = self.parent_dataset.files[i]
            Mwi = Filei.file_parameters["Mw"]
            if "Mw2" in Filei.file_parameters:
                Mw2i = Filei.file_parameters["Mw2"]
            else:
                Mw2i = 0
            if "phi" in Filei.file_parameters:
                phii = Filei.file_parameters["phi"]
            else:
                phii = 0
            if "phi2" in Filei.file_parameters:
                phi2i = Filei.file_parameters["phi2"]
            else:
                phi2i = 0
            Ti = Filei.file_parameters["T"]
            Mw.append((Mwi, Mw2i, phii, phi2i))
            Tlist.append(Ti)

        p = list(set(Mw))
        Tdict = {}
        for c in p:
            Tdict[c] = []
        for i in range(nfiles):
            Filei = self.parent_dataset.files[i]
            Tdict[Mw[i]].append([Tlist[i], i, Filei.file_name_short, Filei])
        return p, Mw, Tdict

    def do_error(self, line):
        """Override the error calculation for TTS

        The error is calculated as the vertical distance between theory points, in the current view,\
        calculated over all possible pairs of theory tables, when the theories overlap in the horizontal direction and\
        they correspond to files with the same Mw (if the parameters Mw2 and phi exist, their values are also
        used to classify the error). 1/2 of the error is added to each file.
        Report the error of the current theory on all the files.\n\
        File error is calculated as the mean square of the residual, averaged over all calculated points in the shifted tables.\n\
        Total error is the mean square of the residual, averaged over all points considered in all files.

        Arguments:
            - line {[type]} -- [description]
        """
        total_error = 0
        npoints = 0
        view = self.parent_dataset.parent_application.current_view
        nfiles = len(self.parent_dataset.files)
        file_error = np.zeros(nfiles)
        file_points = np.zeros(nfiles, dtype=np.int)
        xth = []
        yth = []
        xmin = np.zeros((nfiles, view.n))
        xmax = np.zeros((nfiles, view.n))
        for i in range(nfiles):
            Filei = self.parent_dataset.files[i]
            xthi, ythi, success = view.view_proc(
                self.tables[Filei.file_name_short], Filei.file_parameters)
            # We need to sort arrays
            for k in range(view.n):
                x = xthi[:, k]
                p = x.argsort()
                xthi[:, k] = xthi[p, k]
                ythi[:, k] = ythi[p, k]
            xth.append(xthi)
            yth.append(ythi)

            xmin[i, :] = np.amin(xthi, 0)
            xmax[i, :] = np.amax(xthi, 0)

        #Mwset, Mw, Tdict = self.get_cases()
        MwUnique = {}
        for o in self.Mwset:
            MwUnique[o] = [0.0, 0]

        for i in range(nfiles):
            for j in range(i + 1, nfiles):
                if (self.Mw[i] != self.Mw[j]): continue
                for k in range(view.n):
                    condition = (xth[j][:, k] > xmin[i, k]) * (
                        xth[j][:, k] < xmax[i, k])
                    x = np.extract(condition, xth[j][:, k])
                    y = np.extract(condition, yth[j][:, k])
                    yinterp = interp(x, xth[i][:, k], yth[i][:, k])
                    error = np.sum((yinterp - y)**2)
                    npt = len(y)
                    total_error += error
                    npoints += npt
                    MwUnique[self.Mw[i]][0] += error
                    MwUnique[self.Mw[i]][1] += npt

        if (line == ""):
            # table='''<table border="1" width="100%">'''
            # table+='''<tr><th>Mw</th><th>Mw2</th><th>phi</th><th>phi2</th><th>Error</th><th># Pts.</th></tr>'''
            table = [['%-12s' % 'Mw', '%-12s' % 'Mw2', '%-12s' % 'phi', '%-12s' % 'phi2', '%-12s' % 'Error', '%-12s' % '# Pts.' ],]
            p = list(MwUnique.keys())
            p.sort()
            for o in p:
                if (MwUnique[o][1] > 0):
                    # table+='''<tr><td>%4g</td><td>%4g</td><td>%4g</td><td>%4g</td><td>%8.3g</td><td>(%5d)</td></tr>'''%(o[0], o[1], o[2], o[3], MwUnique[o][0] / MwUnique[o][1], MwUnique[o][1])
                    table.append(['%-12.4g' % o[0], '%-12.4g' % o[1], '%-12.4g' % o[2], '%-12.4g' % o[3], '%-12.3g' % (MwUnique[o][0] / MwUnique[o][1]), '%-12d' % MwUnique[o][1] ])
                else:
                    # table+='''<tr><td>%4g</td><td>%4g</td><td>%4g</td><td>%4g</td><td>%s</td><td>(%5d)</td></tr>'''%(o[0], o[1], o[2], o[3], "-", MwUnique[o][1])
                    table.append(['%-12.4g' % o[0], '%-12.4g' % o[1], '%-12.4g' % o[2], '%-12.4g' % o[3], '%-12s' % '-', '%-12d' % MwUnique[o][1] ])
            # table+='''</table><br>'''
            self.Qprint(table)
        if (npoints > 0):
            total_error /= npoints
        else:
            total_error = 1e10
        if (line == ""):
            self.Qprint("<b>TOTAL ERROR</b>: %12.5g (%6d)<br>" % (total_error, npoints))
        return total_error

    def func_fitTTS(self, *param_in):
        """[summary]

        [description]

        Arguments:
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
                par.value = param_in[0][ind]
                ind += 1
        self.do_calculate("")
        error = self.do_error("none")
        return error

    def func_fitTTS_one(self, *param_in):
        """[summary]

        [description]

        Arguments:
            - \*param_in {[type]} -- [description]

        Returns:
            - [type] -- [description]
        """
        H = param_in[0][0]
        V = 0
        if self.parameters["vert"].value:
            V = param_in[0][1]
        tt = np.array(self.current_table, copy=True)
        tt[:, 0] = tt[:, 0] * np.power(10.0, H)
        tt[:, 1] = tt[:, 1] * np.power(10.0, V)
        tt[:, 2] = tt[:, 2] * np.power(10.0, V)
        xmin = self.current_master_curve[0, 0]
        xmax = self.current_master_curve[-1, 0]
        condition = (tt[:, 0] > xmin) * (tt[:, 0] < xmax)
        x0 = np.extract(condition, tt[:, 0])
        x1 = np.extract(condition, tt[:, 1])
        x2 = np.extract(condition, tt[:, 2])
        tt = np.array([x0, x1, x2])
        tt = np.transpose(tt)

        yinterp1 = interp(tt[:, 0], self.current_master_curve[:, 0],
                          self.current_master_curve[:, 1])
        #print(H)
        #print(tt[:,1]-yinterp1)
        yinterp2 = interp(tt[:, 0], self.current_master_curve[:, 0],
                          self.current_master_curve[:, 2])
        error = np.sum((np.log10(yinterp1) - np.log10(tt[:, 1]))**2) + np.sum(
            (np.log10(yinterp2) - np.log10(tt[:, 2]))**2)
        #error=np.sum((yinterp1-tt[:,1])**2)
        npt = len(yinterp1) * 2
        #npt=len(yinterp1)
        #print(H, V, error/npt)
        #input("HELLO")
        return error / npt

    def do_fit(self, line):
        """Minimize the error

        [description]

        Arguments:
            - line {[type]} -- [description]
        """
        self.fitting = True
        start_time = time.time()
        #view = self.parent_dataset.parent_application.current_view
        self.Qprint('''<hr><h2>Parameter Fitting</h2>''')
        self.Mwset, self.Mw, self.Tdict = self.get_cases()
        # Case by case, T by T, we optimize the overlap of all files with the
        # corresponding cases at the selected temperature
        Tdesired = self.parameters["T"].value
        #print (self.Tdict)
        self.aT_vs_T = {}
        for case in self.Tdict.keys():
            self.Qprint('<h3>Mw=%g Mw2=%g phi=%g phi2=%g</h3>' % (case[0], case[1], case[2], case[3]))
            Temps0 = [x[0] for x in self.Tdict[case]]
            Temps = np.abs(
                np.array([x[0] for x in self.Tdict[case]]) - Tdesired)
            Filenames = [x[2] for x in self.Tdict[case]]
            Files = [x[3] for x in self.Tdict[case]]
            indices = np.argsort(Temps)

            # first master curve is built from first file in indices list
            fname = Filenames[indices[0]]
            self.parent_dataset

            self.current_master_curve = np.array(
                Files[indices[0]].data_table.data, copy=True)
            self.current_master_curve.view('i8,i8,i8').sort(
                order=['f1'], axis=0)
            self.shiftParameters[fname] = (0.0, 0.0)

            # table='''<table border="1" width="100%">'''
            # table+='''<tr><th>T</th><th>log(Hshift)</th><th>log(Vshift)</th></tr>'''
            table = [['%-12s' % 'T','%-12s' % 'log(Hshift)','%-12s' % 'log(Vshift)'], ]
            #self.Qprint('%6s %11s %11s' % ('T', 'log(Hshift)', 'log(Vshift)'))
            indices = np.delete(indices, 0, None)

            for i in indices:
                XSHIFT = 0.0
                YSHIFT = 0.0
                if (Temps[i] == 0):
                    # Add to current_master_curve
                    fname = Filenames[i]

                    tt = np.array(Files[i].data_table.data, copy=True)
                    self.current_master_curve = np.concatenate(
                        (self.current_master_curve, tt), axis=0)
                    self.current_master_curve = self.current_master_curve[
                        self.current_master_curve[:, 0].argsort()]
                    self.shiftParameters[fname] = (XSHIFT, YSHIFT)

                else:
                    fname = Filenames[i]
                    tt = np.array(Files[i].data_table.data, copy=True)
                    # Calculate preliminary shift factors (horizontal and vertical)
                    if (any(Files[i].isshifted)):
                        initial_guess = [Files[i].xshift[0], Files[i].yshift[0]]
                    else:
                        # Calculate mid-point of tt
                        indmiddle = int(len(tt[:, 0]) / 2)
                        xmid = tt[indmiddle, 0]
                        ymid = tt[indmiddle, 1]
                        xmidinterp = interp(ymid, self.current_master_curve[:, 1],
                                            self.current_master_curve[:, 0])
                        xshift = np.log10(xmidinterp / xmid)

                        # minimize shift factors so the overlap is maximum
                        initial_guess = [xshift]
                        if self.parameters["vert"].value:
                            initial_guess.append(0)

                    self.current_table = tt
                    self.current_file_min = fname
                    res = minimize(self.func_fitTTS_one, initial_guess, method='Nelder-Mead')
                    if (not res['success']):
                        self.Qprint("Solution not found: %s" % res['message'])
                        return
                    XSHIFT = res.x[0]
                    if self.parameters["vert"].value:
                        YSHIFT = res.x[1]
                    else:
                        YSHIFT = 0.0

                    # Add to current_master_curve
                    # Set the theory file for that particular file
                    ttcopy = np.array(tt, copy=True)
                    ttcopy[:, 0] = ttcopy[:, 0] * np.power(10.0, XSHIFT)
                    ttcopy[:, 1] = ttcopy[:, 1] * np.power(10.0, YSHIFT)
                    ttcopy[:, 2] = ttcopy[:, 2] * np.power(10.0, YSHIFT)
                    self.current_master_curve = np.concatenate(
                        (self.current_master_curve, ttcopy), axis=0)
                    self.current_master_curve = self.current_master_curve[
                        self.current_master_curve[:, 0].argsort()]
                    self.shiftParameters[fname] = (XSHIFT, YSHIFT)

            # Print final table of T and shift factors
            indTsorted = sorted(range(len(Temps0)), key=lambda k: Temps0[k])
            self.aT_vs_T[case[0]] = [] # for Arrhenius activaiton Energy
            for i in indTsorted:
                fname = Filenames[i]
                sparam = self.shiftParameters[fname]
                # table+='''<tr><td>%6.3g</td><td>%11.3g</td><td>%11.3g</td></tr>'''%(Temps0[i], sparam[0], sparam[1])
                table.append(['%-12.3g' % Temps0[i],'%-12.3g' % sparam[0],'%-12.3g' % sparam[1]])
                #self.Qprint('%6.3g %11.3g %11.3g' % (Temps0[i], sparam[0], sparam[1]))
                self.aT_vs_T[case[0]].append((sparam[0], Temps0[i]))
            self.Qprint(table)
        self.fitting = False
        self.do_calculate(line, timing=False)
        self.Qprint('''<i>---Fitted in %.3g seconds---</i><br>''' % (time.time() - start_time))

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
            - [type] -- [description]
        """
        file_names = list(self.tables.keys())
        if not text:
            completions = file_names[:]
        else:
            completions = [f for f in file_names if f.startswith(text)]
        return completions

    def do_save(self, line, extra_txt=''):
        """Save the results from TTSShiftAutomatic theory predictions to a TTS file

        [description]

        Arguments:
            - line {[type]} -- [description]
        """
        nfiles = len(self.parent_dataset.files)
        MwUnique = list(set(self.Mw))
        MwUnique.sort()

        counter = 0
        for m in MwUnique:
            data = np.zeros(0)
            fparam = {}
            for i in range(nfiles):
                if (self.Mw[i] == m):
                    Filei = self.parent_dataset.files[i]
                    ttable = self.tables[Filei.file_name_short]
                    T_array = np.full((ttable.num_rows, 1), Filei.file_parameters["T"])
                    data = np.append(data, np.append(ttable.data, T_array, axis=1))
                    data = np.reshape(data, (-1, ttable.num_columns + 1))
                    fparam.update(Filei.file_parameters)
            data = data[data[:, 0].argsort()]
            fparam["T"] = self.parameters["T"].value

            try:
                chem_name = '%s_' % fparam["chem"]
            except KeyError:
                chem_name = ''

            if line == "":
                ofilename = os.path.dirname(
                    self.parent_dataset.files[0].file_full_path
                ) + os.sep + chem_name+ 'Mw' + str(
                    m[0]) + 'k' + '_Mw2' + str(m[1]) + '_phi' + str(
                        m[2]) + '_phiB' + str(m[3]) + str(fparam["T"]) + '.tts'
            else:
                ofilename = line + os.sep + chem_name + 'Mw' + str(
                    m[0]) + 'k' + '_Mw2' + str(m[1]) + '_phi' + str(
                        m[2]) + '_phiB' + str(m[3]) + str(fparam["T"]) + extra_txt + '.tts'
            fout = open(ofilename, 'w')
            for i in sorted(fparam):
                fout.write(i + "=" + str(fparam[i]) + ";")
            k = list(self.parameters.keys())
            k.sort()
            for i in k:
                fout.write(i + '=' + str(self.parameters[i].value) + ';')
            fout.write('\n')
            fout.write('# Master curve predicted with WLF Theory\n')
            fout.write('# Date: ' + time.strftime("%Y-%m-%d %H:%M:%S") +
                       ' - User: ' + getpass.getuser() + '\n')
            k = Filei.file_type.col_names
            for i in k:
                fout.write(i + '\t')
            fout.write('T \t\n')
            for i in range(data.shape[0]):
                for j in range(data.shape[1]):
                    fout.write(str(data[i, j]) + '\t')
                fout.write('\n')
            fout.close()
            counter += 1

        # print information
        msg = 'Saved %d TTS file(s) in "%s"' % (counter, line)
        if CmdBase.mode == CmdMode.GUI:
            QMessageBox.information(self, 'Save TTS', msg)
        else:
            print(msg)


class CLTheoryTTSShiftAutomatic(BaseTheoryTTSShiftAutomatic, Theory):
    """[summary]

    [description]
    """

    def __init__(self, name="", parent_dataset=None, ax=None):
        """
        **Constructor**

        Keyword Arguments:
            - name {[type]} -- [description] (default: {""})
            - parent_dataset {[type]} -- [description] (default: {None})
            - ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, ax)


class GUITheoryTTSShiftAutomatic(BaseTheoryTTSShiftAutomatic, QTheory):
    """[summary]

    [description]
    """

    def __init__(self, name="", parent_dataset=None, ax=None):
        """
        **Constructor**

        Keyword Arguments:
            - name {[type]} -- [description] (default: {""})
            - parent_dataset {[type]} -- [description] (default: {None})
            - ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, ax)

        # add widgets specific to the theory
        tb = QToolBar()
        tb.setIconSize(QSize(24, 24))
        self.verticalshift = tb.addAction(QIcon(':/Icon8/Images/new_icons/icons8-vertical-shift.png'), 'Vertical shift')
        self.verticalshift.setCheckable(True)
        self.verticalshift.setChecked(True)
        # self.savemaster = tb.addAction(self.style().standardIcon(
        #     getattr(QStyle, 'SP_DialogSaveButton')), 'Save Master Curve')
        self.cbTemp = QComboBox()
        self.populate_TempComboBox()
        self.cbTemp.setToolTip("Select a goal Temperature")
        tb.addWidget(self.cbTemp)
        self.refreshT = tb.addAction(QIcon(':/Icon8/Images/new_icons/icons8-reset.png'), 'Refresh T list')
        self.saveShiftFactors = tb.addAction(QIcon(':/Icon8/Images/new_icons/icons8-save-ShiftFactors.png'), 'Save shift factors')
        self.arrhe_tb = tb.addAction(QIcon(':/Icon8/Images/new_icons/activation_energy.png'), 'Print Arrhenius activation energy')

        self.thToolsLayout.insertWidget(0, tb)
        connection_id = self.verticalshift.triggered.connect(self.do_vertical_shift)
        # connection_id = self.savemaster.triggered.connect(self.do_save_dialog)
        connection_id = self.cbTemp.currentIndexChanged.connect(self.change_temperature)
        connection_id = self.refreshT.triggered.connect(self.refresh_temperatures)
        connection_id = self.saveShiftFactors.triggered.connect(self.save_shift_factors)
        connection_id = self.arrhe_tb.triggered.connect(self.print_activation_energy)

        self.dir_start = "data/"

    def print_activation_energy(self):
        # Evaluate activation ennergy from Arrhenius fit
        if self.aT_vs_T == []:
            self.Qprint("<h3>Apply TTS first</h3>")
            return
        def f(invT, Ea):
            return Ea/8.314 * (invT - 1/(273.15 + self.parameters["T"].value))
        Ea_list = []
        for case in self.aT_vs_T:
            lnaT = [np.log(10)*aT for aT, _ in self.aT_vs_T[case]]
            invT = [1/(273.15 + T) for _, T in self.aT_vs_T[case]]
            popt, pcov = curve_fit(f, invT, lnaT, p0=[1e3])
            alpha = 0.05  # 95% confidence interval = 100*(1-alpha)
            n = len(invT)  # number of data points
            p = 1  # number of parameters
            dof = max(0, n - p)  # number of degrees of freedom
            # student-t value for the dof and confidence level
            tval = distributions.t.ppf(1.0 - alpha / 2., dof)
            Ea_list.append((case, popt[0]/1e3, np.sqrt(np.diag(pcov))[0] * tval/1e3))
        if len(Ea_list) == 1:
            self.Qprint("<h3>Arrhenius Ea = %.3g ± %.3g kJ/mol</h3>" % (popt[0]/1e3, np.sqrt(np.diag(pcov))[0] * tval/1e3))
        else:
            table = [["Mw", "Ea (kJ/mol)"],]
            for items in Ea_list:
                table.append(["%s" % items[0], "%.3g ± %.3g" % (items[1], items[2])])
            self.Qprint(table)

    def populate_TempComboBox(self):
        k = list(self.Tdict.keys())
        a = sorted(list(set([x[0] for x in self.Tdict[k[0]]])))
        for i in range(1, len(k)):
            b = sorted([x[0] for x in self.Tdict[k[i]]])
            a = sorted(list(set(a) & set(b)))
        self.cbTemp.clear()
        for t in a:
            self.cbTemp.addItem(str(t))
        self.set_param_value("T", float(self.cbTemp.currentText()))
        self.update_parameter_table()

    def do_vertical_shift(self):
        self.set_param_value("vert", self.verticalshift.isChecked())

    # def do_save_dialog(self):
    #     folder = str(
    #         QFileDialog.getExistingDirectory(
    #             self, "Select Directory to save Master curves"))
    #     self.do_save(folder)

    def change_temperature(self):
        try:
            self.set_param_value("T", float(self.cbTemp.currentText()))
            self.update_parameter_table()
        except:
            pass

    def refresh_temperatures(self):
        self.Mwset, self.Mw, self.Tdict = self.get_cases()
        self.populate_TempComboBox()

    def save_shift_factors(self):
        dilogue_name = "Select Folder for Saving Shift Factors"
        folder = QFileDialog.getExistingDirectory(self, dilogue_name, self.dir_start)
        if (not isdir(folder)):
            return
        self.dir_start = folder
        nsaved = 0
        for case in self.Tdict.keys():
            fname=""
            if (case[0]>0):
                fname+="Mw%g"%case[0]
            if (case[1]>0):
                fname+="MwB%g"%case[1]
            if (case[2]>0):
                fname+="phi%g"%case[2]
            if (case[3]>0):
                fname+="phiB%g"%case[3]
            with open(join(folder, fname+'.ttsf'), 'w') as fout:
                Temps0 = [x[0] for x in self.Tdict[case]]
                Filenames = [x[2] for x in self.Tdict[case]]
                Files = [x[3] for x in self.Tdict[case]]
                indTsorted = sorted(range(len(Temps0)), key=lambda k: Temps0[k])

                f0 = Files[0]
                for pname in f0.file_parameters:
                    if pname != 'T':
                        fout.write('%s=%s;' % (pname, f0.file_parameters[pname]))
                fout.write('\n')
                fout.write("%-12s %-12s %-12s\n" % ('T', 'aT', 'bT'))
                fout.write("%-12s %-12s %-12s\n" % ('[°C]', '[-]', '[-]'))

                for i in indTsorted:
                    fname = Filenames[i]
                    sparam = self.shiftParameters[fname]
                    fout.write('%-12g %-12g %-12g\n'%(Temps0[i], 10.0**sparam[0], 10.0**sparam[1]))
                nsaved += 1
        msg = 'Saved %d shift parameter file(s) in "%s"' % (nsaved, folder)
        if CmdBase.mode == CmdMode.GUI:
            QMessageBox.information(self, 'Saved Files', msg)
        else:
            print(msg)
