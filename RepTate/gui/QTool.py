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
# Copyright (2018-2023): Jorge Ramirez, Victor Boudara, Universidad Politécnica de Madrid, University of Leeds
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
"""Module QTool

Module that defines the GUI counterpart of the class Tool.

"""

import sys
import ast
import numpy as np

from os.path import dirname, join, abspath
from PySide6.QtWidgets import (
    QWidget,
    QTabWidget,
    QTreeWidget,
    QTreeWidgetItem,
    QFrame,
    QHeaderView,
    QMessageBox,
    QDialog,
    QVBoxLayout,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
    QComboBox,
    QToolBar,
    QAbstractItemView,
)
from PySide6.QtCore import Qt, QSize, Signal
from PySide6.QtGui import QIcon, QCursor, QTextCursor
from RepTate.core.Parameter import OptType, ParameterType
from RepTate.core.units import available_units, units_are_compatible
from math import ceil, floor
from collections import OrderedDict

import logging
from html.parser import HTMLParser


class MLStripper(HTMLParser):
    """Remove HTML tags from string"""

    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return "".join(self.fed)


if getattr(sys, "frozen", False):
    # If the application is run as a bundle, the PyInstaller bootloader
    # extends the sys module by a flag frozen=True and sets the app
    # path into variable _MEIPASS'.
    PATH = sys._MEIPASS
else:
    PATH = dirname(abspath(__file__))
sys.path.append(PATH)
from RepTate.gui.Ui_ToolTab import Ui_ToolTab


class EditToolParametersDialog(QDialog):
    """Create the form used to modify a tool's parameter properties."""

    def __init__(self, parent, p_name):
        super().__init__(parent)
        self.parent_tool = parent
        self.tabs = QTabWidget()
        self.all_pattr = {}
        index = 0
        for pname in self.parent_tool.parameters:
            tab = self.create_param_tab(pname)
            self.tabs.addTab(tab, pname)
            if pname == p_name:
                index = self.tabs.indexOf(tab)
        self.tabs.setCurrentIndex(index)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.tabs)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)
        self.setWindowTitle("Tool Parameters")

    def create_param_tab(self, p_name):
        """Create a form to edit one tool parameter's properties."""
        tab = QWidget()
        layout = QFormLayout()

        p = self.parent_tool.parameters[p_name]
        attr_dict = {}
        for attr_name, attr_value in p.__dict__.items():
            if attr_name == "type":
                widget = QComboBox()
                for option in [
                    "real",
                    "integer",
                    "discrete_real",
                    "discrete_integer",
                    "boolean",
                    "string",
                ]:
                    widget.addItem(option)
                widget.setCurrentText(str(attr_value).split(".")[-1])
            elif attr_name == "opt_type":
                widget = QComboBox()
                for option in ["opt", "nopt", "const"]:
                    widget.addItem(option)
                widget.setCurrentText(str(attr_value).split(".")[-1])
            elif attr_name == "display_flag":
                widget = QComboBox()
                widget.addItem("True")
                widget.addItem("False")
                widget.setCurrentText("%s" % attr_value)
            elif attr_name == "display_unit" and p.quantity and p.internal_unit:
                widget = self._display_unit_widget(p, attr_value)
            elif attr_name in ["value", "error"]:
                continue
            else:
                widget = QLineEdit()
                if attr_name in [
                    "name",
                    "description",
                    "quantity",
                    "internal_unit",
                    "display_unit",
                ]:
                    widget.setReadOnly(True)
                widget.setText("%s" % attr_value)
            layout.addRow("%s:" % attr_name, widget)
            attr_dict[attr_name] = widget

        tab.setLayout(layout)
        self.all_pattr[p_name] = attr_dict
        return tab

    def _display_unit_widget(self, parameter, current_unit):
        try:
            compatible_units = [
                unit.symbol for unit in available_units(parameter.quantity) if units_are_compatible(unit.symbol, parameter.internal_unit)
            ]
        except ValueError:
            compatible_units = []
        if compatible_units:
            widget = QComboBox()
            for unit_symbol in compatible_units:
                widget.addItem(unit_symbol)
            widget.setCurrentText("%s" % current_unit)
            return widget
        widget = QLineEdit()
        widget.setReadOnly(True)
        widget.setText("%s" % current_unit)
        return widget


# class QTool(Ui_ToolTab, QWidget, Tool):
class QTool(QWidget, Ui_ToolTab):
    """Abstract class to describe a tool"""

    toolname = ""
    """ toolname {str} -- Tool name """
    description = ""
    """ description {str} -- Description of Tool """
    citations = []
    """ citations {list of str} -- Articles that should be cited """
    doi = []

    print_signal = Signal(str)

    def __init__(self, name="QTool", parent_app=None):
        """**Constructor**"""
        QWidget.__init__(self)
        Ui_ToolTab.__init__(self)
        # Tool.__init__(self, name=name, parent_app=parent_app)
        # super().__init__(name=name, parent_app=parent_app)
        self.setupUi(self)

        self.name = name
        self.parent_application = parent_app
        self.parameters = OrderedDict()  # keep the dictionary key in order for the parameter table
        self.active = True  # defines if the Tool is plotted
        self.applytotheory = True  # Do we also apply the tool to the theory?

        # LOGGING STUFF
        self.logger = logging.getLogger(self.parent_application.logger.name + "." + self.name)
        self.logger.debug("New " + self.toolname + " Tool")
        # np.seterr(all="call")
        # np.seterr(all="ignore")
        np.seterrcall(self.write)

        self.do_cite("")

        self.print_signal.connect(self.print_qtextbox)  # Asynchronous print when using multithread

        self.tb = QToolBar()
        self.tb.setIconSize(QSize(24, 24))
        self.actionActive.setChecked(True)
        self.actionApplyToTheory.setChecked(True)
        self.tb.addAction(self.actionActive)
        self.tb.addAction(self.actionApplyToTheory)
        self.verticalLayout.insertWidget(0, self.tb)

        # build the tool widget
        self.toolParamTable.setIndentation(0)
        self.toolParamTable.setColumnCount(2)
        self.toolParamTable.setHeaderItem(QTreeWidgetItem(["Parameter", "Value"]))
        self.toolParamTable.header().resizeSections(QHeaderView.ResizeToContents)
        self.toolParamTable.setAlternatingRowColors(True)
        self.toolParamTable.setFrameShape(QFrame.NoFrame)
        self.toolParamTable.setFrameShadow(QFrame.Plain)
        self.toolParamTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.toolTextBox.setReadOnly(True)
        self.toolTextBox.setContextMenuPolicy(Qt.CustomContextMenu)
        self.toolTextBox.customContextMenuRequested.connect(self.toolTextBox_context_menu)

        self.actionActive.triggered.connect(self.handle_actionActivepressed)
        self.actionApplyToTheory.triggered.connect(self.handle_actionApplyToTheorypressed)

        self.toolParamTable.itemDoubleClicked.connect(self.onTreeWidgetItemDoubleClicked)
        self.toolParamTable.itemChanged.connect(self.handle_parameterItemChanged)
        self.toolParamTable.setEditTriggers(QTreeWidget.EditKeyPressed)

    def write(self, type, flag):
        """Write numpy error logs to the logger"""
        self.logger.info("numpy: %s (flag %s)" % (type, flag))

    def destructor(self):
        """If the Tool needs to erase some memory in a special way, any
        child theory must rewrite this funcion"""
        pass

    def precmd(self, line):
        """Calculations before the Tool is calculated

        This function could be erased
        This method is called after the line has been input but before
        it has been interpreted. If you want to modifdy the input line
        before execution (for example, variable substitution) do it here."""
        super(Tool, self).precmd(line)
        return line

    def update_parameter_table(self):
        """Added so that Maxwell modes works in CL. CHECK IF THIS CAN BE REMOVED"""
        pass

    def plot_tool_stuff(self):
        """Special function to plot tool graphical objects"""
        pass

    def calculate_all(self, n, x, y, ax=None, color=None, file_parameters=[]):
        """Calculate the tool for all views"""
        newxy = []
        lenx = 1e9
        for i in range(n):
            self.Qprint("<b>Series %d</b>" % (i + 1))
            xcopy = x[:, i]
            ycopy = y[:, i]
            xcopy, ycopy = self.calculate(xcopy, ycopy, ax, color, file_parameters)
            newxy.append([xcopy, ycopy])
            lenx = min(lenx, len(xcopy))
        x = np.resize(x, (lenx, n))
        y = np.resize(y, (lenx, n))
        for i in range(n):
            x[:, i] = np.resize(newxy[i][0], lenx)
            y[:, i] = np.resize(newxy[i][1], lenx)
        return x, y

    def calculate(self, x, y, ax=None, color=None, file_parameters=[]):
        return x, y

    def clean_graphic_stuff(self):
        pass

    def do_cite(self, line):
        """Print citation information"""
        if len(self.citations) > 1:
            for i in range(len(self.citations)):
                self.Qprint("""<b><font color=red>CITE</font>:</b> <a href="%s">%s</a><p>""" % (self.doi[i], self.citations[i]))

    def do_plot(self, line=""):
        """Update plot"""
        self.parent_application.update_all_ds_plots()

    def set_param_value(self, name, value):
        """Set the value of a parameter of the tool"""
        p = self.parameters[name]
        try:
            if p.type == ParameterType.real:
                try:
                    val = float(value)
                except ValueError:
                    return "Value must be a float", False
                if val < p.min_value:
                    p.value = p.min_value
                    return "Value must be greater than %.4g" % p.min_value, False
                elif val > p.max_value:
                    p.value = p.max_value
                    return "Value must be smaller than %.4g" % p.max_value, False
                else:
                    p.value = val
                    return "", True

            elif p.type == ParameterType.integer:
                try:
                    val = int(value)  # convert to int
                except ValueError:
                    return "Value must be an integer", False
                if val < p.min_value:
                    p.value = p.min_value
                    return "Value must be greater than %d" % p.min_value, False
                elif val > p.max_value:
                    p.value = p.max_value
                    return "Value must be smaller than %d" % p.max_value, False
                else:
                    p.value = val
                    return "", True

            elif p.type == ParameterType.discrete_integer:
                try:
                    val = int(value)  # convert to int
                except ValueError:
                    return "Value must be an integer", False
                if val in p.discrete_values:
                    p.value = val
                    return "", True
                else:
                    message = "Values allowed: " + ", ".join([str(s) for s in p.discrete_values])
                    print(message)
                    return message, False

            elif p.type == ParameterType.discrete_real:
                try:
                    val = float(value)
                except ValueError:
                    return "Value must be a float", False
                if val in p.discrete_values:
                    p.value = val
                    return "", True
                else:
                    message = "Values allowed: " + ", ".join([str(s) for s in p.discrete_values])
                    print(message)
                    return message, False

            elif p.type == ParameterType.boolean:
                if value in [True, "true", "True", "1", "t", "T", "y", "yes"]:
                    p.value = True
                else:
                    p.value = False
                return "", True
            elif p.type == ParameterType.string:
                p.value = value
                return "", True

            else:
                return "", False

        except ValueError as e:
            print("In set_param_value:", e)
            return "", False

    def set_param_value_from_display(self, name, value):
        """Set a tool parameter from the value currently displayed in the GUI."""
        p = self.parameters[name]
        if not (p.internal_unit and p.display_unit):
            return self.set_param_value(name, value)
        try:
            internal_value = p.value_from_display(float(value))
        except ValueError:
            return "Value must be a float", False
        return self.set_param_value(name, internal_value)

    def Qprint(self, msg, end="<br>"):
        """Print a message on the Tool info area"""
        if isinstance(msg, list):
            msg = self.table_as_html(msg)
        self.print_signal.emit(msg + end)

    def table_as_html(self, tab):
        header = tab[0]
        rows = tab[1:]
        nrows = len(rows)
        table = """<table border="1" width="100%">"""
        # header
        table += "<tr>"
        table += "".join(["<th>%s</th>" % h for h in header])
        table += "</tr>"
        # data
        for row in rows:
            table += "<tr>"
            table += "".join(["<td>%s</td>" % d for d in row])
            table += "</tr>"
        table += """</table><br>"""
        return table

    def table_as_ascii(self, tab):
        text = ""
        for row in tab:
            text += " ".join(row)
            text += "\n"
        return text

    def strip_tags(self, html_text):
        s = MLStripper()
        s.feed(html_text)
        return s.get_data()

    def print_qtextbox(self, msg):
        """Print message in the GUI log text box"""
        self.toolTextBox.moveCursor(QTextCursor.End)
        self.toolTextBox.insertHtml(msg)
        self.toolTextBox.verticalScrollBar().setValue(self.toolTextBox.verticalScrollBar().maximum())
        self.toolTextBox.moveCursor(QTextCursor.End)

    def toolTextBox_context_menu(self):
        """Custom contextual menu for the theory textbox"""
        menu = self.toolTextBox.createStandardContextMenu()
        menu.addSeparator()
        menu.addAction("Increase Font Size", lambda: self.change_toolTextBox_fontsize(1.25))
        menu.addAction("Deacrease Font Size", lambda: self.change_toolTextBox_fontsize(0.8))
        menu.addAction("Clear Text", self.toolTextBox.clear)
        menu.exec_(QCursor.pos())

    def change_toolTextBox_fontsize(self, factor):
        """Change the toolTextBox font size by a factor `factor`"""
        font = self.toolTextBox.currentFont()
        if factor < 1:
            font_size = ceil(font.pointSize() * factor)
        else:
            font_size = floor(font.pointSize() * factor)
        font.setPointSize(font_size)
        self.toolTextBox.document().setDefaultFont(font)

    def editItem(self, item, column):
        print(column)

    def update_parameter_table(self):
        """Update the Tool parameter table"""
        previous_block_state = self.toolParamTable.blockSignals(True)
        try:
            # clean table
            self.toolParamTable.clear()

            # populate table
            for param in self.parameters:
                p = self.parameters[param]
                if p.display_flag:  # only allowed param enter the table
                    if p.type == ParameterType.string:
                        item = QTreeWidgetItem(self.toolParamTable, [p.display_label(), p.value])
                    else:
                        item = QTreeWidgetItem(
                            self.toolParamTable,
                            [p.display_label(), "%0.4g" % p.display_value()],
                        )
                    item.setData(0, Qt.UserRole, p.name)
                    item.setToolTip(0, p.description)

                    item.setFlags(item.flags() | Qt.ItemIsEditable)
            self.toolParamTable.header().resizeSections(QHeaderView.ResizeToContents)
        finally:
            self.toolParamTable.blockSignals(previous_block_state)

    def handle_parameterItemChanged(self, item, column):
        """Modify parameter values when changed in the Tool table"""
        param_changed = item.data(0, Qt.UserRole) or item.text(0)
        if column == 0:  # param was checked/unchecked
            if item.checkState(0) == Qt.Checked:
                self.parameters[param_changed].opt_type = OptType.opt
            elif item.checkState(0) == Qt.Unchecked:
                self.parameters[param_changed].opt_type = OptType.nopt
            return
        # else, assign the entered value
        new_value = item.text(1)
        message, success = self.set_param_value_from_display(param_changed, new_value)
        if not success:
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            if message != "":
                msg.setText("Not a valid value\n" + message)
            else:
                msg.setText("Not a valid value")
            msg.exec_()
            item.setText(1, str(self.parameters[param_changed].display_value()))
        self.parent_application.update_all_ds_plots()

    def handle_actionActivepressed(self, checked):
        if checked:
            self.actionActive.setIcon(QIcon(":/Icon8/Images/new_icons/icons8-toggle-on.png"))
        else:
            self.actionActive.setIcon(QIcon(":/Icon8/Images/new_icons/icons8-toggle-off.png"))
        self.actionActive.setChecked(checked)
        self.active = checked
        self.parent_application.update_all_ds_plots()

    # def actionActivepressed(self):
    #     self.active = self.actionActive.isChecked()
    #     self.parent_application.update_all_ds_plots()

    def handle_actionApplyToTheorypressed(self, checked):
        if checked:
            self.actionApplyToTheory.setIcon(QIcon(":/Icon8/Images/new_icons/icons8-einstein-yes.png"))
        else:
            self.actionApplyToTheory.setIcon(QIcon(":/Icon8/Images/new_icons/icons8-einstein-no.png"))
        self.actionApplyToTheory.setChecked(checked)
        self.applytotheory = checked
        self.parent_application.update_all_ds_plots()

    def onTreeWidgetItemDoubleClicked(self, item, column):
        """Start editing text when a table cell is double clicked"""
        if column == 0:
            p_name = item.data(0, Qt.UserRole) or item.text(0)
            dialog = EditToolParametersDialog(self, p_name)
            if dialog.exec_():
                self.apply_tool_parameter_properties(dialog)
        elif column == 1:
            self.toolParamTable.editItem(item, column)

    def apply_tool_parameter_properties(self, dialog):
        """Apply edited tool parameter properties from the properties dialog."""
        for pname in self.parameters:
            p = self.parameters[pname]
            attr_dict = dialog.all_pattr[pname]
            for attr_name, widget in attr_dict.items():
                if attr_name == "type":
                    setattr(p, attr_name, ParameterType[widget.currentText()])
                elif attr_name == "opt_type":
                    setattr(p, attr_name, OptType[widget.currentText()])
                elif attr_name == "display_flag":
                    setattr(p, attr_name, ast.literal_eval(widget.currentText()))
                elif attr_name == "display_unit":
                    if isinstance(widget, QComboBox):
                        val = widget.currentText()
                        if units_are_compatible(val, p.internal_unit):
                            setattr(p, attr_name, val)
                elif attr_name == "discrete_values":
                    val = widget.text()
                    values = ast.literal_eval(val)
                    if isinstance(values, list):
                        setattr(p, attr_name, values)
                elif attr_name in [
                    "name",
                    "description",
                    "quantity",
                    "internal_unit",
                ]:
                    continue
                else:
                    val = float(widget.text())
                    setattr(p, attr_name, val)
        self.update_parameter_table()
        self.parent_application.update_all_ds_plots()
