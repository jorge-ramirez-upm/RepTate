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
"""Module TheoryDiscrMWD

Module that defines the theory to discretize a molecular weight distribution.

"""
import os
from CmdBase import CmdBase, CmdMode
from Parameter import Parameter, ParameterType, OptType
from Theory import Theory
from QTheory import QTheory
import numpy as np
from PyQt5.QtCore import Qt, QSize, QFile
from PyQt5.QtWidgets import QToolBar, QSpinBox, QFileDialog, QMessageBox
from PyQt5.QtGui import QIcon
from DraggableArtists import DragType, DraggableBinSeries


class TheoryDiscrMWD(CmdBase):
    """Discretize a Molecular Weight Distribution
    
    [description]
    """
    thname = "Discretize MWD"
    description = "Discretize a Molecular Weight Distribution"
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
        return GUITheoryDiscrMWD(
            name, parent_dataset,
            ax) if (CmdBase.mode == CmdMode.GUI) else CLTheoryDiscrMWD(
                name, parent_dataset, ax)


class BaseTheoryDiscrMWD:
    """[summary]
    
    [description]
    """
    help_file = 'http://reptate.readthedocs.io/manual/Applications/MWD/Theory/theory.html#mwd-discretization'
    single_file = True
    thname = TheoryDiscrMWD.thname
    citations = TheoryDiscrMWD.citations
    doi = TheoryDiscrMWD.doi

    def __init__(self, name="", parent_dataset=None, ax=None):
        """
        **Constructor**
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {""})
            - parent_dataset {[type]} -- [description] (default: {None})
            - ax {[type]} -- [description] (default: {None})
        """
        super().__init__(name, parent_dataset, ax)
        self.function = self.discretise_mwd
        self.has_modes = False
        self.view_bins = True
        self.bins = None
        self.current_file = None
        self.NBIN_MIN = 1
        self.NBIN_MAX = 100

        self.parameters["Mn"] = Parameter(
            "Mn",
            1000,
            "Number-average molecular mass",
            ParameterType.real,
            opt_type=OptType.const,
            display_flag=False)
        self.parameters["Mw"] = Parameter(
            "Mw",
            1000,
            "Weight-average molecular mass",
            ParameterType.real,
            opt_type=OptType.const,
            display_flag=False)
        self.parameters["Mz"] = Parameter(
            "Mz",
            1,
            "z-average molecular mass",
            ParameterType.real,
            opt_type=OptType.const,
            display_flag=False)
        self.parameters["PDI"] = Parameter(
            "PDI",
            1,
            "Polydispersity index",
            ParameterType.real,
            opt_type=OptType.const,
            display_flag=False)

        mmin = self.parent_dataset.minpositivecol(0)
        mmax = self.parent_dataset.maxcol(0)
        nbin = int(np.round(
            3 * np.log10(mmax / mmin)))  # default: 3 bins per decade
        self.parameters["logmmin"] = Parameter(
            "logmmin",
            np.log10(mmin),
            "Log of minimum molecular mass",
            ParameterType.real,
            opt_type=OptType.const,
            display_flag=False)
        self.parameters["logmmax"] = Parameter(
            "logmmax",
            np.log10(mmax),
            "Log of maximum molecular mass",
            ParameterType.real,
            opt_type=OptType.const,
            display_flag=False)
        self.parameters["nbin"] = Parameter(
            name="nbin",
            value=nbin,
            description="Number of molecular weight bins",
            type=ParameterType.integer,
            min_value=self.NBIN_MIN,
            max_value=self.NBIN_MAX,
            opt_type=OptType.const,
            display_flag=False)

        self.set_equally_spaced_bins()
        self.setup_graphic_bins()

    def set_equally_spaced_bins(self):
        """Find the first active file in the dataset and setup the bins"""
        for f in self.theory_files():
            ft = f.data_table.data
            m_arr = ft[:, 0]
            w_arr = ft[:, 1]
            try:
                mmin = min(m_arr[np.nonzero(w_arr)])
                mmax = max(m_arr[np.nonzero(w_arr)])
            except:
                mmin = m_arr[0]
                mmax = m_arr[-1]
            self.parameters["logmmin"].value = np.log10(mmin)
            self.parameters["logmmax"].value = np.log10(mmax)
            nbin = self.parameters["nbin"].value
            bins_edges = np.logspace(np.log10(mmin), np.log10(mmax), nbin + 1)
            for i in range(nbin + 1):
                self.parameters["logM%02d" % i] = Parameter(
                    "logM%02d" % i,
                    np.log10(bins_edges[i]),
                    "Log of molecular mass",
                    ParameterType.real,
                    opt_type=OptType.const,
                    display_flag=False)
            self.current_file = f

    def set_param_value(self, name, new_value):
        """[summary]
        
        [description]
        
        Arguments:
            - name {[type]} -- [description]
            - value {[type]} -- [description]
        """
        if (name == "nbin"):
            nbinold = self.parameters["nbin"].value
        message, success = super().set_param_value(name, new_value)
        if not success:
            return message, success
        if (name == "nbin"):
            new_nbin = self.parameters["nbin"].value
            mminold = self.parameters["logmmin"].value
            mmaxold = self.parameters["logmmax"].value
            for i in range(nbinold + 1):
                del self.parameters["logM%02d" % i]
            mnew = np.logspace(mminold, mmaxold, new_nbin + 1)
            for i in range(new_nbin + 1):
                self.parameters["logM%02d" % i] = Parameter(
                    "logM%02d" % i,
                    np.log10(mnew[i]),
                    "Log molecular mass %d" % i,
                    ParameterType.real,
                    opt_type=OptType.const,
                    display_flag=False)
            if self.autocalculate:
                self.do_calculate("")
        elif (name == 'logmmin') or (
                name == 'logmmax'):  #make bins equally spaced again
            nbin = self.parameters["nbin"].value
            mmin = self.parameters["logmmin"].value
            mmax = self.parameters["logmmax"].value
            mnew = np.logspace(mmin, mmax, nbin + 1)
            for i in range(nbin + 1):
                self.parameters["logM%02d" % i].value = np.log10(mnew[i])
            if self.autocalculate:
                self.do_calculate("")
        return '', True

    def setup_graphic_bins(self):
        """[summary]
        
        [description]
        """
        nbin = self.parameters["nbin"].value
        #marker at the Mw value of the bin
        self.Mw_bin = self.ax.plot(np.zeros(nbin), np.zeros(nbin))[0]
        self.Mw_bin.set_marker('|')
        self.Mw_bin.set_linestyle('')
        self.Mw_bin.set_visible(False)
        # self.Mw_bin.set_markerfacecolor('yellow')
        self.Mw_bin.set_markeredgecolor('black')
        self.Mw_bin.set_markeredgewidth(4)
        self.Mw_bin.set_markersize(18)
        self.Mw_bin.set_alpha(1)

        #setup the movable edge bins
        self.bins = np.logspace(self.parameters["logmmin"].value,
                                self.parameters["logmmax"].value, nbin + 1)
        self.graphic_bins = self.ax.plot(
            self.bins, np.zeros(nbin + 1), picker=10)[0]
        self.graphic_bins.set_marker('d')
        self.graphic_bins.set_linestyle('')
        self.graphic_bins.set_visible(self.view_bins)
        self.graphic_bins.set_markerfacecolor('yellow')
        self.graphic_bins.set_markeredgecolor('red')
        self.graphic_bins.set_markeredgewidth(3)
        self.graphic_bins.set_markersize(18)
        self.graphic_bins.set_alpha(0.75)
        self.artist_bins = DraggableBinSeries(
            self.graphic_bins, DragType.horizontal,
            self.parent_dataset.parent_application.current_view.log_x,
            self.parent_dataset.parent_application.current_view.log_y,
            self.drag_bin)

        self.extra_data['bin_height'] = np.zeros(nbin)
        self.extra_data['bin_edges'] = np.zeros(nbin + 1)
        for i in range(nbin + 1):
            self.extra_data['bin_edges'][i] = np.power(10, self.parameters["logM%02d" % i].value)
        
    def set_extra_data(self, extra_data):
        """Define the extra_data dict and set the bin number
        Redefinition of the QTheory function"""
        self.extra_data = extra_data
        nbin = len(self.extra_data['bin_height'])
        try:
            self.spinbox.blockSignals(True)
            self.spinbox.setValue(nbin)
            self.spinbox.blockSignals(False)
        except:
            # in CL mode
            pass

    def destructor(self):
        """Called when the theory tab is closed"""
        self.graphic_bins_visible(False)
        self.ax.lines.remove(self.graphic_bins)

    def show_theory_extras(self, show=False):
        """Called when the active theory is changed"""
        if CmdBase.mode == CmdMode.GUI:
            self.Qhide_theory_extras(show)
        self.graphic_bins_visible(show)

    def graphic_bins_visible(self, state):
        """[summary]
        
        [description]
        """
        self.view_bins = state
        self.graphic_bins.set_visible(state)  #movable edge bins
        self.Mw_bin.set_visible(state)  #Mw tick marks
        self.set_bar_plot(state)  #bar plot

        if self.view_bins:
            self.artist_bins.connect()
        else:
            self.artist_bins.disconnect()
        # self.do_calculate("")
        self.parent_dataset.parent_application.update_plot()

    def drag_bin(self, newx, newy):
        """[summary]
        
        [description]
        
        Arguments:
            - dx {[type]} -- [description]
            - dy {[type]} -- [description]
        """
        nbin = self.parameters["nbin"].value
        newx = np.sort(newx)
        self.parameters["logmmin"].value = np.log10(newx[0])
        self.parameters["logmmax"].value = np.log10(newx[nbin])
        for i in range(nbin + 1):
            self.set_param_value("logM%02d" % i, np.log10(newx[i]))
        self.do_calculate("")
        self.update_parameter_table()

    def do_error(self, line):
        """[summary]
        
        [description]
        
        Arguments:
            line {[type]} -- [description]
        """
        pass

    def do_fit(self, line=''):
        """Fit not allowed in this theory"""
        pass

    def calculate_moments(self, f, line=""):
        """Calculate the moments Mn, Mw, and Mz of a molecular mass distribution
        
        [description]
        
        Arguments:
            - f {[type]} -- [description]
        """
        n = f[:, 0].size
        Mw = 0
        tempMn = 0
        tempM2 = 0
        tempM3 = 0

        for i in range(n):
            M = f[i, 0]
            w = f[i, 1]
            # M = np.power(10, (np.log10(f[i + 1, 0]) + np.log10(f[i, 0])) / 2 )
            Mw += w * M
            tempM3 += w * M**3 # w*M^3
            tempM2 += w * M * M  # w*M^2
            tempMn += w / M  # w/M
        
        if tempMn * Mw * tempM2 != 0:
            Mn = 1 / tempMn
            Mz = tempM2 / Mw
            Mzp1 = tempM3 / tempM2
            PDI = Mw / Mn
        else:
            PDI = Mzp1 = Mz = Mw = Mn = np.nan
            self.Qprint("Could not determine moments")

        # if line == "input" and CmdBase.mode == CmdMode.GUI:
        #     file_table = self.parent_dataset.DataSettreeWidget.topLevelItem(0)
        #     self.parent_dataset.DataSettreeWidget.blockSignals(True)
        #     file_table.setText(1, "%0.3g" % (Mn / 1000))
        #     file_table.setText(2, "%0.3g" % (Mw / 1000))
        #     file_table.setText(3, "%0.3g" % PDI)
        #     self.parent_dataset.DataSettreeWidget.blockSignals(False)

        if line == "discretized":
            self.set_param_value("Mn", Mn / 1000)
            self.set_param_value("Mw", Mw / 1000)
            self.set_param_value("Mz", Mz / 1000)
            self.set_param_value("PDI", PDI)

        if line == "":
            return Mn / 1000, Mw / 1000, PDI, Mz / Mw
        else:
            self.Qprint('''<h3>Characteristics of the %s MWD<br></h3>''' % line, end='')
            # table='''<table border="1" width="100%">'''
            # table+='''<tr><th>Mn (kg/mol)</th><th>Mw (kg/mol)</th><th>Mw/Mn</th><th>Mz/Mw</th><th>Mz+1/Mz</th></tr>'''
            # table+='''<tr><td>%.3g</td><td>%.3g</td><td>%.3g</td><td>%.3g</td><td>%.3g</td></tr>'''%(Mn / 1000, Mw / 1000, PDI, Mz / Mw, Mzp1/Mz)
            # table+='''</table><br>'''
            table = [['%-12s' % 'Mn (kg/mol)', '%-12s' % 'Mw (kg/mol)', '%-9s' % 'Mw/Mn', '%-9s' % 'Mz/Mw', '%-9s' % 'Mz+1/Mz'],]
            table.append(['%-12.3g' % (Mn / 1000), '%-12.3g' % (Mw / 1000), '%-9.3g' % PDI, '%-9.3g' % (Mz / Mw), '%-9.3g' % (Mzp1 / Mz)])
            self.Qprint(table)

    def discretise_mwd(self, f=None):
        """Discretize a molecular weight distribution
        
        [description]
        
        Keyword Arguments:
            - f {[type]} -- [description] (default: {None})
        """
        self.extra_data['current_fname'] = f.file_name_short
        # sort M, w with M increasing in ft
        f.data_table.data = f.data_table.data[np.argsort(
            f.data_table.data[:, 0])]
        ft = f.data_table.data

        if f != self.current_file:
            self.set_equally_spaced_bins()

        #normalize area under the data points to compute the moments
        n = ft[:, 0].size
        temp_area = 0
        temp = np.zeros((n - 1, 2))
        for i in range(n - 1):
            dlogM = np.log10(ft[i + 1, 0]) - np.log10(ft[i, 0])
            mean_w = (ft[i, 1] + ft[i + 1, 1]) / 2
            temp_area += mean_w * dlogM
            temp[i, 0] = np.power(
                10, (np.log10(ft[i + 1, 0]) + np.log10(ft[i, 0])) / 2)
            temp[i, 1] = mean_w * dlogM
        if temp_area != 0:
            temp[:, 1] /= temp_area
        self.calculate_moments(temp, "input")

        nbin = self.parameters["nbin"].value
        edge_bins = np.zeros(nbin + 1)
        for i in range(nbin + 1):
            edge_bins[i] = np.power(10, self.parameters["logM%02d" % i].value)

        #each M-bin is the Mw value of along the bin width
        out_mbins = np.zeros(nbin)  #output M bins
        for i in range(nbin):
            x = []  # list of M containing bin edges and data point in between
            y = [
            ]  # list of weight containg interpolated values at bin edges and data points
            w_interp = np.interp(
                [edge_bins[i], edge_bins[i + 1]],
                ft[:, 0],
                ft[:, 1],
                left=0,
                right=0)  #interpolate out of range values to zero
            x.append(edge_bins[i])
            y.append(w_interp[0])
            for j in range(n):
                if edge_bins[i] <= ft[j, 0] and ft[j, 0] < edge_bins[i + 1]:
                    x.append(ft[j, 0])
                    y.append(ft[j, 1])
            x.append(edge_bins[i + 1])
            y.append(w_interp[1])
            tempM = 0
            for j in range(len(x)):
                tempM += x[j] * y[j]  # w * M(w)
            out_mbins[i] = tempM
            s = np.sum(y)
            if s != 0:
                out_mbins[i] /= s

        #add area inder the curve to w_out and normalize by bin width
        w_out = np.zeros(nbin)
        for i in range(nbin):
            x = []
            y = []
            w_interp = np.interp(
                [edge_bins[i], edge_bins[i + 1]],
                ft[:, 0],
                ft[:, 1],
                left=0,
                right=0)
            x.append(edge_bins[i])
            y.append(w_interp[0])
            for j in range(n):
                if edge_bins[i] <= ft[j, 0] and ft[j, 0] < edge_bins[i + 1]:
                    x.append(ft[j, 0])
                    y.append(ft[j, 1])
            x.append(edge_bins[i + 1])
            y.append(w_interp[1])
            w_out[i] = np.trapz(
                y, x=np.log10(x)) / (
                    np.log10(edge_bins[i + 1]) - np.log10(edge_bins[i]))

        # copy weights and M into theory table
        tt = self.tables[f.file_name_short]
        tt.num_columns = 2
        tt.num_rows = len(w_out)
        tt.data = np.zeros((tt.num_rows, tt.num_columns))

        #save into extra_data
        self.extra_data['bin_height'] = w_out
        self.extra_data['bin_edges'] = edge_bins

        #compute moments of discretized distribution
        arg_nonzero = np.flatnonzero(w_out)
        nbin_out = len(arg_nonzero)
        saved_th = np.zeros((nbin_out, 2))
        saved_th[:, 0] = out_mbins[arg_nonzero]
        for i, arg in enumerate(arg_nonzero):
            saved_th[i, 1] = (
                np.log10(edge_bins[arg + 1]) - np.log10(edge_bins[arg])
            ) * w_out[arg]
        saved_th[:, 1] /= np.sum(saved_th[:, 1])
        self.calculate_moments(saved_th, "discretized")
        self.extra_data['saved_th'] = saved_th


    def plot_theory_stuff(self):
        """[summary]
        
        [description]
        """
        nbin = self.parameters["nbin"].value
        x = np.zeros(nbin + 1)
        y = np.zeros(nbin + 1)
        for i in range(nbin + 1):
            x[i] = self.parameters["logM%02d" % i].value
        self.graphic_bins.set_data(np.power(10, x), y)

        #set the bar plot
        self.set_bar_plot(True)

        #set the tick marks of for each bin Mw value
        self.Mw_bin.set_data(self.extra_data['saved_th'][:, 0],
                             np.zeros(len(self.extra_data['saved_th'][:, 0])))
        self.Mw_bin.set_visible(True)

    def set_bar_plot(self, visible=True):
        """Hide/Show the bar plot"""
        try:
            self.bar_bins.remove()  #remove existing bars, if any
        except:
            pass  #no bar plot to remove
        if visible:
            bin_e = self.extra_data['bin_edges']
            edges = bin_e[:-1]  #remove last bin
            nbin = len(edges)
            width = np.zeros(nbin)
            for i in range(nbin):
                width[i] = (bin_e[i + 1] - bin_e[i])
            self.bar_bins = self.ax.bar(
                edges,
                self.extra_data['bin_height'],
                width,
                align='edge',
                color='grey',
                edgecolor='black',
                alpha=0.5)

    def get_mwd(self):
        m = np.copy(self.extra_data['saved_th'][:, 0])
        phi = np.copy(self.extra_data['saved_th'][:, 1])
        return m, phi


class CLTheoryDiscrMWD(BaseTheoryDiscrMWD, Theory):
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


class GUITheoryDiscrMWD(BaseTheoryDiscrMWD, QTheory):
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
        self.spinbox = QSpinBox()
        self.spinbox.setRange(self.NBIN_MIN, self.NBIN_MAX)  # min and max number of modes
        self.spinbox.setSuffix(" bins")
        self.spinbox.setValue(self.parameters["nbin"].value)  #initial value
        tb.addWidget(self.spinbox)
        self.thToolsLayout.insertWidget(0, tb)
        #view bins button
        self.view_bins_button = tb.addAction(
            QIcon(':/Icon8/Images/new_icons/icons8-visible.png'), 'View modes')
        self.view_bins_button.setCheckable(True)
        self.view_bins_button.setChecked(True)
        self.thToolsLayout.insertWidget(0, tb)
        self.thToolsLayout.insertWidget(0, tb)

        #connections signal and slots
        connection_id = self.view_bins_button.triggered.connect(
            self.handle_view_bins_button_triggered)
        connection_id = self.spinbox.valueChanged.connect(
            self.handle_spinboxValueChanged)

        #disable useless buttons for this theory
        self.parent_dataset.actionMinimize_Error.setDisabled(True)
        self.parent_dataset.actionShow_Limits.setDisabled(True)
        self.parent_dataset.actionVertical_Limits.setDisabled(True)
        self.parent_dataset.actionHorizontal_Limits.setDisabled(True)

    def handle_spinboxValueChanged(self, value):
        """Handle a change of the parameter 'nbin'
        
        [description]
        
        Arguments:
            value {[type]} -- [description]
        """
        self.spinbox.setValue(value)
        self.set_param_value("nbin", value)
        self.update_parameter_table()

    def Qhide_theory_extras(self, state):
        """Uncheck the view_bins_button button and change button activation state.
        Called when curent theory is changed
        
        [description]
        """
        self.view_bins_button.setChecked(state)
        self.parent_dataset.actionMinimize_Error.setDisabled(state)
        self.parent_dataset.actionShow_Limits.setDisabled(state)
        self.parent_dataset.actionVertical_Limits.setDisabled(state)
        self.parent_dataset.actionHorizontal_Limits.setDisabled(state)

    def handle_view_bins_button_triggered(self, checked):
        """[summary]
        
        [description]
        """
        self.graphic_bins_visible(checked)
        self.set_bar_plot(True)  #leave the bar plot on
        self.parent_dataset.parent_application.update_plot()
        
    def do_save(self, dir, extra_txt=''):
        nbin = self.parameters['nbin'].value
        file_out = os.path.join(dir, '%s_TH_%dbins%s.txt' % (self.extra_data['current_fname'], nbin, extra_txt))
        fout = open(file_out, 'w')
        # output polymers
        Mn, Mw, PDI, Mz_Mw = self.calculate_moments(self.extra_data['saved_th'], "")
        fout.write("Mn=%.3g;Mw=%.3g;PDI=%.3g;Mz/Mw=%.3g\n" % (Mn, Mw, PDI,
                                                              Mz_Mw))
        fout.write("%-10s %12s\n" % ("M", "phi(M)"))
        nbin_out = len(self.extra_data['saved_th'][:, 0])
        for i in range(nbin_out):
            fout.write("%-10.3e %12.6e\n" % (self.extra_data['saved_th'][i, 0],
                                             self.extra_data['saved_th'][i, 1]))

        # print information
        msg = "Saved %d bins to \"%s\"" % (nbin_out, file_out)
        if CmdBase.mode == CmdMode.GUI:
            QMessageBox.information(self, 'Saved discretized MWD', msg)
        else:
            print(msg)