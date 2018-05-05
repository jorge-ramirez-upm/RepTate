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
"""Module Application

Module that defines the basic class from which all applications are derived.

"""
import io
#import logging
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator, LogLocator, NullFormatter

from CmdBase import CmdBase, CmdMode
from Theory import Theory
from DataSet import DataSet
from TheoryBasic import *

from MultiView import MultiView, PlotOrganizationType
from PyQt5.QtWidgets import QMenu, QApplication
from PyQt5.QtGui import QCursor, QImage

from collections import OrderedDict
from TheoryBasic import TheoryPolynomial, TheoryPowerLaw, TheoryExponential, TheoryTwoExponentials


class Application(CmdBase):
    """Main abstract class that represents an application
    
    """
    name = "Template"
    description = "Abstract class that defines basic functionality"
    extension = ""

    def __init__(self,
                 name="ApplicationTemplate",
                 parent=None,
                 nplots=1,
                 ncols=1,
                 **kwargs):
        """
        **Constructor**
        
        Keyword Arguments:
            - name {[type]} -- [description] (default: {"ApplicationTemplate"})
            - parent {[type]} -- [description] (default: {None})
        """

        super().__init__()
        self.name = name
        self.parent_manager = parent
        #self.logger = logging.getLogger('ReptateLogger')
        self.views = OrderedDict()
        self.filetypes = OrderedDict() # keep filetypes in order
        self.theories = OrderedDict()  # keep theory combobox in order
        self.datasets = {}
        self.current_view = 0
        self.num_datasets = 0
        self.legend_visible = False
        self.multiviews = []  #default view order in multiplot views
        self.nplots = nplots  #number of plots
        self.ncols = ncols  #number of columns in the multiplot
        self.current_viewtab = 0

        self.artists_clicked = []
        self.autoscale = True

        # Theories available everywhere
        self.common_theories = OrderedDict()  # keep theory combobox in order
        self.common_theories[TheoryPolynomial.thname] = TheoryPolynomial
        self.common_theories[TheoryPowerLaw.thname] = TheoryPowerLaw
        self.common_theories[TheoryExponential.thname] = TheoryExponential
        self.common_theories[TheoryTwoExponentials.thname] = TheoryTwoExponentials

        # MATPLOTLIB STUFF
        self.multiplots = MultiView(PlotOrganizationType.OptimalRow,
                                    self.nplots, self.ncols, self)
        self.multiplots.plotselecttabWidget.setCurrentIndex(
            self.current_viewtab)
        self.figure = self.multiplots.figure
        self.axarr = self.multiplots.axarr  #
        self.canvas = self.multiplots.canvas

        connection_id = self.figure.canvas.mpl_connect('pick_event',
                                                       self.onpick)
        connection_id = self.figure.canvas.mpl_connect('button_release_event',
                                                       self.onrelease)
        connection_id = self.figure.canvas.mpl_connect('scroll_event', self.zoom_wheel)

        if (CmdBase.mode == CmdMode.cmdline):
            # self.figure.show()
            self.multiplots.show()

    def add_common_theories(self):
        for th in self.common_theories.values():
            self.theories[th.thname] = th

    def onrelease(self, event):
        """Called when releasing mouse"""
        if event.button == 3:  #if release a right click
            self.open_figure_popup_menu(event)
            self.artists_clicked.clear()

    def onpick(self, event):
        """Called when clicking on a plot/artist"""
        if event.mouseevent.button == 3:  #right click in plot
            self.artists_clicked.append(
                event.artist)  #collect all artists under mouse

    def open_figure_popup_menu(self, event):
        """Open a menu to let the user copy data or chart to clipboard"""
        main_menu = QMenu()

        #copy chart action
        copy_chart_action = main_menu.addAction("Copy Chart to Clipboard")
        copy_chart_action.triggered.connect(self.copy_chart)

        #copy data sub-menu
        if self.artists_clicked:  #do nothing if list of artists is empty
            menu = QMenu("Copy Data To Clipboard")
            for artist in self.artists_clicked:
                action_print_coordinates = menu.addAction(artist.aname)
                action_print_coordinates.triggered.connect(
                    lambda: self.clipboard_coordinates(artist))
            main_menu.addMenu(menu)

        #launch menu
        if main_menu.exec_(QCursor.pos()):
            self.artists_clicked.clear()

    def copy_chart(self):
        """ Copy current chart to clipboard
        """
        buf = io.BytesIO()
        self.figure.savefig(buf, dpi=150)
        QApplication.clipboard().setImage(QImage.fromData(buf.getvalue()))
        buf.close()

    def clipboard_coordinates(self, artist):
        """Copy data to clipboard in tab-separated format"""
        x, y = artist.get_data()
        line_strings = []
        for i in range(len(x)):
            line_strings.append(str(x[i]) + "\t" + str(y[i]))
        array_string = "\n".join(line_strings)
        QApplication.clipboard().setText(array_string)

    def handle_close_window(self, evt):
        """[summary]
        
        [description]
        
        Arguments:
            - evt {[type]} -- [description]
        
        Returns:
            [type] -- [description]
        """
        print("\nApplication window %s has been closed\n" % self.name)
        print(
            "Please, return to the RepTate prompt and delete the application")

    def zoom_wheel(self, event):
        """[summary]
        
        [description]
        
        Arguments:
            - event {[type]} -- [description]
        """
        # get the current x and y limits
        base_scale = 1.1
        cur_xlim = self.axarr[0].get_xlim()
        cur_ylim = self.axarr[0].get_ylim()
        # set the range
        #cur_xrange = (cur_xlim[1] - cur_xlim[0])*.5
        #cur_yrange = (cur_ylim[1] - cur_ylim[0])*.5
        xdata = event.xdata  # get event x location
        ydata = event.ydata  # get event y location
        if (xdata == None or ydata == None):
            return
        if event.button == 'up':
            # deal with zoom in
            scale_factor = 1 / base_scale
        elif event.button == 'down':
            # deal with zoom out
            scale_factor = base_scale
        else:
            # deal with something that should never happen
            scale_factor = 1
        # Get distance from the cursor to the edge of the figure frame
        x_left = xdata - cur_xlim[0]
        x_right = cur_xlim[1] - xdata
        y_top = ydata - cur_ylim[0]
        y_bottom = cur_ylim[1] - ydata
        # set new limits
        self.axarr[0].set_xlim(
            [xdata - x_left * scale_factor, xdata + x_right * scale_factor])
        self.axarr[0].set_ylim(
            [ydata - y_top * scale_factor, ydata + y_bottom * scale_factor])
        self.axarr[0].figure.canvas.draw()  # force re-draw

    def new(self, line):
        """Create new empty dataset in the application
        
        [description]
        
        Arguments:
            - line {[type]} -- [description]
        
        Returns:
            - [type] -- [description]
        """
        self.num_datasets += 1
        if (line == ""):
            dsname = "DataSet%02d" % self.num_datasets
            dsdescription = ""
        else:
            items = line.split(',')
            dsname = items[0]
            if (len(items) > 1):
                dsdescription = items[1]
            else:
                dsdescription = ""
        ds = DataSet(dsname, dsdescription, self)
        return ds, dsname

    def do_new(self, line):
        """Create a new empty dataset in this application.
        
        [description]
        
        Arguments:
            line {str} -- [NAME [, DESCRIPTION]]
        """
        ds, dsname = self.new(line)
        self.datasets[dsname] = ds
        if (self.mode == CmdMode.batch):
            ds.prompt = ''
        else:
            ds.prompt = self.prompt[:-2] + '/' + ds.name + '> '
        ds.cmdloop()

    def delete(self, ds_name):
        """Delete a dataset from the current application
        
        [description]
        
        Arguments:
            - ds_name {[type]} -- [description]
        """
        if ds_name in self.datasets.keys():
            self.remove_ds_ax_lines(ds_name)
            for th in self.datasets[ds_name].theories.values():
                try:
                    th.destructor()
                except:
                    pass
            self.datasets[ds_name].theories.clear()
            self.datasets[ds_name].files.clear()
            del self.datasets[ds_name]
        else:
            print("Data Set \"%s\" not found" % ds_name)

    def remove_ds_ax_lines(self, ds_name):
        """Remove all dataset file artists from ax including theory ones
        
        [description]
        
        Arguments:
            - ds_name {[type]} -- [description]
        """
        try:
            ds = self.datasets[ds_name]
        except KeyError:
            return
        for th in ds.theories.values():
            for tt in th.tables.values():
                for i in range(tt.MAX_NUM_SERIES):
                    for nx in range(self.nplots):
                        self.axarr[nx].lines.remove(tt.series[nx][i])
        for file in ds.files:
            for i in range(file.data_table.MAX_NUM_SERIES):
                for nx in range(self.nplots):
                    self.axarr[nx].lines.remove(file.data_table.series[nx][i])

    def do_delete(self, name):
        """Delete a dataset from the current application
        
        [description]
        
        Arguments:
            - name {[type]} -- [description]
        """
        self.delete(name)

    def complete_delete(self, text, line, begidx, endidx):
        """Complete delete dataset command
        
        [description]
        
        Arguments:
            - text {[type]} -- [description]
            - line {[type]} -- [description]
            - begidx {[type]} -- [description]
            - endidx {[type]} -- [description]
        
        Returns:
            - [type] -- [description]
        """
        dataset_names = list(self.datasets.keys())
        if not text:
            completions = dataset_names[:]
        else:
            completions = [f for f in dataset_names if f.startswith(text)]
        return completions

    def list(self):
        """List the datasets in the current application
        
        [description]
        """
        for ds in self.datasets.values():
            print("%s:\t%s" % (ds.name, ds.description))

    def do_list(self, line):
        """List the datasets in the current application
        
        [description]
        
        Arguments:
            - line {[type]} -- [description]
        """
        self.list()

    def do_switch(self, name):
        """Switch the current dataset
        
        [description]
        
        Arguments:
            - name {[type]} -- [description]
        """
        done = False
        if name in self.datasets.keys():
            ds = self.datasets[name]
            ds.cmdloop()
        else:
            print("Dataset \"%s\" not found" % name)

    def complete_switch(self, text, line, begidx, endidx):
        """Complete the switch dataset command
        
        [description]
        
        Arguments:
            - text {[type]} -- [description]
            - line {[type]} -- [description]
            - begidx {[type]} -- [description]
            - endidx {[type]} -- [description]
        
        Returns:
            - [type] -- [description]
        """
        ds_names = list(self.datasets.keys())
        if not text:
            completions = ds_names[:]
        else:
            completions = [f for f in ds_names if f.startswith(text)]
        return completions

# FILE TYPE STUFF

    def filetype_available(self):
        """List available file types in the current application
        
        [description]
        """
        ftypes = list(self.filetypes.values())
        for ftype in ftypes:
            print("%s:\t%s\t*.%s" % (ftype.name, ftype.description,
                                     ftype.extension))

    def do_filetype_available(self, line):
        """List available file types in the current application
        
        [description]
        
        Arguments:
            - line {[type]} -- [description]
        """
        self.filetype_available()

# VIEW STUFF

    def set_views(self):
        """Set current view and assign availiable view
        labels to viewComboBox if in GUI mode
        
        [description]
        """
        for i, view_name in enumerate(self.views):  #loop over the keys
            if i == 0:
                #index 0 is the defaut view
                self.current_view = self.views[view_name]
            #add view name to the list of views avaliable
            if CmdBase.mode == CmdMode.GUI:
                self.viewComboBox.insertItem(i, view_name)

        if CmdBase.mode == CmdMode.GUI:
            #index 0 is the defaut selection
            self.viewComboBox.setCurrentIndex(0)

    def view_available(self):
        """List available views in the current application
        
        [description]
        """
        for view in self.views.values():
            if (view == self.current_view):
                print("*%s:\t%s" % (view.name, view.description))
            else:
                print("%s:\t%s" % (view.name, view.description))

    def do_view_available(self, line):
        """List available views in the current application
        
        [description]
        
        Arguments:
            - line {[type]} -- [description]
        """
        self.view_available()

    def view_switch(self, name):
        """Change to another view from open application
        
        [description]
        
        Arguments:
            - name {[type]} -- [description]
        """
        if name in list(self.views.keys()):
            self.current_view = self.views[name]
            if self.current_viewtab == 0:
                self.multiviews[0] = self.views[name]
            else:
                self.multiviews[self.current_viewtab - 1] = self.views[name]
        else:
            print("View \"%s\" not found" % name)
        # Update the plots!
        # Loop over datasets and call do_plot()
        temp = self.autoscale
        self.autoscale = True
        self.update_all_ds_plots()
        self.autoscale = temp

    def update_all_ds_plots(self):
        """[summary]
        
        [description]
        """
        for ds in self.datasets.values():
            ds.do_plot()

    def do_view_switch(self, name):
        """Change to another view from open application
        
        [description]
        
        Arguments:
            - name {[type]} -- [description]
        """
        self.view_switch(name)

    def complete_view_switch(self, text, line, begidx, endidx):
        """Complete switch view command
        
        [description]
        
        Arguments:
            - text {[type]} -- [description]
            - line {[type]} -- [description]
            - begidx {[type]} -- [description]
            - endidx {[type]} -- [description]
        
        Returns:
            - [type] -- [description]
        """
        view_names = list(self.views.keys())
        if not text:
            completions = view_names[:]
        else:
            completions = [f for f in view_names if f.startswith(text)]
        return completions

# THEORY STUFF

    def theory_available(self):
        """List available theories in the current application
        
        [description]
        """
        for t in list(self.theories.values()):
            print("%s:\t%s" % (t.thname, t.description))

    def do_theory_available(self, line):
        """List available theories in the current application
        
        [description]
        
        Arguments:
            line {[type]} -- [description]
        """
        self.theory_available()

# LEGEND STUFF

    def legend(self):
        """[summary]
        
        [description]
        """
        self.legend_visible = not self.legend_visible
        self.set_legend_properties()
        self.canvas.draw()

    def do_legend(self, line):
        """[summary]
        
        [description]
        
        Arguments:
            - line {[type]} -- [description]
        """
        self.legend()


# OTHER STUFF

    def update_plot(self):
        """[summary]
        
        [description]
        """
        self.set_axes_properties(self.autoscale)
        #self.set_legend_properties()
        self.canvas.draw()

    def set_axes_properties(self, autoscale=True):
        """[summary]
        
        [description]
        """
        for nx in range(self.nplots):
            view = self.multiviews[nx]
            if (view.log_x):
                self.axarr[nx].set_xscale("log")
                #self.axarr[nx].xaxis.set_minor_locator(LogLocator(subs=range(10)))
                locmaj = LogLocator(base=10.0, subs=(1.0, ), numticks=100)
                self.axarr[nx].xaxis.set_major_locator(locmaj)
                locmin = LogLocator(
                    base=10.0, subs=np.arange(2, 10) * .1, numticks=100)
                self.axarr[nx].xaxis.set_minor_locator(locmin)
                self.axarr[nx].xaxis.set_minor_formatter(NullFormatter())
            else:
                self.axarr[nx].set_xscale("linear")
                self.axarr[nx].xaxis.set_minor_locator(AutoMinorLocator())
            if (view.log_y):
                self.axarr[nx].set_yscale("log")
                #self.axarr[nx].yaxis.set_minor_locator(LogLocator(subs=range(10)))
                locmaj = LogLocator(base=10.0, subs=(1.0, ), numticks=100)
                self.axarr[nx].yaxis.set_major_locator(locmaj)
                locmin = LogLocator(
                    base=10.0, subs=np.arange(2, 10) * .1, numticks=100)
                self.axarr[nx].yaxis.set_minor_locator(locmin)
                self.axarr[nx].yaxis.set_minor_formatter(NullFormatter())
            else:
                self.axarr[nx].set_yscale("linear")
                self.axarr[nx].yaxis.set_minor_locator(AutoMinorLocator())

            self.axarr[nx].set_xlabel(view.x_label + ' [' + view.x_units + ']')
            self.axarr[nx].set_ylabel(view.y_label + ' [' + view.y_units + ']')

            # self.axarr[nx].plot(self.xData,self.yData)

            if autoscale:
                self.axarr[nx].relim(True)
                self.axarr[nx].autoscale(True)
                self.axarr[nx].autoscale_view()
                self.axarr[nx].set_aspect("auto")

    def set_legend_properties(self):
        """[summary]
        
        [description]
        """
        # pass
        leg = self.axarr[0].legend(frameon=True, ncol=2)
        if (self.legend_visible):
            leg.draggable()
        else:
            try:
                leg.remove()
            except AttributeError as e:
                pass
                #print("legend: %s"%e)
