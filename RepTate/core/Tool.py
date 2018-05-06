# RepTate: Rheology of Entangled Polymers: Toolkit for the Analysis of Tool and Experiments
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
# Copyright (2018): Jorge Ramirez, Victor Boudara, Universidad Politécnica de Madrid, University of Leeds
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
"""Module Tool

Module that defines the basic structure and properties of a Tool.

"""
import os
import enum
import time
import getpass
import numpy as np
from scipy.stats.distributions import t

from CmdBase import CmdBase, CmdMode
from DataTable import DataTable
from Parameter import Parameter, ParameterType, OptType
from DraggableArtists import DraggableVLine, DraggableHLine, DragType
from PyQt5.QtGui import QTextCursor
from PyQt5.QtCore import pyqtSignal

from collections import OrderedDict


class Tool(CmdBase):
    """Abstract class to describe a Tool
    """
    toolname = ""
    """ toolname {str} -- Tool name """
    description = ""
    """ description {str} -- Description of Tool """
    citations = ""
    """ citations {str} -- Articles that should be cited """

    print_signal = pyqtSignal(str)

    def __init__(self, name="Tool", parent_dataset=None, axarr=None):
        """
        **Constructor**
        
        The following variables should be set by the particular realization of the Tool:
            - parameters     (dict): Parameters of the Tool
            - function       (func): Function that calculates the Tool
            - eps            (real): precision for the tool
        
        Keyword Arguments:
            - name {str} -- Name of Tool (default: {"Tool"})
            - parent_dataset {DataSet} -- DataSet that contains the Tool (default: {None})
            - ax {matplotlib axes} -- matplotlib graph (default: {None})
        """
        super().__init__()

        self.name = name
        self.parent_dataset = parent_dataset
        self.axarr = axarr
        self.ax = axarr[0]  #Tool calculation only on this plot
        self.parameters = OrderedDict()  # keep the dictionary key in order for the parameter table
        self.tables = {}
        self.thtables = {}
        self.function = None
        self.active = True  #defines if the Tool is plotted
        self.axarr[0].autoscale(False)

        # Tool OPTIONS
        self.eps = 1e-4

        ax = self.ax

        # XRANGE for Calculation of the Tool (SHALL WE USE THE RANGE OF THE THEORY?)
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

        # YRANGE for Calculation of the Tool
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

        # Pre-create as many tables as files in the dataset (for both data and 1 active theory)
        for f in parent_dataset.files:
            self.tables[f.file_name_short] = DataTable(
                axarr, "Tool-" + f.file_name_short)
            #initiallize Tool table: important for 'single_file' theories
            ft = f.data_table
            tt = self.tables[f.file_name_short]
            tt.num_columns = ft.num_columns
            tt.num_rows = ft.num_rows
            tt.data = np.zeros((tt.num_rows, tt.num_columns))

            #Repeat the same for 1 active theory
            self.thtables[f.file_name_short] = DataTable(
                axarr, "Tool-TH-" + f.file_name_short)
            #initiallize Tool table: important for 'single_file' theories
            ft = f.data_table
            tt = self.thtables[f.file_name_short]
            tt.num_columns = ft.num_columns
            tt.num_rows = ft.num_rows
            tt.data = np.zeros((tt.num_rows, tt.num_columns))

        self.do_cite("")

        if CmdBase.mode == CmdMode.GUI:
            self.print_signal.connect(self.print_qtextbox)  # Asynchronous print when using multithread

    def precmd(self, line):
        """Calculations before the Tool is calculated
        
        This function could be erased
        This method is called after the line has been input but before
        it has been interpreted. If you want to modifdy the input line
        before execution (for example, variable substitution) do it here.
        
        Arguments:
            - line {[type]} -- [description]
        
        Returns:
            - [type] -- [description]
        """
        super(Tool, self).precmd(line)
        return line

    def update_parameter_table(self):
        """
        Added so that Maxwell modes works in CL
        """
        pass
        
    def handle_actionCalculate_Tool(self):
        """Used only in non GUI mode"""
        self.do_calculate("")

    def do_calculate(self, line):
        """Calculate the Tool"""
        if not self.tables:
            return

        start_time = time.time()
        view = self.parent_dataset.parent_application.current_view
        for f in self.parent_dataset.files:
            self.function(f, view)
        self.do_plot(line)
        self.Qprint("\n---Calculated in %.3g seconds---" %
                               (time.time() - start_time))
        self.do_cite("")

    def do_print(self, line):
        """Print the Tool table associated with the given file name
        
        [description]
        
        Arguments:
            - line {[type]} -- [description]
        """
        if line in self.tables:
            print(self.tables[line].data)
        else:
            print("Tool table for \"%s\" not found" % line)

        if line in self.thtables:
            print(self.thtables[line].data)
        else:
            print("Tool table for theory of \"%s\" not found" % line)

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
        """View and switch the minimization state of the Tool parameters
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

    def plot_tool_stuff(self):
        """[summary]
        
        [description]
        """
        pass

# SAVE Tool STUFF (IS THIS NEEDED?)

    # def do_save(self, line):
        # """Save the results from all Tool calculations to file? 
        
        # [description]
        
        # Arguments:
            # - line {[type]} -- [description]
        # """
        # self.Qprint('Saving calculations(s) of ' + self.name + ' Tool')
        # for f in self.parent_dataset.files:
            # fparam = f.file_parameters
            # ttable = self.tables[f.file_name_short]
            # if line == '':
                # ofilename = os.path.splitext(
                    # f.file_full_path)[0] + '_TH' + os.path.splitext(
                        # f.file_full_path)[1]
            # else:
                # ofilename = os.path.join(line, f.file_name_short + '_Tool' + os.path.splitext(
                        # f.file_full_path)[1])
            # # print("ofilename", ofilename)
            # # print('File: ' + f.file_name_short)
            # fout = open(ofilename, 'w')
            # k = list(f.file_parameters.keys())
            # k.sort()
            # for i in k:
                # fout.write(i + "=" + str(f.file_parameters[i]) + ";")
            # fout.write('\n')
            # fout.write('# Results of ' + self.toolname + ' Tool\n')
            # fout.write('# ')
            # k = list(self.parameters.keys())
            # k.sort()
            # for i in k:
                # fout.write(i + '=' + str(self.parameters[i].value) + '; ')
            # fout.write('\n')
            # fout.write('# Date: ' + time.strftime("%Y-%m-%d %H:%M:%S") +
                       # ' - User: ' + getpass.getuser() + '\n')
            # k = f.file_type.col_names
            # for i in k:
                # fout.write(i + '\t')
            # fout.write('\n')
            # for i in range(ttable.num_rows):
                # for j in range(ttable.num_columns):
                    # fout.write(str(ttable.data[i, j]) + '\t')
                # fout.write('\n')
            # fout.close()

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
        """Set/show xrange for Tool calculation and shows limits
        
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
        """Set/show yrange for Tool calculation and shows limits
        
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


    def do_cite(self, line):
        """Print citation information
        
        [description]
        
        Arguments:
            - line {[type]} -- [description]
        """
        if (self.citations != ""):
            self.Qprint("\nCITE: "+self.citations+"\n")

    def do_plot(self, line):
        """Call the plot from the parent Dataset
        
        [description]
        
        Arguments:
            - line {[type]} -- [description]
        """
        self.parent_dataset.do_plot(line)

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
            super(Tool, self).default(line)

    def do_hide(self):
        """Hide the Tool artists and associated tools
        
        [description]
        """
        self.active = False
        self.set_xy_limits_visible(False, False)  # hide xrange and yrange
        for table in self.tables.values():
            for i in range(table.MAX_NUM_SERIES):
                for nx in range(self.parent_dataset.nplots):
                    table.series[nx][i].set_visible(False)
        try:
            self.show_Tool_extras(False)
        except:  # current Tool has no extras
            # print("current Tool has no extras to hide")
            pass

    def set_tool_table_visible(self, fname, state):
        """Show/Hide all Tool lines related to the file "fname" """
        tt = self.tables[fname]
        for i in range(tt.MAX_NUM_SERIES):
            for nx in range(self.parent_dataset.nplots):
                tt.series[nx][i].set_visible(state)
        tt = self.thtables[fname]
        for i in range(tt.MAX_NUM_SERIES):
            for nx in range(self.parent_dataset.nplots):
                tt.series[nx][i].set_visible(state)

    def do_show(self):
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
        for fname in self.thtables:
            if fname in self.parent_dataset.inactive_files:
                return
            else:
                tt = self.thtables[fname]
                for i in range(tt.MAX_NUM_SERIES):
                    for nx in range(self.parent_dataset.nplots):
                        tt.series[nx][i].set_visible(True)
        try:
            self.show_Tool_extras(True)
        except:  # current Tool has no extras
            # print("current Tool has no extras to show")
            pass
        self.parent_dataset.do_plot("")

    def Qprint(self, msg, end='\n'):
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
        self.thTextBox.insertPlainText(msg)
        self.thTextBox.verticalScrollBar().setValue(
            self.thTextBox.verticalScrollBar().maximum())
        self.thTextBox.moveCursor(QTextCursor.End)