import logging
import itertools
import seaborn as sns   
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator, LogLocator, NullFormatter
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
        print("Application.__init__(self, name='ApplicationTemplate', parent=None) called")
        super(Application, self).__init__() 
        print("Application.__init__(self, name='ApplicationTemplate', parent=None) ended")

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
        # self.theories[TheoryPolynomial.thname]=TheoryPolynomial
        # self.theories[TheoryPowerLaw.thname]=TheoryPowerLaw
        # self.theories[TheoryExponential.thname]=TheoryExponential
        # self.theories[TheoryExponential2.thname]=TheoryExponential2
            
        # MATPLOTLIB STUFF
        sns.set_style("white")
        sns.set_style("ticks")
        plt.style.use('seaborn-poster')
        self.figure = plt.figure(self.name)
        self.figure.canvas.mpl_connect('close_event', self.handle_close_window)
        self.figure.canvas.mpl_connect('scroll_event', self.zoom_wheel)
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

    def zoom_wheel(self, event):
        # get the current x and y limits
        base_scale = 1.1
        cur_xlim = self.ax.get_xlim()
        cur_ylim = self.ax.get_ylim()
        # set the range
        #cur_xrange = (cur_xlim[1] - cur_xlim[0])*.5
        #cur_yrange = (cur_ylim[1] - cur_ylim[0])*.5
        xdata = event.xdata # get event x location
        ydata = event.ydata # get event y location
        if event.button == 'up':
            # deal with zoom in
            scale_factor = 1/base_scale
        elif event.button == 'down':
            # deal with zoom out
            scale_factor = base_scale
        else:
            # deal with something that should never happen
            scale_factor = 1
            #print event.button
        # Get distance from the cursor to the edge of the figure frame
        x_left = xdata - cur_xlim[0]
        x_right = cur_xlim[1] - xdata
        y_top = ydata - cur_ylim[0]
        y_bottom = cur_ylim[1] - ydata
        # set new limits
        self.ax.set_xlim([xdata - x_left*scale_factor,
                    xdata + x_right*scale_factor])
        self.ax.set_ylim([ydata - y_top*scale_factor,
                    ydata + y_bottom*scale_factor])
        self.ax.figure.canvas.draw() # force re-draw

    def new(self, line):
        """Create new empty dataset in the application"""
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
        return ds, dsname
    
    def do_new(self, line):
        """
        Create a new empty dataset in this application.

        :param str line: [NAME [, Description]]
        :param str NAME: Name of the new dataset (optional)
        :param str DESCRIPTION: Description of the dataset (optional)
        """
        ds, dsname = self.new(line)
        self.datasets[dsname] = ds
        if (self.mode==CmdMode.batch):
            ds.prompt = ''
        else:
            ds.prompt = self.prompt[:-2]+'/'+ds.name+'> '
        ds.cmdloop()
 
    def delete(self, ds_name):
        """Delete a dataset from the current application"""
        if ds_name in self.datasets.keys():
            for th in self.datasets[ds_name].theories.values(): #loop over the DataSet theories
                for table in th.tables.values(): 
                    for i in range(table.MAX_NUM_SERIES):
                        self.ax.lines.remove(table.series[i]) #remove theory matplotlib artist from ax
            del self.datasets[ds_name].theories
            for file in self.datasets[ds_name].files: 
                for i in range(file.data_table.MAX_NUM_SERIES):
                    self.ax.lines.remove(file.data_table.series[i]) #remove data matplotlib artist from ax
            del self.datasets[ds_name] #delete object
        else:
            print("Data Set \"%s\" not found"%ds_name)            
        
 
    def do_delete(self, name):
        """Delete a dataset from the current application"""
        self.delete(name)

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

    def list(self):
        """List the datasets in the current application"""
        for ds in self.datasets.values():
            print("%s:\t%s"%(ds.name, ds.description))            
        
        
    def do_list(self, line):
        """List the datasets in the current application"""
        self.list()
        
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
    def filetype_available(self):
        """List available file types in the current application"""
        ftypes=list(self.filetypes.values())
        for ftype in ftypes:
            print("%s:\t%s\t*.%s"%(ftype.name,ftype.description,ftype.extension))    

    def do_filetype_available(self, line):
        """List available file types in the current application"""
        self.filetype_available()
        
# VIEW STUFF
    def view_available(self):
        """List available views in the current application"""
        for view in self.views.values():
            if (view==self.current_view):
                print("*%s:\t%s"%(view.name,view.description))
            else:
                print("%s:\t%s"%(view.name,view.description))
    
    def do_view_available(self, line):
        """List available views in the current application"""
        self.view_available()
        
    def view_switch(self, name):
        """Change to another view from open application"""
        if name in list(self.views.keys()):
            self.current_view=self.views[name]
        else:
            print("View \"%s\" not found"%name)
        # Update the plots!
        # Loop over datasets and call do_plot()
        self.update_all_ds_plots()
    
    def update_all_ds_plots(self):
        for ds in self.datasets.values():
            ds.do_plot()

    def do_view_switch(self, name):
        """Change to another view from open application"""
        self.view_switch(name)
        
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
    def theory_available(self):
        """List available theories in the current application"""
        for t in list(self.theories.values()):
            print("%s:\t%s"%(t.thname,t.description))    
    
    def do_theory_available(self, line):
        """List available theories in the current application"""
        self.theory_available()
        
# LEGEND STUFF
    def legend(self):
        self.legend_visible = not self.legend_visible 
        self.set_legend_properties()
        self.figure.canvas.draw()

    def do_legend(self, line):
        self.legend()
    
# OTHER STUFF
    def update_plot(self):
        self.set_axes_properties()
        self.set_legend_properties()
        self.figure.canvas.draw()   

    def set_axes_properties(self):       
        if (self.current_view.log_x): 
            self.ax.set_xscale("log")
            #self.ax.xaxis.set_minor_locator(LogLocator(subs=range(10)))
            locmaj = LogLocator(base=10.0, subs=(1.0, ), numticks=100)
            self.ax.xaxis.set_major_locator(locmaj)
            locmin = LogLocator(base=10.0, subs=np.arange(2, 10) * .1, numticks=100)
            self.ax.xaxis.set_minor_locator(locmin)
            self.ax.xaxis.set_minor_formatter(NullFormatter())
        else:
            self.ax.set_xscale("linear")
            self.ax.xaxis.set_minor_locator(AutoMinorLocator())
        if (self.current_view.log_y): 
            self.ax.set_yscale("log")
            #self.ax.yaxis.set_minor_locator(LogLocator(subs=range(10)))
            locmaj = LogLocator(base=10.0, subs=(1.0, ), numticks=100)
            self.ax.yaxis.set_major_locator(locmaj)
            locmin = LogLocator(base=10.0, subs=np.arange(2, 10) * .1, numticks=100)
            self.ax.yaxis.set_minor_locator(locmin)
            self.ax.yaxis.set_minor_formatter(NullFormatter())
        else:
            self.ax.set_yscale("linear")
            self.ax.yaxis.set_minor_locator(AutoMinorLocator())
        
        self.ax.set_xlabel(self.current_view.x_label + ' [' + self.current_view.x_units + ']')
        self.ax.set_ylabel(self.current_view.y_label + ' [' + self.current_view.y_units + ']')
        self.ax.relim(True)
        self.ax.autoscale(True)
        self.ax.autoscale_view()

    def set_legend_properties(self):
        leg=self.ax.legend(frameon=True, ncol=2)
        if (self.legend_visible):
            leg.draggable()
        else:
            try:
                leg.remove()
            except AttributeError as e:
                pass
                #print("legend: %s"%e)

