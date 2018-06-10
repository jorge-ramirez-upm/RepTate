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

    def __init__(self, name="Tool", parent_app=None):
        """
        **Constructor**
        
        The following variables should be set by the particular realization of the Tool:
            - parameters     (dict): Parameters of the Tool
        
        Keyword Arguments:
            - name {str} -- Name of Tool (default: {"Tool"})
        """
        super().__init__()

        self.name = name
        self.parent_application = parent_app
        self.parameters = OrderedDict()  # keep the dictionary key in order for the parameter table
        self.active = True  #defines if the Tool is plotted
        self.applytotheory = True # Do we also apply the tool to the theory?

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

    def calculate_all(self, n, x, y, ax=None, color=None):
        """Calculate the tool for all views"""
        newxy = []
        lenx=1e9
        for i in range(n):
            xcopy = x[:, i]
            ycopy = y[:, i]
            xcopy, ycopy = self.calculate(xcopy, ycopy, ax, color)
            newxy.append([xcopy,ycopy])
            lenx=min(lenx, len(xcopy))
        x = np.resize(x, (lenx,n))
        y = np.resize(y, (lenx,n))
        for i in range(n):
            x[:, i] = np.resize(newxy[i][0], lenx)
            y[:, i] = np.resize(newxy[i][1], lenx)
        return x, y

    def calculate(self, x, y, ax=None, color=None):
        return x, y

    def clean_graphic_stuff(self):
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

    def do_activate(self, line):
        self.active = not self.active

    def do_applytotheory(self, line):
        self.applytotheory = not self.applytotheory

    def do_cite(self, line):
        """Print citation information
        
        [description]
        
        Arguments:
            - line {[type]} -- [description]
        """
        if (self.citations != ""):
            self.Qprint("\nCITE: "+self.citations+"\n")

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
            super(Tool, self).default(line)

    def Qprint(self, msg, end='<br>'):
        """[summary]
        
        [description]
        
        Arguments:
            - msg {[type]} -- [description]
        """
        if CmdBase.mode == CmdMode.GUI:
            self.print_signal.emit(msg + end)
        else:
            if end == '<br>':
                end = '\n'
            print(msg, end=end)

    def print_qtextbox(self, msg):
        """Print message in the GUI log text box"""
        self.toolTextBox.insertHtml(msg)
        self.toolTextBox.verticalScrollBar().setValue(
            self.toolTextBox.verticalScrollBar().maximum())
        self.toolTextBox.moveCursor(QTextCursor.End)