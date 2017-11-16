import sys
import os
import logging
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
import seaborn as sns   
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_pdf import PdfPages
import itertools
import Symbols_rc
import numpy as np
from PyQt5 import QtCore
from PyQt5.QtWidgets import QToolBar, QToolButton, QMenu, QFileDialog, QMessageBox, QInputDialog, QLineEdit, QHeaderView
from QDataSet import *
from DataFiles import *
from QFile import *
from Application import *
from DraggableArtists import *

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s
    
Ui_AppWindow, QMainWindow = loadUiType('gui/QApplicationWindow.ui')

class QApplicationWindow(Application, QMainWindow, Ui_AppWindow):
    def __init__(self, name='Application Template', parent=None):
        print("QApplicationWindow.__init__(self) called")
        super(QApplicationWindow, self).__init__(name, parent)
        print("QApplicationWindow.__init__(self) ended")

        if CmdBase.mode!=CmdMode.GUI:
            return None
        
        QMainWindow.__init__(self)
        Ui_AppWindow.__init__(self)

        self.setupUi(self)
        self.logger = logging.getLogger('ReptateLogger')
        self.name = name
        self.parent_application = parent
        self.canvas = 0
        self.tab_count = 0
        self.curves = []
        self.zorder = 100
        #self.views={} # we use 'views' of Application.py
       
        # Accept Drag and drop events
        self.setAcceptDrops(True)

        # DataSet Tabs behaviour ##########
        self.DataSettabWidget.setTabsClosable(True)
        self.DataSettabWidget.setUsesScrollButtons(True)
        self.DataSettabWidget.setMovable(True)    
        
        ################
        # SETUP TOOLBARS
        # Data Inspector Toolbar
        tb = QToolBar()
        tb.setIconSize(QtCore.QSize(24,24))
        tb.addAction(self.actionCopy)
        tb.addAction(self.actionPaste)
        tb.addAction(self.actionShiftVertically)
        tb.addAction(self.actionShiftHorizontally)
        self.LayoutDataInspector.insertWidget(0, tb)
        
        # Dataset Toolbar
        tb = QToolBar()
        tb.setIconSize(QtCore.QSize(24,24))
        tb.addAction(self.actionNew_Empty_Dataset)
        tb.addAction(self.actionNew_Dataset_From_File)
        tb.addAction(self.actionView_All_Sets)
        tbut = QToolButton()
        tbut.setPopupMode(QToolButton.MenuButtonPopup)
        tbut.setDefaultAction(self.actionData_Representation)
        menu=QMenu()
        menu.addAction(self.actionShow_Smaller_Symbols)
        menu.addAction(self.actionResetSymbolsSize)
        menu.addAction(self.actionShow_Larger_Symbols)
        menu.setMaximumWidth(80)
        menu.setToolTipsVisible(True)
        tbut.setMenu(menu)
        tb.addWidget(tbut)
        #
        tb.addAction(self.actionReload_Data)
        tbut = QToolButton()
        tbut.setPopupMode(QToolButton.MenuButtonPopup)
        tbut.setDefaultAction(self.actionShow_Limits)
        menu=QMenu()
        menu.addAction(self.actionNo_Limits)
        menu.addAction(self.actionVertical_Limits)
        menu.addAction(self.actionHorizontal_Limits)
        menu.addAction(self.actionBoth_Limits)
        tbut.setMenu(menu)
        tb.addWidget(tbut)
        #
        tb.addAction(self.actionInspect_Data)
        tb.addAction(self.actionPrint)
        self.ViewDataTheoryLayout.insertWidget(1, tb)
        self.ViewDataTheorydockWidget.Width=500
        self.ViewDataTheorydockWidget.setTitleBarWidget(QWidget())                

        # Tests TableWidget
        self.tableWidget.setRowCount(30)
        self.tableWidget.setColumnCount(10)
        self.tableWidget.setHorizontalHeaderLabels(['x','y','z','a','b','c','d','e','f','g'])

        # Hide Data Inspector
        self.DataInspectordockWidget.hide()

        # PLOT Style
        # sns.set_style("white")
        # sns.set_style("ticks")
        # #plt.style.use('seaborn-talk')
        # #plt.style.use('seaborn-paper')
        # plt.style.use('seaborn-poster')
        # self.figure=plt.figure()
        # self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self.figure)
        self.mplvl.addWidget(self.canvas)


        # self.canvas.draw()
        # self.update_Qplot()
        # sns.despine() # Remove up and right side of plot box
        # LEGEND STUFF
        # leg=plt.legend(loc='upper left', frameon=True, ncol=2)
        # if leg:
        #     leg.draggable()
                

        # EVENT HANDLING
        #connection_id = self.figure.canvas.mpl_connect('button_press_event', self.onclick)
        connection_id = self.figure.canvas.mpl_connect('resize_event', self.resizeplot)
        #connection_id = self.figure.canvas.mpl_connect('motion_notify_event', self.on_plot_hover)   
        connection_id = self.actionPrint.triggered.connect(self.printPlot)
        connection_id = self.actionInspect_Data.triggered.connect(self.showDataInspector)
        connection_id = self.actionNew_Empty_Dataset.triggered.connect(self.createNew_Empty_Dataset)
        connection_id = self.actionNew_Dataset_From_File.triggered.connect(self.openDataset)
       # connection_id = self.actionNew_Dataset_From_File.triggered.connect(self.createNew_Dataset_From_File)
        connection_id = self.actionReload_Data.triggered.connect(self.handle_actionReload_Data)

        connection_id = self.actionShow_Smaller_Symbols.triggered.connect(self.Smaller_Symbols)
        connection_id = self.actionResetSymbolsSize.triggered.connect(self.ResetSymbolsSize)
        connection_id = self.actionShow_Larger_Symbols.triggered.connect(self.Larger_Symbols)

        connection_id = self.actionNo_Limits.triggered.connect(self.No_Limits)
        connection_id = self.actionVertical_Limits.triggered.connect(self.Vertical_Limits)
        connection_id = self.actionHorizontal_Limits.triggered.connect(self.Horizontal_Limits)
        connection_id = self.actionBoth_Limits.triggered.connect(self.Both_Limits)
            
        connection_id = self.viewComboBox.currentIndexChanged.connect(self.change_view)

        connection_id = self.DataSettabWidget.tabCloseRequested.connect(self.close_data_tab_handler)
        connection_id = self.DataSettabWidget.tabBarDoubleClicked.connect(self.handle_doubleClickTab)
        connection_id = self.DataSettabWidget.currentChanged.connect(self.handle_currentChanged)
        connection_id = self.actionView_All_Sets.toggled.connect(self.handle_actionView_All_Sets)
        connection_id = self.actionShiftVertically.triggered.connect(self.handle_actionShiftTriggered)
        connection_id = self.actionShiftHorizontally.triggered.connect(self.handle_actionShiftTriggered)
        connection_id = self.DataInspectordockWidget.visibilityChanged.connect(self.handle_inspectorVisibilityChanged)

        # TEST GET CLICKABLE OBJECTS ON THE X AXIS
        #xaxis = self.ax.get_xticklabels()
        #print (xaxis)
    def handle_inspectorVisibilityChanged(self, visible):
        if not visible:
            self.disconnect_curve_drag()
        else:
            ds = self.DataSettabWidget.currentWidget()
            if ds:
                ds.populate_inspector(ds.highlighed_file)
        
    def handle_actionShiftTriggered(self):
        if not self.highlighed_file:
            return
        moveH = self.actionShiftHorizontally.isChecked()
        moveV = self.actionShiftVertically.isChecked()
        self.curves.clear()
        if moveH and moveV:
            mode = DragType.both
        elif moveH:
            mode = DragType.horizontal
        elif moveV:
            mode = DragType.vertical
        else:
            self.disconnect_curve_drag()
            return
        for curve in self.highlighed_file.data_table.series:
            cur = DraggableSeries(curve, mode, self.current_view.log_x, self.current_view.log_y)
            self.curves.append(cur)

    def disconnect_curve_drag(self):
        for curve in self.curves:
            curve.disconnect()
        self.actionShiftHorizontally.setChecked(False)
        self.actionShiftVertically.setChecked(False)
        

    def handle_actionReload_Data(self):
        """Reload the data files: remove and reopen the current files"""
        tab = self.DataSettabWidget.currentWidget()
        if tab == None:
            return
        ds = self.datasets[tab.name]
        paths_to_reopen = self.clear_files_from_dataset(ds)
        if paths_to_reopen:
            self.new_tables_from_files(paths_to_reopen)
        self.disconnect_curve_drag()

    def clear_files_from_dataset(self, ds):
        """Remove all files from dataset and widgetTree,
        return a list with the full path of deleted files"""
        file_paths_cleaned = []
        #remove files from dataset
        for file in ds.files:
            file_paths_cleaned.append(file.file_full_path)
            for i in range(file.data_table.MAX_NUM_SERIES):
                self.ax.lines.remove(file.data_table.series[i])
        del ds.files[:]
        #remove tables from widget
        ntable = ds.DataSettreeWidget.topLevelItemCount()
        for i in range(ntable):
            ds.DataSettreeWidget.takeTopLevelItem(0)
        return file_paths_cleaned

    def handle_actionView_All_Sets(self, checked):
        """Show all datasets simultaneously"""
        if len(self.datasets) < 2:
            return
        if checked:
            for ds in self.datasets.values():
                ds.Qshow_all()
                ds.do_plot()
        else:
            #trigger a false change of tab to hide other dataset files from figure
            self.handle_currentChanged(self.DataSettabWidget.currentIndex())
        self.update_Qplot()

    def handle_currentChanged(self, index):
        """Change figure when the active DataSet tab is changed"""
        if index == -1: #There is no tab
            self.update_Qplot()
            return
        if self.actionView_All_Sets.isChecked():
            return
        ds_name = self.DataSettabWidget.widget(index).name
        ds = self.datasets[ds_name]
        ds.Qshow_all() #show all data of current dataset, except previously unticked files

        #hide files of all datasets except current one
        ntab = self.DataSettabWidget.count()
        if ntab > 1:
            for i in range(ntab): 
                if i!=index:
                    ds_name_to_hide = self.DataSettabWidget.widget(i).name
                    self.datasets[ds_name_to_hide].do_hide_all()
        ds.do_plot()
        self.update_Qplot()

    def handle_doubleClickTab(self, index):
        """Edit DataSet-tab name"""
        old_name = self.DataSettabWidget.tabText(index)
        new_tab_name, success = QInputDialog.getText (
                self, "Change Name",
                "Insert New Tab Name",
                QLineEdit.Normal,
                old_name)
        if (success and new_tab_name!=""):    
            self.DataSettabWidget.setTabText(index, new_tab_name)

    def close_data_tab_handler(self, index):
        """Delete a dataset tab from the current application"""
        ds_name = self.DataSettabWidget.widget(index).name
        self.delete(ds_name) #call Application.delete to delete DataSet
        self.DataSettabWidget.removeTab(index)
        
        #if not current tab, need to update plot
        current_index = self.DataSettabWidget.currentIndex()
        self.handle_currentChanged(current_index) #trigger a false tab change to current tab
           
    def change_view(self):
        """Change plot view"""
        selected_view_name = self.viewComboBox.currentText()
        self.view_switch(selected_view_name) #view_switch of Application
        self.update_Qplot()
        self.disconnect_curve_drag()
        ds = self.DataSettabWidget.currentWidget()
        if ds:
            ds.highlight_series(self.highlighed_file)

    def populate_views(self):
        """Assign availiable view labels to ComboBox"""
        for i in self.views:
            #add keys of 'views' dict to the list of views avaliable 
            self.viewComboBox.addItem(i) 

    def dragEnterEvent(self, e):      
        if e.mimeData().hasUrls():
            e.accept()
        else:
            e.ignore() 

    def dropEvent(self, e):
        reptatelogger = logging.getLogger('ReptateLogger')
        paths_to_open = []
        for url in e.mimeData().urls():
            path = url.toLocalFile()
            if os.path.isfile(path):
                paths_to_open.append(path)
        self.new_tables_from_files(paths_to_open)

    def update_Qplot(self):
        plt.tight_layout(pad=1.2)
        # self.canvas = FigureCanvas(self.figure)
        #self.mplvl.addWidget(self.canvas)
        self.canvas.draw()

    def addTableToCurrentDataSet(self, dt, ext):
        """Add file table to curent dataset tab"""
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
        newitem = QFile(ds.DataSettreeWidget, lnew)
        newitem.setCheckState(0, 2)
        
    def createNew_Empty_Dataset(self):
        """Add New empty tab to DataSettabWidget"""
        self.num_datasets += 1 #increment counter of Application
        num = self.num_datasets
        ds_name = 'Set%d'%num
        ds = QDataSet(name=ds_name, parent=self)
        self.datasets[ds_name] = ds
        ind = self.DataSettabWidget.addTab(ds, ds_name)

        #Set the new tab the active tab
        self.DataSettabWidget.setCurrentIndex(ind)
        #Define the tab column names (header)
        dfile = list(self.filetypes.values())[0] 
        dataset_header=dfile.basic_file_parameters[:]
        dataset_header.insert(0, "File")
        ds.DataSettreeWidget.setHeaderItem(QTreeWidgetItem(dataset_header))   
        hd=ds.DataSettreeWidget.header()
        hd.setSectionsClickable(True)
        w=ds.DataSettreeWidget.width()
        w/=hd.count()
        for i in range(hd.count()):
            hd.resizeSection(i, w)
            #hd.setTextAlignment(i, Qt.AlignHCenter)
        
        #Define the inspector column names (header)
        if num == 1:
            inspect_header = dfile.col_names[:]
            inspec_tab = self.tableWidget.setHorizontalHeaderLabels(inspect_header)


    def openDataset(self):
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
        if (self.DataSettabWidget.count()==0):
                self.createNew_Empty_Dataset()
        tab = self.DataSettabWidget.currentWidget()
        ds = self.datasets[tab.name]
        success, newtables, ext = ds.do_open(paths_to_open)
        self.check_no_param_missing(newtables, ext)
        if success==True:
            for dt in newtables:
                self.addTableToCurrentDataSet(dt, ext)
            ds.do_plot()
            self.update_Qplot()
        else:
            QMessageBox.about(self, "Open", success)
    
    def check_no_param_missing(self, newtables, ext):
        for dt in newtables:
            e_list = []
            for param in self.filetypes[ext].basic_file_parameters[:]:
                try:
                    temp = dt.file_parameters[param]
                except KeyError:
                    e_list.append(param)
            if len(e_list)>0:
                message = "Parameter(s) {%s} not found in file '%s'\n Value(s) set to 0"%(", ".join(e_list), dt.file_name_short)
                header = "Missing Parameter"
                QMessageBox.warning(self, header, message)
                for e_param in e_list:
                    dt.file_parameters[e_param] = "0"

    def openFileNamesDialog(self, ext_filter="All Files (*)"):  
        # file browser window  
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        dir_start = "data/"
        dilogue_name = "Open"
        selected_files, _ = QFileDialog.getOpenFileNames(self, dilogue_name, dir_start, ext_filter, options=options)
        return selected_files

    def showDataInspector(self):
        if self.DataInspectordockWidget.isHidden():
            self.DataInspectordockWidget.show()
        else:
            self.DataInspectordockWidget.hide()
        
    def printPlot(self):
        fileName = QFileDialog.getSaveFileName(self,
            "Export plot", "", "Image (*.png);;PDF (*.pdf);; Postscript (*.ps);; EPS (*.eps);; Vector graphics (*.svg)");
        # TODO: Set DPI, FILETYPE, etc
        plt.savefig(fileName[0])
        
    def on_plot_hover(self, event):
        pass
        
    def onclick(self, event):
        if event.dblclick:
            pickedtick = event.artist
            print(event)
            print(pickedtick)

    def resizeplot(self, event=""):
        # TIGHT LAYOUT in order to view axes and everything
        plt.tight_layout(pad=1.2)


    def No_Limits(self):
        self.actionShow_Limits.setIcon(self.actionNo_Limits.icon())

    def Vertical_Limits(self):
        self.actionShow_Limits.setIcon(self.actionVertical_Limits.icon())

    def Horizontal_Limits(self):
        self.actionShow_Limits.setIcon(self.actionHorizontal_Limits.icon())

    def Both_Limits(self):
        self.actionShow_Limits.setIcon(self.actionBoth_Limits.icon())
        
    def Smaller_Symbols(self):
        tab = self.DataSettabWidget.currentWidget()
        if tab == None:
            return
        ds = self.datasets[tab.name]
        msize = ds.marker_size - 5
        ds.marker_size = msize if msize>0 else 2
        ds.do_plot()
        # self.actionData_Representation.setIcon(self.actionShow_Smaller_Symbols.icon())

    def ResetSymbolsSize(self):
        tab = self.DataSettabWidget.currentWidget()
        if tab == None:
            return        
        ds = self.datasets[tab.name]
        ds.marker_size = 12
        ds.do_plot()
        # self.actionData_Representation.setIcon(self.actionResetSymbolsSize.icon()) 
   
    def Larger_Symbols(self):
        tab = self.DataSettabWidget.currentWidget()
        if tab == None:
            return
        ds = self.datasets[tab.name]
        msize = ds.marker_size + 5
        ds.marker_size = msize if msize<26 else 26
        ds.do_plot()
        # self.actionData_Representation.setIcon(self.actionShow_Larger_Symbols.icon())
    
    def DEBUG_populate_current_Dataset_with_random_data(self):
        # Plot some random walks
        num_lines=10
        num_points=200
        #palette = itertools.cycle(sns.color_palette("Set1",n_colors=num_lines, desat=.5)) 
        #palette = itertools.cycle(sns.color_palette("Blues_d",n_colors=num_lines)) 
        pname="default" # nipy_spectral gist_ncar gist_rainbow Dark2 cool, afmhot, hsl, husl, deep, muted, bright, pastel, dark, colorblind, viridis
        #palette = itertools.cycle(sns.color_palette(pname,num_lines)) 
        palette=itertools.cycle(((0,0,0),(1.0,0,0),(0,1.0,0),(0,0,1.0),(1.0,1.0,0),(1.0,0,1.0),(0,1.0,1.0),(0.5,0,0),(0,0.5,0),(0,0,0.5),(0.5,0.5,0),(0.5,0,0.5),(0,0.5,0.5),(0.25,0,0),(0,0.25,0),(0,0,0.25),(0.25,0.25,0),(0.25,0,0.25),(0,0.25,0.25)))
        markerlst = itertools.cycle(('o', 'v', '^', '<', '>', '8', 's', 'p', '*', 'h', 'H', 'D', 'd')) 
        linelst = itertools.cycle((':', '-', '-.', '--'))

        # Add New tab to DataSettabWidget
        if (self.DataSettabWidget.count()==0): return
        ds=self.DataSettabWidget.currentWidget()
        
        nold = ds.DataSettreeWidget.topLevelItemCount()
        for i in range(nold):
            marker=next(markerlst)
            edgecolors=next(palette)

        for i in range(num_lines):
            root = QFile(ds.DataSettreeWidget, ['Line %02d'%(i+nold), "%g"%np.sin(i), "%g"%(1-1/(i+1))])
            root.setCheckState(0, 2)
            root.setIcon(0, QIcon(':/Icons/Images/symbols/'+pname+str(i+1)+'.ico'))
            
            x=np.arange(num_points)
            y=np.cumsum(np.random.randn(num_points))
            
            # DIFFERENT STYLES
            # JUST LINES
            #self.ax.plot(y, color=next(palette), label='Line %d'%i)
            # LINES with DIFFERENT STYLES, BLACK
            #self.ax.plot(y, linestyle=next(linelst), color='black', label='Line %d'%i)
            # LINES with DIFFERENT STYLES, DIFFERENT COLORS
            #self.ax.plot(y, linestyle=next(linelst), color=next(palette), label='Line %d'%i)
            # LINES WITH FILLED SYMBOLS
            #self.ax.plot(y, color=next(palette), marker=next(markerlst), label='Line %d'%i)
            # LINES WITH FILLED SYMBOLS WITH BLACK BORDERS
            #c=next(palette)
            #self.ax.plot(y, color=c, marker=next(markerlst), ms=12, markerfacecolor=c, markeredgewidth=1, markeredgecolor='black', label='Line %d'%i)
            # EMPTY SYMBOLS 
           
            #root.series=self.ax.scatter(x, y, marker=next(markerlst), s=120, facecolors='none', edgecolors=next(palette), linewidths=1, label='Line %02d'%(i+nold))

            
            # EMPTY BLACK AND WHITE SYMBOLS 
            #self.ax.scatter(x, y, marker=next(markerlst), s=120, facecolors='none', edgecolors='black', label='Line %d'%i)
            # FILLED SYMBOLS with Black borders
            #self.ax.scatter(x, y, marker=next(markerlst), s=120, facecolors=next(palette), edgecolors='black', label='Line %d'%i)
            #root = QTreeWidgetItem(ds.DataSettreeWidget, ['Line %d'%i, "%g"%np.sin(i), "%g"%(1-1/(i+1))])

           
                        
        # LEGEND STUFF
        leg=plt.legend(loc='upper left', frameon=True, ncol=2)
        if leg:
            leg.draggable()
            
        # LIMITS AND AXIS LABELS
        # TODO: Need to define a Units module to handle this!!!
        self.ax.set_xlim(0, num_points)
        self.ax.set_xlabel("t (s)")
        self.ax.set_ylabel("r (m)")
    
        plt.tight_layout(pad=1.2)
        self.canvas.draw()