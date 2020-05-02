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
"""Module DataSet

Module that describes the basic container for data sets (sets of experimental data
read from different files), as well as the particular theories that are being applied
to that data set.

"""
import os
import glob

from enum import Enum
from RepTate.core.CmdBase import CmdBase, CmdMode
from RepTate.core.Theory import Theory
from RepTate.core.Tool import Tool
from RepTate.core.FileType import TXTColumnFile
from RepTate.core.File import File
from RepTate.core.DataTable import DataTable

import itertools
from collections import OrderedDict

import numpy as np
from scipy.integrate import simps
import matplotlib.patheffects as pe
from colorama import Fore
import logging

class ColorMode(Enum):
    """Class to describe how to change colors in the current DataSet"""
    fixed = 0
    variable = 1
    gradient = 2
    modes = ["Fixed color", "Variable color (from palette)", "Color gradient"]
    color1 = (0, 0, 0, 1)  #black RGB
    color2 = (1, 0, 0, 1)  #red RGB
    colorpalettes = {
        "Rainbow":
        [(0, 0, 0), (1.0, 0, 0), (0, 1.0, 0), (0, 0, 1.0), (1.0, 1.0, 0),
         (1.0, 0, 1.0), (0, 1.0, 1.0), (0.5, 0, 0), (0, 0.5, 0), (0, 0, 0.5),
         (0.5, 0.5, 0), (0.5, 0, 0.5), (0, 0.5, 0.5), (0.25, 0, 0),
         (0, 0.25, 0), (0, 0, 0.25), (0.25, 0.25, 0), (0.25, 0,
                                                       0.25), (0, 0.25, 0.25)],
        "Pastel":
        [(0.573, 0.776, 1.0), (0.592, 0.941, 0.667), (1.0, 0.624, 0.604),
         (0.816, 0.733, 1.0), (1.0, 0.996, 0.639), (0.69, 0.878, 0.902),
         (0.573, 0.776, 1.0), (0.592, 0.941, 0.667), (1.0, 0.624, 0.604),
         (0.816, 0.733, 1.0), (1.0, 0.996, 0.639), (0.69, 0.878, 0.902),
         (0.573, 0.776, 1.0), (0.592, 0.941, 0.667), (1.0, 0.624, 0.604)],
        "Bright":
        [(0.0, 0.247, 1.0), (0.012, 0.929, 0.227), (0.91, 0.0, 0.043),
         (0.541, 0.169, 0.886), (1.0, 0.769, 0.0), (0.0, 0.843,
                                                    1.0), (0.0, 0.247, 1.0),
         (0.012, 0.929, 0.227), (0.91, 0.0, 0.043), (0.541, 0.169,
                                                     0.886), (1.0, 0.769, 0.0),
         (0.0, 0.843, 1.0), (0.0, 0.247, 1.0), (0.012, 0.929,
                                                0.227), (0.91, 0.0, 0.043)],
        "Dark": [(0, 0, 0), (0.0, 0.11, 0.498), (0.004, 0.459,
                                                 0.09), (0.549, 0.035, 0.0),
                 (0.463, 0.0, 0.631), (0.722, 0.525,
                                       0.043), (0.0, 0.388, 0.455), (0.0, 0.11,
                                                                     0.498),
                 (0.004, 0.459, 0.09), (0.549, 0.035,
                                        0.0), (0.463, 0.0,
                                               0.631), (0.722, 0.525, 0.043),
                 (0.0, 0.388, 0.455), (0.0, 0.11,
                                       0.498), (0.004, 0.459,
                                                0.09), (0.549, 0.035, 0.0)],
        "ColorBlind":
        [(0, 0, 0), (0.0, 0.447, 0.698), (0.0, 0.62, 0.451),
         (0.835, 0.369, 0.0), (0.8, 0.475, 0.655), (0.941, 0.894, 0.259),
         (0.337, 0.706, 0.914), (0.0, 0.447, 0.698), (0.0, 0.62, 0.451),
         (0.835, 0.369, 0.0), (0.8, 0.475, 0.655), (0.941, 0.894, 0.259),
         (0.337, 0.706, 0.914), (0.0, 0.447, 0.698), (0.0, 0.62,
                                                      0.451), (0.835, 0.369,
                                                               0.0)],
        "Paired":
        [(0.651, 0.808, 0.890), (0.122, 0.471, 0.706), (0.698, 0.875, 0.541),
         (0.200, 0.627, 0.173), (0.984, 0.604, 0.600), (0.890, 0.102, 0.11),
         (0.992, 0.749, 0.435), (1.0, 0.498, 0.0), (0.792, 0.698, 0.839),
         (0.416, 0.239, 0.604), (1.0, 1.0, 0.6), (0.694, 0.349, 0.157),
         (0.651, 0.808, 0.890), (0.122, 0.471, 0.706), (0.698, 0.875,
                                                        0.541), (0.200, 0.627,
                                                                 0.173)]
    }


class SymbolMode(Enum):
    """Class to describe how to change the symbols in the DataSet"""
    fixed = 0
    fixedfilled = 1
    variable = 2
    variablefilled = 3
    modes = [
        "Fixed empty symbol", "Fixed filled symbol", "Variable empty symbols",
        "Variable filled symbols"
    ]
    symbol1 = '.'
    symbol1_name = 'point'
    allmarkers = [
        '.', 'o', 'v', '^', '<', '>', '1', '2', '3', '4', '8', 's', 'p', 'P',
        '*', 'h', 'H', '+', 'x', 'X', 'D', 'd', '|', '_'
    ]
    allmarkernames = [
        'point', 'circle', 'triangle_down', 'triangle_up', 'triangle_left',
        'triangle_right', 'tri_down', 'tri_up', 'tri_left', 'tri_right',
        'octagon', 'square', 'pentagon', 'plus (filled)', 'star', 'hexagon1',
        'hexagon2', 'plus', 'x', 'x (filled)', 'diamond', 'thin_diamond',
        'vline', 'hline'
    ]
    filledmarkers = [
        '.', 'o', 'v', '^', '<', '>', '8', 's', 'p', 'P', '*', 'h', 'H', 'X',
        'D', 'd'
    ]
    filledmarkernames = [
        'point', 'circle', 'triangle_down', 'triangle_up', 'triangle_left',
        'triangle_right', 'octagon', 'square', 'pentagon', 'plus (filled)',
        'star', 'hexagon1', 'hexagon2', 'x (filled)', 'diamond', 'thin_diamond'
    ]


class ThLineMode(Enum):
    """Class to describe how to change the line types in Theories"""
    as_data = 0
    fixed = 1
    color = (0, 0, 0, 1)  #black RGB
    linestyles = OrderedDict(
        [('solid', (0, ())), ('loosely dotted', (0, (1, 10))), ('dotted',
                                                                (0, (1, 5))),
         ('densely dotted', (0, (1, 1))), ('loosely dashed', (0, (5, 10))),
         ('dashed', (0, (5, 5))), ('densely dashed', (0, (5, 1))),
         ('loosely dashdotted',
          (0, (3, 10, 1, 10))), ('dashdotted',
                                 (0, (3, 5, 1, 5))), ('densely dashdotted',
                                                      (0, (3, 1, 1, 1))),
         ('loosely dashdotdotted',
          (0, (3, 10, 1, 10, 1, 10))), ('dashdotdotted',
                                        (0, (3, 5, 1, 5, 1,
                                             5))), ('densely dashdotdotted',
                                                    (0, (3, 1, 1, 1, 1, 1)))])


class DataSet(CmdBase):  # cmd.Cmd not using super() is OK for CL mode.
    """Abstract class to describe a data set"""

    def __init__(self, name="DataSet", parent=None):
        """**Constructor**"""
        super().__init__()

        self.name = name
        self.parent_application = parent
        self.nplots = self.parent_application.nplots
        self.files = []
        self.current_file = None
        self.num_files = 0
        # Marker settings
        self.marker_size = 12
        self.line_width = 1
        self.colormode = ColorMode.variable.value
        self.color1 = ColorMode.color1.value
        self.color2 = ColorMode.color2.value
        self.th_line_mode = ThLineMode.as_data.value
        self.th_color = ThLineMode.color.value
        self.palette_name = 'ColorBlind'
        self.symbolmode = SymbolMode.fixed.value
        self.symbol1 = SymbolMode.symbol1.value
        self.symbol1_name = SymbolMode.symbol1_name.value
        self.th_linestyle = 'solid'
        self.th_line_width = 1.5
        #
        self.theories = {}
        self.num_theories = 0
        self.inactive_files = {}
        self.current_theory = None
        self.table_icon_list = [
        ]  #save the file's marker shape, fill and color there
        self.selected_file = None

        # LOGGING STUFF
        self.logger = logging.getLogger(self.parent_application.logger.name + '.' + self.name)
        self.logger.debug('New DataSet')
        np.seterrcall(self)

    def write(self, msg):
        """Write numpy error logs to the logger"""
        self.logger.debug(msg)

# DATASET STUFF ##########################################################################################################

    def do_list(self, line=""):
        """List files and theories in the current DataSet"""
        self.do_list_files()
        self.do_list_theories()

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
                elif offset==2:
                    prefix="|  |--"
                    done=True
                else:
                    print("Wrong argument for the tree command.")
            except ValueError:
                print("Wrong argument for the tree command.")
        if done:
            for t in self.theories.values():
                print(prefix + Fore.MAGENTA + "%s"%t.name + Fore.RESET)
            for f in self.files:
                print(prefix + "%s"%f.file_name_short)

    def get_tree(self):
        return list(self.theories.keys())

    def change_file_visibility(self, file_name_short, check_state=True):
        """Hide/Show file in the figure"""
        file_matching = []
        for file in self.files:
            if file.file_name_short == file_name_short:  #find changed file
                file_matching.append(file)
        if len(file_matching) == 0:
            raise ValueError('Could not match file \"%s\"' % file_name_short)
            return
        if len(file_matching) > 1:
            raise ValueError(
                'Too many match for file \"%s\"' % file_name_short)
            return

        file_matching[0].active = check_state

        #hide datatable
        dt = file_matching[0].data_table
        for i in range(dt.MAX_NUM_SERIES):
            for nx in range(self.nplots):  #loop over the plots
                dt.series[nx][i].set_visible(check_state)
        #hide theory table
        for th in self.theories.values():
            th.set_th_table_visible(file_matching[0].file_name_short,
                                    check_state)


        #save the check_state to recover it upon change of tab or 'view all' events
        if check_state == False:
            self.inactive_files[file_matching[0]
                                .file_name_short] = file_matching[0]
        else:
            try:
                del self.inactive_files[file_matching[0].file_name_short]
            except KeyError:
                pass
        self.do_plot()

    def do_show_all(self, line):
        """Show all files in the current DataSet"""
        for file in self.files:
            if file.file_name_short not in self.inactive_files:
                file.active = True
                dt = file.data_table
                for i in range(dt.MAX_NUM_SERIES):
                    for nx in range(self.nplots):  #loop over the plots
                        dt.series[nx][i].set_visible(True)
        if self.current_theory:
            self.theories[self.current_theory].do_show()
        self.do_plot("")

    def do_hide_all(self, line):
        """Hide all files in the current DataSet"""
        for file in self.files:
            file.active = False
            dt = file.data_table
            for i in range(dt.MAX_NUM_SERIES):
                for nx in range(self.nplots):  #loop over the plots
                    dt.series[nx][i].set_visible(False)
        for th in self.theories.values():
            th.do_hide()
        self.do_plot("")

    def do_file_hide(self, line):
        """Hide a specific file"""
        done = False
        for index, f in enumerate(self.files):
            if (f.file_name_short == line):
                if not f.active:
                    print("File %s is already hidden"%line)
                    return
                f.active = False
                dt = f.data_table
                for i in range(dt.MAX_NUM_SERIES):
                        for nx in range(self.nplots):
                            dt.series[nx][i].set_visible(False)
                done = True
                self.do_plot()
        if (not done):
            print("File \"%s\" not found" % line)

    def complete_file_hide(self, text, line, begidx, endidx):
        """Complete with the names of files that are currently visible"""
        f_names = [fl.file_name_short for fl in self.files if fl.active]
        if not text:
            completions = f_names[:]
        else:
            completions = [f for f in f_names if f.startswith(text)]
        return completions

    def do_file_show(self, line):
        """Show a specific file"""
        done = False
        for index, f in enumerate(self.files):
            if (f.file_name_short == line):
                if f.active:
                    print("File %s is already visible"%line)
                    return
                f.active = True
                dt = f.data_table
                for i in range(dt.MAX_NUM_SERIES):
                        for nx in range(self.nplots):
                            dt.series[nx][i].set_visible(True)
                done = True
                self.do_plot()
        if (not done):
            print("File \"%s\" not found" % line)

    def complete_file_show(self, text, line, begidx, endidx):
        """Complete with the names of the files in the DataSet that are currently hidden"""
        f_names = [fl.file_name_short for fl in self.files if not fl.active]
        if not text:
            completions = f_names[:]
        else:
            completions = [f for f in f_names if f.startswith(text)]
        return completions

    def do_plot(self, line=""):
        """Plot the current dataset using the current view of the parent application"""
        # view = self.parent_application.current_view

        self.table_icon_list.clear()
        filled = False
        if self.symbolmode == SymbolMode.fixed.value:  #single symbol, empty?
            markers = [self.symbol1]
            marker_names = [self.symbol1_name]
        elif self.symbolmode == SymbolMode.fixedfilled.value:  #single symbol, filled?
            markers = [self.symbol1]
            marker_names = [self.symbol1_name]
            filled = True
        elif self.symbolmode == SymbolMode.variable.value:  #variable symbols, empty
            markers = SymbolMode.allmarkers.value
            marker_names = SymbolMode.allmarkernames.value
        else:  #
            markers = SymbolMode.filledmarkers.value  #variable symbols, filled
            marker_names = SymbolMode.filledmarkernames.value
            filled = True

        if self.colormode == ColorMode.fixed.value:  #single color?
            colors = [self.color1]
        elif self.colormode == ColorMode.variable.value:  #variable colors from palette
            colors = ColorMode.colorpalettes.value[self.palette_name]
        else:
            n = len(self.files) - len(
                self.inactive_files)  #number of files to plot
            if n < 2:
                colors = [self.color1]  # only one color needed
            else:  #interpolate the color1 and color2
                r1, g1, b1, a1 = self.color1
                r2, g2, b2, a2 = self.color2
                dr = (r2 - r1) / (n - 1)
                dg = (g2 - g1) / (n - 1)
                db = (b2 - b1) / (n - 1)
                da = (a2 - a1) / (n - 1)
                colors = []
                for i in range(n):  #create a color palette
                    colors.append((r1 + i * dr, g1 + i * dg, b1 + i * db,
                                   a1 + i * da))

        linelst = itertools.cycle((':', '-', '-.', '--'))
        palette = itertools.cycle((colors))
        markerlst = itertools.cycle((markers))
        marker_name_lst = itertools.cycle((marker_names))
        size = self.marker_size  #if file.size is None else file.size
        width = self.line_width
        #theory settings
        th_linestyle = ThLineMode.linestyles.value[self.th_linestyle]

        for to in self.parent_application.tools:
            to.clean_graphic_stuff()
            if to.active:
                to.Qprint("<hr><h2>Calculating...</h2>")

        for j, file in enumerate(self.files):
            dt = file.data_table

            marker = next(markerlst)  #if file.marker is None else file.marker
            marker_name = next(
                marker_name_lst)  #if file.marker is None else file.marker
            color = next(palette)  #if file.color is None else file.color
            face = color if filled else 'none'
            if self.th_line_mode == ThLineMode.as_data.value:
                th_color = color
            else:
                th_color = self.th_color
            if CmdBase.mode == CmdMode.GUI:
                if file.active:
                    #save file name with associated marker shape, fill and color
                    self.table_icon_list.append((file.file_name_short,
                                                 marker_name, face, color))

            for nx in range(self.nplots):
                view = self.parent_application.multiviews[nx]
                try:
                    x, y, success = view.view_proc(dt, file.file_parameters)
                except TypeError as e:
                    print("in do_plot()", e)
                    return

                ## Apply current shifts to data
                #for i in range(view.n):
                #    if file.isshifted[i]:
                #        if view.log_x:
                #            x[:,i]*=np.power(10, file.xshift[i])
                #        else:
                #            x[:,i]+=file.xshift[i]
                #        if view.log_y:
                #            y[:,i]*=np.power(10, file.yshift[i])
                #        else:
                #            y[:,i]+=file.yshift[i]

                # Apply the currently active tools
                for to in self.parent_application.tools:
                    if file.active and to.active:
                        to.Qprint("<h3>"+file.file_name_short+"</h3>")
                        x, y = to.calculate_all(view.n, x, y, self.parent_application.axarr[nx], color)

                # Apply current shifts to data
                for i in range(view.n):
                    if file.isshifted[i]:
                        if view.log_x:
                            x[:,i]*=np.power(10, file.xshift[i])
                        else:
                            x[:,i]+=file.xshift[i]
                        if view.log_y:
                            y[:,i]*=np.power(10, file.yshift[i])
                        else:
                            y[:,i]+=file.yshift[i]

                for i in range(dt.MAX_NUM_SERIES):
                    if (i < view.n and file.active):
                        dt.series[nx][i].set_data(x[:, i], y[:, i])
                        dt.series[nx][i].set_visible(True)
                        dt.series[nx][i].set_marker(marker)
                        if i == 0:
                            face = color if filled else 'none'
                        elif i == 1: # filled and empty symbols
                            if face == 'none':
                                face = color
                            elif face == color:
                                face = 'none'
                        else:
                            face = color
                            fillstyles=["left", "right", "bottom", "top"]
                            fs = fillstyles[i-2]
                            dt.series[nx][i].set_fillstyle(fs)
                        dt.series[nx][i].set_markerfacecolor(face)
                        dt.series[nx][i].set_markeredgecolor(color)
                        dt.series[nx][i].set_markeredgewidth(width)
                        dt.series[nx][i].set_markersize(size)
                        dt.series[nx][i].set_linestyle('')
                        if (file.active and i == 0):
                            label = ""
                            for pmt in file.file_type.basic_file_parameters:
                                try:
                                    label += pmt + '=' + str(
                                        file.file_parameters[pmt]) + ' '
                                except KeyError as e:  #if parameter missing from data file
                                    self.logger.warning("Parameter %s not found in data file"%e)
                                    # if CmdBase.mode != CmdMode.GUI:
                                    #     print(
                                    #         "Parameter %s not found in data file"
                                    #         % (e))
                            #dt.series[nx][i].set_label(file.file_name_short)
                            dt.series[nx][i].set_label(label)
                        else:
                            dt.series[nx][i].set_label('')
                    else:
                        dt.series[nx][i].set_visible(False)
                        dt.series[nx][i].set_label('')

                for th in self.theories.values():
                    if th.active:
                        th.plot_theory_stuff()
                    tt = th.tables[file.file_name_short]
                    try:
                        x, y, success = view.view_proc(tt,
                                                       file.file_parameters)
                    except Exception as e:
                        print("in do_plot th", e)
                        continue

                    # Apply the currently active tools
                    for to in self.parent_application.tools:
                        if (file.active and to.active and to.applytotheory):
                            to.Qprint("* <i>"+th.name+"</i>")
                            x, y = to.calculate_all(view.n, x, y, self.parent_application.axarr[nx], color)

                    for i in range(tt.MAX_NUM_SERIES):
                        if (i < view.n and file.active and th.active):
                            tt.series[nx][i].set_data(x[:, i], y[:, i])
                            tt.series[nx][i].set_visible(True)
                            if view.with_thline or i > 0:
                                tt.series[nx][i].set_marker('')
                                if i == 1: # 2nd theory line with different style
                                    if self.th_linestyle == 'solid':
                                        th_linestyle = ThLineMode.linestyles.value['dashed']
                                    else:
                                        th_linestyle = ThLineMode.linestyles.value['solid']
                                elif i == 2: # 3rd theory line with different style
                                    if self.th_linestyle == 'solid':
                                        th_linestyle = ThLineMode.linestyles.value['dashdotted']
                                    else:
                                        th_linestyle = ThLineMode.linestyles.value['dotted']
                                else:
                                    th_linestyle = ThLineMode.linestyles.value[self.th_linestyle]
                                tt.series[nx][i].set_linestyle(th_linestyle)
                            else:
                                tt.series[nx][i].set_linestyle('')
                                tt.series[nx][i].set_marker('.')
                                if view.filled:
                                    tt.series[nx][i].set_markerfacecolor(th_color)
                                else:
                                    tt.series[nx][i].set_markerfacecolor('none')
                                tt.series[nx][i].set_markersize(size)

                            tt.series[nx][i].set_linewidth(self.th_line_width)
                            tt.series[nx][i].set_color(th_color)
                            tt.series[nx][i].set_label('')
                            tt.series[nx][i].set_path_effects([pe.Normal()])
                        else:
                            tt.series[nx][i].set_visible(False)
                            tt.series[nx][i].set_label('')
        self.parent_application.update_datacursor_artists()
        self.parent_application.update_plot()

    def do_sort(self, line):
        """Sort files in dataset according to the value of a file parameter

Examples:
    sort Mw,reverse
    sort T

Arguments:
    - Par {[str]} -- File parameter according to which the files will be sorted
    - reverse -- The files will be sorted in reverse order"""
        items = line.split(',')
        if (len(items) == 0):
            print("Wrong number of arguments")
        elif (len(items) == 1):
            fp = items[0]
            rev = False
        elif (len(items) == 2):
            fp = items[0]
            rev = (items[1].strip() == "reverse")
        else:
            print("Wrong number of arguments")

        if self.current_file:
            if fp in self.current_file.file_parameters:
                self.files.sort(
                    key=lambda x: float(x.file_parameters[fp]), reverse=rev)
                self.do_plot()
            elif fp == "File":
                self.files.sort(key=lambda x: x.file_name_short, reverse=rev)
                self.do_plot()
            else:
                self.logger.warning("Parameter %s not found in files" % line)
                # print("Parameter %s not found in files" % line)

    def complete_sort(self, text, line, begidx, endidx):
        """Complete with the list of file parameters of the current file in the current dataset"""
        if (self.current_file == None):
            print("A file must be selected first")
            return
        fp_names = list(self.current_file.file_parameters.keys())
        if not text:
            completions = fp_names[:]
        else:
            completions = [f for f in fp_names if f.startswith(text)]
        return completions

# FILE STUFF ##########################################################################################################

    def do_file_delete(self, line):
        """Delete file from the data set"""
        done = False
        for index, f in enumerate(self.files):
            if (f.file_name_short == line):
                if (self.current_file == f):
                    self.current_file = None
                dt = f.data_table
                for i in range(dt.MAX_NUM_SERIES):
                        for nx in range(self.nplots):
                            self.parent_application.axarr[nx].lines.remove(dt.series[nx][i])
                self.files.remove(f)
                done = True
                self.do_plot()
        if (not done):
            print("File \"%s\" not found" % line)

    def complete_file_delete(self, text, line, begidx, endidx):
        f_names = [fl.file_name_short for fl in self.files]
        if not text:
            completions = f_names[:]
        else:
            completions = [f for f in f_names if f.startswith(text)]
        return completions

    def do_list_files(self, line=""):
        """List the files in the current dataset. Active files are shown with an *. Hidden files are shown with (-)."""
        print("FILES IN THE CURRENT DATASET")
        print("============================")
        for f in self.files:
            if (f == self.current_file):
                c="*"
            else:
                c=" "
            if f.active:
                a=""
            else:
                a="(-)"

            print(Fore.RED + "%s "%c + Fore.RESET + "%s "%f.file_name_short + Fore.CYAN + "%s"%a + Fore.RESET)

    def do_list_files_details(self, line):
        """List the files in the dataset with the file parameters"""
        for f in self.files:
            print(f)

    def do_file_new(self, line):
        """Add an empty file of the given type to the current Data Set

Arguments:
    - line {str} -- TYPE (extension of file) [, NAME (name, optional)]"""
        if (line == ""):
            print("Missing file type")
            return
        items = line.split(',')
        if (len(items) == 0):
            print("Missing file type")
            return
        elif (len(items) == 1):
            ext = items[0]
            fname = os.getcwd() + os.path.sep + "DummyFile%02d" % (
                self.num_files + 1) + "." + ext
        elif (len(items) == 2):
            ext = items[0]
            fname = os.getcwd() + os.path.sep + items[1] + "." + ext
        else:
            print("Wrong number of arguments")

        if (ext in self.parent_application.filetypes):
            self.num_files += 1
            f = File(fname, self.parent_application.filetypes[ext], self,
                     self.parent_application.axarr)
            self.files.append(f)
            self.current_file = f
            #leg=self.current_application.ax.legend([], [], loc='upper left', frameon=True, ncol=2, title='Hello')
            #if leg:
            #    leg.draggable()
            #self.current_application.figure.canvas.draw()
        else:
            print("File type \"%s\" cannot be read by application %s" %
                  (line, self.parent_application.name))

    def complete_file_new(self, text, line, begidx, endidx):
        """Complete new file command"""
        file_types = list(self.parent_application.filetypes.keys())
        if not text:
            completions = file_types[:]
        else:
            completions = [f for f in file_types if f.startswith(text)]
        return completions

    def new_dummy_file(self, fname="", xrange=[], yval=0, zval=[], fparams={}, file_type=None):
        """Create File from xrange and file parameters
        xrange: list of x points
        yval: float
        fparam: dict containing file parameter names and values
        """
        if fname == "":
            filename = "dummy_" + "_".join([pname + "%.3g" % fparams[pname] for pname in fparams]) + "." + file_type.extension
        else:
            filename = fname + "_".join([pname + "%.3g" % fparams[pname] for pname in fparams]) + "." + file_type.extension
        f = File(file_name=filename, file_type=file_type, parent_dataset=self, axarr=self.parent_application.axarr)
        f.file_parameters = fparams
        dt = f.data_table
        dt.num_columns = len(file_type.col_names)
        dt.num_rows = len(xrange)
        dt.data = np.zeros((dt.num_rows, dt.num_columns))
        dt.data[:,0] = xrange
        if isinstance(yval, list):
            for i in range(1, dt.num_columns):
                dt.data[:, i] = yval[:]
        else:
            for i in range(1, dt.num_columns):
                dt.data[:, i] = yval
        if zval != [] and dt.num_columns > 2:
            dt.data[:, 2] = zval[:]

        unique = True
        for file in self.files:
            if f.file_name_short == file.file_name_short:  #check if file already exists in current ds
                unique = False
        if unique:
            self.files.append(f)
            self.current_file = f
            for th_name in self.theories:
                #add a theory table
                self.theories[th_name].tables[
                    f.file_name_short] = DataTable(
                        self.parent_application.axarr,
                        "TH_" + f.file_name_short)
                self.theories[th_name].function(f)
            if CmdBase.mode == CmdMode.GUI:
                return f, True
        else:
            return None, False

    def do_open(self, line):
        """Open file(s)

Arguments:
    - line {str} -- FILENAMES (pattern expansion characters -- \*, ? -- allowed"""
        if CmdBase.mode != CmdMode.GUI:
            f_names = glob.glob(line)
            if not f_names:
                f_names = line.split(
                )  #allow to provide multiple file names separated by a space
        else:
            f_names = line
        newtables = []
        if (line == "" or len(f_names) == 0):
            message = "No valid file names provided"
            if CmdBase.mode != CmdMode.GUI:
                print(message)
                return
            return (message, None, None)
        f_ext = [os.path.splitext(x)[1].split('.')[-1] for x in f_names]
        if (f_ext.count(f_ext[0]) != len(f_ext)):
            message = "File extensions of files must be equal!"
            if CmdBase.mode != CmdMode.GUI:
                print(message)
                print(f_names)
                return
            return (message, None, None)
        if (f_ext[0] in self.parent_application.filetypes):
            ft = self.parent_application.filetypes[f_ext[0]]
            for f in f_names:
                if not os.path.isfile(f):
                    print("File \"%s\" does not exists" % f)
                    continue  # next file name
                df = ft.read_file(f, self, self.parent_application.axarr)
                unique = True
                for file in self.files:
                    if df.file_name_short == file.file_name_short:  #check if file already exists in current ds
                        unique = False
                if unique:
                    self.files.append(df)
                    self.current_file = df
                    newtables.append(df)
                    for th_name in self.theories:
                        #add a theory table
                        self.theories[th_name].tables[
                            df.file_name_short] = DataTable(
                                self.parent_application.axarr,
                                "TH_" + df.file_name_short)
            if CmdBase.mode == CmdMode.GUI:
                return (True, newtables, f_ext[0])
            else:
                self.do_plot()
        else:
            message = "File type \"%s\" does not exists" % f_ext[0]
            if CmdBase.mode != CmdMode.GUI:
                print(message)
                return
            return (message, None, None)

    def do_reload_data(self, line=""):
        """Reload data files in the current DataSet"""
        for file in self.files:
            if not file.active:
                continue
            path = file.file_full_path
            ft = file.file_type
            if not os.path.isfile(path):
                self.logger.warning("Could not open file %s: %s"%(file.file_name_short, path))
                continue
            df = ft.read_file(path, self, None)
            file.header_lines = df.header_lines[:]
            file.file_parameters.clear()
            file.file_parameters.update(df.file_parameters)
            file.data_table.data = np.array(df.data_table.data)
            file.data_table.num_columns = df.data_table.num_columns
            file.data_table.num_rows = df.data_table.num_rows
        self.do_plot("")

    def __listdir(self, root):
        """List directory 'root' appending the path separator to subdirs."""
        res = []
        for name in os.listdir(root):
            path = os.path.join(root, name)
            if os.path.isdir(path):
                name += os.sep
                #name += '/'
            res.append(name)
        return res

    def __complete_path(self, path=None):
        """Perform completion of filesystem path"""
        if not path:
            return self.__listdir('.')

        dirname, rest = os.path.split(path)
        tmp = dirname if dirname else '.'
        res = [
            os.path.join(dirname, p) for p in self.__listdir(tmp)
            if p.startswith(rest)
        ]

        # more than one match, or single match which does not exist (typo)
        if len(res) > 1 or not os.path.exists(path):
            return res
        # resolved to a single directory, so return list of files below it
        if os.path.isdir(path):
            return [os.path.join(path, p) for p in self.__listdir(path)]
        # exact file match terminates this completion
        return [path + ' ']

    def complete_open(self, text, line, begidx, endidx):
        """Complete the file_open command"""
        test = line.split()
        if (len(test) > 1):
            result = self.__complete_path(test[1])
        else:
            result = self.__complete_path()

        return result

        #f_names=[]
        #for f in list(self.parent_application.filetypes.keys()):
        #    pattern='%s**.%s'%(text,f)
        #    #f_names += glob.glob('data/**/*.%s'%f, recursive=True)
        #    f_names += glob.glob(pattern, recursive=True)
        #if not text:
        #    completions = f_names[:]
        #else:
        #    completions = [ f
        #                    for f in f_names
        #                    if f.startswith(text)
        #                    ]
        #return completions

    def do_file_active(self, line):
        """Change active file in the current dataset"""
        done=False
        for f in self.files:
            if (f.file_name_short == line):
                self.current_file = f
                done = True
        if (not done):
            print("File \"%s\" not found" % line)

    complete_file_active = complete_file_delete

    def do_file(self, line):
        """Show the contents of a given file on the screen (if the file name is not specified, it shows the current file)"""
        done = False
        if line=="":
            line=self.current_file.file_name_short
        for index, file in enumerate(self.files):
            if (file.file_name_short == line):
                done = True
                print(Fore.YELLOW + "File: " + Fore.RESET + file.file_name_short)
                print(Fore.CYAN + "Path: " + Fore.RESET + file.file_full_path)
                print(Fore.RED + "Parameters: " + Fore.RESET)
                print(file.file_parameters)
                print(Fore.GREEN + "Header Lines: " + Fore.RESET)
                print(file.header_lines)
                dfile = list(self.parent_application.filetypes.values())[0]
                inspect_header = [a+' [' + b + ']' for a,b in zip(dfile.col_names,dfile.col_units)]
                print(Fore.BLUE + "Column Header: " + Fore.RESET)
                print(inspect_header)
                print(Fore.MAGENTA + "Data: " + Fore.RESET)
                print(file.data_table.data)
        if (not done):
            print("File \"%s\" not found" % line)

    complete_file = complete_file_delete

# THEORY STUFF ##########################################################################################################

    def do_available(self, line):
        """List available filetypes and theories in parent application"""
        self.parent_application.do_available_filetypes()
        self.parent_application.do_available_theories()

    def do_available_filetypes(self, line):
        """List available filetypes in parent application"""
        self.parent_application.do_available_filetypes()

    def do_available_theories(self, line):
        """List available theories in parent application"""
        self.parent_application.do_available_theories()

    def do_delete(self, name):
        """Delete a theory from the current dataset"""
        if name in self.theories.keys():
            self.theories[name].destructor()
            for tt in self.theories[
                    name].tables.values():  # remove matplotlib artist from ax
                for i in range(tt.MAX_NUM_SERIES):
                    for nx in range(self.nplots):
                        self.parent_application.axarr[nx].lines.remove(
                            tt.series[nx][i])
            del self.theories[name]
            self.do_plot("")
        else:
            print("Theory \"%s\" not found" % name)

    def complete_delete(self, text, line, begidx, endidx):
        """Complete delete theory command"""
        th_names = list(self.theories.keys())
        if not text:
            completions = th_names[:]
        else:
            completions = [f for f in th_names if f.startswith(text)]
        return completions

    def do_list_theories(self, line=""):
        """List open theories in current dataset"""
        if len(self.theories)>0:
            print("OPEN THEORIES IN THE CURRENT DATASET")
            print("====================================")
        for t in self.theories.values():
            print(Fore.MAGENTA + "%s:"%t.name + Fore.RESET + (15-len(t.name))*" " + "%s"%t.thname)

    def new(self, line):
        """Create a new theory"""
        """Add a new theory of the type specified to the current Data Set"""
        thtypes = list(self.parent_application.theories.keys())
        if (line in thtypes):
            if (self.current_file is None):
                print("Current dataset is empty\n" "%s was not created" % line)
                return
            self.num_theories += 1
            th_id = ''.join(
                c for c in line
                if c.isupper())  #get the upper case letters of th_name
            th_id = "%s%d" % (th_id, self.num_theories)  #append number
            th = self.parent_application.theories[line](
                th_id, self, self.parent_application.axarr)
            self.theories[th.name] = th
            self.current_theory = th.name
            if self.mode == CmdMode.GUI:
                if th.autocalculate:
                    th.do_calculate('')
                else:
                    th.Qprint("<font color=green><b>Press \"Calculate\"</b></font>")
                return th, th_id
            else:
                if (self.mode == CmdMode.batch):
                    th.prompt = ''
                else:
                    th.prompt = self.prompt[:-2] + '/' + Fore.MAGENTA + th_id + '> '
                if th.autocalculate:
                    th.do_calculate('')
                return th, th_id
        else:
            print("Theory \"%s\" does not exists" % line)
            return None, None

    def do_new(self, line, calculate=True):
        """Add a new theory of the type specified to the current Data Set"""
        thtypes = list(self.parent_application.theories.keys())
        if (line in thtypes):
            if (self.current_file is None):
                print("Current dataset is empty\n" "%s was not created" % line)
                return
            self.num_theories += 1
            #th_id = "%s%02d"%(line,self.num_theories)
            # th_id = ''.join(c for c in line if c.isupper()) #get the upper case letters of th_name
            #th_id = "%s%02d" % (line, self.num_theories)
            th_id = ''.join(
                c for c in line
                if c.isupper())  #get the upper case letters of th_name
            th_id = "%s%d" % (th_id, self.num_theories)  #append number
            th = self.parent_application.theories[line](
                th_id, self, self.parent_application.axarr)
            self.theories[th.name] = th
            self.current_theory = th.name
            if self.mode == CmdMode.GUI:
                if calculate and th.autocalculate:
                    th.do_calculate('')
                else:
                    th.Qprint("<font color=green><b>Press \"Calculate\"</b></font>")
                return th
            else:
                if (self.mode == CmdMode.batch):
                    th.prompt = ''
                else:
                    th.prompt = self.prompt[:-2] + '/' + Fore.MAGENTA + th_id + '> '
                if calculate:
                    th.do_calculate('')
                th.cmdloop()
        else:
            print("Theory \"%s\" does not exists" % line)

    def complete_new(self, text, line, begidx, endidx):
        """Complete new theory command"""
        theory_names = list(self.parent_application.theories.keys())
        if not text:
            completions = theory_names[:]
        else:
            completions = [f for f in theory_names if f.startswith(text)]
        return completions

    def do_switch(self, line):
        """Change the active theory"""
        if line in self.theories.keys():
            th = self.theories[line]
            self.current_theory = line
            th.cmdloop()
        else:
            print("Theory \"%s\" not found" % line)

    complete_switch=complete_delete

    def do_legend(self, line):
        """Show/hide the legend"""
        self.parent_application.do_legend(line)

    def mincol(self, col):
        """Minimum value in table column line of all Files in DataSet"""
        min = 1e100
        for f in self.files:
            minfile = f.mincol(col)
            if minfile < min:
                min = minfile
        return min

    def minpositivecol(self, col):
        """Minimum positive value in table column line of all Files in DataSet"""
        min = 1e100
        for f in self.files:
            minfile = f.minpositivecol(col)
            if minfile < min:
                min = minfile
        return min

    def maxcol(self, col):
        """Maximum value in table column line of all Files in DataSet"""
        max = -1e100
        for f in self.files:
            maxfile = f.maxcol(col)
            if maxfile > max:
                max = maxfile
        return max
