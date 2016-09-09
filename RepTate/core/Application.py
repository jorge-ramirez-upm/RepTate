import logging
import itertools
import seaborn as sns   
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator, LogLocator

from CmdBase import *
from FileType import *
from View import *
from Theory import *
from DataSet import *

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
        self.views=[]
        self.filetypes={}
        self.theories={}
        self.datasets=[]
        self.current_view=0
        self.current_theory=0
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
        self.datasets.append(ds)
        ds.prompt = self.prompt[:-2]+'/'+ds.name+'> '
        ds.cmdloop()
 
    def do_delete(self, name):
        """Delete a dataset from the current application"""
        done=False
        for index, ds in enumerate(self.datasets):
            if (ds.name==name):
                self.datasets.remove(ds)
                done=True
        if (not done):
            print("Data Set \"%s\" not found"%name)            

    def complete_delete(self, text, line, begidx, endidx):
        """Complete delete dataset command"""
        dataset_names=[ds.name for ds in self.datasets]
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
        for ds in self.datasets:
            print("%s:\t%s"%(ds.name, ds.description))            
            # MORE DETAILS NEEDED?
            #if (self.check_files_exist()): 
            #    keylist=list(ds.file_parameters.keys())
            #    print("File\t",'\t'.join(keylist))
            #    for i, f in enumerate(ds.files):
            #        vallist=[]
            #        for k in keylist:
            #            vallist.append(f.file_parameters[k])
            #        if (f==ds.current_file):
            #            print("*%s\t%s"%(f.file_name_short,'\t'.join(vallist)))
            #        else:
            #            print(" %s\t%s"%(f.file_name_short,'\t'.join(vallist)))
            #    for i, t in enumerate(ds.theories):
            #        if (t==ds.current_theory):
            #            print("  *%s: %s\t %s"%(t.name, t.thname, t.description))
            #        else:
            #            print("   %s: %s\t %s"%(t.name, t.thname, t.description))
            
    #def do_dataset_plot(self, line):
    #    """Plot the current dataset using the current view"""
    #    if (not self.check_application_exist()): return
    #    if (not self.check_datasets_exist()): return
    #    self.current_application.plot_current_dataset()
        
    def do_switch(self, name):
        """ Switch the current dataset"""
        done=False
        for ds in self.datasets:
            if (ds.name==name):
                ds.cmdloop()
                done=True
        if (not done):
            print("Dataset \"%s\" not found"%line)                        

    def complete_switch(self, text, line, begidx, endidx):
        """ Complete the switch dataset command"""
        ds_names=[ds.name for ds in self.datasets]
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
        for view in self.views:
            if (view==self.current_view):
                print("*%s:\t%s"%(view.name,view.description))
            else:
                print("%s:\t%s"%(view.name,view.description))

    def do_view_switch(self, name):
        """Change to another view from open application"""
        done=False
        for view in self.views:
            if (view.name==name):
                self.current_view=view
                done=True
        if (not done):
            print("View \"%s\" not found"%name)                        

    def complete_view_switch(self, text, line, begidx, endidx):
        """Complete switch view command"""
        view_names=[vw.name for vw in self.views]
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

