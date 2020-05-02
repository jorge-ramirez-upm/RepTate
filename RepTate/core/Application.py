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
"""Module Application

Module that defines the basic class from which all applications are derived.

"""
import io
#import logging
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator, LogLocator, NullFormatter

from RepTate.core.CmdBase import CmdBase, CmdMode
from RepTate.core.Theory import Theory
from RepTate.core.DataSet import DataSet
from RepTate.theories.TheoryBasic import *
from RepTate.core.Tool import *

from RepTate.core.MultiView import MultiView, PlotOrganizationType
from PyQt5.QtWidgets import QMenu, QApplication
from PyQt5.QtGui import QImage, QColor
from PyQt5.QtCore import Qt

from collections import OrderedDict
from RepTate.theories.TheoryBasic import TheoryPolynomial, TheoryPowerLaw, TheoryExponential, TheoryTwoExponentials
from RepTate.tools.ToolIntegral import ToolIntegral
from RepTate.tools.ToolFindPeaks import ToolFindPeaks
from RepTate.tools.ToolGradient import ToolGradient
from RepTate.tools.ToolSmooth import ToolSmooth
from RepTate.tools.ToolBounds import ToolBounds
from RepTate.tools.ToolEvaluate import ToolEvaluate
from RepTate.tools.ToolInterpolate import ToolInterpolateExtrapolate
from RepTate.tools.ToolMaterialsDatabase import ToolMaterialsDatabase
from RepTate.core.mplcursors import cursor
from colorama import Fore, Style
import logging

class Application(CmdBase):
    """Main abstract class that represents an application

    """
    name = "Template"
    description = "Abstract class that defines basic functionality"
    extension = ""

    def __init__(self,
                 name="ApplicationTemplate",
                 parent=None,
                 nplot_max=4,
                 ncols=2,
                 **kwargs):
        """
        **Constructor**"""

        super().__init__()
        self.name = name
        self.parent_manager = parent
        self.views = OrderedDict()
        self.filetypes = OrderedDict() # keep filetypes in order
        self.theories = OrderedDict()  # keep theory combobox in order
        self.availabletools = OrderedDict()     # keep tools combobox in order
        self.extratools = OrderedDict()     # keep tools combobox in order
        self.datasets = {}
        self.tools = []
        self.num_tools = 0
        self.current_view = 0
        self.num_datasets = 0
        self.legend_visible = False
        self.multiviews = []  #default view order in multiplot views
        self.nplot_max = nplot_max  # maximun number of plots
        self.nplots = nplot_max  # current number of plots
        self.ncols = ncols  #number of columns in the multiplot
        self.current_viewtab = 0

        self.autoscale = True

        # Theories available everywhere
        self.common_theories = OrderedDict()  # keep theory combobox in order
        self.common_theories[TheoryPolynomial.thname] = TheoryPolynomial
        self.common_theories[TheoryPowerLaw.thname] = TheoryPowerLaw
        self.common_theories[TheoryExponential.thname] = TheoryExponential
        self.common_theories[TheoryTwoExponentials.thname] = TheoryTwoExponentials

        # Tools available everywhere
        self.availabletools[ToolBounds.toolname] = ToolBounds
        self.availabletools[ToolEvaluate.toolname] = ToolEvaluate
        self.availabletools[ToolFindPeaks.toolname] = ToolFindPeaks
        self.availabletools[ToolGradient.toolname] = ToolGradient
        self.availabletools[ToolIntegral.toolname] = ToolIntegral
        self.availabletools[ToolInterpolateExtrapolate.toolname] = ToolInterpolateExtrapolate
        self.availabletools[ToolSmooth.toolname] = ToolSmooth
        self.extratools[ToolMaterialsDatabase.toolname] = ToolMaterialsDatabase

        # MATPLOTLIB STUFF
        self.set_multiplot(self.nplots, self.ncols)
        # self.multiplots = MultiView(PlotOrganizationType.OptimalRow,
        #                             self.nplots, self.ncols, self)
        # self.multiplots.plotselecttabWidget.setCurrentIndex(
        #     self.current_viewtab)
        # self.figure = self.multiplots.figure
        # self.axarr = self.multiplots.axarr  #
        # self.canvas = self.multiplots.canvas
        self.ax_opt_defaults = {'fontweight': 'normal', 'fontsize': 20, 'style': 'normal', 'family': 'sans-serif', 'color_ax':  QColor(0, 0, 0).getRgbF(),'color_label':  QColor(0, 0, 0).getRgbF(), 'tick_label_size':20, 'axis_thickness': 1.25, 'grid': 0, 'label_size_auto':1, 'tick_label_size_auto':1}
        self.ax_opts = self.ax_opt_defaults.copy()

        connection_id = self.figure.canvas.mpl_connect('resize_event', self.resizeplot)
        connection_id = self.figure.canvas.mpl_connect('scroll_event', self.zoom_wheel)
        connection_id = self.figure.canvas.mpl_connect('button_press_event', self.on_press)
        connection_id = self.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)
        connection_id = self.figure.canvas.mpl_connect('button_release_event', self.onrelease)

        # Variables used during matplotlib interaction
        self.artists_clicked = []
        self._pressed_button = None # To store active button during interaction
        self._axes = None # To store x and y axes concerned by interaction
        self._event = None  # To store reference event during interaction
        self._was_zooming = False

        if (CmdBase.mode == CmdMode.cmdline):
            # self.figure.show()
            self.multiplots.setWindowFlags(self.multiplots.windowFlags()
                                           & ~Qt.WindowCloseButtonHint)
            self.multiplots.show()
        self.datacursor_ = None

        # LOGGING STUFF
        self.logger = logging.getLogger(self.parent_manager.logger.name + '.' + self.name)
        self.logger.debug('New LVE app')

    def resizeplot(self, event=""):
        """Rescale plot graphics when the window is resized"""
        if not (self.ax_opts['label_size_auto'] or self.ax_opts['tick_label_size_auto']):
            return
        #large window settings
        w_large = 900
        h_large = 650
        font_large = 16
        #small window settings
        w_small = 300
        h_small = 400
        font_small = 10
        #interpolate for current window size
        geometry = self.multiplots.frameGeometry()
        width = geometry.width()
        height = geometry.height()
        scale_w = font_small + (width - w_small)*(font_large - font_small)/(w_large - w_small)
        scale_h = font_small + (height - h_small)*(font_large - font_small)/(h_large - h_small)
        font_size = min(scale_w, scale_h)
        #resize plot fonts
        for ax in self.axarr:
            if self.ax_opts['label_size_auto']:
                ax.xaxis.label.set_size(font_size)
                ax.yaxis.label.set_size(font_size)
            if self.ax_opts['tick_label_size_auto']:
                ax.tick_params(which='major', labelsize=font_size)
                ax.tick_params(which='minor', labelsize=font_size*.8)

    def zoom_wheel(self, event):
        base_scale = 1.1
        if event.button == 'up':
            # deal with zoom in
            scale_factor = 1 / base_scale
        elif event.button == 'down':
            # deal with zoom out
            scale_factor = base_scale
        else:
            # deal with something that should never happen
            scale_factor = 1

        # if event.step > 0:
            # scale_factor = self.scale_factor
        # else:
            # scale_factor = 1. / self.scale_factor

        # Go through all axes to enable zoom for multiple axes subplots
        x_axes, y_axes = self._axes_to_update(event)

        for ax in x_axes:
            transform = ax.transData.inverted()
            xdata, ydata = transform.transform_point((event.x, event.y))

            xlim = ax.get_xlim()
            xlim = self._zoom_range(xlim[0], xlim[1],
                                    xdata, scale_factor,
                                    ax.get_xscale())
            ax.set_xlim(xlim)

        for ax in y_axes:
            ylim = ax.get_ylim()
            ylim = self._zoom_range(ylim[0], ylim[1],
                                    ydata, scale_factor,
                                    ax.get_yscale())
            ax.set_ylim(ylim)

        if x_axes or y_axes:
            self.figure.canvas.draw()

    def _axes_to_update(self, event):
        """Returns two sets of Axes to update according to event.

        Takes care of multiple axes and shared axes.

        :param MouseEvent event: Matplotlib event to consider
        :return: Axes for which to update xlimits and ylimits
        :rtype: 2-tuple of set (xaxes, yaxes)

        """
        x_axes, y_axes = set(), set()

        # Go through all axes to enable zoom for multiple axes subplots
        for ax in self.figure.axes:
            if ax.contains(event)[0]:
                # For twin x axes, makes sure the zoom is applied once
                shared_x_axes = set(ax.get_shared_x_axes().get_siblings(ax))
                if x_axes.isdisjoint(shared_x_axes):
                    x_axes.add(ax)

                # For twin y axes, makes sure the zoom is applied once
                shared_y_axes = set(ax.get_shared_y_axes().get_siblings(ax))
                if y_axes.isdisjoint(shared_y_axes):
                    y_axes.add(ax)

        return x_axes, y_axes

    def _zoom_range(self, begin, end, center, scale_factor, scale):
        """Compute a 1D range zoomed around center.
        :param float begin: The begin bound of the range.
        :param float end: The end bound of the range.
        :param float center: The center of the zoom (i.e., invariant point)
        :param float scale_factor: The scale factor to apply.
        :param str scale: The scale of the axis
        :return: The zoomed range (min, max)
        """
        if begin < end:
            min_, max_ = begin, end
        else:
            min_, max_ = end, begin

        if scale == 'linear':
            old_min, old_max = min_, max_
        elif scale == 'log':
            old_min = np.log10(min_ if min_ > 0. else np.nextafter(0, 1))
            center = np.log10(
                center if center > 0. else np.nextafter(0, 1))
            old_max = np.log10(max_) if max_ > 0. else 0.
        else:
            logging.warning(
                'Zoom on wheel not implemented for scale "%s"' % scale)
            return begin, end

        offset = (center - old_min) / (old_max - old_min)
        range_ = (old_max - old_min) / scale_factor
        new_min = center - offset * range_
        new_max = center + (1. - offset) * range_

        if scale == 'log':
            try:
                new_min, new_max = 10. ** float(new_min), 10. ** float(new_max)
            except OverflowError:  # Limit case
                new_min, new_max = min_, max_
            if new_min <= 0. or new_max <= 0.:  # Limit case
                new_min, new_max = min_, max_

        if begin < end:
            return new_min, new_max
        else:
            return new_max, new_min

    def on_press(self, event):
        if event.button == 2: # Pan
            x_axes, y_axes = self._axes_to_update(event)
            if x_axes or y_axes:
                self._axes = x_axes, y_axes
                self._pressed_button = event.button
                self._pan(event)
        elif event.button == 3: # Zoom
            x_axes, y_axes = self._axes_to_update(event)
            if x_axes or y_axes:
                self._axes = x_axes, y_axes
                self._pressed_button = event.button
                self._zoom_area(event)

    def on_motion(self, event):
        if self._pressed_button == 2:  # pan
            self._pan(event)
        elif self._pressed_button == 3:  # zoom area
            self._zoom_area(event)

    def onrelease(self, event):
        """Called when releasing mouse"""
        if event.button == 3:  #if release a right click
            self._zoom_area(event)
            if not self._was_zooming and CmdBase.mode == CmdMode.GUI:
                self.open_figure_popup_menu(event)
            self.artists_clicked.clear()
            self._was_zooming = False
        elif event.button == 2:
            self._pan(event)
        self._pressed_button = None

    def _pan(self, event):
        if event.name == 'button_press_event':  # begin pan
            self._event = event

        elif event.name == 'button_release_event':  # end pan
            self._event = None

        elif event.name == 'motion_notify_event':  # pan
            if self._event is None:
                return

            if event.x != self._event.x:
                for ax in self._axes[0]:
                    xlim = self._pan_update_limits(ax, 0, event, self._event)
                    ax.set_xlim(xlim)

            if event.y != self._event.y:
                for ax in self._axes[1]:
                    ylim = self._pan_update_limits(ax, 1, event, self._event)
                    ax.set_ylim(ylim)

            if event.x != self._event.x or event.y != self._event.y:
                self.figure.canvas.draw()

            self._event = event

    def _pan_update_limits(self, ax, axis_id, event, last_event):
        """Compute limits with applied pan."""
        assert axis_id in (0, 1)
        if axis_id == 0:
            lim = ax.get_xlim()
            scale = ax.get_xscale()
        else:
            lim = ax.get_ylim()
            scale = ax.get_yscale()

        pixel_to_data = ax.transData.inverted()
        data = pixel_to_data.transform_point((event.x, event.y))
        last_data = pixel_to_data.transform_point((last_event.x, last_event.y))

        if scale == 'linear':
            delta = data[axis_id] - last_data[axis_id]
            new_lim = lim[0] - delta, lim[1] - delta
        elif scale == 'log':
            try:
                delta = math.log10(data[axis_id]) - \
                    math.log10(last_data[axis_id])
                new_lim = [pow(10., (math.log10(lim[0]) - delta)),
                           pow(10., (math.log10(lim[1]) - delta))]
            except (ValueError, OverflowError):
                new_lim = lim  # Keep previous limits
        else:
            logging.warning('Pan not implemented for scale "%s"' % scale)
            new_lim = lim
        return new_lim

    def _zoom_area(self, event):
        if event.name == 'button_press_event':  # begin drag
            self._event = event
            self._patch = plt.Rectangle(
                xy=(event.xdata, event.ydata), width=0, height=0,
                fill=False, linewidth=1., linestyle=':', color='gray')
            self._event.inaxes.add_patch(self._patch)

            canvas = self._patch.figure.canvas
            axes = self._patch.axes
            self._patch.set_animated(True)
            canvas.draw()
            self.background = canvas.copy_from_bbox(self._patch.axes.bbox)
            axes.draw_artist(self._patch)
            canvas.update()

        elif event.name == 'button_release_event':  # end drag
            self.background = None
            try:
                self._patch.remove()
                del self._patch
            except AttributeError:
                # self._patch do not exist
                pass
            if self._event == None:
                self._was_zooming = False
                return
            if (abs(event.x - self._event.x) < 3 or
                    abs(event.y - self._event.y) < 3):
                self._was_zooming = False
                return  # No zoom when points are too close

            x_axes, y_axes = self._axes

            for ax in x_axes:
                pixel_to_data = ax.transData.inverted()
                end_pt = pixel_to_data.transform_point((event.x, event.y))
                begin_pt = pixel_to_data.transform_point(
                    (self._event.x, self._event.y))

                min_ = min(begin_pt[0], end_pt[0])
                max_ = max(begin_pt[0], end_pt[0])
                if (end_pt[0]>begin_pt[0]):
                    if not ax.xaxis_inverted():
                        ax.set_xlim(min_, max_)
                    else:
                        ax.set_xlim(max_, min_)
                else:
                    min_now, max_now = ax.get_xlim()
                    if ax.get_xscale() == 'log':
                        fac = 10.0**((math.log10(max_) - math.log10(min_))/2)
                        if not ax.xaxis_inverted():
                            ax.set_xlim(min_now/fac, max_now*fac)
                        else:
                            ax.set_xlim(max_now*fac, min_now/fac)
                    else:
                        dx = max_ - min_
                        if not ax.xaxis_inverted():
                            ax.set_xlim(min_now-dx, max_now+dx)
                        else:
                            ax.set_xlim(max_now+dx, min_now-dx)

            for ax in y_axes:
                pixel_to_data = ax.transData.inverted()
                end_pt = pixel_to_data.transform_point((event.x, event.y))
                begin_pt = pixel_to_data.transform_point(
                    (self._event.x, self._event.y))

                min_ = min(begin_pt[1], end_pt[1])
                max_ = max(begin_pt[1], end_pt[1])
                if (end_pt[1]<begin_pt[1]):
                    if not ax.yaxis_inverted():
                        ax.set_ylim(min_, max_)
                    else:
                        ax.set_ylim(max_, min_)
                else:
                    min_now, max_now = ax.get_ylim()
                    if ax.get_yscale() == 'log':
                        fac = 10.0**((math.log10(max_) - math.log10(min_))/2)
                        if not ax.yaxis_inverted():
                            ax.set_ylim(min_now/fac, max_now*fac)
                        else:
                            ax.set_ylim(max_now*fac, min_now/fac)
                    else:
                        dy = max_ - min_
                        if not ax.yaxis_inverted():
                            ax.set_ylim(min_now-dy, max_now+dy)
                        else:
                            ax.set_ylim(max_now+dy, min_now-dy)

            self._event = None
            self._was_zooming = True
            self.figure.canvas.draw()


        elif event.name == 'motion_notify_event':  # drag
            if self._event is None:
                return

            if event.inaxes != self._event.inaxes:
                return  # Ignore event outside plot

            self._patch.set_width(event.xdata - self._event.xdata)
            self._patch.set_height(event.ydata - self._event.ydata)

            canvas = self._patch.figure.canvas
            axes = self._patch.axes
            canvas.restore_region(self.background)
            axes.draw_artist(self._patch)
            canvas.update()

    def update_datacursor_artists(self):
        """Update the datacursor instance
        Called at the end of ds.do_plot() and when plot-tab is changed"""
        try:
            self.datacursor_.remove()
        except AttributeError:
            pass
        del self.datacursor_

        if CmdBase.mode == CmdMode.GUI:
            ds_list = [self.DataSettabWidget.currentWidget(),]
            if self.actionView_All_Sets.isChecked():
                ds_list = self.datasets.values()
            artists = []
            for ds in ds_list:
                if ds:
                    th = ds.TheorytabWidget.currentWidget()
                    for f in ds.files:
                        if f.active:
                            dt = f.data_table
                            for j in range(dt.MAX_NUM_SERIES):
                                if self.current_viewtab == 0:
                                    # all artists
                                    for i in range(self.nplots):
                                        artists.append(dt.series[i][j])
                                        if th:
                                            artists.append(th.tables[f.file_name_short].series[i][j])
                                else:
                                    # only artists of current tab
                                    artists.append(dt.series[self.current_viewtab - 1][j])
                                    if th:
                                        artists.append(th.tables[f.file_name_short].series[self.current_viewtab - 1][j])
                self.datacursor_ = cursor(pickables=artists)
                self.datacursor_.bindings["deselect"] = 1
        else:
            axs = [self.axarr[i] for i in range(self.nplots)]
            self.datacursor_ = cursor(pickables=axs)
            self.datacursor_.bindings["deselect"] = 1
        @self.datacursor_.connect("add")
        def _(sel):
            x, y = sel.target
            sel.annotation.set(text="%.3g; %.3g"%(x,y), size=13)
            sel.annotation.get_bbox_patch().set(alpha=0.7)
            sel.annotation.arrow_patch.set(ec="red", alpha=0.5)

    def delete_multiplot(self):
        del self.multiplots

    def set_multiplot(self, nplots, ncols):
        """defines the plot"""
        self.multiplots = MultiView(PlotOrganizationType.OptimalRow,
                                    nplots, ncols, self)
        self.multiplots.plotselecttabWidget.setCurrentIndex(
            self.current_viewtab)
        self.figure = self.multiplots.figure
        self.axarr = self.multiplots.axarr  #
        self.canvas = self.multiplots.canvas

    def set_view_tools(self, view_name):
        """Redefined in Child application. Called when view is changed"""
        pass

    def add_common_theories(self):
        for th in self.common_theories.values():
            self.theories[th.thname] = th

    def refresh_plot(self):
        self.view_switch(self.current_view.name)

    def copy_chart(self):
        """ Copy current chart to clipboard
        """
        buf = io.BytesIO()
        self.figure.savefig(buf, dpi=150)
        QApplication.clipboard().setImage(QImage.fromData(buf.getvalue()))
        buf.close()

    def clipboard_coordinates(self, artist):
        """Copy data to clipboard in tab-separated format"""
        try:
            x, y = artist.get_data()
        except:
            return
        line_strings = []
        for i in range(len(x)):
            line_strings.append(str(x[i]) + "\t" + str(y[i]))
        array_string = "\n".join(line_strings)
        QApplication.clipboard().setText(array_string)

    # JR: I THINK THE FOLLOWING FUNCTION IS NOT NEEDED ANYMORE
    # def handle_close_window(self, evt):
    #     """[summary]

    #     [description]

    #     Arguments:
    #         - evt {[type]} -- [description]

    #     Returns:
    #         [type] -- [description]
    #     """
    #     print("\nApplication window %s has been closed\n" % self.name)
    #     print(
    #         "Please, return to the RepTate prompt and delete the application")

    def new(self, line):
        """Create new empty dataset in the application"""
        self.num_datasets += 1
        if (line == ""):
            dsname = "Set%d" % self.num_datasets
        else:
            dsname = line
        ds = DataSet(dsname, self)
        if (self.mode == CmdMode.batch):
            ds.prompt = ''
        else:
            ds.prompt = self.prompt[:-2] + '/' + Fore.YELLOW + ds.name + '> '
        return ds, dsname

    def do_new(self, line):
        """Create a new empty dataset in this application."""
        ds, dsname = self.new(line)
        self.datasets[dsname] = ds
        ds.cmdloop()

    def delete(self, ds_name):
        """Delete a dataset from the current application"""
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
        """Remove all dataset file artists from ax including theory ones"""
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
        """Delete a dataset from the current application"""
        self.delete(name)
    do_del = do_delete

    def complete_delete(self, text, line, begidx, endidx):
        """Complete delete dataset command"""
        dataset_names = list(self.datasets.keys())
        if not text:
            completions = dataset_names[:]
        else:
            completions = [f for f in dataset_names if f.startswith(text)]
        return completions
    complete_del = complete_delete

    def do_list(self, line=""):
        """List the datasets in the current application"""
        self.do_list_tools()
        self.do_list_datasets()

    def do_list_datasets(self, line=""):
        """List the datasets in the current application"""
        if len(self.datasets)>0:
            print("DATASETS IN THE CURRENT APPLICATION")
            print("===================================")
        for ds in self.datasets.values():
            print(Fore.YELLOW + "%s"%ds.name + Fore.RESET)

    def do_tree(self, line):
        """List all the tools, datasets, files and theories in the current application"""
        done=False
        if line=="":
            offset=0
            prefix=""
            done=True
        else:
            try:
                offset=int(line)
                if offset==1:
                    prefix="|--"
                    done=True
                else:
                    print("Wrong argument for the tree command.")
            except ValueError:
                print("Wrong argument for the tree command.")
        if done:
            for t in self.tools:
                print(prefix + Fore.CYAN + t.name + Fore.RESET)
            for ds in self.datasets.keys():
                print(prefix + Fore.YELLOW + "%s"%self.datasets[ds].name + Fore.RESET)
                self.datasets[ds].do_tree(str(offset+1))

    def do_switch(self, line):
        """Set focus to an open set/theory/tool.
By hitting TAB, all the currently accessible elements are shown.
Arguments:
    - name {str} -- Name of the set/theory/tool to switch the focus to."""
        items=line.split('.')
        listtools = [x.name for x in self.tools]
        if len(items)>1:
            name=items[0]
            if name in self.datasets.keys():
                ds = self.datasets[name]
                ds.cmdqueue.append('switch '+'.'.join(items[1:]))
                ds.cmdloop()
            else:
                print("DataSet \"%s\" not found" % name)
        else:
            name=items[0]
            if name in self.datasets.keys():
                ds = self.datasets[name]
                ds.cmdloop()
            elif name in listtools:
                try:
                    idx = listtools.index(line)
                    self.tools[idx].cmdloop()
                except AttributeError as e:
                    print("Tool\"%s\" not found" % line)
            else:
                print("DataSet \"%s\" not found" % name)

    def complete_switch(self, text, line, begidx, endidx):
        """Complete switch command"""
        setlist = list(self.datasets.keys())
        thlist = []
        for ds in setlist:
            thnames = self.datasets[ds].get_tree()
            thlist += [ds + '.' + t for t in thnames]
        switchlist = setlist + thlist
        if not text:
            completions = switchlist[:]
        else:
            completions = [f for f in switchlist if f.startswith(text)]
        return completions

    def get_tree(self):
        ds_names = list(self.datasets.keys())
        thlist = []
        for ds in ds_names:
            thnames = self.datasets[ds].get_tree()
            thlist += [ds + '.' + t for t in thnames]
        to_names = [t.name for t in self.tools]

        return ds_names + thlist + to_names

# FILE TYPE STUFF

    def do_available_filetypes(self, line=""):
        """List available file types in the current application"""
        print("AVAILABLE FILETYPES")
        print("===================")
        ftypes = list(self.filetypes.values())
        for ftype in ftypes:
            print("%s ("%ftype.name + Fore.CYAN + "*.%s"%ftype.extension + Fore.RESET + "): %s"%ftype.description)

# VIEW STUFF

    def set_views(self):
        """Set current view and assign availiable view labels to viewComboBox if in GUI mode"""
        for i, view_name in enumerate(self.views):  #loop over the keys
            if i == 0:
                #index 0 is the defaut view
                self.current_view = self.views[view_name]
            #add view name to the list of views avaliable
            if CmdBase.mode == CmdMode.GUI:
                self.viewComboBox.insertItem(i, view_name)
                self.viewComboBox.setItemData(i, self.views[view_name].description, Qt.ToolTipRole)

        if CmdBase.mode == CmdMode.GUI:
            #index 0 is the defaut selection
            self.viewComboBox.setCurrentIndex(0)

    def do_available_views(self, line=""):
        """List available views in the current application"""
        print("AVAILABLE VIEWS")
        print("===============")
        for view in self.views.values():
            if (view == self.current_view):
                c = Fore.RED + "*" + Fore.RESET
            else:
                c = " "
            print(c + Fore.BLUE + Style.BRIGHT + "%s"%view.name +
                    Fore.RESET + Style.RESET_ALL + ":\t%s" %view.description)

    def do_available(self, line):
        """Views and Tools available in the current application"""
        self.do_available_tools()
        self.do_available_filetypes()
        self.do_available_views()
        self.do_available_theories()

    def view_switch(self, name):
        """Change to another view from open application"""
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
        """Update all plots from all DataSets"""
        for ds in self.datasets.values():
            ds.do_plot()

    def do_plot(self, name=""):
        """Update and refresh all plots"""
        self.update_all_ds_plots()

    def do_view(self, name):
        """Change the active view"""
        self.view_switch(name)

    def complete_view(self, text, line, begidx, endidx):
        """Complete view command"""
        view_names = list(self.views.keys())
        if not text:
            completions = view_names[:]
        else:
            completions = [f for f in view_names if f.startswith(text)]
        return completions

# THEORY STUFF

    def do_available_theories(self, line=""):
        """List available theories in the current application"""
        print("AVAILABLE THEORIES")
        print("==================")
        for t in list(self.theories.values()):
            print(Fore.MAGENTA + "%s:"%t.thname + (20-len(t.thname))*" " + Fore.RESET + "%s"%t.description)

# TOOL STUFF
    def do_available_tools(self, line=""):
        """List available tools in the current application"""
        print("AVAILABLE TOOLS")
        print("===============")
        for t in list(self.availabletools.values()):
            print(Fore.CYAN + "%s"%t.toolname + Fore.RESET + ":\t%s"%t.description)
        for t in list(self.extratools.values()):
            print(Fore.CYAN + "%s"%t.toolname + Fore.RESET + ":\t%s"%t.description)

    def do_tool_new(self, line):
        """Add a new tool of the type specified to the list of tools"""
        tooltypes = list(self.availabletools.keys())
        extratooltypes = list(self.extratools.keys())
        if ((line in tooltypes) or (line in extratooltypes)):
            self.num_tools += 1
            to_id = ''.join(
                c for c in line
                if c.isupper())  #get the upper case letters of th_name
            to_id = "%s%d" % (to_id, self.num_tools)
            if (line in tooltypes):
                to = self.availabletools[line](to_id, self)
            elif (line in extratooltypes):
                to = self.extratools[line](to_id, self)
            self.tools.append(to)
            if self.mode == CmdMode.GUI:
                return to
            else:
                if (self.mode == CmdMode.batch):
                    to.prompt = ''
                else:
                    to.prompt = self.prompt[:-2] + '/' + Fore.CYAN + to.name + '> '
                to.cmdloop()
        else:
            print("Tool \"%s\" does not exists" % line)

    def complete_tool_new(self, text, line, begidx, endidx):
        """Complete new tool command"""
        tool_names = list(self.availabletools.keys()) + list(self.extratools.keys())
        if not text:
            completions = tool_names[:]
        else:
            completions = [f for f in tool_names if f.startswith(text)]
        return completions

    def do_tool_delete(self, name):
        """Delete a tool from the current application"""
        listtools = [x.name for x in self.tools]
        try:
            idx = listtools.index(name)
            self.tools[idx].destructor()
            del self.tools[idx]
        except AttributeError as e:
            print("Tool \"%s\" not found" % name)

    def complete_tool_delete(self, text, line, begidx, endidx):
        """Complete delete tool command"""
        listtools = [x.name for x in self.tools]
        if not text:
            completions = listtools[:]
        else:
            completions = [f for f in listtools if f.startswith(text)]
        return completions

    def do_list_tools(self, line=""):
        """List opened tools in the current application"""
        if len(self.tools)>0:
            print("OPEN TOOLS IN THIS APPLICATION")
            print("==============================")
        for t in self.tools:
            if t.active:
                print("*" + Fore.CYAN + "%s:"%t.name + Fore.RESET + (15-len(t.name))*" " + "%s"%t.toolname)
            else:
                print(" " + Fore.CYAN + "%s:"%t.name + Fore.RESET + (15-len(t.name))*" " + "%s"%t.toolname)

    def do_tool_switch(self, line):
        """Change the active tool"""
        listtools = [x.name for x in self.tools]
        try:
            idx = listtools.index(line)
            self.tools[idx].cmdloop()
        except AttributeError as e:
            print("Tool\"%s\" not found" % line)

    def complete_tool_switch(self, text, line, begidx, endidx):
        """Complete the tool switch command"""
        completions = self.complete_tool_delete(text, line, begidx, endidx)
        return completions

    def do_tool_activate(self, name):
        """Enable/Disable a given tool"""
        listtools = [x.name for x in self.tools]
        try:
            idx = listtools.index(name)
            self.tools[idx].do_activate(name)
        except AttributeError as e:
            print("Tool \"%s\" not found" % name)
        except ValueError as e:
            print("Tool \"%s\" not found" % name)

    def complete_tool_activate(self, text, line, begidx, endidx):
        """Complete the tool switch command"""
        completions = self.complete_tool_delete(text, line, begidx, endidx)
        return completions

# LEGEND STUFF

    def legend(self):
        """Show/Hide the legend"""
        self.legend_visible = not self.legend_visible
        self.set_legend_properties()
        self.canvas.draw()

    def do_legend(self, line):
        """Show/Hide the legend"""
        self.legend()


# OTHER STUFF

    def update_plot(self):
        """Update the plot in the current application"""
        self.set_axes_properties(self.autoscale)
        #self.set_legend_properties()
        if CmdBase.mode == CmdMode.GUI:
            self.update_legend()
        self.canvas.draw()

    def set_axes_properties(self, autoscale=True):
        """Set axes properties"""
        for nx in range(self.nplots):
            view = self.multiviews[nx]
            ax = self.axarr[nx]
            if (view.log_x):
                ax.set_xscale("log")
                ##ax.xaxis.set_minor_locator(LogLocator(subs=range(10)))
                # locmaj = LogLocator(base=10.0, subs=(1.0, ), numticks=100)
                # ax.xaxis.set_major_locator(locmaj)
                # locmin = LogLocator(
                    # base=10.0, subs=np.arange(2, 10) * .1, numticks=100)
                # ax.xaxis.set_minor_locator(locmin)
                # ax.xaxis.set_minor_formatter(NullFormatter())
            else:
                ax.set_xscale("linear")
                ax.xaxis.set_minor_locator(AutoMinorLocator())
            if (view.log_y):
                ax.set_yscale("log")
                ##ax.yaxis.set_minor_locator(LogLocator(subs=range(10)))
                # locmaj = LogLocator(base=10.0, subs=(1.0, ), numticks=100)
                # ax.yaxis.set_major_locator(locmaj)
                # locmin = LogLocator(
                    # base=10.0, subs=np.arange(2, 10) * .1, numticks=100)
                # ax.yaxis.set_minor_locator(locmin)
                # ax.yaxis.set_minor_formatter(NullFormatter())
            else:
                ax.set_yscale("linear")
                ax.yaxis.set_minor_locator(AutoMinorLocator())

            ax.set_xlabel(view.x_label + ' [' + view.x_units + ']')
            ax.set_ylabel(view.y_label + ' [' + view.y_units + ']')

            if not self.ax_opts['label_size_auto']:
                ax.xaxis.label.set_size(self.ax_opts['fontsize'])
                ax.yaxis.label.set_size(self.ax_opts['fontsize'])

            ax.xaxis.label.set_color(self.ax_opts['color_label'])
            ax.yaxis.label.set_color(self.ax_opts['color_label'])

            ax.xaxis.label.set_style(self.ax_opts['style'])
            ax.yaxis.label.set_style(self.ax_opts['style'])

            ax.xaxis.label.set_family(self.ax_opts['family'])
            ax.yaxis.label.set_family(self.ax_opts['family'])

            ax.xaxis.label.set_weight(self.ax_opts['fontweight'])
            ax.yaxis.label.set_weight(self.ax_opts['fontweight'])

            ax_thick = self.ax_opts['axis_thickness']
            ax.tick_params(which='major', width=1.00*ax_thick, length=5*ax_thick)
            ax.tick_params(which='minor', width=0.75*ax_thick, length=2.5*ax_thick)

            if not self.ax_opts['tick_label_size_auto']:
                ax.tick_params(which='major', labelsize=self.ax_opts['tick_label_size'])
                ax.tick_params(which='minor', labelsize=self.ax_opts['tick_label_size']*.8)

            ax.grid(self.ax_opts['grid'])

            for pos in ['top', 'bottom', 'left', 'right']:
                ax.spines[pos].set_linewidth(ax_thick)
                ax.spines[pos].set_color(self.ax_opts['color_ax'])
            ax.tick_params(which='both', color=self.ax_opts['color_ax'], labelcolor=self.ax_opts['color_ax'])

            if autoscale:
                self.axarr[nx].relim(True)
                self.axarr[nx].autoscale(True)
                self.axarr[nx].autoscale_view()
                self.axarr[nx].set_aspect("auto")

    def set_legend_properties(self):
        """Set default legend properties"""
        # pass
        leg = self.axarr[0].legend(frameon=True, ncol=2)
        if (self.legend_visible):
            leg.set_draggable(True)
            pass
        else:
            try:
                leg.remove()
            except AttributeError as e:
                pass
                #print("legend: %s"%e)

    def do_figure_save(self, line=""):
        """Save the figure to file. Argument = file name. The image format is determined from the file extension."""
        if line=="":
            plt.savefig("RepTateFigure.png")
        else:
            plt.savefig(line)

    def complete_figure_save(self, text, line, begidx, endidx):
        """Complete the figure_save command"""
        return self.complete_cd(text, line, begidx, endidx)
