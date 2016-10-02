import logging
import itertools
import seaborn as sns   
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator, LogLocator
from matplotlib.widgets import Cursor

from CmdBase import *
from FileType import *
from View import *
from Theory import *
from DataSet import *
from TheoryBasic import *

class Application(CmdBase):
    """Main abstract class that represents an application"""    
    name="Template"
    description="Abstract class that defines basic functionality"

    def __init__(self, name="ApplicationTemplate", parent=None):
        """Constructor of Application"""
        super(Application, self).__init__() 
    
        self.name=name
        self.parent_manager = parent
        self.logger = logging.getLogger('ReptateLogger')
        self.views={}
        self.filetypes={}
        self.theories={}
        self.datasets={}
        self.current_view=0
        self.num_datasets=0
        self.legend_visible = False      

        # Theories available everywhere
        self.theories[TheoryPolynomial.thname]=TheoryPolynomial
        self.theories[TheoryPowerLaw.thname]=TheoryPowerLaw
            
        # MATPLOTLIB STUFF
        sns.set_style("white")
        sns.set_style("ticks")
        plt.style.use('seaborn-poster')
        self.figure = plt.figure(self.name)
        self.figure.canvas.mpl_connect('close_event', self.handle_close_window)
        self.ax = self.figure.add_subplot(111)
        sns.despine() # Remove up and right side of plot box
        #CURSOR STUFF
        #self.cursor = Cursor(self.ax, useblit=True, color='red', linewidth=1, linestyle='--')
        # LEGEND STUFF
        #leg=plt.legend([], [], loc='upper left', frameon=True, ncol=2, title='Hello')
        #if leg:
        #    leg.draggable()
        if (CmdBase.mode==CmdMode.cmdline):
            self.figure.show() 
        #self.figure.draw() # DOESN'T WORK!
        #self.figure.set_visible(True) #??? DOES IT DO ANYTHING?

    def handle_close_window(self, evt):
        print("\nApplication window %s has been closed\n"%self.name)
        print("Please, return to the RepTate prompt and delete de application")

    def do_new(self, line):
        """Create a new empty dataset in this application.
        Arguments: [NAME [, Description]]
                NAME: of the new dataset (optional)
                DESCRIPTION: of the dataset (optional)"""
        self.num_datasets+=1
        if (line==""):
            dsname="DataSet%02d"%self.num_datasets
            dsdescription=""
        else:
            items=line.split(',')
            dsname=items[0]
            if (len(items)>1):
                dsdescription=items[1]
            else:
                dsdescription=""
        ds = DataSet(dsname, dsdescription, self)
        self.datasets[dsname]=ds
        ds.prompt = self.prompt[:-2]+'/'+ds.name+'> '
        ds.cmdloop()
 
    def do_delete(self, name):
        """Delete a dataset from the current application"""
        if name in self.datasets.keys():
            del self.datasets[name]
        else:
            print("Data Set \"%s\" not found"%name)            

    def complete_delete(self, text, line, begidx, endidx):
        """Complete delete dataset command"""
        dataset_names=list(self.datasets.keys())
        if not text:
            completions = dataset_names[:]
        else:
            completions = [ f
                            for f in dataset_names
                            if f.startswith(text)
                            ]
        return completions

    def do_list(self, line):
        """List the datasets in the current application"""
        for ds in self.datasets.values():
            print("%s:\t%s"%(ds.name, ds.description))            
        
    def do_switch(self, name):
        """ Switch the current dataset"""
        done=False
        if name in self.datasets.keys():
            ds=self.datasets[name]
            ds.cmdloop()
        else:
            print("Dataset \"%s\" not found"%name)                        

    def complete_switch(self, text, line, begidx, endidx):
        """ Complete the switch dataset command"""
        ds_names=list(self.datasets.keys())
        if not text:
            completions = ds_names[:]
        else:
            completions = [ f
                            for f in ds_names
                            if f.startswith(text)
                            ]
        return completions

# FILE TYPE STUFF
    def do_filetype_available(self, line):
        """List available file types in the current application"""
        ftypes=list(self.filetypes.values())
        for ftype in ftypes:
            print("%s:\t%s\t*.%s"%(ftype.name,ftype.description,ftype.extension))

# VIEW STUFF
    def do_view_available(self, line):
        """List available views in the current application"""
        for view in self.views.values():
            if (view==self.current_view):
                print("*%s:\t%s"%(view.name,view.description))
            else:
                print("%s:\t%s"%(view.name,view.description))

    def do_view_switch(self, name):
        """Change to another view from open application"""
        done=False
        if name in list(self.views.keys()):
            self.current_view=self.views[name]
        else:
            print("View \"%s\" not found"%name)                        

    def complete_view_switch(self, text, line, begidx, endidx):
        """Complete switch view command"""
        view_names=list(self.views.keys())
        if not text:
            completions = view_names[:]
        else:
            completions = [ f
                            for f in view_names
                            if f.startswith(text)
                            ]
        return completions


# THEORY STUFF
    def do_theory_available(self, line):
        """List available theories in the current application"""
        for t in list(self.theories.values()):
            print("%s:\t%s"%(t.thname,t.description))

# LEGEND STUFF
    def do_legend_switch(self, line):
        self.legend_visible = not self.legend_visible 
        self.set_legend_properties()
        self.figure.canvas.draw()

# OTHER STUFF
    def update_plot(self):
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

