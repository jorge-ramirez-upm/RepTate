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
"""Module TheoryTTS

Module for the pseudo theory for Time-Temperature superposition shift of LVE data.

"""
import os
import time
import getpass
import numpy as np
from scipy import interp
from scipy.optimize import minimize, curve_fit
from scipy.stats import distributions
from RepTate.core.CmdBase import CmdBase, CmdMode
from RepTate.core.Parameter import Parameter, ParameterType, OptType
from RepTate.core.Theory import Theory
from RepTate.gui.QTheory import QTheory
from PyQt5.QtWidgets import QWidget, QToolBar, QAction, QStyle, QFileDialog, QMessageBox
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon

class TheoryWLFShift(CmdBase):
    """Time-temperature superposition based on a Williams-Landel-Ferry (WLF) equation with two parameters.

    * **Function**
        .. math::
            \\begin{eqnarray}
            \\omega(T_r) &= & a_T \\omega(T) \\\\
            G(T_r) &= & b_T G(T) \\\\
            \\log_{10} a_T &= & \\frac{-B_1 (T-T_r)}{(B_2+T_r)(B_2+T)} \\\\
            b_T &= & \\frac{\\rho(T_r)T_r}{\\rho(T)T} = \\frac{(1+\\alpha T)(T_r+273.15)}{(1+\\alpha T_r)(T+273.15)} \\\\
            T_g &= &T_g^\\infty - \\frac{C_{T_g}}{M_w}
            \\end{eqnarray}

    * **Parameters**
       - :math:`T_r`: Reference temperature to which the experimental data will be shifted.
       - :math:`B_1`: Material parameter, corresponding to :math:`C_1\cdot C_2`, with :math:`C_1` and :math:`C_2` being the standard WLF material parameters.
       - :math:`B_2`: Material parameter, corresponding to :math:`C_2-T_r`, :math:`C_2` being the standard WLF material parameter.
       - logalpha: Decimal logarithm of the thermal expansion coefficient of the polymer at 0 °C.
       - :math:`C_{T_g}`: Material parameter that describes the dependence of :math:`T_g` with :math:`M_w`.
       - dx12: Fraction of 1-2 (vynil) units (valid for polybutadiene).

    """
    thname = "WLF Shift"
    description = "TTS shift based on the WLF equation"
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
        return GUITheoryWLFShift(
            name, parent_dataset,
            ax) if (CmdBase.mode == CmdMode.GUI) else CLTheoryWLFShift(
                name, parent_dataset, ax)


class BaseTheoryWLFShift:
    """[summary]

    [description]
    """
    help_file = 'http://reptate.readthedocs.io/manual/Applications/TTS/Theory/theory.html#williams-landel-ferry-tts-shift'
    single_file = False
    thname = TheoryWLFShift.thname
    citations = TheoryWLFShift.citations
    doi = TheoryWLFShift.doi

    def __init__(self, name="", parent_dataset=None, ax=None):
        """
        **Constructor**

        Keyword Arguments:
            - name {[type]} -- [description] (default: {""})
            - parent_dataset {[type]} -- [description] (default: {None})
            - ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, ax)
        self.function = self.TheoryWLFShift
        self.parameters["Tr"] = Parameter(
            name="Tr",
            value=25,
            description="Reference T to WLF shift the data to",
            type=ParameterType.real,
            opt_type=OptType.const)
        self.parameters["B1"] = Parameter(
            name="B1",
            value=850,
            description="Material parameter B1 for WLF Shift",
            type=ParameterType.real,
            opt_type=OptType.opt)
        self.parameters["B2"] = Parameter(
            name="B2",
            value=126,
            description="Material parameter B2 for WLF Shift",
            type=ParameterType.real,
            opt_type=OptType.opt)
        self.parameters["logalpha"] = Parameter(
            name="logalpha",
            value=-3.18,
            description="Log_10 of the thermal expansion coefficient at 0 °C",
            type=ParameterType.real,
            opt_type=OptType.const)
        self.parameters["CTg"] = Parameter(
            name="CTg",
            value=14.65,
            description="Molecular weight dependence of Tg",
            type=ParameterType.real,
            opt_type=OptType.const)
        self.parameters["dx12"] = Parameter(
            name="dx12",
            value=0,
            description="Fraction 1,2 vinyl units (for PBd)",
            type=ParameterType.real,
            opt_type=OptType.const)
        self.parameters["vert"] = Parameter(
            name="vert",
            value=True,
            description="Shift vertically",
            type=ParameterType.boolean,
            opt_type=OptType.const,
            display_flag=False)
        self.parameters["iso"] = Parameter(
            name="iso",
            value=True,
            description="Isofrictional state",
            type=ParameterType.boolean,
            opt_type=OptType.const,
            display_flag=False)

        self.get_material_parameters()
        self.shift_factor_dic = {}


    def TheoryWLFShift(self, f=None):
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

        Tr = self.parameters["Tr"].value
        B1 = self.parameters["B1"].value
        B2 = self.parameters["B2"].value
        alpha = np.power(10.0, self.parameters["logalpha"].value)
        CTg = self.parameters["CTg"].value
        dx12 = self.parameters["dx12"].value
        iso = self.parameters["iso"].value
        vert = self.parameters["vert"].value

        Tf = f.file_parameters["T"]
        Mw = f.file_parameters["Mw"]

        # Trying a new expression for the shift
        if iso:
            B2 += CTg / Mw - 68.7 * dx12
            Trcorrected = Tr - CTg / Mw + 68.7 * dx12
        else:
            Trcorrected = Tr
        aT = np.power(10.0, -B1 *(Tf - Trcorrected) / (B2 + Trcorrected) / (B2 + Tf))
        tt.data[:, 0] = ft.data[:, 0] * aT

        if vert:
            bT = (1 + alpha * Tf) * (Tr + 273.15) / (1 + alpha * Tr) / (
                Tf + 273.15)
        else:
            bT = 1
        tt.data[:, 1] = ft.data[:, 1] * bT
        tt.data[:, 2] = ft.data[:, 2] * bT
        self.shift_factor_dic[f.file_name_short] = [Tf, aT, bT, Mw]

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
        Mw = []
        xmin = np.zeros((nfiles, view.n))
        xmax = np.zeros((nfiles, view.n))
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
            Mw.append((Mwi, Mw2i, phii, phi2i))

            xmin[i, :] = np.amin(xthi, 0)
            xmax[i, :] = np.amax(xthi, 0)

        MwUnique = {}
        p = list(set(Mw))
        for o in p:
            MwUnique[o] = [0.0, 0]

        for i in range(nfiles):
            for j in range(i + 1, nfiles):
                if (Mw[i] != Mw[j]): continue
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
                    MwUnique[Mw[i]][0] += error
                    MwUnique[Mw[i]][1] += npt

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
        if (line == ""):
            self.Qprint("")
            B1 = self.parameters["B1"].value
            B2 = self.parameters["B2"].value
            Tr = self.parameters["Tr"].value
            self.Qprint("<h3>WLF Params @ Tr = %g</h3>" % Tr)
            self.Qprint("<b>C1</b> = %g" % (B1 / (B2 + Tr)))
            self.Qprint("<b>C2</b> = %g<br>" % (B2 + Tr))

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
        self.do_calculate("", timing=False)
        error = self.do_error("none")
        return error

    def do_fit(self, line):
        """Minimize the error

        [description]

        Arguments:
            - line {[type]} -- [description]
        """
        self.is_fitting = True
        start_time = time.time()
        #view = self.parent_dataset.parent_application.current_view
        self.Qprint('''<hr><h2>Parameter Fitting</h2>''')
        self.shift_factor_dic = {}
        # Mount the vector of parameters (Active ones only)
        initial_guess = []
        k = list(self.parameters.keys())
        k.sort()
        for p in k:
            par = self.parameters[p]
            if par.opt_type == OptType.opt:
                initial_guess.append(par.value)
        if (not initial_guess):
            self.Qprint("No parameter to minimize")
            return
        opt = dict(return_full=True)
        self.nfev = 0

        res = minimize(self.func_fitTTS, initial_guess, method='Nelder-Mead')

        if (not res['success']):
            self.Qprint("Solution not found: %s" % res['message'])
            return

        self.Qprint('<b>%g</b> function evaluations' % (res['nfev']))

        ind = 0
        # table='''<table border="1" width="100%">'''
        # table+='''<tr><th>Parameter</th><th>Value</th></tr>'''
        table = [['%-18s' % 'Parameter', '%-18s' % 'Value'], ]

        for p in k:
            par = self.parameters[p]
            if par.opt_type == OptType.opt:
                ind += 1
                # table+='''<tr><td>%s</td><td>%10.4g</td></tr>'''%(par.name, par.value)
                table.append(['%-18s' % par.name, '%-18.4g' % par.value])
            else:
                #table+='''<tr><td>%s</td><td>%10.4g</td></tr>'''%(par.name, par.value)
                pass
        # table+='''</table><br>'''
        self.Qprint(table)
        self.is_fitting = False
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
        """Save the results from WLFShift theory predictions to a TTS file

        [description]

        Arguments:
            - line {[type]} -- [description]
        """
        nfiles = len(self.parent_dataset.files)
        Mw = []
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
            Mw.append((Mwi, Mw2i, phii, phi2i))
        MwUnique = list(set(Mw))
        MwUnique.sort()

        counter = 0
        for m in MwUnique:
            data = np.zeros(0)
            fparam = {}
            for i in range(nfiles):
                if (Mw[i] == m):
                    Filei = self.parent_dataset.files[i]
                    ttable = self.tables[Filei.file_name_short]
                    T_array = np.full((ttable.num_rows, 1), Filei.file_parameters["T"])
                    data = np.append(data, np.append(ttable.data, T_array, axis=1))
                    data = np.reshape(data, (-1, ttable.num_columns + 1))
                    fparam.update(Filei.file_parameters)
            data = data[data[:, 0].argsort()]
            fparam["T"] = self.parameters["Tr"].value

            try:
                chem_name = '%s_' % fparam["chem"]
            except KeyError:
                chem_name = ''

            if line == "":
                ofilename = os.path.dirname(
                    self.parent_dataset.files[0].file_full_path
                ) + os.sep + chem_name + 'Mw' + str(
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


class CLTheoryWLFShift(BaseTheoryWLFShift, Theory):
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


class GUITheoryWLFShift(BaseTheoryWLFShift, QTheory):
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
        self.isofrictional = tb.addAction(QIcon(':/Icon8/Images/new_icons/icons8-iso.png'),
                                          'Shift to isofrictional state')
        self.isofrictional.setCheckable(True)
        self.isofrictional.setChecked(True)
        self.saveShiftFactors = tb.addAction(QIcon(':/Icon8/Images/new_icons/icons8-save-ShiftFactors.png'), 'Save shift factors')
        self.arrhe_tb = tb.addAction(QIcon(':/Icon8/Images/new_icons/activation_energy.png'), 'Print Arrhenius activation energy')
        # self.savemaster = tb.addAction(self.style().standardIcon(
        #     getattr(QStyle, 'SP_DialogSaveButton')), 'Save Master Curve')
        self.thToolsLayout.insertWidget(0, tb)
        connection_id = self.verticalshift.triggered.connect(
            self.do_vertical_shift)
        connection_id = self.isofrictional.triggered.connect(
            self.do_isofrictional)
        connection_id = self.saveShiftFactors.triggered.connect(self.save_shift_factors)
        connection_id = self.arrhe_tb.triggered.connect(self.print_activation_energy)
        # connection_id = self.savemaster.triggered.connect(self.do_save_dialog)
        self.dir_start = "data/"

    def print_activation_energy(self):
        # Evaluate activation ennergy from Arrhenius fit
        M_set = list(set([l[-1] for l in self.shift_factor_dic.values()]))
        def f(invT, Ea):
            return Ea/8.314 * (invT - 1/(273.15 + self.parameters["Tr"].value))
        Ea_list = []
        for M in M_set:
            invT = []
            lnaT = []
            for s in self.shift_factor_dic.values():
                if s[-1] == M:
                    invT.append(1/(273.15 + s[0]))
                    lnaT.append(np.log(s[1]))
            popt, pcov = curve_fit(f, invT, lnaT, p0=[1e3])
            alpha = 0.05  # 95% confidence interval = 100*(1-alpha)
            n = len(invT)  # number of data points
            p = 1  # number of parameters
            dof = max(0, n - p)  # number of degrees of freedom
            # student-t value for the dof and confidence level
            tval = distributions.t.ppf(1.0 - alpha / 2., dof)
            Ea_list.append((M, popt[0]/1e3, np.sqrt(np.diag(pcov))[0] * tval/1e3))
        if len(M_set) == 1:
            self.Qprint("<h3>Arrhenius Ea = %.3g ± %.3g kJ/mol</h3>" % (popt[0]/1e3, np.sqrt(np.diag(pcov))[0] * tval/1e3))
        else:
            table = [["Mw", "Ea (kJ/mol)"],]
            for items in Ea_list:
                table.append(["%s" % items[0], "%.3g ± %.3g" % (items[1], items[2])])
            self.Qprint(table)

    def do_vertical_shift(self):
        self.set_param_value("vert", self.verticalshift.isChecked())

    def do_isofrictional(self):
        self.set_param_value("iso", self.isofrictional.isChecked())

    # def do_save_dialog(self):
    #     folder = str(
    #         QFileDialog.getExistingDirectory(
    #             self, "Select Directory to save Master curves"))
    #     self.do_save(folder)
    def save_shift_factors(self):
        dilogue_name = "Select Folder for Saving Shift Factors"
        folder = QFileDialog.getExistingDirectory(self, dilogue_name, self.dir_start)
        if (not os.path.isdir(folder)):
            return
        self.dir_start = folder
        nsaved = 0
        Mw_list = []
        for f in self.parent_dataset.files:
            if f.active:
                Mw_list.append(f.file_parameters["Mw"])
        Mw_list = set(Mw_list)
        for Mw in Mw_list:
            flag_first = True
            list_out = []
            with open(os.path.join(folder, 'shift_factors_Mw%s.ttsf' % Mw), 'w') as fout:
                for f in self.parent_dataset.files:
                    if f.active and f.file_parameters["Mw"] == Mw:
                        if flag_first:
                            # write file header
                            for pname in f.file_parameters:
                                if pname != 'T':
                                    fout.write('%s=%s;' % (pname, f.file_parameters[pname]))
                            fout.write('\n')
                            fout.write("%-12s %-12s %-12s\n" % ('T', 'aT', 'bT'))
                            fout.write("%-12s %-12s %-12s\n" % ('[°C]', '[-]', '[-]'))
                            nsaved += 1
                            flag_first = False
                        T, aT, bT, _ = self.shift_factor_dic[f.file_name_short]
                        list_out.append((T, aT, bT))
                list_out.sort()
                for (T, aT, bT) in list_out:
                    fout.write("%-12g %-12g %-12g\n" % (T, aT, bT))

        msg = 'Saved %d shift parameter file(s) in "%s"' % (nsaved, folder)
        if CmdBase.mode == CmdMode.GUI:
            QMessageBox.information(self, 'Saved Files', msg)
        else:
            print(msg)
