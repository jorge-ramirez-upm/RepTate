import sys
import enum
import math
import numpy as np
import itertools
import seaborn as sns   
#from UI_Multimatplotlib import Ui_Form
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QHBoxLayout, QTabWidget, QWidget, QSizePolicy
from PyQt5.QtCore import QSize, QMetaObject, Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
import matplotlib.gridspec as gridspec

class PlotOrganizationType(enum.Enum):
    """[summary]
    
    For Vertical and Horizontal, the number of columns is discarded
    Vertical:
    -------
    -------
    -------
    ...
    -------

    Horizontal:
    |  |  | ... |

    OptimalRow:
    The plots are organized in nplots/ncols X ncols giving more importance to the first plot, 
    which will occupy as much space as available from the first row

    OptimalColumn:
    The plots are organized in nplots/ncols X ncols giving more importance to the first plot, 
    which will occupy as much space as available from the first column

    Specified:
    The user must provide a GridSpec with the desired organization of plots

    """
    Vertical=0
    Horizontal=1
    OptimalRow=2
    OptimalColumn=3
    Specified=4

class MultiView(QWidget):
    def __init__(self, pot=PlotOrganizationType.Vertical, nplots=1, ncols=1, parent=None):
        QDialog.__init__(self)
        self.pot = pot
        self.nplots = nplots
        self.ncols = ncols
        self.setupUi(self)
        self.parent = parent
        
    def setupUi(self, matplotlibWidget):
        sns.set_style("white")
        sns.set_style("ticks")
        plt.style.use('seaborn-poster')
        matplotlibWidget.setObjectName("matplotlibWidget")
        self.horizontalLayout = QHBoxLayout(matplotlibWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.plotselecttabWidget = QTabWidget(matplotlibWidget)
        self.plotselecttabWidget.setMaximumSize(QSize(22, 1000))
        self.plotselecttabWidget.setTabPosition(QTabWidget.West)
        self.plotselecttabWidget.setTabShape(QTabWidget.Triangular)
        self.plotselecttabWidget.setUsesScrollButtons(False)
        self.plotselecttabWidget.setDocumentMode(False)
        self.plotselecttabWidget.setTabsClosable(False)
        self.plotselecttabWidget.setObjectName("plotselecttabWidget")
        self.plotselecttabWidget.setStyleSheet("QTabBar::tab { color:black; height: 40px; }")

        # Create a tab for all plots
        if (self.nplots>1):
            self.tab = QWidget()
            self.tab.setMaximumSize(QSize(0, 0))
            self.plotselecttabWidget.addTab(self.tab, "All")
        else:
            self.plotselecttabWidget.setVisible(False)
        # Create a tab for each plot
        for i in range(self.nplots):
            self.tab = QWidget()
            self.tab.setMaximumSize(QSize(0, 0))
            self.plotselecttabWidget.addTab(self.tab, "%d"%(i+1))
        self.horizontalLayout.addWidget(self.plotselecttabWidget)
        self.plotselecttabWidget.setCurrentIndex(0)
       
        self.plotcontainer = QVBoxLayout()
        self.plotcontainer.setObjectName("plotcontainer")
        self.horizontalLayout.addLayout(self.plotcontainer)    
        
        # Create the multiplot figure
        gs = self.organizeplots(self.pot, self.nplots, self.ncols)
        self.axarr = []
        self.figure = plt.figure()
        for i in range(self.nplots):
            self.axarr.append(self.figure.add_subplot(gs[i]))
        
        #self.figure, self.axarr = plt.subplots(self.nplots)
        self.bbox = []
        x0min = y0min = 1e9
        x1max = y1max = -1e9
        for i in range(self.nplots):
            bboxnow = self.axarr[i].get_position()
            self.bbox.append(bboxnow)
            x0min = min(x0min, bboxnow.x0)
            y0min = min(y0min, bboxnow.y0)
            x1max = max(x1max, bboxnow.x1)
            y1max = max(y1max, bboxnow.y1)

        #fine tuning specific to nplots=3
        self.bbox[0].y0 += 0.1
        self.bbox[0].y1 += 0.1
        self.bbox[1].x1 -= 0.05
        self.bbox[2].x0 += 0.05
        #make room for axes labels in single plot
        y0min += 0.1
        x0min += 0.05
        self.bboxmax = [x0min, y0min, x1max-x0min, y1max-y0min]

        self.canvas = FigureCanvasQTAgg(self.figure)
        self.canvas.setFocusPolicy( Qt.ClickFocus )
        self.canvas.setFocus()
        self.plotcontainer.addWidget(self.canvas)

        connection_id = self.plotselecttabWidget.currentChanged.connect(self.handle_plottabChanged)        
        sns.despine()
        
    def handle_plottabChanged(self, index):
        if index == 0: #multiplots
            for i in range(self.nplots):
                self.axarr[i].set_position(self.bbox[i])
                self.axarr[i].set_visible(True)
        else: #single plot max-size
            tab_to_maxi = index - 1
            for i in range(self.nplots):
                if i == tab_to_maxi: #hide other plots
                    self.axarr[i].set_visible(True)
                    self.axarr[i].set_position(self.bboxmax)
                else:
                    self.axarr[i].set_visible(False)
        self.canvas.draw()

    def organizeHorizontal(self, nplots):
        gs = gridspec.GridSpec(1, self.nplots)
        return gs

    def organizeVertical(self, nplots):
        gs = gridspec.GridSpec(self.nplots, 1)
        return gs

    def organizeOptimalRow(self, nplots, ncols):
        row = math.ceil(nplots / ncols)
        gstmp = gridspec.GridSpec(row, ncols)
        gs=[]
        # First row might be different
        gs.append(gstmp[0,0:row*ncols-nplots+1])
        for j in range(row*ncols-nplots+1,ncols):
            gs.append(gstmp[0,j])
        for i in range(1,row):
            for j in range(ncols):
                gs.append(gstmp[i,j])
        return gs

    def organizeOptimalColumn(self, nplots, ncols):
        row = math.ceil(nplots/ncols)
        gstmp = gridspec.GridSpec(row, ncols)
        gs = []
        # First column might be different
        gs.append(gstmp[0:row*ncols-nplots+1,0])
        for j in range(row*ncols-nplots+1,row):
            gs.append(gstmp[j,0])
        for i in range(1,ncols):
            for j in range(row):
                gs.append(gstmp[j, i])

        return gs

    def organizeplots(self, organizationtype, nplots=1, ncols=1, gs=None):
        if organizationtype == PlotOrganizationType.Vertical:
            return self.organizeVertical(nplots)
        elif organizationtype == PlotOrganizationType.Horizontal:
            return self.organizeHorizontal(nplots)
        elif organizationtype == PlotOrganizationType.OptimalRow:
            return self.organizeOptimalRow(nplots, ncols)
        elif organizationtype == PlotOrganizationType.OptimalColumn:
            return self.organizeOptimalColumn(nplots, ncols)
        elif organizationtype == PlotOrganizationType.Specified:
            pass
        elif organizationtype == PlotOrganizationType.DefaultOrganization:
            pass
