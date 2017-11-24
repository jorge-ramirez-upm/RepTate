import os
import glob

from enum import Enum
from CmdBase import *
from Theory import *
from FileType import *
from File import *
# from Application import *
from tabulate import tabulate
import itertools

class ColorMode(Enum):
    fixed = 0
    variable = 1
    gradient = 2
    modes = ["Fixed color", "Variable color (from palette)", "Color gradient"]
    color1 = (0, 0, 0, 1) #black RGB
    color2 =(1, 0, 0, 1) #red RGB
    colorpalettes = {
        "Rainbow": [(0,0,0),(1.0,0,0),(0,1.0,0),(0,0,1.0),(1.0,1.0,0),(1.0,0,1.0),(0,1.0,1.0),(0.5,0,0),(0,0.5,0),(0,0,0.5),(0.5,0.5,0),(0.5,0,0.5),(0,0.5,0.5),(0.25,0,0),(0,0.25,0),(0,0,0.25),(0.25,0.25,0),(0.25,0,0.25),(0,0.25,0.25)]
    }

class SymbolMode(Enum):
    fixed = 0
    fixedfilled = 1
    variable = 2
    variablefilled = 3
    modes = ["Fixed empty symbol","Fixed filled symbol", "Variable empty symbols", "Variable filled symbols"]
    symbol1 = '.'
    allmarkers = ['.','o','v','^','<','>','1','2','3','4','8','s','p','P','*','h','H','+','x','X','D','d','|','_']
    allmarkernames = ['point', 'circle', 'triangle_down', 'triangle_up','triangle_left', 'triangle_right', 'tri_down', 'tri_up', 'tri_left','tri_right', 'octagon', 'square', 'pentagon', 'plus (filled)','star', 'hexagon1', 'hexagon2', 'plus', 'x', 'x (filled)','diamond', 'thin_diamond', 'vline', 'hline']
    filledmarkers = ['.','o','v','^','<','>','8','s','p','P','*','h','H','X','D','d']
    filledmarkernames = ['point', 'circle', 'triangle_down', 'triangle_up','triangle_left', 'triangle_right', 'octagon', 'square', 'pentagon', 'plus (filled)','star', 'hexagon1', 'hexagon2', 'x (filled)','diamond', 'thin_diamond']

class DataSet(CmdBase): # cmd.Cmd not using super() is OK for CL mode.
    """Abstract class to describe a data set"""
    def __init__(self, name="DataSet", description="", parent=None):
        "Constructor"
        super().__init__() 

        self.name = name
        self.description = description
        self.parent_application = parent
        self.files = [] # TODO: Shall we change this list into a dict?
        self.current_file = None
        self.num_files = 0
        self.marker_size = 12
        self.line_width = 1
        self.colormode = ColorMode.variable
        self.color1 = ColorMode.color1.value
        self.color2 = ColorMode.color2.value
        self.palette = ColorMode.colorpalettes.value["Rainbow"]
        self.symbolmode = SymbolMode.fixed
        self.symbol1 = SymbolMode.symbol1.value
        self.theories = {}
        self.num_theories = 0
        self.inactive_files = {}
        self.current_theory = None

# DATASET STUFF ##########################################################################################################
    def do_list(self, line):
        """List the files in the current dataset"""
        keylist=list(ds.file_parameters.keys()) 
        print("File\t",'\t'.join(keylist))
        for f in self.files:
            for i, f in enumerate(ds.files):
                vallist=[]
                for k in keylist:
                    vallist.append(f.file_parameters[k])
                if (f==ds.current_file):
                    print("*%s\t%s"%(f.file_name_short,'\t'.join(vallist)))
                else:
                    print(" %s\t%s"%(f.file_name_short,'\t'.join(vallist)))
            for i, t in enumerate(ds.theories):
                print("   %s: %s\t %s"%(t.name, t.thname, t.description))

    def change_file_visibility(self, file_name_short, check_state=True):
        """Hide/Show file in the figure"""
        file_matching = []
        for file in self.files:
            if file.file_name_short == file_name_short: #find changed file
                file_matching.append(file)
        if len(file_matching)==0:
            raise ValueError ('Could not match file \"%s\"'%file_name_short)
            return
        if len(file_matching)>1:
            raise ValueError ('Too many match for file \"%s\"'%file_name_short)
            return

        file_matching[0].active = check_state
        for i in range(file_matching[0].data_table.MAX_NUM_SERIES):
            file_matching[0].data_table.series[i].set_visible(check_state)

        #save the check_state to recover it upon change of tab or 'view all' events
        if check_state==False:
            self.inactive_files[file_matching[0].file_name_short] = file_matching[0]
        else:
            try:
                del self.inactive_files[file_matching[0].file_name_short]
            except KeyError:
                pass
        self.do_plot()

    def do_show_all(self):
        for file in self.files:
            if file.file_name_short not in self.inactive_files:
                file.active = True
                for i in range(file.data_table.MAX_NUM_SERIES):
                    file.data_table.series[i].set_visible(True)
        if self.current_theory:
            self.theories[self.current_theory].do_show()

    def do_hide_all(self):
        for file in self.files:
            file.active = False
            for i in range(file.data_table.MAX_NUM_SERIES):
                file.data_table.series[i].set_visible(False)
        for th in self.theories.values():
            th.do_hide()

    def do_plot(self, line=""):
        """Plot the current dataset using the current view of the parent application"""
        # palette = itertools.cycle(((0,0,0),(1.0,0,0),(0,1.0,0),(0,0,1.0),(1.0,1.0,0),(1.0,0,1.0),(0,1.0,1.0),(0.5,0,0),(0,0.5,0),(0,0,0.5),(0.5,0.5,0),(0.5,0,0.5),(0,0.5,0.5),(0.25,0,0),(0,0.25,0),(0,0,0.25),(0.25,0.25,0),(0.25,0,0.25),(0,0.25,0.25)))
        #markerlst = itertools.cycle(('o', 'v', '^', '<', '>', '8', 's', 'p', '*', 'h', 'H', 'D', 'd')) 
        # markerlst = itertools.cycle(['.','o','v','^','<','>','1','2','3','4','8','s','p','P','*','h','H','+','x','X','D','d','|','_'])
        view = self.parent_application.current_view
        
        filled = False
        if self.symbolmode == SymbolMode.fixed: #single symbol, empty?
            markers = [self.symbol1]
        elif self.symbolmode == SymbolMode.fixedfilled: #single symbol, filled?
            markers = [self.symbol1]
            filled = True
        elif self.symbolmode == SymbolMode.variable: #variable symbols, empty
            markers = SymbolMode.allmarkers.value
        else: #
            markers = SymbolMode.filledmarkers.value #variable symbols, filled
            filled = True

        if self.colormode == ColorMode.fixed: #single color?
            colors = [self.color1]
        elif self.colormode == ColorMode.variable: #variable colors from palette
            colors = self.palette
        else:
            n = len(self.files) - len(self.inactive_files) #number of files to plot
            if n < 2:
                colors = [self.color1] # only one color needed
            else: #interpolate the color1 and color2 
                r1, g1, b1, a1 = self.color1
                r2, g2, b2, a2 =  self.color2
                dr = (r2 - r1)/(n - 1)
                dg = (g2 - g1)/(n - 1) 
                db = (b2 - b1)/(n - 1)
                da = (a2 - a1)/(n - 1) 
                colors = []
                for i in range(n): #create a color palette
                    colors.append((r1 + i*dr, g1 + i*dg, b1 + i*db, a1 + i*da))

        linelst = itertools.cycle((':', '-', '-.', '--'))
        palette = itertools.cycle((colors))
        markerlst = itertools.cycle((markers))
        size =  self.marker_size #if file.size is None else file.size
        width = self.line_width
        for file in self.files:
            try:
                x, y, success = view.view_proc(file.data_table, file.file_parameters)
            except TypeError as e:
                print(e)
                return

            marker = next(markerlst) #if file.marker is None else file.marker 
            color =  next(palette) #if file.color is None else file.color
            face = color if filled else 'none'

            for i in range(file.data_table.MAX_NUM_SERIES):
                if (i<view.n and file.active):
                    file.data_table.series[i].set_data(x[:,i], y[:,i])
                    file.data_table.series[i].set_visible(True)
                    file.data_table.series[i].set_marker(marker)
                    file.data_table.series[i].set_markerfacecolor(face)
                    file.data_table.series[i].set_markeredgecolor(color)
                    file.data_table.series[i].set_markeredgewidth(width)
                    file.data_table.series[i].set_markersize(size)
                    file.data_table.series[i].set_linestyle('')
                    if (file.active and i==0):
                        label=""
                        for pmt in file.file_type.basic_file_parameters:
                            try:
                                label+=pmt+'='+str(file.file_parameters[pmt])+' ';
                            except KeyError as e: #if parameter missing from data file
                                if CmdBase.mode!=CmdMode.GUI:
                                    print("Parameter %s not found in data file"%(e))
                        #file.data_table.series[i].set_label(file.file_name_short)
                        file.data_table.series[i].set_label(label)
                    else:
                        file.data_table.series[i].set_label('')
                else:
                    file.data_table.series[i].set_visible(False)
                    file.data_table.series[i].set_label('')
        
            for th in self.theories.values():
                tt = th.tables[file.file_name_short]
                x, y, success = view.view_proc(tt, file.file_parameters)
                for i in range(tt.MAX_NUM_SERIES):
                    if (i<view.n and file.active and th.active):
                        tt.series[i].set_data(x[:,i], y[:,i])
                        tt.series[i].set_visible(True)
                        tt.series[i].set_marker('')
                        tt.series[i].set_linestyle('-')
                        tt.series[i].set_color(color)
                        tt.series[i].set_label('')
                    else:
                        tt.series[i].set_visible(False)
                        tt.series[i].set_label('')
                th.plot_theory_stuff()
        
        # if CmdBase.mode!=CmdMode.GUI: 
        self.parent_application.update_plot()

    def do_sort(self, line):
        """Sort files in dataset according to the value of a file parameter
           sort Mw [,reverse]

           .. todo:: sort series in plot too
           """
        items=line.split(',')
        if (len(items)==0):
            print ("Wrong number of arguments")
        elif (len(items)==1):
            fp=items[0]
            rev=False
        elif (len(items)==2):
            fp=items[0]
            rev=(items[1].strip()=="reverse")
        else:
            print("Wrong number of arguments")

        if fp in self.current_file.file_parameters:
            self.files.sort(key = lambda x: float(x.file_parameters[fp]), reverse=rev)
        elif fp=="File":
            self.files.sort(key = lambda x: x.file_name_short, reverse=rev)
        else:
            print("Parameter %s not found in files"%line)

    def complete_sort(self, text, line, begidx, endidx):
        """Complete with the list of file parameters of the current file in the current dataset"""
        if (self.current_file==None):
            print ("A file must be selected first")
            return
        fp_names=list(self.current_file.file_parameters.keys())
        if not text:
            completions = fp_names[:]
        else:
            completions = [ f
                            for f in fp_names
                            if f.startswith(text)
                            ]
        return completions
            
# FILE STUFF ##########################################################################################################
    def do_delete(self, line):
        """Delete file from the data set"""
        done = False
        for index, f in enumerate(self.files):
            if (f.file_name_short==line):
                if (self.current_file==f):
                    self.current_file = None
                self.files.remove(f)
                done = True
        if (not done):
            print("File \"%s\" not found"%line)

    def complete_delete(self, text, line, begidx, endidx):
        f_names=[fl.file_name_short for fl in self.files]
        if not text:
            completions = f_names[:]
        else:
            completions = [ f
                            for f in f_names
                            if f.startswith(text)
                            ]
        return completions
    
    def do_list(self, line):
        """List the files in the current dataset"""
        for f in self.files:
            if (f==self.current_file):
                print("*%s"%f.file_name_short)
            else:
                print("%s"%f.file_name_short)

    def do_list_details(self, line):
        """List the files in the dataset with the file parameters"""
        for f in self.files:
            print(f)            

    def do_new(self, line):
        """
        Add an empty file of the given type to the current Data Set

        :param str line: Arguments: TYPE [, NAME]
        :param str TYPE: extension of file
        :param str NAME: Name (optional)
        """
        if (line==""): 
            print("Missing file type")
            return
        items=line.split(',')
        if (len(items)==0):
            print("Missing file type")
            return
        elif (len(items)==1):
            ext=items[0]
            fname=os.getcwd()+os.path.sep+"DummyFile%02d"%(self.num_files+1)+"."+ext
        elif (len(items)==2):
            ext=items[0]
            fname=os.getcwd()+os.path.sep+items[1]+"."+ext
        else:
            print("Wrong number of arguments")
        
        if (ext in self.parent_application.filetypes):  
            self.num_files+=1
            f = File(fname, self.parent_application.filetypes[ext], self, self.parent_application.ax)
            self.files.append(f)
            self.current_file=f
            #leg=self.current_application.ax.legend([], [], loc='upper left', frameon=True, ncol=2, title='Hello')
            #if leg:
            #    leg.draggable()
            #self.current_application.figure.canvas.draw()
        else:
            print("File type \"%s\" cannot be read by application %s"%(line,self.parent_application.name))
    
    def complete_new(self, text, line, begidx, endidx):
        """Complete new file command"""
        file_types=list(self.parent_application.filetypes.keys())
        if not text:
            completions = file_types[:]
        else:
            completions = [ f
                            for f in file_types
                            if f.startswith(text)
                            ]
        return completions

    def do_open(self, line):
        """
        Open file(s) from the current folder

        :param str line: FILENAMES (pattern expansion characters -- \*, ? -- allowed

        .. todo:: ALLOW OPENING FILES INSIDE SUBFOLDERS
        """
        if CmdBase.mode!=CmdMode.GUI:
            f_names = glob.glob(line)
        else:
            f_names = line
        
        newtables = []
        if (line=="" or len(f_names)==0): 
            message = "No valid file names provided"
            if CmdBase.mode!=CmdMode.GUI:
                print(message)
                return
            return (message, None, None)
        f_ext = [os.path.splitext(x)[1].split('.')[-1] for x in f_names]
        if (f_ext.count(f_ext[0])!=len(f_ext)):
            message = "File extensions of files must be equal!"
            if CmdBase.mode!=CmdMode.GUI:
                print (message)
                print (f_names)
                return
            return (message, None, None)

        if (f_ext[0] in self.parent_application.filetypes): 
            ft = self.parent_application.filetypes[f_ext[0]] 
            for f in f_names:
                df = ft.read_file(f, self, self.parent_application.ax)
                unique = True
                for file in self.files:
                    if df.file_name_short == file.file_name_short: #check if file already exists in current ds
                        unique = False
                if unique:
                    self.files.append(df)
                    self.current_file=df
                    newtables.append(df)
                    for th_name in self.theories:
                        #add a theory table
                        self.theories[th_name].tables[df.file_name_short]=DataTable(self.parent_application.ax)
                        self.theories[th_name].function(df)
            if CmdBase.mode==CmdMode.GUI:
                return (True, newtables, f_ext[0])
        else:
            message = "File type \"%s\" does not exists"%f_ext[0]
            if CmdBase.mode!=CmdMode.GUI:
                print (message)
                return
            return (message, None, None)
    
    # def reload_data(self):
    #     paths_to_open = []
    #     for file in self.files:
    #         paths_to_open.append([file.file_full_path, file.file_type])
    #     del self.files[:]

    #     for i in len(paths_to_open):
    #         path, ft = paths_to_open[i]
    #         df = ft.read_file(path, self, self.parent_application.ax)
            
        
        
            
        

    def __listdir(self, root):
        "List directory 'root' appending the path separator to subdirs."
        res = []
        for name in os.listdir(root):
            path = os.path.join(root, name)
            if os.path.isdir(path):
                name += os.sep
                #name += '/'
            res.append(name)
        return res


    def __complete_path(self, path=None):
        "Perform completion of filesystem path."
        if not path:
            return self.__listdir('.')
        
        dirname, rest = os.path.split(path)
        tmp = dirname if dirname else '.'
        res = [os.path.join(dirname, p)
                for p in self.__listdir(tmp) if p.startswith(rest)]
                
        # more than one match, or single match which does not exist (typo)
        if len(res) > 1 or not os.path.exists(path):
            return res
        # resolved to a single directory, so return list of files below it
        if os.path.isdir(path):
            return [os.path.join(path, p) for p in self.__listdir(path)]
        # exact file match terminates this completion
        return [path + ' ']

    def complete_open(self, text, line, begidx, endidx):
        """
        Complete the file_open command

        .. todo:: ALLOW COMPLETING FILES INSIDE SUBFOLDERS
        .. todo:: IF NO DATASET, CREATE EMPTY ONE
        .. todo:: IF NO APPLICATION, SEARCH AND OPEN AVAILABLE ONE THAT MATCHES FILE EXTENSION
        """
        "Completions for the cd command."
        test=line.split()
        if (len(test)>1):
            result=self.__complete_path(test[1])
        else:
            result=self.__complete_path()
        
        return result

        #f_names=[]
        #for f in list(self.parent_application.filetypes.keys()):
        #    pattern='%s**.%s'%(text,f)
        #    #f_names += glob.glob('data/**/*.%s'%f, recursive=True)
        #    f_names += glob.glob(pattern, recursive=True)
        #if not text:
        #    completions = f_names[:]
        #else:
        #    completions = [ f
        #                    for f in f_names
        #                    if f.startswith(text)
        #                    ]
        #return completions

    def do_switch(self, line):
        """Change active file in the current dataset"""
        for f in self.files:
            if (f.file_name_short==line):
                self.current_file=f    
                done=True
        if (not done):
            print("File \"%s\" not found"%line)                        

    #complete_switch = complete_delete

    def do_print(self, line):
        """
        Show the contents of the current file on the screen
        
        .. todo:: Change it so the file name can be selected
        """
        file = self.current_file
        print("Path: %s"%file.file_full_path)
        print(file.file_parameters)
        print(file.header_lines)
        print(file.data_table.data)
        print(tabulate(file.data_table.data, tablefmt="grid", floatfmt=".4g", headers=file.data_table.column_names))

# THEORY STUFF ##########################################################################################################
    def do_theory_delete(self, name):
        """Delete a theory from the current dataset"""
        if name in self.theories.keys():
            for table in self.theories[name].tables.values(): # remove matplotlib artist from ax
                for i in range(table.MAX_NUM_SERIES):
                    self.parent_application.ax.lines.remove(table.series[i])
            del self.theories[name]
        else:
            print("Theory \"%s\" not found"%name)            

    def complete_theory_delete(self, text, line, begidx, endidx):
        """Complete delete theory command"""
        th_names=list(self.theories.keys())
        if not text:
            completions = th_names[:]
        else:
            completions = [ f
                            for f in th_names
                            if f.startswith(text)
                            ]
        return completions

    def do_theory_list(self, line):
        """List open theories in current dataset"""
        for t in self.theories.values():
            print("   %s: %s\t %s"%(t.name, t.thname, t.description))

    def do_theory_new(self, line):
        """Add a new theory of the type specified to the current Data Set"""
        thtypes = list(self.parent_application.theories.keys())
        if (line in thtypes):
            if (self.current_file is None):
                print("Current dataset is empty\n"
                    "%s was not created"%line)
                return
            if self.parent_application.theories[line].single_file and len(self.files)>1:
                print("Theory %s cannot be applied to multiple data files"%line)
            self.num_theories += 1
            th_id = "%s%02d"%(line,self.num_theories)
            th = self.parent_application.theories[line](th_id, self, self.parent_application.ax)
            self.theories[th.name]=th
            if (self.mode!=CmdMode.GUI): 
                if (self.mode==CmdMode.batch):
                    th.prompt = ''
                else:
                    th.prompt = self.prompt[:-2]+'/'+th.name+'> '
                th.cmdloop()
            th.do_calculate("")
            return th
        else:
            print("Theory \"%s\" does not exists"%line)
    
    def complete_theory_new(self, text, line, begidx, endidx):
        """Complete new theory command"""        
        theory_names=list(self.parent_application.theories.keys())
        if not text:
            completions = theory_names[:]
        else:
            completions = [ f
                            for f in theory_names
                            if f.startswith(text)
                            ]
        return completions

    def do_theory_switch(self, line):
        """Change the active theory"""
        if line in self.theories.keys():
            th=self.theories[line]
            th.cmdloop()
        else:
            print("Theory \"%s\" not found"%line)                        
        
    def complete_theory_switch(self, text, line, begidx, endidx):
        """Complete the theory switch command"""
        completions = self.complete_theory_delete(text, line, begidx, endidx)
        return completions

    def do_legend(self, line):
        self.parent_application.do_legend(line)
