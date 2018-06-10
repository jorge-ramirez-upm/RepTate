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
"""Module QApplicationWindow

Module that defines the basic GUI class from which all GUI applications are derived.
It is the GUI counterpart of Application.

""" 
import io
import re
import traceback
import numpy as np
from os.path import dirname, join, abspath, isfile, isdir
#import logging
from PyQt5.QtGui import QIcon, QColor, QStandardItem
from PyQt5.uic import loadUiType
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QToolBar, QToolButton, QMenu, QFileDialog, QMessageBox, QInputDialog, QLineEdit, QHeaderView, QColorDialog, QDialog, QDialogButtonBox, QTreeWidgetItem, QApplication, QTabWidget, QComboBox, QVBoxLayout, QSplitter, QLabel, QTableWidget, QTableWidgetItem
from QDataSet import QDataSet
from DataTable import DataTable
from DataSetWidgetItem import DataSetWidgetItem
from DataSet import ColorMode, SymbolMode, ThLineMode
from CmdBase import CmdBase, CmdMode
from Application import Application
from DraggableArtists import DragType, DraggableSeries, DraggableNote
from SpreadsheetWidget import SpreadsheetWidget
from collections import OrderedDict

#To recompile the symbol-settings dialog:
#pyuic5 gui/markerSettings.ui -o gui/markerSettings.py
from markerSettings import Ui_Dialog

from SpreadsheetWidget import SpreadsheetWidget

# I think the following lines are not needed anymore
#try:
#    _fromUtf8 = QtCore.QString.fromUtf8
#except AttributeError:
#    _fromUtf8 = lambda s: s
    
PATH = dirname(abspath(__file__))
Ui_AppWindow, QMainWindow = loadUiType(join(PATH,'QApplicationWindow.ui'))

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
        #self.logger = logging.getLogger('ReptateLogger')
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
        self.shiftTable = QTableWidget(DataTable.MAX_NUM_SERIES,2, self)
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

        #custom QTable to have the copy/pastefeature
        self.inspector_table = SpreadsheetWidget(self)
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
        self.cbtool.setToolTip("Choose a Tool")
        model = self.cbtool.model()
        i = 0
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
        tb.addAction(self.actionNew_Dataset_From_File)
        tb.addAction(self.actionView_All_Sets)
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
        self.mpl_toolbar.addAction(self.actionAdd_Annotation)
        self.mpl_toolbar.addAction(self.actionShow_Legend)
        self.mpl_toolbar.addAction(self.actionCopyChart)
        self.mpl_toolbar.setVisible(False)
        self.mplvl.addWidget(self.mpl_toolbar)

                
        # self.canvas.draw()
        # self.update_Qplot()
        # LEGEND STUFF
        self.legend = None
        # leg=plt.legend(loc='upper left', frameon=True, ncol=2)
        # if leg:
        #     leg.draggable()
                

        # EVENT HANDLING
        #connection_id = self.figure.canvas.mpl_connect('button_press_event', self.onclick)
        connection_id = self.figure.canvas.mpl_connect('resize_event', self.resizeplot)
        #connection_id = self.figure.canvas.mpl_connect('motion_notify_event', self.on_plot_hover)   
        connection_id = self.actionShowFigureTools.triggered.connect(self.viewMPLToolbar)
        connection_id = self.actionInspect_Data.triggered.connect(self.showDataInspector)
        connection_id = self.actionNew_Empty_Dataset.triggered.connect(self.handle_createNew_Empty_Dataset)
        connection_id = self.actionNew_Dataset_From_File.triggered.connect(self.openDataset)
        connection_id = self.actionReload_Data.triggered.connect(self.handle_actionReload_Data)
        connection_id = self.actionAutoscale.triggered.connect(self.handle_actionAutoscale)

        connection_id = self.actionNew_Tool.triggered.connect(self.handle_actionNewTool)
        connection_id = self.TooltabWidget.tabCloseRequested.connect(self.handle_toolTabCloseRequested)
        connection_id = self.qtabbar.tabMoved.connect(self.handle_toolTabMoved)
        
        connection_id = self.viewComboBox.currentIndexChanged.connect(self.change_view)
        connection_id = self.actionSave_View.triggered.connect(self.save_view)

        connection_id = self.DataSettabWidget.tabCloseRequested.connect(self.close_data_tab_handler)
        connection_id = self.DataSettabWidget.tabBarDoubleClicked.connect(self.handle_doubleClickTab)
        connection_id = self.DataSettabWidget.currentChanged.connect(self.handle_currentChanged)
        connection_id = self.actionView_All_Sets.toggled.connect(self.handle_actionView_All_Sets)
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
        connection_id = self.actionTrack_data.triggered.connect(self.handle_annotation)
        connection_id = self.actionCopyChart.triggered.connect(self.copy_chart)
        self.graphicnotes = []
        self.artistnotes = []
        connection_id = self.actionAdd_Annotation.triggered.connect(self.add_annotation)
        connection_id = self.actionShow_Legend.triggered.connect(self.handle_actionShow_Legend)
        plt.connect('motion_notify_event', self.mpl_motion_event)

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
        self.legend_opts = {'loc':'best', 'ncol':1, 'fontsize':12, 'markerfirst':True, 'frameon':True, 'fancybox':True, 'shadow':True, 'framealpha':None, 'facecolor':None, 'edgecolor':None, 'mode':None, 'title':None, 'borderpad': None, 'labelspacing':None, 'handletextpad':None, 'columnspacing':None}
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
        connection_id = self.dialog.ui.rbEmpty.clicked.connect(self.populate_cbSymbolType)
        connection_id = self.dialog.ui.rbFilled.clicked.connect(self.populate_cbSymbolType)
        connection_id = self.dialog.ui.pushApply.clicked.connect(self.handle_apply_button_pressed)


        self.dataset_actions_disabled(True)

        # connection_id = self.checkBoxColor.toggled.connect(self)
        # TEST GET CLICKABLE OBJECTS ON THE X AXIS
        #xaxis = self.ax.get_xticklabels()
        #print (xaxis)  

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
        tool_name = self.cbtool.currentText()
        if tool_name != '':
            self.new_tool(tool_name)
            self.update_all_ds_plots()
        
    def new_tool(self, tool_name, tool_tab_id=""):
        """Create new tool"""
        newtool = self.do_tool_add(tool_name)

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

    def mpl_motion_event(self, event):
        """[summary]
        
        [description]
        
        Arguments:
            - event {[type]} -- [description]
        """
        if not self.handle_annotation.checked:
            return
        """.. todo:: Code to draw annotation. It doesn't work!"""
        
    def handle_annotation(self, checked):
        """Draw and hide the annotation box.
        
        [description]
        
        Arguments:
            - checked {[type]} -- [description]
        """
        if self.current_viewtab == 0:
            ax = self.axarr[0]
        else:
            ax = self.axarr[self.current_viewtab - 1]
        if (checked):
            self.annotation = ax.annotate(
                '', xy=(0, 0), ha = 'left',
                xytext = (-40, 40), textcoords = 'offset points', va = 'center',
                bbox = dict(
                    boxstyle='roundtooth,pad=0.3', fc='yellow', alpha=0.20),
                arrowprops = dict(
                    arrowstyle="-|>", connectionstyle="arc3,rad=-0.2")
                )
            self.canvas.draw()
        else:
            self.annotation.remove()
            self.canvas.draw()

    def add_annotation(self):
        if self.current_viewtab == 0:
            ax = self.axarr[0]
        else:
            ax = self.axarr[self.current_viewtab - 1]
        text, ok = QInputDialog.getText(self, 'Annotation (LaTeX allowed)', 'Enter the annotation text:')
        if ok:
            xmin, xmax = ax.get_xlim()
            ymin, ymax = ax.get_ylim()
            xpos = (xmin+xmax)/2
            ypos = (ymin+ymax)/2
            ann = ax.annotate(text, xy=(xpos, ypos), xytext=(xpos, ypos), size=20, va="center", ha="center")
            self.graphicnotes.append(ann)
            self.artistnotes.append(DraggableNote(ann, DragType.both, None, None))
            self.canvas.draw()

    def handle_actionShow_Legend(self):
        """toogle view/hide the legend"""
        self.dialog.ui.cb_show_legend.setChecked(not self.dialog.ui.cb_show_legend.isChecked())
        self.update_legend()

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
                            label = label.replace('['+p+']', str(val))
                    N.append(label)
            self.legend = ax.legend(L, N, **self.legend_opts)            
                
            self.legend.draggable(self.legend_draggable)

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
        
        success = self.dialog.exec_() #this blocks the rest of the app as opposed to .show()
        if success == 1:
            self.handle_apply_button_pressed()
        else:
            ds.do_plot()

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
            self.legend_opts['fontsize'] = self.dialog.ui.fontsizeSpinBox.value()
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
        """Reload the data files: remove and reopen the current files
        
        [description]
        """
        ds = self.DataSettabWidget.currentWidget()
        if not ds:
            return
        self.disconnect_curve_drag()
        paths_to_reopen, th_to_reopen, success = self.clear_files_and_th_from_dataset(ds)
        if success:
            if paths_to_reopen:
                self.new_tables_from_files(paths_to_reopen)
            for th_name, tab_name in th_to_reopen:
                ds.new_theory(th_name, tab_name)
        else:
            QMessageBox.warning(self, 'Reload Error', 'Error in locating some data files')

    def clear_files_and_th_from_dataset(self, ds):
        """Remove all files from dataset and widgetTree,
        return a list with the full path of deleted files and opened theories
        
        [description]
        
        Arguments:
            - ds {[type]} -- [description]
        
        Returns:
            - [type] -- [description]
        """
        file_paths_cleaned = []
        th_cleaned = []
        #save file names
        for f in ds.files:
            fpath = f.file_full_path
            print(fpath)
            if not isfile(fpath):
                return None, None, False
            file_paths_cleaned.append(fpath)
        #remove lines from figure
        self.remove_ds_ax_lines(ds.name) 
        ds.set_no_limits(ds.current_theory) 
        #remove tables from ds
        ntable = ds.DataSettreeWidget.topLevelItemCount()
        for i in range(ntable):
            ds.DataSettreeWidget.takeTopLevelItem(0)
        #save theory tabs of ds
        ntabs = ds.TheorytabWidget.count()
        for i in range(ntabs):
            th = ds.TheorytabWidget.widget(0)
            try:
                th.destructor()
            except:
                pass
            thname = th.thname
            thtabname = ds.TheorytabWidget.tabText(0)
            th_cleaned.append((thname, thtabname))
            ds.TheorytabWidget.removeTab(0)
        
        ds.files.clear()
        ds.theories.clear()
        return file_paths_cleaned, th_cleaned, True

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
            ds.Qshow_all() #show all data of current dataset, except previously unticked files
            ntab = self.DataSettabWidget.count()
            for i in range(ntab): 
                if i!=index:
                    ds_to_hide = self.DataSettabWidget.widget(i) #hide files of all datasets except current one
                    ds_to_hide.do_hide_all()
                    ds_to_hide.set_no_limits(ds_to_hide.current_theory) 
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

    def change_view(self):
        """Change plot view
        
        [description]
        """
        selected_view_name = self.viewComboBox.currentText()
        ds = self.DataSettabWidget.currentWidget()
        if ds:
            if ds.current_theory:
                ds.theories[ds.current_theory].is_xrange_visible = False
                ds.theories[ds.current_theory].is_yrange_visible = False
                ds.theories[ds.current_theory].set_xy_limits_visible(False, False)
                
        self.view_switch(selected_view_name) #view_switch of Application
        self.set_view_tools(selected_view_name)
        self.update_Qplot()
        self.disconnect_curve_drag()
        if ds:
            ds.highlight_series()

    def set_view_tools(self, view_name):
        pass

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
        """Add file table to curent dataset tab
        
        [description]
        
        Arguments:
            - dt {[type]} -- [description]
            - ext {[type]} -- [description]
        """
        ds = self.DataSettabWidget.currentWidget()
        lnew = []
        for param in self.filetypes[ext].basic_file_parameters[:]:
            try:
                lnew.append(str(dt.file_parameters[param]))
            except KeyError as e:
                header = "Missing Parameter"
                message = "Parameter %s not found in file '%s'."%(e, dt.file_name_short)
                QMessageBox.warning(self, header, message)
                
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
        
    def new_tables_from_files(self, paths_to_open):
        """[summary]
        
        [description]
        
        Arguments:
            - paths_to_open {[type]} -- [description]
        """
        if (self.DataSettabWidget.count()==0):
                self.createNew_Empty_Dataset()
        ds = self.DataSettabWidget.currentWidget()
        success, newtables, ext = ds.do_open(paths_to_open)
        if success==True:
            self.check_no_param_missing(newtables, ext)
            for dt in newtables:
                self.addTableToCurrentDataSet(dt, ext)
            ds.do_plot()
            self.update_Qplot()
            # ds.DataSettreeWidget.blockSignals(True) #avoid triggering 'itemChanged' signal that causes a call to do_plot()
            ds.set_table_icons(ds.table_icon_list)
            # ds.DataSettreeWidget.blockSignals(False)
        else:
            QMessageBox.about(self, "Open", success)
    
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
                header = "Missing Parameter"
                QMessageBox.warning(self, header, message)
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
        
    def on_plot_hover(self, event):
        """[summary]
        
        [description]
        
        Arguments:
            - event {[type]} -- [description]
        """
        pass

    def resizeplot(self, event=""):
        """[summary]
        
        [description]
        """
        #large window settings
        w_large = 900
        h_large = 650
        font_large = 16
        #small window settings
        w_small = 300
        h_small = 400
        font_small = 10
        #interpolate for current window size
        width = event.width 
        height = event.height
        scale_w = font_small + (width - w_small)*(font_large - font_small)/(w_large - w_small)
        scale_h = font_small + (height - h_small)*(font_large - font_small)/(h_large - h_small)
        font_size = min(scale_w, scale_h)
        #resize plot fonts
        for ax in self.axarr:
            for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] + ax.get_xticklabels() + ax.get_yticklabels()):
                item.set_fontsize(font_size)
  