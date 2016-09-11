import os
import glob

from CmdBase import *
from Theory import *
from FileType import *
from File import *
from Application import *
#from DataTable import *

class DataSet(CmdBase):
    """Abstract class to describe a data set"""

    def __init__(self, name="DataSet", description="", parent=None):
        "Constructor"
        super(DataSet, self).__init__() 

        self.name=name
        self.description=description
        self.parent_application=parent

        self.files=[]
        self.current_file=None
        self.num_files=0

        self.theories=[]
        self.current_theory=None
        self.num_theories=0

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
                if (t==ds.current_theory):
                    print("  *%s: %s\t %s"%(t.name, t.thname, t.description))
                else:
                    print("   %s: %s\t %s"%(t.name, t.thname, t.description))

    def do_plot(self, line):
        """Plot the current dataset using the current view of the parent application"""
        palette = itertools.cycle(((0,0,0),(1.0,0,0),(0,1.0,0),(0,0,1.0),(1.0,1.0,0),(1.0,0,1.0),(0,1.0,1.0),(0.5,0,0),(0,0.5,0),(0,0,0.5),(0.5,0.5,0),(0.5,0,0.5),(0,0.5,0.5),(0.25,0,0),(0,0.25,0),(0,0,0.25),(0.25,0.25,0),(0.25,0,0.25),(0,0.25,0.25)))
        markerlst = itertools.cycle(('o', 'v', '^', '<', '>', '8', 's', 'p', '*', 'h', 'H', 'D', 'd')) 
        linelst = itertools.cycle((':', '-', '-.', '--'))

        view = self.parent_application.current_view
        for file in self.files:
            x=np.zeros((file.data_table.num_rows,1))
            y=np.zeros((file.data_table.num_rows,view.n))
            for i in range(file.data_table.num_rows):
                vec=file.data_table.data[i,:]
                x[i], y[i], success = view.view_proc(vec, file.file_parameters)
            marker=next(markerlst)
            color=next(palette)
            for i in range(file.data_table.MAX_NUM_SERIES):
                if (i<view.n):
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
        
        self.parent_application.update_plot()

    def do_sort(self, line):
        """Sort files in dataset according to the value of a file parameter
           sort Mw [,reverse]
           
           """
        items=line.split(',')
        if (len(items)==0):
            print ("Wrong number of arguments")
        elif (len(items)==1):
            fp=items[0]
            rev=False
        elif (len(items)==2):
            fp=items[0]
            rev=(items[1]=="reverse")
        else:
            print("Wrong number of arguments")

        if fp in self.current_file.file_parameters:
            self.files.sort(key = lambda x: float(x.file_parameters[fp]), reverse=rev)
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
        done=False
        for index, f in enumerate(self.files):
            if (f.file_name_short==line):
                if (self.current_file==f):
                    self.current_file=None
                self.files.remove(f)
                done=True
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
        """Add an empty file of the given type to the current Data Set
        Arguments: TYPE [, NAME]
                TYPE: extension of file
                NAME: Name (optional)
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
        """Open file(s) from the current folder
           Arguments: FILENAMES (pattern expansion characters -- *, ? -- allowed
           TODO: ALLOW OPENING FILES INSIDE SUBFOLDERS
        """
        f_names = glob.glob(line)
        if (line=="" or len(f_names)==0): 
            print("No valid file names provided")
            return        
        f_ext = [os.path.splitext(x)[1].split('.')[-1] for x in f_names]
        if (f_ext.count(f_ext[0])!=len(f_ext)):
            print ("File extensions of files must be equal!")
            print (f_names)
            return
        if (f_ext[0] in self.parent_application.filetypes): 
            ft = self.parent_application.filetypes[f_ext[0]] 
            for f in f_names:
                df = ft.read_file(f, self, self.parent_application.ax)
                self.files.append(df)
                self.current_file=df
        else:
            print("File type \"%s\" does not exists"%f_ext[0])

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
        """Complete the file_open command
           TODO: ALLOW COMPLETING FILES INSIDE SUBFOLDERS
           TODO: IF NO DATASET, CREATE EMPTY ONE
           TODO: IF NO APPLICATION, SEARCH AND OPEN AVAILABLE ONE THAT MATCHES FILE EXTENSION
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

    complete_switch = complete_delete

    def do_print(self, line):
        """Show the contents of the current file on the screen
           TODO: Change it so the file name can be selected"""
        file = self.current_file
        print("Path: %s"%file.file_full_path)
        print(file.file_parameters)
        print(file.header_lines)
        print(file.data_table.data)

# THEORY STUFF ##########################################################################################################
    def do_theory_delete(self, name):
        """Delete a theory from the current dataset"""
        done=False
        for index, th in enumerate(self.current_application.current_dataset.theories):
            if (th.name==name):
                if (self.current_application.current_dataset.current_theory==th):
                    if (index<len(self.current_application.current_dataset.theories)-1):
                        self.current_application.current_dataset.current_theory=self.current_application.current_dataset.theories[index+1]
                    else:
                        self.current_application.current_dataset.current_theory=self.current_application.current_dataset.theories[0]
                self.current_application.current_dataset.theories.remove(th)
                done=True
        if (not done):
            print("Theory \"%s\" not found"%name)            

    def complete_theory_delete(self, text, line, begidx, endidx):
        """Complete delete theory command"""
        th_names=[]
        for th in self.current_application.current_dataset.theories:
            th_names.append(th.name)
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
        for t in self.theories:
            if (t==self.current_theory):
                print("  *%s: %s\t %s"%(t.name, t.thname, t.description))
            else:
                print("   %s: %s\t %s"%(t.name, t.thname, t.description))

    def do_theory_new(self, line):
        """Add a new theory of the type specified to the current Data Set"""
        thtypes=list(self.parent_application.theories.keys())
        if (line in thtypes):
            self.num_theories+=1
            
            th=self.parent_application.theories[line]("%s%02d"%(line,self.num_theories), self, self.parent_application.ax)
            self.theories.append(th)
            self.current_theory=th
            th.prompt = self.prompt[:-2]+'/'+th.name+'> '
            th.cmdloop()
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
        if (not self.check_application_exist()): return
        if (not self.check_datasets_exist()): return
        for th in self.current_application.current_dataset.theories:
            if (th.name==line):
                self.current_application.current_dataset.current_theory=th
                done=True
        if (not done):
            print("Theory \"%s\" not found"%line)                        
        
    def complete_theory_switch(self, text, line, begidx, endidx):
        """Complete the theory switch command"""
        completions = self.complete_theory_delete(text, line, begidx, endidx)
        return completions

