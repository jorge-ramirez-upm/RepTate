import logging
import itertools
import seaborn as sns   
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator, LogLocator

from FileType import *
from View import *
from Theory import *
from DataSet import *

class Application(object):
    """Main abstract class that represents an application"""    
    name="Template"
    description="Abstract class that defines basic functionality"

    def __init__(self,):
        """Constructor of Application"""
        self.logger = logging.getLogger('ReptateLogger')
        self.views=[]
        self.filetypes={}
        self.theories={}
        self.datasets=[]
        self.current_view=0
        self.current_theory=0
        self.current_dataset=0
        self.num_datasets=0
        self.legend_visible = False        
            
        # MATPLOTLIB STUFF
        sns.set_style("white")
        sns.set_style("ticks")
        plt.style.use('seaborn-poster')
        self.figure = plt.figure(self.name)
        self.ax = self.figure.add_subplot(111)
        sns.despine() # Remove up and right side of plot box
        # LEGEND STUFF
        #leg=plt.legend([], [], loc='upper left', frameon=True, ncol=2, title='Hello')
        #if leg:
        #    leg.draggable()
        self.figure.show() # TO SEE THE RESULTS
        #self.figure.set_visible(True) #??? DOES IT DO ANYTHING?

    def new_dataset(self, name="DataSet", description=""):
        """Creates an empty dataset and adds it to the current application"""
        ds = DataSet(name, description)
        self.datasets.append(ds)
        self.current_dataset=ds
        self.num_datasets+=1

    def plot_current_dataset(self):
        palette = itertools.cycle(((0,0,0),(1.0,0,0),(0,1.0,0),(0,0,1.0),(1.0,1.0,0),(1.0,0,1.0),(0,1.0,1.0),(0.5,0,0),(0,0.5,0),(0,0,0.5),(0.5,0.5,0),(0.5,0,0.5),(0,0.5,0.5),(0.25,0,0),(0,0.25,0),(0,0,0.25),(0.25,0.25,0),(0.25,0,0.25),(0,0.25,0.25)))
        markerlst = itertools.cycle(('o', 'v', '^', '<', '>', '8', 's', 'p', '*', 'h', 'H', 'D', 'd')) 
        linelst = itertools.cycle((':', '-', '-.', '--'))

        for file in self.current_dataset.files:
            x=np.zeros((file.data_table.num_rows,1))
            y=np.zeros((file.data_table.num_rows,self.current_view.n))
            for i in range(file.data_table.num_rows):
                vec=file.data_table.data[i,:]
                x[i], y[i], success = self.current_view.view_proc(vec, file.file_parameters)
            marker=next(markerlst)
            color=next(palette)
            for i in range(file.data_table.MAX_NUM_SERIES):
                if (i<self.current_view.n):
                    file.data_table.series[i].set_data(x, y[:,i])
                    file.data_table.series[i].set_visible(True)
                    file.data_table.series[i].set_marker(marker)
                    file.data_table.series[i].set_markerfacecolor('none')
                    file.data_table.series[i].set_markeredgecolor(color)
                    file.data_table.series[i].set_markeredgewidth(1)
                    file.data_table.series[i].set_markersize(12)
                    file.data_table.series[i].set_linestyle('')
                    if (file.active and i==0):
                        file.data_table.series[i].set_label(file.file_name_short)
                    else:
                        file.data_table.series[i].set_label('')
                else:
                    file.data_table.series[i].set_visible(False)
                    file.data_table.series[i].set_label('')
        
        self.set_axes_properties()
        self.set_legend_properties()
        self.figure.canvas.draw()

    def set_axes_properties(self):       
        if (self.current_view.log_x): 
            self.ax.set_xscale("log")
            self.ax.xaxis.set_minor_locator(LogLocator(subs=range(10)))
        else:
            self.ax.set_xscale("linear")
            self.ax.xaxis.set_minor_locator(AutoMinorLocator())
        if (self.current_view.log_y): 
            self.ax.set_yscale("log")
            self.ax.yaxis.set_minor_locator(LogLocator(subs=range(10)))
        else:
            self.ax.set_yscale("linear")
            self.ax.yaxis.set_minor_locator(AutoMinorLocator())
        
        self.ax.set_xlabel(self.current_view.x_label)
        self.ax.set_ylabel(self.current_view.y_label)
        self.ax.relim(True)
        self.ax.autoscale_view()

    def set_legend_properties(self):
        leg=self.ax.legend(frameon=True, ncol=2)
        if (self.legend_visible):
            leg.draggable()
        else:
            leg.remove()
 