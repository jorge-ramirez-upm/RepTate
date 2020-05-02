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
"""Module QApplicationWindow

Module that defines the basic GUI class from which all GUI applications are derived.
It is the GUI counterpart of Application.

"""
import io
import re
import traceback
import math
from numpy import *
import numpy as np
from os.path import dirname, join, abspath, isfile, isdir
#import logging
from PyQt5.QtGui import QIcon, QColor, QCursor, QStandardItem, QIntValidator, QDoubleValidator
from PyQt5.uic import loadUiType
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame, QGroupBox, QFormLayout, QLineEdit, QHBoxLayout, QWidget, QToolBar, QToolButton, QMenu, QFileDialog, QMessageBox, QInputDialog, QLineEdit, QHeaderView, QColorDialog, QDialog, QDialogButtonBox, QTreeWidgetItem, QApplication, QTabWidget, QComboBox, QVBoxLayout, QSplitter, QLabel, QTableWidget, QTableWidgetItem, QRadioButton
from RepTate.gui.QDataSet import QDataSet
from RepTate.core.DataTable import DataTable
from RepTate.gui.DataSetWidgetItem import DataSetWidgetItem
from RepTate.core.DataSet import ColorMode, SymbolMode, ThLineMode
from RepTate.core.CmdBase import CmdBase, CmdMode
from RepTate.core.Application import Application
from RepTate.core.DraggableArtists import DragType, DraggableSeries, DraggableNote
from RepTate.gui.SpreadsheetWidget import SpreadsheetWidget
from collections import OrderedDict
from RepTate.gui.ImportExcelWindow import ImportExcelWindow

#To recompile the symbol-settings dialog:
#pyuic5 gui/markerSettings.ui -o gui/markerSettings.py
from RepTate.gui.markerSettings import Ui_Dialog

# I think the following lines are not needed anymore
#try:
#    _fromUtf8 = QtCore.QString.fromUtf8
#except AttributeError:
#    _fromUtf8 = lambda s: s

PATH = dirname(abspath(__file__))
Ui_AppWindow, QMainWindow = loadUiType(join(PATH,'QApplicationWindow.ui'))
Ui_EditAnnotation, QDialog = loadUiType(join(PATH,'annotationedit.ui'))
Ui_AddDummyFiles, QDialog = loadUiType(join(PATH,'dummyfilesDialog.ui'))

class AddDummyFiles(QDialog, Ui_AddDummyFiles):
    def __init__(self, parent=None, filetype=None):
        super(AddDummyFiles, self).__init__(parent)
        QDialog.__init__(self)
        Ui_AddDummyFiles.__init__(self)
        self.setupUi(self)

        for p in filetype.basic_file_parameters:
            item = QTreeWidgetItem(self.parameterTreeWidget,[p,"0","1","10"])
            item.setCheckState(0, 0)
            item.setIcon(0, QIcon())
            item.setFlags(item.flags() | Qt.ItemIsEditable)
            cb = QComboBox(self.parameterTreeWidget)
            cb.addItems(["Linear", "Log"])
            self.parameterTreeWidget.setItemWidget(item, 4, cb)

        for i in range(4):
            self.parameterTreeWidget.setColumnWidth(i,60)

        connection_id = self.parameterTreeWidget.itemDoubleClicked.connect(self.handle_itemDoubleClicked)

    def handle_itemDoubleClicked(self, item, column):
        if (column>0 and column<4):
            self.parameterTreeWidget.editItem(item, column)

class AddFileFunction(QDialog):
    def __init__(self, parent=None, filetype=None):
        super(AddFileFunction, self).__init__(parent)
        QDialog.__init__(self)
        self.filetype = filetype
        self.createParametersGroupBox(filetype)
        self.createColumnsGroupBox(filetype)
        self.createLabelGroupBox()
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.parametersGroupBox)
        mainLayout.addWidget(self.columnsGroupBox)
        mainLayout.addWidget(self.labelGroupBox)
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok
                                     | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)
        self.setWindowTitle("New File from Function")

    def createParametersGroupBox(self, filetype):
        """Create a form to set the new values of important file parameters"""
        self.parametersGroupBox = QGroupBox(
            "Parameters of \"%s\" file" % filetype.name)
        layout = QFormLayout()
        parameters = filetype.basic_file_parameters
        self.param_dict = {}
        self.p_new = []
        for i, pname in enumerate(parameters):  #loop over the Parameters
            self.p_new.append(QLineEdit())
            self.p_new[i].setValidator(QDoubleValidator())
            self.p_new[i].setText("0")
            layout.addRow("%s:" % pname, self.p_new[i])
            self.param_dict[pname] = self.p_new[i]
        self.parametersGroupBox.setLayout(layout)

    def createColumnsGroupBox(self, filetype):
        """Create a form to set the new values the file columns"""
        self.columnsGroupBox = QGroupBox(
            "Columns of \"%s\" file" % filetype.name)
        layout = QFormLayout()
        cols = filetype.col_names
        self.col_dict = {}
        self.c_new = []
        for i, cname in enumerate(cols):  #loop over the Parameters
            self.c_new.append(QLineEdit())
            self.c_new[i].setText("x")
            layout.addRow("%s" % cname, self.c_new[i])
            self.col_dict[cname] = self.c_new[i]
        self.columnsGroupBox.setLayout(layout)

    def createLabelGroupBox(self):
        """Set the range and scale (linear or logarithmic) of the label x"""
        self.labelGroupBox = QGroupBox(
            "Range of label x")
        layout = QFormLayout()
        self.lab_dict = {}
        self.l_new = []
        self.l_new.append(QLineEdit())
        self.l_new[0].setText("0")
        self.l_new[0].setValidator(QDoubleValidator())
        layout.addRow("xmin", self.l_new[0])
        self.lab_dict["xmin"] = self.l_new[0]
        self.l_new.append(QLineEdit())
        self.l_new[1].setText("1000")
        self.l_new[1].setValidator(QDoubleValidator())
        layout.addRow("xmax", self.l_new[1])
        self.lab_dict["xmax"] = self.l_new[1]
        self.l_new.append(QLineEdit())
        self.l_new[2].setText("100")
        self.l_new[2].setValidator(QIntValidator())
        layout.addRow("npoints", self.l_new[2])
        self.lab_dict["npoints"] = self.l_new[2]
        self.l_new.append(QRadioButton())
        self.l_new[3].setText("Linear")
        self.l_new.append(QRadioButton())
        layout.addRow("", self.l_new[3])
        self.l_new[3].setChecked(True)
        self.l_new[4].setText("Logarithmic")
        layout.addRow("", self.l_new[4])
        self.labelGroupBox.setLayout(layout)


class EditAnnotation(QDialog, Ui_EditAnnotation):
    def __init__(self, parent=None, annotation=None):
        super(EditAnnotation, self).__init__(parent)
        QDialog.__init__(self)
        Ui_EditAnnotation.__init__(self)

        self.setupUi(self)

        self.annotation = annotation
        self.textLineEdit.setText(annotation.get_text())
        x, y = annotation.get_position()
        self.xLineEdit.setText('%.4g'%x)
        self.yLineEdit.setText('%.4g'%y)
        color = annotation.get_color()
        col = QColor(color[0]*255, color[1]*255, color[2]*255)
        self.labelFontColor.setStyleSheet("background: %s"%col.name())
        self.rotationSpinBox.setValue(annotation.get_rotation())
        self.hacomboBox.setCurrentText(annotation.get_horizontalalignment())
        self.vacomboBox.setCurrentText(annotation.get_verticalalignment())
        self.fontweightComboBox.setCurrentText(annotation.get_fontweight())
        self.fontstyleComboBox.setCurrentText(annotation.get_fontstyle())
        self.fontsizeannotationSpinBox.setValue(annotation.get_fontsize())
        self.framealphaannotationSpinBox.setValue(annotation.get_alpha())
        self.fontfamilyComboBox.setCurrentText(annotation.get_fontfamily()[0])

        connection_id = self.pickFontColor.clicked.connect(self.handle_pickFontColor)
        connection_id = self.pushApply.clicked.connect(self.apply_changes)
        connection_id = self.pushOK.clicked.connect(self.apply_changes)
        connection_id = self.pushDelete.clicked.connect(self.delete)

        self.color = None

    def showColorDialog(self):
        """Show the color picker and return the picked QtColor or `None`"""
        wtitle = "Select color for the annotation \"%s\""%self.annotation.get_text()
        color = QColorDialog.getColor(title=wtitle,
            options=QColorDialog.DontUseNativeDialog)
        if not color.isValid():
            color = None
        return color

    def apply_changes(self):
        self.annotation.set_text(self.textLineEdit.text())
        self.annotation.set_position((float(self.xLineEdit.text()),float(self.yLineEdit.text())))
        if self.color:
            self.annotation.set_color(self.color.getRgbF())
        self.annotation.set_rotation(self.rotationSpinBox.value())
        self.annotation.set_horizontalalignment(self.hacomboBox.currentText())
        self.annotation.set_verticalalignment(self.vacomboBox.currentText())
        self.annotation.set_fontweight(self.fontweightComboBox.currentText())
        self.annotation.set_fontstyle(self.fontstyleComboBox.currentText())
        self.annotation.set_fontsize(self.fontsizeannotationSpinBox.value())
        self.annotation.set_alpha(self.framealphaannotationSpinBox.value())
        self.annotation.set_family(self.fontfamilyComboBox.currentText())
        self.annotation.figure.canvas.draw()

    def delete(self):
        btns = (QMessageBox.Yes | QMessageBox.No)
        msg = "Do you want to delete the the annotation \"%s\""%self.annotation.get_text()
        title = 'Delete annotation'
        ans = QMessageBox.question(self, title, msg, buttons=btns)
        if ans == QMessageBox.Yes:
            self.annotation.remove()
            self.pushCancel.click()

    def handle_pickFontColor(self):
        """Call the color picker and save the selected legend face color in
        RGB format in the dataset legend info.
        """
        self.color = self.showColorDialog()
        if self.color:
            self.labelFontColor.setStyleSheet("background: %s"%self.color.name())


class ViewShiftFactors(QDialog):
    def __init__(self, parent=None, fnames=None, factorsx=None, factorsy=None):
        super(ViewShiftFactors, self).__init__(parent)

        self.setWindowTitle("View/Edit Shift Factors")
        layout = QVBoxLayout(self)

        nfiles = len(fnames)
        ncurves = len(factorsx[0])

        self.table = SpreadsheetWidget()  #allows copy/paste
        self.table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.table.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.table.setRowCount(nfiles)
        self.table.setColumnCount(2*ncurves)
        hlabels=[]
        for i in range(ncurves):
            hlabels.append("x%d"%(i+1))
        self.table.setHorizontalHeaderLabels(hlabels)
        self.table.setVerticalHeaderLabels(fnames)
        for i in range(nfiles):
            for j in range(ncurves):
                self.table.setItem(i, 2*j, QTableWidgetItem("%g"%factorsx[i][j]))
                self.table.setItem(i, 2*j+1, QTableWidgetItem("%g"%factorsy[i][j]))
        self.table.resizeRowsToContents()
        self.table.resizeColumnsToContents()
        layout.addWidget(self.table)

        # OK and Cancel buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        self.adjustSize()


class QApplicationWindow(Application, QMainWindow, Ui_AppWindow):
    """[summary]

    [description]
    """
    def __init__(self, name='Application Template', parent=None, **kwargs):
        """
        **Constructor**

        Keyword Arguments:
            - parent {[type]} -- [description] (default: {None})

        Returns:
            - [type] -- [description]
        """

        super().__init__(name, parent, **kwargs)

        if CmdBase.mode!=CmdMode.GUI:
            return None

        QMainWindow.__init__(self)
        Ui_AppWindow.__init__(self)

        self.setupUi(self)
        self.name = name
        self.parent_application = parent
        self.tab_count = 0
        self.curves = []
        self.zorder = 100
        self.dir_start = 'Data/' # default folder opened

        # Accept Drag and drop events
        self.setAcceptDrops(True)

        # DataSet Tabs behaviour ##########
        self.DataSettabWidget.setTabsClosable(True)
        #self.DataSettabWidget.setTabBarAutoHide(True)
        self.DataSettabWidget.setUsesScrollButtons(True)
        self.DataSettabWidget.setMovable(True)

        ############################
        # SETUP DATA INSPECTOR PANEL
        # Data Inspector Toolbar
        self.data_inspector_panel_widget = QWidget(self)
        vblayout = QVBoxLayout()
        vblayout.setContentsMargins(0, 0, 0, 0)
        vblayout.setSpacing(0)

        tb = QToolBar()
        tb.setIconSize(QtCore.QSize(24,24))
        tb.addAction(self.actionCopy)
        tb.addAction(self.actionPaste)
        tb.addSeparator()
        tb.addAction(self.actionShiftVertically)
        tb.addAction(self.actionShiftHorizontally)
        tb.addAction(self.actionViewShiftFactors)
        tb.addAction(self.actionSaveShiftFactors)
        tb.addAction(self.actionResetShiftFactors)
        vblayout.addWidget(tb)
        # Shift factors stuff
        self.shiftTable = SpreadsheetWidget(self) # has a 'copy' method
        self.shiftTable.setColumnCount(2)
        self.shiftTable.setRowCount(DataTable.MAX_NUM_SERIES)
        # disable Paste
        self.shiftTable.paste = lambda: None

        self.shiftTable.setHorizontalHeaderLabels(["Xshift", "Yshift"])
        self.shiftTable.horizontalHeader().setStyleSheet("color: blue; font: bold;")
        self.shiftTable.verticalHeader().setStyleSheet("color: blue; font: bold;")
        for i in range(DataTable.MAX_NUM_SERIES):
            for j in range(2):
                item = QTableWidgetItem()
                item.setText("0")
                item.setBackground(QColor(255,255,205))
                self.shiftTable.setItem(i, j, item)
        self.shiftTable.resizeRowsToContents()
        iHeight = 0
        for i in range(DataTable.MAX_NUM_SERIES):
            iHeight += self.shiftTable.verticalHeader().sectionSize(i)
        iHeight += self.shiftTable.horizontalHeader().height()
        self.shiftTable.setFixedHeight(iHeight)
        iWidth = 0
        for i in range(2):
            iWidth += self.shiftTable.horizontalHeader().sectionSize(i)
        iWidth += self.shiftTable.verticalHeader().width()
        self.shiftTable.setMinimumWidth(iWidth)
        self.shiftTable.setVisible(False)
        vblayout.addWidget(self.shiftTable)

        #custom QTable to have the copy/paste/delete features
        self.inspector_table = SpreadsheetWidget(self)
        self.inspector_table.delete_disabled = False
        vblayout.addWidget(self.inspector_table)
        self.data_inspector_panel_widget.setLayout(vblayout)

        ######################
        # VIEW Toolbar
        self.saveViewtoolButton.setDefaultAction(self.actionSave_View)

        ################
        # TOOLS TOOLBAR
        # In the Data Inspector area (at the bottom)
        self.tool_panel_widget = QWidget(self)
        vblayout2 = QVBoxLayout()
        vblayout2.setContentsMargins(0, 0, 0, 0)
        vblayout2.setSpacing(0)

        tb = QToolBar()
        tb.setIconSize(QtCore.QSize(24,24))
        tb.addAction(self.actionNew_Tool)
        self.cbtool = QComboBox()
        model = self.cbtool.model()
        self.cbtool.setToolTip("Choose a Tool")

        item = QStandardItem('Select:')
        item.setForeground(QColor('grey'))
        model.appendRow(item)
        i = 1
        for tool_name in self.availabletools.keys():
            item = QStandardItem(tool_name)
            item.setToolTip(self.availabletools[tool_name].description)
            model.appendRow(item)
            i += 1
        self.cbtool.insertSeparator(i)
        for tool_name in self.extratools.keys():
            item = QStandardItem(tool_name)
            item.setForeground(QColor('blue'))
            item.setToolTip(self.extratools[tool_name].description)
            model.appendRow(item)

        tb.addWidget(self.cbtool)
        vblayout2.addWidget(tb)
        self.TooltabWidget = QTabWidget()
        self.TooltabWidget.setTabsClosable(True)
        self.TooltabWidget.setTabShape(1)
        self.TooltabWidget.setMovable(1)
        self.qtabbar = self.TooltabWidget.tabBar()
        vblayout2.addWidget(self.TooltabWidget)
        self.tool_panel_widget.setLayout(vblayout2)

        # Data inspector and Tool panels separated by spliter
        spliter = QSplitter(QtCore.Qt.Vertical)
        spliter.addWidget(self.data_inspector_panel_widget)
        spliter.addWidget(self.tool_panel_widget)
        spliter.setStretchFactor(0, 1)
        spliter.setStretchFactor(1, 6)
        self.LayoutDataInspector.addWidget(spliter)

        # Dataset Toolbar
        tb = QToolBar()
        tb.setIconSize(QtCore.QSize(24,24))
        tb.addAction(self.actionNew_Empty_Dataset)

        #tb.addAction(self.actionNew_Dataset_From_File)
        tbut = QToolButton()
        tbut.setPopupMode(QToolButton.MenuButtonPopup)
        tbut.setDefaultAction(self.actionNew_Dataset_From_File)
        menu = QMenu()
        menu.addAction(self.actionAddDummyFiles)
        menu.addAction(self.actionAdd_File_With_Function)
        menu.addAction(self.action_import_from_excel)
        tbut.setMenu(menu)
        tb.addWidget(tbut)
        # view all sets / theories
        tbut2 = QToolButton()
        tbut2.setPopupMode(QToolButton.MenuButtonPopup)
        tbut2.setDefaultAction(self.actionView_All_Sets)
        menu2 = QMenu()
        menu2.addAction(self.actionView_All_SetTheories)
        tbut2.setMenu(menu2)
        tb.addWidget(tbut2)
        #
        tb.addAction(self.actionMarkerSettings)
        tb.addAction(self.actionReload_Data)
        tb.addAction(self.actionInspect_Data)
        tb.addAction(self.actionShowFigureTools)
        self.ViewDataTheoryLayout.insertWidget(1, tb)
        self.ViewDataTheorydockWidget.Width=500
        self.ViewDataTheorydockWidget.setTitleBarWidget(QWidget())
        self.actionAutoscale = tb.addAction(QIcon(':/Images/Images/new_icons/icons8-padlock-96.png'), "Lock XY axes")
        self.actionAutoscale.setCheckable(True)


        # Tests TableWidget
        self.inspector_table.setRowCount(30)
        self.inspector_table.setColumnCount(10)
        self.inspector_table.setHorizontalHeaderLabels(['x','y','z','a','b','c','d','e','f','g'])

        # Hide Data Inspector
        self.DataInspectordockWidget.hide()

        self.mplvl.addWidget(self.multiplots)

        self.mpl_toolbar = NavigationToolbar2QT(self.canvas, self)
        self.mpl_toolbar.setIconSize(QtCore.QSize(16, 16))
        self.mpl_toolbar.setFixedHeight(36)
        self.mpl_toolbar.layout().setSpacing(0)
        self.mpl_toolbar.addAction(self.actionTrack_data)
        self.mpl_toolbar.setVisible(False)
        self.mplvl.addWidget(self.mpl_toolbar)


        # self.canvas.draw()
        # self.update_Qplot()
        # LEGEND STUFF
        self.legend = None

        # EVENT HANDLING
        # Matplotlib events
        #connection_id = self.figure.canvas.mpl_connect('resize_event', self.resizeplot)
        connection_id = self.figure.canvas.mpl_connect('pick_event', self.onpick)
        #connection_id = self.figure.canvas.mpl_connect('button_release_event', self.onrelease)
        #connection_id = self.figure.canvas.mpl_connect('scroll_event', self.zoom_wheel)
        #connection_id = self.figure.canvas.mpl_connect('button_press_event', self.on_press)
        #connection_id = self.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)

        connection_id = self.actionShowFigureTools.triggered.connect(self.viewMPLToolbar)
        connection_id = self.actionInspect_Data.triggered.connect(self.showDataInspector)
        connection_id = self.actionNew_Empty_Dataset.triggered.connect(self.handle_createNew_Empty_Dataset)
        connection_id = self.actionNew_Dataset_From_File.triggered.connect(self.openDataset)
        connection_id = self.actionAddDummyFiles.triggered.connect(self.addDummyFiles)
        connection_id = self.actionAdd_File_With_Function.triggered.connect(self.addFileFunction)
        connection_id = self.action_import_from_excel.triggered.connect(self.handle_action_import_from_excel)
        connection_id = self.actionReload_Data.triggered.connect(self.handle_actionReload_Data)
        connection_id = self.actionAutoscale.triggered.connect(self.handle_actionAutoscale)

        connection_id = self.actionNew_Tool.triggered.connect(self.handle_actionNewTool)
        connection_id = self.TooltabWidget.tabCloseRequested.connect(self.handle_toolTabCloseRequested)
        connection_id = self.qtabbar.tabMoved.connect(self.handle_toolTabMoved)

        connection_id = self.viewComboBox.currentIndexChanged.connect(self.handle_change_view)
        connection_id = self.actionSave_View.triggered.connect(self.save_view)
        connection_id = self.sp_nviews.valueChanged.connect(self.sp_nviews_valueChanged)

        connection_id = self.DataSettabWidget.tabCloseRequested.connect(self.close_data_tab_handler)
        connection_id = self.DataSettabWidget.tabBarDoubleClicked.connect(self.handle_doubleClickTab)
        connection_id = self.DataSettabWidget.currentChanged.connect(self.handle_currentChanged)
        connection_id = self.actionView_All_Sets.toggled.connect(self.handle_actionView_All_Sets)
        connection_id = self.actionView_All_SetTheories.triggered.connect(self.handle_actionView_All_SetTheories)
        connection_id = self.actionShiftVertically.triggered.connect(self.handle_actionShiftTriggered)
        connection_id = self.actionShiftHorizontally.triggered.connect(self.handle_actionShiftTriggered)
        connection_id = self.actionViewShiftFactors.triggered.connect(self.handle_actionViewShiftTriggered)
        connection_id = self.actionSaveShiftFactors.triggered.connect(self.handle_actionSaveShiftTriggered)
        connection_id = self.actionResetShiftFactors.triggered.connect(self.handle_actionResetShiftTriggered)
        connection_id = self.DataInspectordockWidget.visibilityChanged.connect(self.handle_inspectorVisibilityChanged)

        connection_id = self.actionMarkerSettings.triggered.connect(self.handle_actionMarkerSettings)

        connection_id = self.actionCopy.triggered.connect(self.inspector_table.copy)
        connection_id = self.actionPaste.triggered.connect(self.inspector_table.paste)

        # Annotation stuff
        #connection_id = self.actionTrack_data.triggered.connect(self.handle_annotation)
        self.graphicnotes = []
        self.artistnotes = []
        #plt.connect('motion_notify_event', self.mpl_motion_event)

        #Setting up the marker-settings dialog
        # self.marker_dic = {'square': 's', 'plus (filled)': 'P', 'point': '.', 'triangle_right': '>', 'hline': '_', 'vline': '|', 'pentagon': 'p', 'tri_left': '3', 'tri_up': '2', 'circle': 'o', 'diamond': 'D', 'star': '*', 'hexagon1': 'h', 'octagon': '8', 'hexagon2': 'H', 'tri_right': '4', 'x (filled)': 'X', 'thin_diamond': 'd', 'tri_down': '1', 'triangle_left': '<', 'plus': '+', 'triangle_down': 'v', 'triangle_up': '^', 'x': 'x'}
        self.dialog = QDialog()
        self.dialog.ui = Ui_Dialog()
        self.dialog.ui.setupUi(self.dialog)
        self.populate_cbSymbolType()
        self.populate_cbPalette()
        self.populate_cbTheoryLine()
        self.color1 = None
        self.color2 = None
        self.color_th = None
        self.legend_opts = {'loc':'best', 'ncol':1, 'fontsize':12, 'title_fontsize':12, 'markerfirst':True, 'frameon':True, 'fancybox':True, 'shadow':True, 'framealpha':None, 'facecolor':None, 'edgecolor':None, 'mode':None, 'title':None, 'borderpad': None, 'labelspacing':None, 'handletextpad':None, 'columnspacing':None}
        self.annotation_opts = {'alpha': 1.0, 'color': QColor(0, 0, 0).getRgbF(), 'family':'sans-serif', 'horizontalalignment':'center', 'rotation': 0.0, 'fontsize':16, 'style': 'normal',  'verticalalignment': 'center', 'fontweight':'normal'}

        # dialog import data from excel
        self.excel_import_gui = None

        self.legend_draggable = True
        self.default_legend_labels = True
        self.legend_labels = ""
        # self.populate_markers()
        self.fparam_backup = [] #temporary storage of the file parameters
        self.dialog.ui.spinBox.setSingleStep(3) #increment in the marker size dialog
        connection_id = self.dialog.ui.pickColor1.clicked.connect(self.handle_pickColor1)
        connection_id = self.dialog.ui.pickColor2.clicked.connect(self.handle_pickColor2)
        connection_id = self.dialog.ui.pickThColor.clicked.connect(self.handle_pickThColor)
        connection_id = self.dialog.ui.pickFaceColor.clicked.connect(self.handle_pickFaceColor)
        connection_id = self.dialog.ui.pickEdgeColor.clicked.connect(self.handle_pickEdgeColor)
        connection_id = self.dialog.ui.pickFontColor.clicked.connect(self.handle_pickFontColor)
        connection_id = self.dialog.ui.pickFontColor_ax.clicked.connect(self.handle_pickFontColor_ax)
        connection_id = self.dialog.ui.pickFontColor_label.clicked.connect(self.handle_pickFontColor_label)
        connection_id = self.dialog.ui.reset_all_pb.clicked.connect(self.handle_reset_all_pb)
        connection_id = self.dialog.ui.rbEmpty.clicked.connect(self.populate_cbSymbolType)
        connection_id = self.dialog.ui.rbFilled.clicked.connect(self.populate_cbSymbolType)
        connection_id = self.dialog.ui.pushApply.clicked.connect(self.handle_apply_button_pressed)

        self.dataset_actions_disabled(True)
        self.sp_nviews.setMaximum(self.nplot_max)
        # connection_id = self.checkBoxColor.toggled.connect(self)
        # TEST GET CLICKABLE OBJECTS ON THE X AXIS
        #xaxis = self.ax.get_xticklabels()
        #print (xaxis)

    def sp_nviews_valueChanged(self, new_nplots):
        """Change the current number of views displayed in the app"""
        self.nplots = new_nplots
        self.multiplots.reorg_fig(new_nplots)

    def save_view(self):
        dir_start = "data/"
        dilogue_name = "Select Folder for Saving data in Current View as txt"
        folder = QFileDialog.getExistingDirectory(self, dilogue_name, dir_start)
        if isdir(folder):
            ds = self.DataSettabWidget.currentWidget()
            if ds:
                nfout = 0
                for f in ds.files:
                    if f.active:
                        series = f.data_table.series
                        all_views_data = OrderedDict()
                        max_row_len = 0
                        max_view_name_len = 0
                        for nx, view in enumerate(self.multiviews):
                            max_view_name_len = max(max_view_name_len, len(view.name) + 3)
                            data_view = []
                            for i in range(view.n):
                                x, y = series[nx][i].get_data()
                                if i > 0 and np.array_equal(x, data_view[0][0]):
                                    # if x1=x2, only use y
                                    data_view.append([y,])
                                else:
                                    data_view.append([x,y])
                                max_row_len = max(max_row_len, len(series[nx][i].get_data()[0]) )
                            all_views_data[view.name] = data_view

                        nviews = len(self.multiviews)
                        with open(join(folder, f.file_name_short) + '_VIEW.txt', 'w') as fout:
                            # header with file parameters
                            fout.write('#view(s)=[%s];' % (', '.join([v.name for v in self.multiviews])))
                            for pname in f.file_parameters:
                                fout.write('%s=%s;' % (pname, f.file_parameters[pname]))
                            fout.write('\n')

                            # column titles
                            field_width = []
                            for view_name in all_views_data:
                                view = self.views[view_name]
                                snames_index = 0
                                for xy in all_views_data[view_name]:
                                    # loop over the different series in the view "view_name"
                                    if len(xy) > 1:
                                        # case where there is x and y series
                                        fw1 = max(len(view.x_label), 15)
                                        fw2 = max(len(view.snames[snames_index]), 15)
                                        fout.write('{0:<{1}s}\t'.format(view.x_label, fw1))
                                        fout.write('{0:<{1}s}\t'.format(view.snames[snames_index], fw2))
                                        field_width.append(fw1)
                                        field_width.append(fw2)
                                    else:
                                        # case where there is y series only
                                        fw = max(len(view.snames[snames_index]), 15)
                                        fout.write('{0:{1}s}\t'.format(view.snames[snames_index], fw))
                                        field_width.append(fw)
                                    snames_index += 1
                            fout.write('\n')

                            # data lines
                            for i in range(max_row_len):
                                fw_index = 0 # field_width index
                                for view_name in all_views_data:
                                    data_view = all_views_data[view_name]
                                    for xy in data_view:
                                        if len(xy) > 1:
                                            # case where there is x and y series
                                            fw1 = field_width[fw_index]
                                            fw2 = field_width[fw_index + 1]
                                            fw_index += 2
                                            try:
                                                fout.write('{0:<{1}.8e}\t'.format(xy[0][i], fw1))
                                                fout.write('{0:<{1}.8e}\t'.format(xy[1][i], fw2))
                                            except:
                                                fout.write('{0:{1}s}\t'.format('', fw1))
                                                fout.write('{0:{1}s}\t'.format('', fw2))
                                        else:
                                            # case where there is y series only
                                            fw = field_width[fw_index]
                                            fw_index += 1
                                            try:
                                                fout.write('{0:<{1}.8e}\t'.format(xy[0][i], fw1))
                                            except:
                                                fout.write('{0:{1}s}\t'.format('', fw))
                                fout.write('\n')
                        nfout += 1

            QMessageBox.warning(self, "Saving views", "Wrote %d file(s) ending \"_VIEW.txt\" in \"%s/\"" % (nfout, folder))


    def handle_actionNewTool(self):
        """Create new tool"""
        if self.cbtool.currentIndex() == 0:
            # by default, open first tool in the list
            tool_name = self.cbtool.itemText(1)
        else:
            tool_name = self.cbtool.currentText()
        # reset the combobox selection
        self.cbtool.setCurrentIndex(0)
        if tool_name != '':
            self.new_tool(tool_name)
            self.update_all_ds_plots()

    def new_tool(self, tool_name, tool_tab_id=""):
        """Create new tool"""
        newtool = self.do_tool_new(tool_name)

        # add new tool tab
        if tool_tab_id == "":
            tool_tab_id = newtool.name
            tool_tab_id = ''.join(
                c for c in tool_tab_id
                if c.isupper())  #get the upper case letters of tool_name
            tool_tab_id = "%s%d" % (tool_tab_id, self.num_tools)  #append number
        index = self.TooltabWidget.addTab(newtool, tool_tab_id)
        self.TooltabWidget.setCurrentIndex(index)  #set new tool tab as curent tab
        self.TooltabWidget.setTabToolTip(index, tool_name)  #set new-tab tool tip
        return newtool

    def handle_toolTabCloseRequested(self, index):
        """Delete a Tool tab"""
        tool_name = self.TooltabWidget.widget(index).name
        self.do_tool_delete(tool_name)  #call DataSet.do_theory_delete
        self.TooltabWidget.removeTab(index)
        self.update_all_ds_plots()

    def handle_toolTabMoved(self, f, t):
        self.tools.insert(f, self.tools.pop(t))
        self.update_all_ds_plots()


    def handle_actionAutoscale(self, checked):
        self.autoscale = not checked
        if self.autoscale:
            self.actionAutoscale.setIcon(QIcon(':/Images/Images/new_icons/icons8-padlock-96.png'))
        else:
            self.actionAutoscale.setIcon(QIcon(':/Images/Images/new_icons/icons8-lock-96.png'))

    def dataset_actions_disabled(self, state):
        """Disable buttons when there is no file in the dataset

        [description]

        Arguments:
            - state {[type]} -- [description]
        """
        self.actionMarkerSettings.setDisabled(state)
        self.viewComboBox.setDisabled(state)
        self.actionSave_View.setDisabled(state)
        self.actionReload_Data.setDisabled(state)
        self.actionInspect_Data.setDisabled(state)
        self.actionShowFigureTools.setDisabled(state)
        self.actionView_All_Sets.setDisabled(state)
        self.actionAutoscale.setDisabled(state)

        ds = self.DataSettabWidget.currentWidget()
        if ds:
            ds.actionNew_Theory.setDisabled(state)
            ds.cbtheory.setDisabled(state)

    def add_annotation(self, action_trig=False, text=None, x=0, y=0, annotation_opts={}):
        if self.current_viewtab == 0:
            ax = self.axarr[0]
        else:
            ax = self.axarr[self.current_viewtab - 1]
        if text is None:
            # annotation from user
            if self._event is None:
                return
            if self._annotation_done:
                return
            text, ok = QInputDialog.getText(self, 'Annotation (LaTeX allowed)', 'Enter the annotation text:')
            if ok:
                ann = ax.annotate(text, xy=(self._event.xdata, self._event.ydata), xytext=(self._event.xdata, self._event.ydata), **self.annotation_opts)
                self.graphicnotes.append(ann)
                self.artistnotes.append(DraggableNote(ann, DragType.both, None, self.edit_annotation))
                self.canvas.draw()
            self._annotation_done = True
        else:
            # annotation from project loading
            ann = ax.annotate(text, xy=(x, y), **annotation_opts)
            self.graphicnotes.append(ann)
            self.artistnotes.append(DraggableNote(ann, DragType.both, None, self.edit_annotation))
            self.canvas.draw()

    def edit_annotation(self, artist):
        d = EditAnnotation(self, artist)
        d.exec_()
        self.canvas.draw()

    def update_legend(self):
        if self.current_viewtab == 0:
            ax = self.axarr[0]
        else:
            ax = self.axarr[self.current_viewtab - 1]

        if not (self.dialog.ui.cb_show_legend.isChecked() and self.DataSettabWidget.currentWidget()):
            # remove legend when button unchecked or when no dataset
            try:
                self.legend.remove()
            except:
                pass # no legend to remove
        else:
            L=[]
            N=[]
            ds = self.DataSettabWidget.currentWidget()
            if self.default_legend_labels:
                # set default legend from app parameters
                self.legend_labels = r""
                ftype = list(self.filetypes.values())[0]
                for p in ftype.basic_file_parameters:
                    self.legend_labels += p + ' = [' + p + '] '
            params = re.findall(r"\[([A-Za-z0-9_]+)\]", self.legend_labels)
            for j, file in enumerate(ds.files):
                if file.active:
                    dt = file.data_table
                    s = dt.series[0][0]
                    L.append(s)
                    label = self.legend_labels
                    for p in params:
                        if p in file.file_parameters:
                            val = file.file_parameters[p]
                            try:
                                val = "%g" % float(val) #format number
                            except ValueError:
                                pass
                            label = label.replace('['+p+']', str(val))
                    N.append(label)
            try:
                self.legend = ax.legend(L, N, **self.legend_opts)
            except TypeError:
                # "title_fontsize" key invalid for Matplotlib < 3.0.0
                tempdic = self.legend_opts.copy()
                tempdic.pop("title_fontsize", None)
                self.legend = ax.legend(L, N, **tempdic)

            self.legend.set_draggable(self.legend_draggable)

            try:
                self.canvas.draw()
            except Exception as e:
                txt=""
                txt+="Exception: %s\n"%traceback.format_exc()
                txt+="\nPlease, check the TITLE and/or LEGEND below:\n\n"
                if (self.legend_opts["title"]!=None):
                    txt+="TITLE: "+self.legend_opts["title"]+"\n"
                txt+="FIRST LEGEND ITEM: "+N[0]
                QMessageBox.warning(self, 'Wrong Title or labels in legend', txt)

    def populate_cbPalette(self):
        """Populate the list color palettes in the marker-settings dialog

        [description]
        """
        for palette in sorted(ColorMode.colorpalettes.value):
            self.dialog.ui.cbPalette.addItem(palette)

    def populate_cbTheoryLine(self):
        """Populate the list theory linestyle in the marker-settings dialog

        [description]
        """
        for ls in ThLineMode.linestyles.value:
            self.dialog.ui.cbTheoryLine.addItem(ls)

    def populate_cbSymbolType(self):
        """Populate the list of the markers in the marker-settings dialog

        Populate the list of the markers of the marker-settings dialog
        with filled or empty markers, depending on the user's choice
        """
        self.dialog.ui.cbSymbolType.clear()
        if self.dialog.ui.rbFilled.isChecked(): #combobox with fillable symbols only
            for m in SymbolMode.filledmarkernames.value:
                ipath = ':/Markers/Images/Matplotlib_markers/marker_%s.png'%m
                self.dialog.ui.cbSymbolType.addItem(QIcon(ipath), m)
        else: #combobox with all symbols only
            for m in SymbolMode.allmarkernames.value:
                ipath = ':/Markers/Images/Matplotlib_markers/marker_%s.png'%m
                self.dialog.ui.cbSymbolType.addItem(QIcon(ipath), m)

    def handle_pickColor1(self):
        """Call the color picker and save the selected color to `color1` in RGB format

        [description]
        """
        color = self.showColorDialog()
        if color: #check for none
            self.dialog.ui.labelPickedColor1.setStyleSheet("background: %s"%color.name())
            self.color1 = color.getRgbF()

    def handle_pickColor2(self):
        """Call the color picker and save the selected color to `color2` in
        RGB format used for gradient color type

        [description]
        """
        color = self.showColorDialog()
        if color:
            self.dialog.ui.labelPickedColor2.setStyleSheet("background: %s"%color.name())
            self.color2 = color.getRgbF()

    def handle_pickThColor(self):
        """Call the color picker and save the selected theory line color in
        RGB format used for gradient color type

        [description]
        """
        color = self.showColorDialog()
        if color:
            self.dialog.ui.labelThPickedColor.setStyleSheet("background: %s"%color.name())
            self.color_th = color.getRgbF()

    def handle_pickFaceColor(self):
        """Call the color picker and save the selected legend face color in
        RGB format in the dataset legend info.
        """
        color = self.showColorDialog()
        if color:
            self.dialog.ui.labelFaceColor.setStyleSheet("background: %s"%color.name())
            self.legend_opts['facecolor']=color.getRgbF()

    def handle_pickEdgeColor(self):
        """Call the color picker and save the selected legend face color in
        RGB format in the dataset legend info.
        """
        color = self.showColorDialog()
        if color:
            self.dialog.ui.labelEdgeColor.setStyleSheet("background: %s"%color.name())
            self.legend_opts['edgecolor']=color.getRgbF()

    def handle_pickFontColor(self):
        """Call the color picker and save the selected legend face color in
        RGB format in the dataset legend info.
        """
        color = self.showColorDialog()
        if color:
            self.dialog.ui.labelFontColor.setStyleSheet("background: %s"%color.name())
            self.annotation_opts['color']=color.getRgbF()

    def handle_pickFontColor_ax(self):
        """Call the color picker and save the selected legend face color in
        RGB format in the dataset legend info.
        """
        color = self.showColorDialog()
        if color:
            self.dialog.ui.labelFontColor_ax.setStyleSheet("background: %s"%color.name())
            self.ax_opts['color_ax'] = color.getRgbF()

    def handle_pickFontColor_label(self):
        """Call the color picker and save the selected legend face color in
        RGB format in the dataset legend info.
        """
        color = self.showColorDialog()
        if color:
            self.dialog.ui.labelFontColor_label.setStyleSheet("background: %s"%color.name())
            self.ax_opts['color_label'] = color.getRgbF()

    def handle_reset_all_pb(self):
        self.ax_opts = self.ax_opt_defaults.copy()
        self.set_axis_marker_settings()

    def showColorDialog(self):
        """Show the color picker and return the picked QtColor or `None`

        [description]

        Returns:
            - [type] -- [description]
        """
        ds = self.DataSettabWidget.currentWidget()
        if ds:
            wtitle = "Select color for %s"%ds.name
            color = QColorDialog.getColor(title=wtitle,
                options=QColorDialog.DontUseNativeDialog)
            if not color.isValid():
                color = None
            return color

    def handle_actionMarkerSettings(self):
        """Show the dialog box where the user can change
        the marker properties: size, shape, color, fill

        [description]
        """
        ds = self.DataSettabWidget.currentWidget()
        if not ds:
            return
        self.fparam_backup = []
        for file in ds.files:
            self.fparam_backup.append([file.color, file.marker, file.size, file.filled])

        #preset the colors in the labels
        col = QColor(ds.color1[0]*255, ds.color1[1]*255, ds.color1[2]*255)
        self.dialog.ui.labelPickedColor1.setStyleSheet("background: %s"%col.name())
        col = QColor(ds.color2[0]*255, ds.color2[1]*255, ds.color2[2]*255)
        self.dialog.ui.labelPickedColor2.setStyleSheet("background: %s"%col.name())
        col = QColor(ds.th_color[0]*255, ds.th_color[1]*255, ds.th_color[2]*255)
        self.dialog.ui.labelThPickedColor.setStyleSheet("background: %s"%col.name())
        #preset the spinbox
        self.dialog.ui.spinBox.setValue(ds.marker_size)
        self.dialog.ui.spinBoxLineW.setValue(ds.line_width)
        self.dialog.ui.sbThLineWidth.setValue(ds.th_line_width)
        #preset radioButtons
            #symbols
        is_fixed = ds.symbolmode == SymbolMode.fixed.value
        self.dialog.ui.rbFixedSymbol.setChecked(is_fixed)
        # self.dialog.ui.rbVariableSymbol.setChecked(not is_fixed)
        self.dialog.ui.cbSymbolType.setDisabled(not is_fixed)
        #preset the color combobox
        ind = self.dialog.ui.cbPalette.findText(ds.palette_name)
        self.dialog.ui.cbPalette.setCurrentIndex(ind)
        #preset radiobutton theory
        if ds.th_line_mode == ThLineMode.as_data.value:
            self.dialog.ui.rbThSameColor.click()
        else:
            self.dialog.ui.rbThFixedColor.click()


            #colors
        # self.dialog.ui.rbFixedColor.setChecked(False)
        # self.dialog.ui.rbGradientColor.setChecked(False)
        # self.dialog.ui.rbPalette.setChecked(False)
        if ds.colormode == ColorMode.fixed.value:
            self.dialog.ui.rbFixedColor.click()
        elif ds.colormode == ColorMode.gradient.value:
            self.dialog.ui.rbGradientColor.click()
        else:
            self.dialog.ui.rbPalette.click()

        # Legend stuff
        self.dialog.ui.locationComboBox.setCurrentText(self.legend_opts['loc'])
        self.dialog.ui.colSpinBox.setValue(self.legend_opts['ncol'])
        self.dialog.ui.fontsizeSpinBox.setValue(self.legend_opts['fontsize'])
        self.dialog.ui.markerfirstCheckBox.setChecked(self.legend_opts['markerfirst'])
        self.dialog.ui.frameonCheckBox.setChecked(self.legend_opts['frameon'])
        self.dialog.ui.fancyboxCheckBox.setChecked(self.legend_opts['fancybox'])
        self.dialog.ui.shadowCheckBox.setChecked(self.legend_opts['shadow'])
        if (self.legend_opts['framealpha']==None):
            self.dialog.ui.framealphaCheckBox.setChecked(False)
            self.dialog.ui.framealphaSpinBox.setValue(0.0)
        else:
            self.dialog.ui.framealphaCheckBox.setChecked(True)
            self.dialog.ui.framealphaSpinBox.setValue(self.legend_opts['framealpha'])
        if (self.legend_opts['facecolor']==None):
            self.dialog.ui.facecolorCheckBox.setChecked(False)
        else:
            self.dialog.ui.facecolorCheckBox.setChecked(True)
            col = QColor(self.legend_opts['facecolor'][0]*255, self.legend_opts['facecolor'][1]*255, self.legend_opts['facecolor'][2]*255)
            self.dialog.ui.labelFaceColor.setStyleSheet("background: %s"%col.name())
        if (self.legend_opts['edgecolor']==None):
            self.dialog.ui.edgecolorCheckBox.setChecked(False)
        else:
            self.dialog.ui.edgecolorCheckBox.setChecked(True)
            col = QColor(self.legend_opts['edgecolor'][0]*255, self.legend_opts['edgecolor'][1]*255, self.legend_opts['edgecolor'][2]*255)
            self.dialog.ui.labelEdgeColor.setStyleSheet("background: %s"%col.name())
        self.dialog.ui.modeCheckBox.setChecked(self.legend_opts['mode']=='expand')
        if (self.legend_opts['title']==None):
            self.dialog.ui.legendtitleCheckBox.setChecked(False)
        else:
            self.dialog.ui.legendtitleCheckBox.setChecked(True)
            self.dialog.ui.legendtitleStr.setText(self.legend_opts['title'])
        if (self.legend_opts['borderpad']==None):
            self.dialog.ui.borderpadCheckBox.setChecked(False)
        else:
            self.dialog.ui.borderpadCheckBox.setChecked(True)
            self.dialog.ui.borderpadSpinBox.setValue(self.legend_opts['borderpad'])
        if (self.legend_opts['labelspacing']==None):
            self.dialog.ui.labelspacingCheckBox.setChecked(False)
        else:
            self.dialog.ui.labelspacingCheckBox.setChecked(True)
            self.dialog.ui.labelspacingSpinBox.setValue(self.legend_opts['labelspacing'])
        if (self.legend_opts['handletextpad']==None):
            self.dialog.ui.handletextpadCheckBox.setChecked(False)
        else:
            self.dialog.ui.handletextpadCheckBox.setChecked(True)
            self.dialog.ui.handletextpadSpinBox.setValue(self.legend_opts['handletextpad'])
        if (self.legend_opts['columnspacing']==None):
            self.dialog.ui.columnspacingCheckBox.setChecked(False)
        else:
            self.dialog.ui.columnspacingCheckBox.setChecked(True)
            self.dialog.ui.columnspacingSpinBox.setValue(self.legend_opts['columnspacing'])
        if (self.default_legend_labels == True):
            self.dialog.ui.legendlabelCheckBox.setChecked(False)
            str = ""
            ftype = list(self.filetypes.values())[0]
            for p in ftype.basic_file_parameters:
                str += p + ' = [' + p + '] '
            self.dialog.ui.legendlabelStr.setText(str)
        else:
            self.dialog.ui.legendlabelCheckBox.setChecked(True)
            self.dialog.ui.legendlabelStr.setText(self.legend_labels)
        self.dialog.ui.draggableCheckBox.setChecked(self.legend_draggable)


        # Annotation stuff
        self.dialog.ui.rotationSpinBox.setValue(self.annotation_opts['rotation'])
        self.dialog.ui.hacomboBox.setCurrentText(self.annotation_opts['horizontalalignment'])
        self.dialog.ui.vacomboBox.setCurrentText(self.annotation_opts['verticalalignment'])
        col = QColor(self.annotation_opts['color'][0]*255, self.annotation_opts['color'][1]*255, self.annotation_opts['color'][2]*255)
        self.dialog.ui.labelFontColor.setStyleSheet("background: %s"%col.name())
        self.dialog.ui.fontweightComboBox.setCurrentText(self.annotation_opts['fontweight'])
        self.dialog.ui.fontstyleComboBox.setCurrentText(self.annotation_opts['style'])
        self.dialog.ui.fontsizeannotationSpinBox.setValue(self.annotation_opts['fontsize'])
        self.dialog.ui.framealphaannotationSpinBox.setValue(self.annotation_opts['alpha'])
        self.dialog.ui.fontfamilyComboBox.setCurrentText(self.annotation_opts['family'])
        #Axis stuff
        self.set_axis_marker_settings()

        success = self.dialog.exec_() #this blocks the rest of the app as opposed to .show()
        if success == 1:
            self.handle_apply_button_pressed()
        else:
            ds.do_plot()

    def set_axis_marker_settings(self):
        col = QColor(self.ax_opts['color_label'][0]*255, self.ax_opts['color_label'][1]*255, self.ax_opts['color_label'][2]*255)
        self.dialog.ui.labelFontColor_label.setStyleSheet("background: %s"%col.name())
        col = QColor(self.ax_opts['color_ax'][0]*255, self.ax_opts['color_ax'][1]*255, self.ax_opts['color_ax'][2]*255)
        self.dialog.ui.labelFontColor_ax.setStyleSheet("background: %s"%col.name())
        self.dialog.ui.fontweightComboBox_ax.setCurrentText(self.ax_opts['fontweight'])
        self.dialog.ui.fontstyleComboBox_ax.setCurrentText(self.ax_opts['style'])
        self.dialog.ui.fontsizeSpinBox_ax.setValue(self.ax_opts['fontsize'])
        self.dialog.ui.fontfamilyComboBox_ax.setCurrentText(self.ax_opts['family'])
        self.dialog.ui.axis_thickness_cb.setValue(self.ax_opts['axis_thickness'])
        self.dialog.ui.tick_label_size_cb.setValue(self.ax_opts['tick_label_size'])
        self.dialog.ui.grid_cb.setChecked(bool(self.ax_opts['grid']))
        self.dialog.ui.label_size_auto_cb.setChecked(bool(self.ax_opts['label_size_auto']))
        self.dialog.ui.tick_label_size_auto_cb.setChecked(bool(self.ax_opts['tick_label_size_auto']))

    def handle_apply_button_pressed(self):
        """Apply the selected marker properties to all the files in the current dataset

        [description]
        """
        ds = self.DataSettabWidget.currentWidget()
        if ds:
            #find the color mode
            if self.dialog.ui.rbFixedColor.isChecked(): #fixed color?
                ds.colormode = ColorMode.fixed.value
                ds.color1 = self.color1 if self.color1 else ColorMode.color1.value
            elif self.dialog.ui.rbPalette.isChecked(): #color from palette?
                ds.colormode = ColorMode.variable.value
                ds.palette_name = self.dialog.ui.cbPalette.currentText()
                # ds.palette = ColorMode.colorpalettes.value[palette_name]
            else: # color from gradient
                ds.colormode = ColorMode.gradient.value
                ds.color1 = self.color1 if self.color1 else ColorMode.color1.value
                ds.color2 = self.color2 if self.color2 else ColorMode.color2.value

            #find Theory color mode
            if self.dialog.ui.rbThSameColor.isChecked():
                ds.th_line_mode = ThLineMode.as_data.value
            else:
                ds.th_line_mode = ThLineMode.fixed.value
                ds.th_color = self.color_th if self.color_th else ThLineMode.color.value

            #find the shape mode
            if self.dialog.ui.rbVariableSymbol.isChecked(): #variable symbols?
                if self.dialog.ui.rbFilled.isChecked(): #filled?
                    ds.symbolmode = SymbolMode.variablefilled.value
                else: #empty
                    ds.symbolmode = SymbolMode.variable.value
            else: #single symbol
                ind = self.dialog.ui.cbSymbolType.currentIndex()
                if self.dialog.ui.rbFilled.isChecked(): #filled?
                    ds.symbolmode = SymbolMode.fixedfilled.value
                    ds.symbol1 = SymbolMode.filledmarkers.value[ind]
                    ds.symbol1_name = self.dialog.ui.cbSymbolType.currentText()
                else: #empty
                    ds.symbolmode = SymbolMode.fixed.value
                    ds.symbol1 = SymbolMode.allmarkers.value[ind]
                    ds.symbol1_name = self.dialog.ui.cbSymbolType.currentText()


            #get the marker size
            ds.marker_size = self.dialog.ui.spinBox.value()
            #get the line width
            ds.line_width = self.dialog.ui.spinBoxLineW.value()
            #get the theory linestyle
            ds.th_linestyle = self.dialog.ui.cbTheoryLine.currentText()
            #get the theory line width
            ds.th_line_width = self.dialog.ui.sbThLineWidth.value()

            # ds.DataSettreeWidget.blockSignals(True) #avoid triggering 'itemChanged' signal that causes a call to do_plot()
            ds.set_table_icons(ds.table_icon_list)
            # ds.DataSettreeWidget.blockSignals(False)

            # Legend stuff
            self.legend_opts['loc'] = self.dialog.ui.locationComboBox.currentText()
            self.legend_opts['ncol'] = self.dialog.ui.colSpinBox.value()
            self.legend_opts['title_fontsize'] = self.legend_opts['fontsize'] = self.dialog.ui.fontsizeSpinBox.value()
            self.legend_opts['markerfirst'] = self.dialog.ui.markerfirstCheckBox.isChecked()
            self.legend_opts['frameon'] = self.dialog.ui.frameonCheckBox.isChecked()
            self.legend_opts['fancybox'] = self.dialog.ui.fancyboxCheckBox.isChecked()
            self.legend_opts['shadow'] = self.dialog.ui.shadowCheckBox.isChecked()
            if (self.dialog.ui.framealphaCheckBox.isChecked()):
                self.legend_opts['framealpha'] = self.dialog.ui.framealphaSpinBox.value()
            else:
                self.legend_opts['framealpha'] = None
            if (self.dialog.ui.facecolorCheckBox.isChecked()):
                pass
            else:
                self.legend_opts['facecolor'] = None
            if (self.dialog.ui.edgecolorCheckBox.isChecked()):
                pass
            else:
                self.legend_opts['edgecolor'] = None
            if (self.dialog.ui.modeCheckBox.isChecked()):
                self.legend_opts['mode'] = 'expand'
            else:
                self.legend_opts['mode'] = None
            if (self.dialog.ui.legendtitleCheckBox.isChecked()):
                self.legend_opts['title'] = r""+self.dialog.ui.legendtitleStr.text()
            else:
                self.legend_opts['title'] = None
            if (self.dialog.ui.borderpadCheckBox.isChecked()):
                self.legend_opts['borderpad'] = self.dialog.ui.borderpadSpinBox.value()
            else:
                self.legend_opts['borderpad'] = None
            if (self.dialog.ui.labelspacingCheckBox.isChecked()):
                self.legend_opts['labelspacing'] = self.dialog.ui.labelspacingSpinBox.value()
            else:
                self.legend_opts['labelspacing'] = None
            if (self.dialog.ui.handletextpadCheckBox.isChecked()):
                self.legend_opts['handletextpad'] = self.dialog.ui.handletextpadSpinBox.value()
            else:
                self.legend_opts['handletextpad'] = None
            if (self.dialog.ui.columnspacingCheckBox.isChecked()):
                self.legend_opts['columnspacing'] = self.dialog.ui.columnspacingSpinBox.value()
            else:
                self.legend_opts['columnspacing'] = None
            if (self.dialog.ui.legendlabelCheckBox.isChecked()):
                self.default_legend_labels = False
                self.legend_labels = self.dialog.ui.legendlabelStr.text()
            else:
                self.default_legend_labels = True
            self.legend_draggable = self.dialog.ui.draggableCheckBox.isChecked()

            # Annotation stuff
            self.annotation_opts['alpha'] = self.dialog.ui.framealphaannotationSpinBox.value()
            self.annotation_opts['family'] = self.dialog.ui.fontfamilyComboBox.currentText()
            self.annotation_opts['horizontalalignment'] = self.dialog.ui.hacomboBox.currentText()
            self.annotation_opts['rotation'] = self.dialog.ui.rotationSpinBox.value()
            self.annotation_opts['fontsize'] = self.dialog.ui.fontsizeannotationSpinBox.value()
            self.annotation_opts['style'] = self.dialog.ui.fontstyleComboBox.currentText()
            self.annotation_opts['verticalalignment'] = self.dialog.ui.vacomboBox.currentText()
            self.annotation_opts['fontweight'] = self.dialog.ui.fontweightComboBox.currentText()

            #Axis stuff
            self.ax_opts['family'] = self.dialog.ui.fontfamilyComboBox_ax.currentText()
            self.ax_opts['fontsize'] = self.dialog.ui.fontsizeSpinBox_ax.value()
            self.ax_opts['style'] = self.dialog.ui.fontstyleComboBox_ax.currentText()
            self.ax_opts['fontweight'] = self.dialog.ui.fontweightComboBox_ax.currentText()
            self.ax_opts['axis_thickness'] = self.dialog.ui.axis_thickness_cb.value()
            self.ax_opts['tick_label_size'] = self.dialog.ui.tick_label_size_cb.value()
            self.ax_opts['grid'] = int(self.dialog.ui.grid_cb.isChecked())
            self.ax_opts['label_size_auto'] = int(self.dialog.ui.label_size_auto_cb.isChecked())
            self.ax_opts['tick_label_size_auto'] = int(self.dialog.ui.tick_label_size_auto_cb.isChecked())
            self.resizeplot()
            ds.do_plot() # update plot and legend

    def handle_inspectorVisibilityChanged(self, visible):
        """Handle the hide/show event of the data inspector

        [description]

        Arguments:
            - visible {[type]} -- [description]
        """
        self.actionInspect_Data.setChecked(visible)
        if visible:
            ds = self.DataSettabWidget.currentWidget()
            if ds:
                ds.populate_inspector()
        else:
            self.disconnect_curve_drag()

    def handle_actionViewShiftTriggered(self):
        ds = self.DataSettabWidget.currentWidget()
        if ds is None:
            return
        fnames = [file.file_name_short for file in ds.files]
        factorsx = [file.xshift for file in ds.files]
        factorsy = [file.yshift for file in ds.files]
        d = ViewShiftFactors(self, fnames, factorsx, factorsy)
        if d.exec_():
            nfiles = len(fnames)
            ncurves = len(factorsx[0])
            for i in range(nfiles):
                f = ds.files[i]
                for j in range(ncurves):
                    f.xshift[j] = float(d.table.item(i, 2*j).text())
                    f.yshift[j] = float(d.table.item(i, 2*j+1).text())

    def handle_actionSaveShiftTriggered(self):
        ds = self.DataSettabWidget.currentWidget()
        if ds is None:
            return
        dir_start = "data/"
        dilogue_name = "Select Folder for Saving shift factors of current dataset as txt"
        folder = QFileDialog.getExistingDirectory(self, dilogue_name, dir_start)
        if isdir(folder):
            with open(join(folder, 'Shift_Factors.txt'), 'w') as fout:
                f0 = ds.files[0]
                fparam = f0.file_type.basic_file_parameters
                for pname in f0.file_parameters:
                    if pname not in fparam:
                        fout.write('%s=%s;' % (pname, f0.file_parameters[pname]))
                fout.write('\n')
                for p in fparam:
                    fout.write('%s '%p)
                ncurves = len(f0.xshift)
                for i in range(ncurves):
                    fout.write('x%d y%d '%(i+1,i+1))
                fout.write('\n')
                for i, f in enumerate(ds.files):
                    if f.active:
                        for p in fparam:
                            fout.write('%s '%f.file_parameters[p])
                        for j in range(ncurves):
                            fout.write('%g %g '%(f.xshift[j], f.yshift[j]))
                        fout.write('\n')


    def handle_actionResetShiftTriggered(self):
        ds = self.DataSettabWidget.currentWidget()
        if ds is None:
            return
        for file in ds.files:
            file.xshift = [0]*DataTable.MAX_NUM_SERIES
            file.yshift = [0]*DataTable.MAX_NUM_SERIES
            file.isshifted = [False]*DataTable.MAX_NUM_SERIES
            ds.do_plot()
        for i in range(DataTable.MAX_NUM_SERIES):
            for j in range(2):
                item = self.shiftTable.item(i, j)
                item.setText("0")

    def handle_actionShiftTriggered(self):
        """Allow the current 'selected_file' to be dragged

        [description]
        """
        self.shiftTable.setVisible((self.actionShiftHorizontally.isChecked() or self.actionShiftVertically.isChecked()))
        ds = self.DataSettabWidget.currentWidget()
        if not ds.selected_file:
            return
        moveH = self.actionShiftHorizontally.isChecked()
        moveV = self.actionShiftVertically.isChecked()
        if moveH and moveV:
            mode = DragType.both
        elif moveH:
            mode = DragType.horizontal
        elif moveV:
            mode = DragType.vertical
        else:
            self.disconnect_curve_drag()
            return
        for curve in self.curves:
            curve.disconnect()
        self.curves.clear()

        for i, curve in enumerate(ds.selected_file.data_table.series[0]): #drag allowed on axarr[0] only
            x, y, success = self.current_view.view_proc(ds.selected_file.data_table, ds.selected_file.file_parameters)
            cur = DraggableSeries(curve, mode, self.current_view.log_x, self.current_view.log_y, xref=x[0], yref=y[0], function=self.update_shifts, functionendshift=self.finish_shifts, index=i)
            self.curves.append(cur)

    def update_shifts(self, dx, dy, index):
        ds = self.DataSettabWidget.currentWidget()
        if not ds.selected_file:
            return
        item = self.shiftTable.item(index, 0)
        item.setText("%g"%(ds.selected_file.xshift[index]+dx))
        item = self.shiftTable.item(index, 1)
        item.setText("%g"%(ds.selected_file.yshift[index]+dy))


    def finish_shifts(self, dx, dy, index):
        ds = self.DataSettabWidget.currentWidget()
        if not ds.selected_file:
            return
        ds.selected_file.xshift[index]+=dx
        ds.selected_file.yshift[index]+=dy
        ds.selected_file.isshifted[index] = True

    def disconnect_curve_drag(self):
        """Remove the Matplotlib drag connections
        and reset the shift buttons in the data inspector

        [description]
        """
        for curve in self.curves:
            curve.disconnect()
        self.curves.clear()
        #self.actionShiftHorizontally.setChecked(False)
        #self.actionShiftVertically.setChecked(False)

    def handle_actionReload_Data(self):
        """Reload the data files in the current DataSet"""
        ds = self.DataSettabWidget.currentWidget()
        if not ds:
            return
        ds.do_reload_data()

    # def handle_actionReload_Data(self):
    #     """Reload the data files: remove and reopen the current files

    #     [description]
    #     """
    #     ds = self.DataSettabWidget.currentWidget()
    #     if not ds:
    #         return
    #     self.disconnect_curve_drag()
    #     paths_to_reopen, th_to_reopen, success = self.clear_files_and_th_from_dataset(ds)
    #     if success:
    #         if paths_to_reopen:
    #             self.new_tables_from_files(paths_to_reopen)
    #         for th_name, tab_name in th_to_reopen:
    #             ds.new_theory(th_name, tab_name)
    #     else:
    #         QMessageBox.warning(self, 'Reload Error', 'Error in locating some data files')

    # def clear_files_and_th_from_dataset(self, ds):
    #     """Remove all files from dataset and widgetTree,
    #     return a list with the full path of deleted files and opened theories"""
    #     file_paths_cleaned = []
    #     th_cleaned = []
    #     #save file names
    #     for f in ds.files:
    #         fpath = f.file_full_path
    #         print(fpath)
    #         if not isfile(fpath):
    #             return None, None, False
    #         file_paths_cleaned.append(fpath)
    #     #remove lines from figure
    #     self.remove_ds_ax_lines(ds.name)
    #     ds.set_no_limits(ds.current_theory)
    #     #remove tables from ds
    #     ntable = ds.DataSettreeWidget.topLevelItemCount()
    #     for i in range(ntable):
    #         ds.DataSettreeWidget.takeTopLevelItem(0)
    #     #save theory tabs of ds
    #     ntabs = ds.TheorytabWidget.count()
    #     for i in range(ntabs):
    #         th = ds.TheorytabWidget.widget(0)
    #         try:
    #             th.destructor()
    #         except:
    #             pass
    #         thname = th.thname
    #         thtabname = ds.TheorytabWidget.tabText(0)
    #         th_cleaned.append((thname, thtabname))
    #         ds.TheorytabWidget.removeTab(0)

    #     ds.files.clear()
    #     ds.theories.clear()
    #     return file_paths_cleaned, th_cleaned, True

    def handle_actionView_All_SetTheories(self, checked):
        ds = self.DataSettabWidget.currentWidget()
        if ds:
            for th in ds.theories.values():
                th.do_show()

    def handle_actionView_All_Sets(self, checked):
        """Show all datasets simultaneously

        [description]

        Arguments:
            - checked {[type]} -- [description]
        """
        if len(self.datasets) < 2:
            return
        if checked:
            for ds in self.datasets.values():
                ds.Qshow_all()
                ds.highlight_series()
        else:
            #trigger a false change of tab to hide other dataset files from figure
            self.handle_currentChanged(self.DataSettabWidget.currentIndex())
        self.update_Qplot()

    def handle_currentChanged(self, index):
        """Change figure when the active DataSet tab is changed
        and empty the dataInspector

        [description]

        Arguments:
            - index {[type]} -- [description]
        """
        if self.actionView_All_Sets.isChecked():
            return
        ds = self.DataSettabWidget.widget(index)
        if ds:
            disable_buttons = True if not ds.files else False
            self.dataset_actions_disabled(disable_buttons) # disable/activate buttons buttons
            ntab = self.DataSettabWidget.count()
            for i in range(ntab):
                if i!=index:
                    ds_to_hide = self.DataSettabWidget.widget(i) #hide files of all datasets except current one
                    ds_to_hide.do_hide_all("")
                    ds_to_hide.set_no_limits(ds_to_hide.current_theory)
            ds.Qshow_all() #show all data of current dataset, except previously unticked files
            ds.highlight_series()
            ds.populate_inspector()
        else: # handle case where no dataset is left
            self.dataset_actions_disabled(True)
            self.inspector_table.setRowCount(0) #empty the inspector
            self.DataInspectordockWidget.setWindowTitle("File:")
        self.update_Qplot()

    def handle_doubleClickTab(self, index):
        """Edit DataSet name

        Edit the dataset tab name, leave the 'dataset' dictionary keys unchanged.
        Two datasets can share the sae name.

        Arguments:
            - index {[type]} -- [description]
        """
        old_name = self.DataSettabWidget.tabText(index)
        dlg = QInputDialog(self)
        dlg.setWindowTitle("Change DataSet Name")
        dlg.setLabelText("New DataSet Name:")
        dlg.setTextValue(old_name)
        dlg.resize(400,100)
        success = dlg.exec()
        new_tab_name = dlg.textValue()
        if (success and new_tab_name!=""):
            self.DataSettabWidget.setTabText(index, new_tab_name)
            # self.datasets[old_name].name = new_tab_name
            # self.datasets[new_tab_name] = self.datasets.pop(old_name)

    def close_data_tab_handler(self, index):
        """Delete a dataset tab from the current application

        [description]

        Arguments:
            - index {[type]} -- [description]
        """
        ds = self.DataSettabWidget.widget(index)
        if index == self.DataSettabWidget.currentIndex():
            self.disconnect_curve_drag()
            ds.set_no_limits(ds.current_theory)
        self.delete(ds.name) #call Application.delete to delete DataSet
        self.DataSettabWidget.removeTab(index)
        self.update_legend()

    def handle_change_view(self):
        self.change_view()

    def change_view(self, x_vis=False, y_vis=False):
        """Change plot view

        [description]
        """
        selected_view_name = self.viewComboBox.currentText()
        ds = self.DataSettabWidget.currentWidget()
        if ds:
            if ds.current_theory:
                ds.theories[ds.current_theory].is_xrange_visible = x_vis
                ds.theories[ds.current_theory].is_yrange_visible = y_vis
                ds.theories[ds.current_theory].set_xy_limits_visible(x_vis, y_vis)

        self.view_switch(selected_view_name) #view_switch of Application
        self.set_view_tools(selected_view_name)
        self.update_Qplot()
        self.disconnect_curve_drag()
        if ds:
            ds.highlight_series()

    def dragEnterEvent(self, e):
        """[summary]

        [description]

        Arguments:
            - e {[type]} -- [description]
        """
        if e.mimeData().hasUrls():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        """[summary]

        [description]

        Arguments:
            - e {[type]} -- [description]
        """
        #reptatelogger = logging.getLogger('ReptateLogger')
        paths_to_open = []
        for url in e.mimeData().urls():
            path = url.toLocalFile()
            if isfile(path):
                paths_to_open.append(path)
        self.new_tables_from_files(paths_to_open)

    def update_Qplot(self):
        """[summary]

        [description]
        """
        pass
        # try:
        #     plt.tight_layout(pad=1.2)
        # except:
        #     pass
        # self.canvas = FigureCanvas(self.figure)
        #self.mplvl.addWidget(self.canvas)
        # self.canvas.draw()

    def addTableToCurrentDataSet(self, dt, ext):
        """Add file table to curent dataset tab"""
        ds = self.DataSettabWidget.currentWidget()
        lnew = []
        for param in self.filetypes[ext].basic_file_parameters[:]:
            try:
                s_param = dt.file_parameters[param]
            except KeyError as e:
                # header = "Missing Parameter"
                message = "Parameter %s not found in file '%s'."%(e, dt.file_name_short)
                # QMessageBox.warning(self, header, message)
                self.logger.warning(message)
            else:
                # parameter exists
                try:
                    s_param = "%.3g" % float(s_param)
                except ValueError:
                    s_param = str(dt.file_parameters[param])
                lnew.append(s_param)

        file_name_short = dt.file_name_short
        lnew.insert(0, file_name_short)
        newitem = DataSetWidgetItem(ds.DataSettreeWidget, lnew)
        newitem.setCheckState(0, 2)
        self.dataset_actions_disabled(False) #activate buttons

    def handle_createNew_Empty_Dataset(self):
        """Called when button 'new dataset' pushed"""
        self.createNew_Empty_Dataset()

    def createNew_Empty_Dataset(self, tabname=''):
        """Add New empty tab to DataSettabWidget

        [description]
        """
        self.num_datasets += 1 #increment counter of Application
        num = self.num_datasets
        ds_name = 'Set%d'%num
        ds = QDataSet(name=ds_name, parent=self)
        self.datasets[ds_name] = ds
        if tabname == '':
            tabname = ds_name
        ind = self.DataSettabWidget.addTab(ds, tabname)

        #Set the new tab the active tab
        self.DataSettabWidget.setCurrentIndex(ind)
        #Define the tab column names (header)
        dfile = list(self.filetypes.values())[0]
        dataset_header=dfile.basic_file_parameters[:]
        dataset_header.insert(0, "File")
        ds.DataSettreeWidget.setHeaderItem(QTreeWidgetItem(dataset_header))
        ds.DataSettreeWidget.setSortingEnabled(True)

        hd=ds.DataSettreeWidget.header()
        hd.setSectionsClickable(True)
        w=ds.DataSettreeWidget.width()
        w/=hd.count()
        for i in range(hd.count()):
            hd.resizeSection(i, w)
            #hd.setTextAlignment(i, Qt.AlignHCenter)

        #Define the inspector column names (header)
        if num == 1:
            #inspect_header = dfile.col_names[:]
            inspect_header = [a+' [' + b + ']' for a,b in zip(dfile.col_names,dfile.col_units)]
            inspec_tab = self.inspector_table.setHorizontalHeaderLabels(inspect_header)
        return self.DataSettabWidget.widget(ind)

    def openDataset(self):
        """[summary]

        [description]
        """
        # 'allowed_ext' defines the allowed file extensions
        # should be of form, e.g., "LVE (*.tts *.osc);;Text file (*.txt)"
        allowed_ext = ""
        for ftype in self.filetypes.values():
            allowed_ext += "%s (*%s);;" %(ftype.name, ftype.extension)
        allowed_ext = allowed_ext.rstrip(";")
        paths_to_open = self.openFileNamesDialog(allowed_ext)
        if not paths_to_open:
            return
        self.new_tables_from_files(paths_to_open)

    def handle_action_import_from_excel(self):
        for ftype in self.filetypes.values():
            break
        if self.excel_import_gui is None:
            self.excel_import_gui = ImportExcelWindow(parent=self, headers=ftype.col_names, file_param=ftype.basic_file_parameters)
        if self.excel_import_gui.exec_():
            res_dic = self.excel_import_gui.get_data()
            if res_dic["x"] == []:
                return
            params = self.excel_import_gui.file_param_txt.text().split(";")
            fparams = {}
            for p in params:
                try:
                    pname, pval = p.split("=")
                    fparams[pname] = pval
                except ValueError:
                    pass
            for key in fparams:
                try:
                    fparams[key] = float(fparams[key])
                except ValueError:
                    pass
            ds = self.DataSettabWidget.currentWidget()
            if ds is None:
                self.createNew_Empty_Dataset()
                ds = self.DataSettabWidget.currentWidget()
            fname = "%s_%s_%s_%s" % (res_dic["file"], res_dic["sheet"], res_dic["col1"], res_dic["col2"])
            try:
                fname += "_%s" % res_dic["col3"]
            except:
                pass
            f, success = ds.new_dummy_file(fname=fname+"_", xrange=res_dic["x"], yval=res_dic["y"], zval=res_dic["z"], fparams=fparams, file_type=ftype)
            if success:
                self.addTableToCurrentDataSet(f, ftype.extension)
            if res_dic["flag_nan"]:
                QMessageBox.warning(self, 'Open Excel File', 'Some values could not be read from the file and were set to "nan"')


    def addDummyFiles(self):
        """Add dummy files to dataset"""
        if self.DataSettabWidget.count() == 0:
                self.createNew_Empty_Dataset()
        ds = self.DataSettabWidget.currentWidget()
        ftype = self.filetypes[list(self.filetypes)[0]]
        d = AddDummyFiles(self, ftype)
        parameterstochange = []
        parameterrange = []
        parameterstokeepconstant = []
        parametervalue = []
        if d.exec_():
            for i in range(d.parameterTreeWidget.topLevelItemCount()):
                item = d.parameterTreeWidget.topLevelItem(i)
                if item.checkState(0):
                    parameterstochange.append(item.text(0))
                    pmin = float(item.text(1))
                    pmax = float(item.text(2))
                    npoints = int(item.text(3))
                    cb = d.parameterTreeWidget.itemWidget(item, 4)
                    if cb.currentText() == 'Log':
                        prange = np.logspace(np.log10(pmin), np.log10(pmax), npoints)
                    else:
                        prange = np.linspace(pmin, pmax, npoints)
                    parameterrange.append(prange)
                else:
                    parameterstokeepconstant.append(item.text(0))
                    parametervalue.append(float(item.text(1)))

            nparameterstochange = len(parameterstochange)
            paramsnames = parameterstochange + parameterstokeepconstant
            if nparameterstochange==0:
                cases = [np.array(parametervalue)]
            elif nparameterstochange==1:
                cases = []
                for i in range(len(parameterrange[0])):
                    case = [parameterrange[0][i]] + parametervalue
                    cases.append(np.array(case))
            else:
                for val in parametervalue:
                    parameterrange.append(np.array([val]))
                cases = list(np.array(np.meshgrid(*parameterrange)).T.reshape(-1,len(parameterrange)))

            # print(paramsnames)
            # print(cases)
            yval = float(d.yvaluesLineEdit.text())
            xmin = float(d.xminLineEdit.text())
            xmax = float(d.xmaxLineEdit.text())
            npoints = int(d.npointsLineEdit.text())
            if d.scaleComboBox.currentText() == 'Log':
                xrange = np.logspace(np.log10(xmin), np.log10(xmax), npoints)
            else:
                xrange = np.linspace(xmin, xmax, npoints)
            for c in cases:
                fparams = {}
                for i, pname in enumerate(paramsnames):
                    fparams[pname] = c[i]
                f, success = ds.new_dummy_file(xrange=xrange, yval=yval, fparams=fparams, file_type=ftype)
                if success:
                    self.addTableToCurrentDataSet(f, ftype.extension)

    def addFileFunction(self):
        "Add a File to the current DataSet using a mathematical expression"
        if self.DataSettabWidget.count() == 0:
                self.createNew_Empty_Dataset()
        ds = self.DataSettabWidget.currentWidget()
        ftype = self.filetypes[list(self.filetypes)[0]]
        d = AddFileFunction(self, ftype)
        if d.exec_():
            fparams = {}
            for p in d.param_dict:
                try:
                    fparams[p] = float(d.param_dict[p].text())
                except:
                    fparams[p] = 0
            xmin = float(d.lab_dict['xmin'].text())
            xmax = float(d.lab_dict['xmax'].text())
            npoints = int(d.lab_dict['npoints'].text())
            logscale = d.l_new[4].isChecked()
            if (logscale):
                xrange = np.logspace(np.log10(xmin), np.log10(xmax), npoints)
            else:
                xrange = np.linspace(xmin, xmax, npoints)
            f, success = ds.new_dummy_file(xrange=xrange, yval=0, fparams=fparams, file_type=ftype)

            if success:
                cols = ftype.col_names
                self.safe_dict={}
                safe_list = ['sin', 'cos', 'tan', 'arccos', 'arcsin', 'arctan', 'arctan2', 'deg2rad', 'rad2deg', 'sinh', 'cosh', 'tanh', 'arcsinh', 'arccosh', 'arctanh', 'around', 'round_', 'rint', 'floor', 'ceil','trunc', 'exp', 'log', 'log10', 'fabs', 'mod', 'e', 'pi', 'power', 'sqrt']
                for k in safe_list:
                    self.safe_dict[k] = globals().get(k, None)
                self.safe_dict['x']=xrange
                for i, cname in enumerate(cols):  #loop over the Parameters
                    expr = d.c_new[i].text()
                    x2 = eval(expr, {"__builtins__":None}, self.safe_dict)
                    f.data_table.data[:,i] = x2

                self.addTableToCurrentDataSet(f, ftype.extension)

    def new_tables_from_files(self, paths_to_open):
        """[summary]

        [description]

        Arguments:
            - paths_to_open {[type]} -- [description]
        """
        if (self.DataSettabWidget.count()==0):
                self.createNew_Empty_Dataset()
        ds = self.DataSettabWidget.currentWidget()
        ds.DataSettreeWidget.blockSignals(True) #avoid triggering 'itemChanged' signal that causes a call to do_plot()
        success, newtables, ext = ds.do_open(paths_to_open)
        if success==True:
            self.check_no_param_missing(newtables, ext)
            for dt in newtables:
                self.addTableToCurrentDataSet(dt, ext)
            ds.do_plot()
            self.update_Qplot()
            ds.set_table_icons(ds.table_icon_list)
        else:
            QMessageBox.about(self, "Open", success)
        ds.DataSettreeWidget.blockSignals(False)

    def check_no_param_missing(self, newtables, ext):
        """[summary]

        [description]

        Arguments:
            - newtables {[type]} -- [description]
            - ext {[type]} -- [description]
        """
        for dt in newtables:
            e_list = []
            for param in self.filetypes[ext].basic_file_parameters[:]:
                try:
                    temp = dt.file_parameters[param]
                    if temp == '' or temp == '\n': # case where no value is provided (end line)
                        e_list.append(param)
                except KeyError:
                    e_list.append(param)
            if len(e_list)>0:
                message = "Parameter(s) {%s} not found in file '%s'\n Value(s) set to 0"%(", ".join(e_list), dt.file_name_short)
                # header = "Missing Parameter"
                # QMessageBox.warning(self, header, message)
                self.logger.warning(message)
                for e_param in e_list:
                    dt.file_parameters[e_param] = "0"

    def openFileNamesDialog(self, ext_filter="All Files (*)"):
        """[summary]

        [description]

        Returns:
            - [type] -- [description]
        """
        # file browser window
        qfdlg = QFileDialog(self)
        #options = QFileDialog.Options()
        options = qfdlg.Options()
        #options |= QFileDialog.DontUseNativeDialog
        dilogue_name = "Open"
        #selected_files, _ = QFileDialog.getOpenFileNames(self, dilogue_name, dir_start, ext_filter, options=options)
        selected_files, _ = qfdlg.getOpenFileNames(self, dilogue_name, self.dir_start, ext_filter, options=options)
        if selected_files:
            self.dir_start = dirname(selected_files[0])
        return selected_files

    def showDataInspector(self, checked):
        """[summary]

        [description]

        Arguments:
            - checked {[type]} -- [description]
        """
        if checked:
            self.DataInspectordockWidget.show()
        else:
            self.DataInspectordockWidget.hide()

    def viewMPLToolbar(self, checked):
        """[summary]

        [description]

        Arguments:
            checked {[type]} -- [description]
        """
        if checked:
            self.mpl_toolbar.show()
        else:
            self.mpl_toolbar.hide()

    def printPlot(self):
        """[summary]

        [description]
        """
        fileName = QFileDialog.getSaveFileName(self,
            "Export plot", "", "Image (*.png);;PDF (*.pdf);; Postscript (*.ps);; EPS (*.eps);; Vector graphics (*.svg)");
        # TODO: Set DPI, FILETYPE, etc
        plt.savefig(fileName[0])


    # def resizeplot(self, event=""):
    #     """[summary]

    #     [description]
    #     """
    #     if not (self.ax_opts['label_size_auto'] or self.ax_opts['tick_label_size_auto']):
    #         return
    #     #large window settings
    #     w_large = 900
    #     h_large = 650
    #     font_large = 16
    #     #small window settings
    #     w_small = 300
    #     h_small = 400
    #     font_small = 10
    #     #interpolate for current window size
    #     geometry = self.multiplots.frameGeometry()
    #     width = geometry.width()
    #     height = geometry.height()
    #     scale_w = font_small + (width - w_small)*(font_large - font_small)/(w_large - w_small)
    #     scale_h = font_small + (height - h_small)*(font_large - font_small)/(h_large - h_small)
    #     font_size = min(scale_w, scale_h)
    #     #resize plot fonts
    #     for ax in self.axarr:
    #         if self.ax_opts['label_size_auto']:
    #             ax.xaxis.label.set_size(font_size)
    #             ax.yaxis.label.set_size(font_size)
    #         if self.ax_opts['tick_label_size_auto']:
    #             ax.tick_params(which='major', labelsize=font_size)
    #             ax.tick_params(which='minor', labelsize=font_size*.8)


    def onpick(self, event):
        """Called when clicking on a plot/artist"""
        import matplotlib
        if event.mouseevent.button == 3:  #right click in plot
            if not isinstance(event.artist, matplotlib.legend.Legend):
                if event.artist.get_visible():
                    self.artists_clicked.append(event.artist)  #collect all artists under mouse

    # def onrelease(self, event):
    #     """Called when releasing mouse"""
    #     if event.button == 3:  #if release a right click
    #         self._zoom_area(event)
    #         if not self._was_zooming:
    #             self.open_figure_popup_menu(event)
    #         self.artists_clicked.clear()
    #         self._was_zooming = False
    #     elif event.button == 2:
    #         self._pan(event)
    #     self._pressed_button = None

    # def _zoom_area(self, event):
    #     if event.name == 'button_press_event':  # begin drag
    #         self._event = event
    #         self._patch = plt.Rectangle(
    #             xy=(event.xdata, event.ydata), width=0, height=0,
    #             fill=False, linewidth=1., linestyle=':', color='gray')
    #         self._event.inaxes.add_patch(self._patch)

    #         canvas = self._patch.figure.canvas
    #         axes = self._patch.axes
    #         self._patch.set_animated(True)
    #         canvas.draw()
    #         self.background = canvas.copy_from_bbox(self._patch.axes.bbox)
    #         axes.draw_artist(self._patch)
    #         canvas.update()

    #     elif event.name == 'button_release_event':  # end drag
    #         self.background = None
    #         try:
    #             self._patch.remove()
    #             del self._patch
    #         except AttributeError:
    #             # self._patch do not exist
    #             pass
    #         if self._event == None:
    #             self._was_zooming = False
    #             return
    #         if (abs(event.x - self._event.x) < 3 or
    #                 abs(event.y - self._event.y) < 3):
    #             self._was_zooming = False
    #             return  # No zoom when points are too close

    #         x_axes, y_axes = self._axes

    #         for ax in x_axes:
    #             pixel_to_data = ax.transData.inverted()
    #             end_pt = pixel_to_data.transform_point((event.x, event.y))
    #             begin_pt = pixel_to_data.transform_point(
    #                 (self._event.x, self._event.y))

    #             min_ = min(begin_pt[0], end_pt[0])
    #             max_ = max(begin_pt[0], end_pt[0])
    #             if (end_pt[0]>begin_pt[0]):
    #                 if not ax.xaxis_inverted():
    #                     ax.set_xlim(min_, max_)
    #                 else:
    #                     ax.set_xlim(max_, min_)
    #             else:
    #                 min_now, max_now = ax.get_xlim()
    #                 if ax.get_xscale() == 'log':
    #                     fac = 10.0**((math.log10(max_) - math.log10(min_))/2)
    #                     if not ax.xaxis_inverted():
    #                         ax.set_xlim(min_now/fac, max_now*fac)
    #                     else:
    #                         ax.set_xlim(max_now*fac, min_now/fac)
    #                 else:
    #                     dx = max_ - min_
    #                     if not ax.xaxis_inverted():
    #                         ax.set_xlim(min_now-dx, max_now+dx)
    #                     else:
    #                         ax.set_xlim(max_now+dx, min_now-dx)

    #         for ax in y_axes:
    #             pixel_to_data = ax.transData.inverted()
    #             end_pt = pixel_to_data.transform_point((event.x, event.y))
    #             begin_pt = pixel_to_data.transform_point(
    #                 (self._event.x, self._event.y))

    #             min_ = min(begin_pt[1], end_pt[1])
    #             max_ = max(begin_pt[1], end_pt[1])
    #             if (end_pt[1]<begin_pt[1]):
    #                 if not ax.yaxis_inverted():
    #                     ax.set_ylim(min_, max_)
    #                 else:
    #                     ax.set_ylim(max_, min_)
    #             else:
    #                 min_now, max_now = ax.get_ylim()
    #                 if ax.get_yscale() == 'log':
    #                     fac = 10.0**((math.log10(max_) - math.log10(min_))/2)
    #                     if not ax.yaxis_inverted():
    #                         ax.set_ylim(min_now/fac, max_now*fac)
    #                     else:
    #                         ax.set_ylim(max_now*fac, min_now/fac)
    #                 else:
    #                     dy = max_ - min_
    #                     if not ax.yaxis_inverted():
    #                         ax.set_ylim(min_now-dy, max_now+dy)
    #                     else:
    #                         ax.set_ylim(max_now+dy, min_now-dy)

    #         self._event = None
    #         self._was_zooming = True
    #         self.figure.canvas.draw()


    #     elif event.name == 'motion_notify_event':  # drag
    #         if self._event is None:
    #             return

    #         if event.inaxes != self._event.inaxes:
    #             return  # Ignore event outside plot

    #         self._patch.set_width(event.xdata - self._event.xdata)
    #         self._patch.set_height(event.ydata - self._event.ydata)

    #         canvas = self._patch.figure.canvas
    #         axes = self._patch.axes
    #         canvas.restore_region(self.background)
    #         axes.draw_artist(self._patch)
    #         canvas.update()



    def open_figure_popup_menu(self, event):
        """Open a menu to let the user copy data or chart to clipboard"""
        main_menu = QMenu()

        #copy chart action
        copy_chart_action = main_menu.addAction("Copy Chart To Clipboard")
        copy_chart_action.triggered.connect(self.copy_chart)
        #save chart action
        save_chart_action = main_menu.addAction("Save Chart")
        save_chart_action.triggered.connect(self.mpl_toolbar.save_figure)

        #copy data sub-menu
        if self.artists_clicked:  #do nothing if list of artists is empty
            menu = QMenu("Copy Data To Clipboard")
            for artist in self.artists_clicked:
                action_print_coordinates = menu.addAction(artist._name)
                action_print_coordinates.triggered.connect(
                    lambda: self.clipboard_coordinates(artist))
            main_menu.addMenu(menu)

        main_menu.addSeparator()
        if self._event is not None:
            self._annotation_done = False
            add_annotation = main_menu.addAction(self.actionAdd_Annotation)
            connection_id = self.actionAdd_Annotation.triggered.connect(self.add_annotation)
        refresh_chart_action = main_menu.addAction("Reset view(s)")
        refresh_chart_action.triggered.connect(self.refresh_plot)
        # change view
        n_ax_view_to_change = None
        for i, ax in enumerate(self.axarr):
            if event.inaxes == ax:
                n_ax_view_to_change = i
        if n_ax_view_to_change is not None:
            tab_ind = self.multiplots.plotselecttabWidget.currentIndex()
            if tab_ind != 0:
                n_ax_view_to_change = tab_ind - 1

            menu2 = QMenu("Select View")
            for i in range(self.viewComboBox.count()):
                view_name = self.viewComboBox.itemText(i)
                pick_view = menu2.addAction(view_name)
                pick_view.triggered.connect(lambda _, view_name=view_name: self.change_ax_view(n_ax_view_to_change, view_name))
            main_menu.addMenu(menu2)

        #launch menu
        if main_menu.exec_(QCursor.pos()):
            self.artists_clicked.clear()

    def change_ax_view(self, n_ax, view_name):
        """Change the view corresponding to axis n_ax"""
        tab_ind = self.multiplots.plotselecttabWidget.currentIndex()
        if (n_ax == 0) or (n_ax == tab_ind - 1):
            # change combobox selection
            ind = self.viewComboBox.findText(view_name)
            self.viewComboBox.setCurrentIndex(ind)
        else:
            self.multiviews[n_ax] = self.views[view_name]
            self.refresh_plot()

    # def _pan(self, event):
    #     if event.name == 'button_press_event':  # begin pan
    #         self._event = event

    #     elif event.name == 'button_release_event':  # end pan
    #         self._event = None

    #     elif event.name == 'motion_notify_event':  # pan
    #         if self._event is None:
    #             return

    #         if event.x != self._event.x:
    #             for ax in self._axes[0]:
    #                 xlim = self._pan_update_limits(ax, 0, event, self._event)
    #                 ax.set_xlim(xlim)

    #         if event.y != self._event.y:
    #             for ax in self._axes[1]:
    #                 ylim = self._pan_update_limits(ax, 1, event, self._event)
    #                 ax.set_ylim(ylim)

    #         if event.x != self._event.x or event.y != self._event.y:
    #             self.figure.canvas.draw()

    #         self._event = event

    # def _pan_update_limits(self, ax, axis_id, event, last_event):
    #     """Compute limits with applied pan."""
    #     assert axis_id in (0, 1)
    #     if axis_id == 0:
    #         lim = ax.get_xlim()
    #         scale = ax.get_xscale()
    #     else:
    #         lim = ax.get_ylim()
    #         scale = ax.get_yscale()

    #     pixel_to_data = ax.transData.inverted()
    #     data = pixel_to_data.transform_point((event.x, event.y))
    #     last_data = pixel_to_data.transform_point((last_event.x, last_event.y))

    #     if scale == 'linear':
    #         delta = data[axis_id] - last_data[axis_id]
    #         new_lim = lim[0] - delta, lim[1] - delta
    #     elif scale == 'log':
    #         try:
    #             delta = math.log10(data[axis_id]) - \
    #                 math.log10(last_data[axis_id])
    #             new_lim = [pow(10., (math.log10(lim[0]) - delta)),
    #                        pow(10., (math.log10(lim[1]) - delta))]
    #         except (ValueError, OverflowError):
    #             new_lim = lim  # Keep previous limits
    #     else:
    #         logging.warning('Pan not implemented for scale "%s"' % scale)
    #         new_lim = lim
    #     return new_lim

    # def _zoom_range(self, begin, end, center, scale_factor, scale):
    #     """Compute a 1D range zoomed around center.
    #     :param float begin: The begin bound of the range.
    #     :param float end: The end bound of the range.
    #     :param float center: The center of the zoom (i.e., invariant point)
    #     :param float scale_factor: The scale factor to apply.
    #     :param str scale: The scale of the axis
    #     :return: The zoomed range (min, max)
    #     """
    #     if begin < end:
    #         min_, max_ = begin, end
    #     else:
    #         min_, max_ = end, begin

    #     if scale == 'linear':
    #         old_min, old_max = min_, max_
    #     elif scale == 'log':
    #         old_min = np.log10(min_ if min_ > 0. else np.nextafter(0, 1))
    #         center = np.log10(
    #             center if center > 0. else np.nextafter(0, 1))
    #         old_max = np.log10(max_) if max_ > 0. else 0.
    #     else:
    #         logging.warning(
    #             'Zoom on wheel not implemented for scale "%s"' % scale)
    #         return begin, end

    #     offset = (center - old_min) / (old_max - old_min)
    #     range_ = (old_max - old_min) / scale_factor
    #     new_min = center - offset * range_
    #     new_max = center + (1. - offset) * range_

    #     if scale == 'log':
    #         try:
    #             new_min, new_max = 10. ** float(new_min), 10. ** float(new_max)
    #         except OverflowError:  # Limit case
    #             new_min, new_max = min_, max_
    #         if new_min <= 0. or new_max <= 0.:  # Limit case
    #             new_min, new_max = min_, max_

    #     if begin < end:
    #         return new_min, new_max
    #     else:
    #         return new_max, new_min

    # def zoom_wheel(self, event):
    #     base_scale = 1.1
    #     if event.button == 'up':
    #         # deal with zoom in
    #         scale_factor = 1 / base_scale
    #     elif event.button == 'down':
    #         # deal with zoom out
    #         scale_factor = base_scale
    #     else:
    #         # deal with something that should never happen
    #         scale_factor = 1

    #     # if event.step > 0:
    #         # scale_factor = self.scale_factor
    #     # else:
    #         # scale_factor = 1. / self.scale_factor

    #     # Go through all axes to enable zoom for multiple axes subplots
    #     x_axes, y_axes = self._axes_to_update(event)

    #     for ax in x_axes:
    #         transform = ax.transData.inverted()
    #         xdata, ydata = transform.transform_point((event.x, event.y))

    #         xlim = ax.get_xlim()
    #         xlim = self._zoom_range(xlim[0], xlim[1],
    #                                 xdata, scale_factor,
    #                                 ax.get_xscale())
    #         ax.set_xlim(xlim)

    #     for ax in y_axes:
    #         ylim = ax.get_ylim()
    #         ylim = self._zoom_range(ylim[0], ylim[1],
    #                                 ydata, scale_factor,
    #                                 ax.get_yscale())
    #         ax.set_ylim(ylim)

    #     if x_axes or y_axes:
    #         self.figure.canvas.draw()

    # def on_press(self, event):
    #     if event.button == 2: # Pan
    #         x_axes, y_axes = self._axes_to_update(event)
    #         if x_axes or y_axes:
    #             self._axes = x_axes, y_axes
    #             self._pressed_button = event.button
    #             self._pan(event)
    #     elif event.button == 3: # Zoom
    #         x_axes, y_axes = self._axes_to_update(event)
    #         if x_axes or y_axes:
    #             self._axes = x_axes, y_axes
    #             self._pressed_button = event.button
    #             self._zoom_area(event)

    # def _axes_to_update(self, event):
    #     """Returns two sets of Axes to update according to event.

    #     Takes care of multiple axes and shared axes.

    #     :param MouseEvent event: Matplotlib event to consider
    #     :return: Axes for which to update xlimits and ylimits
    #     :rtype: 2-tuple of set (xaxes, yaxes)

    #     """
    #     x_axes, y_axes = set(), set()

    #     # Go through all axes to enable zoom for multiple axes subplots
    #     for ax in self.figure.axes:
    #         if ax.contains(event)[0]:
    #             # For twin x axes, makes sure the zoom is applied once
    #             shared_x_axes = set(ax.get_shared_x_axes().get_siblings(ax))
    #             if x_axes.isdisjoint(shared_x_axes):
    #                 x_axes.add(ax)

    #             # For twin y axes, makes sure the zoom is applied once
    #             shared_y_axes = set(ax.get_shared_y_axes().get_siblings(ax))
    #             if y_axes.isdisjoint(shared_y_axes):
    #                 y_axes.add(ax)

    #     return x_axes, y_axes

    # def on_motion(self, event):
    #     if self._pressed_button == 2:  # pan
    #         self._pan(event)
    #     elif self._pressed_button == 3:  # zoom area
    #         self._zoom_area(event)
