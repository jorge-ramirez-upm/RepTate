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
"""Module Multiview

Organise the mmultiple Matplotlib views

"""
import sys
import enum
import math
import numpy as np
import itertools
from RepTate.core.CmdBase import CmdBase, CmdMode
#from UI_Multimatplotlib import Ui_Form
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QHBoxLayout, QTabWidget, QWidget, QSizePolicy
from PyQt5.QtCore import QSize, QMetaObject, Qt
import matplotlib as mpl
mpl.use("Qt5Agg")
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
    LEFT=0.15
    RIGHT=0.98
    BOTTOM=0.15
    TOP=0.98
    WSPACE=0.25
    HSPACE=0.35
    DPI = 300

    def __init__(self, pot=PlotOrganizationType.Vertical, nplots=1, ncols=1, parent=None):
        #QDialog.__init__(self)
        #super().__init__(self)
        #QWidget.__init__()
        super().__init__()
        self.parent_application = parent
        self.pot = pot
        self.nplots = nplots
        self.ncols = ncols
        self.setupUi()
        mpl.rcParams['savefig.dpi'] = self.DPI

    def setupUi(self):
        # Remove seaborn dependency
        dark_gray = ".15"
        light_gray = ".8"
        style_dict = {
            "figure.facecolor": "white",
            "text.color": dark_gray,
            "axes.labelcolor": dark_gray,
            "axes.facecolor": "white",
            "axes.edgecolor": dark_gray,
            "axes.linewidth": 1.25,
            "grid.color": light_gray,
            "legend.frameon": False,
            "legend.numpoints": 1,
            "legend.scatterpoints": 1,
            "xtick.direction": "out",
            "ytick.direction": "out",
            "xtick.color": dark_gray,
            "ytick.color": dark_gray,
            "xtick.major.size": 6,
            "ytick.major.size": 6,
            "xtick.minor.size": 3,
            "ytick.minor.size": 3,
            "axes.grid": False,
            "axes.axisbelow": True,
            "image.cmap": "rocket",
            "font.family": ["sans-serif"],
            "font.sans-serif": ["Arial", "DejaVu Sans", "Liberation Sans",
                                "Bitstream Vera Sans", "sans-serif"],
            "grid.linestyle": "-",
            "lines.solid_capstyle": "round",
            }
        mpl.rcParams.update(style_dict)

        self.setObjectName("self")
        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.plotselecttabWidget = QTabWidget(self)
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

        self.set_bbox()

        self.canvas = FigureCanvasQTAgg(self.figure)
        self.canvas.setFocusPolicy( Qt.ClickFocus )
        self.canvas.setFocus()
        self.plotcontainer.addWidget(self.canvas)
        self.init_plot(0)

        connection_id = self.plotselecttabWidget.currentChanged.connect(self.handle_plottabChanged)
        axes = plt.gcf().axes
        for ax_i in axes:
            for side in ["top", "right"]:
                ax_i.spines[side].set_visible(False)

            ax_i.xaxis.tick_bottom()
            ax_i.yaxis.tick_left()
        self.hidden_tab = []

    def set_bbox(self):
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
        self.bboxmax = [x0min, y0min, x1max-x0min, y1max-y0min]

    def reorg_fig(self, nplots):
        """Reorganise the views to show nplots"""
        if CmdBase.mode == CmdMode.GUI:
            self.parent_application.sp_nviews.blockSignals(True)
            self.parent_application.sp_nviews.setValue(nplots)
            self.parent_application.sp_nviews.blockSignals(False)

        self.plotselecttabWidget.blockSignals(True)
        nplot_old = self.nplots
        self.nplots = nplots
        gs = self.organizeplots(self.pot, self.nplots, self.ncols)

        # hide tabs if only one figure
        self.plotselecttabWidget.setVisible(nplots > 1)

        for i in range(nplots):
            self.axarr[i].set_position(gs[i].get_position(self.figure))
            self.axarr[i].set_subplotspec(gs[i])
        for tab in self.hidden_tab:
            tab_id = tab[0]
            widget = tab[1]
            tab_text = tab[2]
            self.plotselecttabWidget.insertTab(tab_id, widget, tab_text)
        self.hidden_tab = []

        for i in range(nplots, len(self.axarr)):
            self.axarr[i].set_visible(False)
            tab_id = i + 1
            widget = self.plotselecttabWidget.widget(nplots + 1)
            tab_text = self.plotselecttabWidget.tabText(nplots + 1)
            self.hidden_tab.append([tab_id, widget, tab_text])
            self.plotselecttabWidget.removeTab(nplots + 1)

        self.set_bbox()
        for i in range(self.nplots):
            self.axarr[i].set_position(self.bbox[i])
        # add new axes to plt
        for i in range(nplot_old, self.nplots):
            try:
                plt.subplot(self.axarr[i])
            except:
                pass
        # remove axes from plt
        for i in range(self.nplots, nplot_old):
            try:
                plt.delaxes(self.axarr[i])
            except:
                pass
        for ds in self.parent_application.datasets.values():
            ds.nplots = nplots
        self.parent_application.update_all_ds_plots()
        self.handle_plottabChanged(0) # switch to all plot tab
        self.plotselecttabWidget.blockSignals(False)

    def init_plot(self, index):
        if index == 0: #multiplots
            for i in range(self.nplots):
                self.axarr[i].set_position(self.bbox[i])
        else: #single plot max-size
            tab_to_maxi = index - 1
            for i in range(self.nplots):
                if i == tab_to_maxi: #hide other plots
                    self.axarr[i].set_visible(True)
                    self.axarr[i].set_position(self.bboxmax)
                else:
                    self.axarr[i].set_visible(False)

        self.parent_application.current_viewtab = index
        self.canvas.draw()

    def handle_plottabChanged(self, index):
        self.parent_application.current_viewtab = index
        if index == 0: #multiplots
            view_name = self.parent_application.multiviews[0].name
            if CmdBase.mode == CmdMode.GUI:
                ind = self.parent_application.viewComboBox.findText(view_name, Qt.MatchExactly)
                self.parent_application.viewComboBox.blockSignals(True)
                self.parent_application.viewComboBox.setCurrentIndex(ind) #set the view combobox according to current view
                self.parent_application.viewComboBox.blockSignals(False)
            for i in range(self.nplots):
                self.axarr[i].set_position(self.bbox[i])
                self.axarr[i].set_visible(True)
                try:
                    plt.subplot(self.axarr[i])
                except:
                    pass

        else: #single plot max-size
            tab_to_maxi = index - 1 # in 0 1 2
            view_name = self.parent_application.multiviews[tab_to_maxi].name
            if CmdBase.mode == CmdMode.GUI:
                ind = self.parent_application.viewComboBox.findText(view_name)
                self.parent_application.viewComboBox.blockSignals(True)
                self.parent_application.viewComboBox.setCurrentIndex(ind) #set the view combobox according to current view
                self.parent_application.viewComboBox.blockSignals(False)
            for i in range(self.nplots):
                if i == tab_to_maxi: #hide other plots
                    self.axarr[i].set_visible(True)
                    self.axarr[i].set_position(self.bboxmax)
                    try:
                        plt.subplot(self.axarr[i])
                    except:
                        pass
                else:
                    self.axarr[i].set_visible(False)
                    try:
                        plt.delaxes(self.axarr[i])
                    except:
                        pass
        self.parent_application.update_datacursor_artists()
        self.canvas.draw()
        self.parent_application.set_view_tools(view_name)

    def organizeHorizontal(self, nplots):
        gs = gridspec.GridSpec(1, self.nplots,left=self.LEFT,right=self.RIGHT,
                                  bottom=self.BOTTOM,top=self.TOP,
                                  wspace=self.WSPACE,hspace=self.HSPACE)
        return gs

    def organizeVertical(self, nplots):
        gs = gridspec.GridSpec(self.nplots, 1,left=self.LEFT,right=self.RIGHT,
                                  bottom=self.BOTTOM,top=self.TOP,
                                  wspace=self.WSPACE,hspace=self.HSPACE)
        return gs

    def organizeOptimalRow(self, nplots, ncols):
        row = math.ceil(nplots / ncols)
        gstmp = gridspec.GridSpec(row, ncols,left=self.LEFT,right=self.RIGHT,
                                  bottom=self.BOTTOM,top=self.TOP,
                                  wspace=self.WSPACE,hspace=self.HSPACE)
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
        gstmp = gridspec.GridSpec(row, ncols,left=self.LEFT,right=self.RIGHT,
                                  bottom=self.BOTTOM,top=self.TOP,
                                  wspace=self.WSPACE,hspace=self.HSPACE)
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
