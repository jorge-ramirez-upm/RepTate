import os
import cmd
import sys
import logging
import logging.handlers
import readline

from ApplicationTest import *
from ApplicationGt import *

class ApplicationManager(cmd.Cmd):
    """Main Reptate container of applications"""

    version = '0.1'
    prompt = 'reptate> '
    intro = 'Reptate Version %s command processor'%version
    
    def __init__ (self, parent=None):
        """Constructor """
        cmd.Cmd.__init__(self)        

        # SETUP LOG
        self.reptatelogger = logging.getLogger('ReptateLogger')
        self.reptatelogger.setLevel(logging.DEBUG) # INFO, WARNING
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
        #log_file_name = 'reptate.log'
        #handler = logging.handlers.RotatingFileHandler(
        #    log_file_name, maxBytes=20000, backupCount=2, mode='w')
        #MainWindow.reptatelogger.addHandler(handler)

        # SETUP READLINE, COMMAND HISTORY FILE, ETC
        readline.read_history_file()

        # SETUP APPLICATIONS
        self.application_counter=0
        self.applications=[]
        self.available_applications={}
        self.available_applications[ApplicationTest.name]=ApplicationTest
        self.available_applications[ApplicationGt.name]=ApplicationGt
        self.current_application=None

# APPLICATION STUFF
    def do_application_available(self, line):
        """List available applications"""
        for app in list(self.available_applications.values()):
            print("%s: %s"%(app.name,app.description))

    def do_application_delete(self, name):
        """Delete an open application"""
        done=False
        for index, app in enumerate(self.applications):
            if (app.name==name):
                if (self.current_application==app):
                    if (index<len(self.applications)-1):
                        self.current_application=self.applications[index+1]
                    else:
                        self.current_application=self.applications[0]
                self.applications.remove(app)
                done=True
        if (not done):
            print("Application \"%s\" not found"%name)            

    def complete_application_delete(self, text, line, begidx, endidx):
        """Complete delete application command"""
        app_names=[]
        for app in self.applications:
            app_names.append(app.name)
        if not text:
            completions = app_names[:]
        else:
            completions = [ f
                            for f in app_names
                            if f.startswith(text)
                            ]
        return completions

    def do_application_list(self, line):
        """List open applications"""
        for app in self.applications:
            if (app==self.current_application):
                print("*%s: %s"%(app.name,app.description))
            else:
                print("%s: %s"%(app.name,app.description))

    def do_application_new(self, name):
        """ Create new application"""
        if (name in self.available_applications):
            self.application_counter+=1
            newapp=self.available_applications[name]()
            newapp.name=newapp.name+str(self.application_counter)
            self.applications.append(newapp)
            self.current_application=newapp
        else:
            print("Application \"%s\" is not available"%name)            
    
    def complete_application_new(self, text, line, begidx, endidx):
        """Complete command"""
        app_names=list(self.available_applications.keys())
        if not text:
            completions = app_names[:]
        else:
            completions = [ f
                            for f in app_names
                            if f.startswith(text)
                            ]
        return completions

    def do_application_switch(self, name):
        """Change to another open application"""
        done=False
        for app in self.applications:
            if (app.name==name):
                self.current_application=app    
                done=True
        if (not done):
            print("Application \"%s\" not found"%name)                        

    def complete_application_switch(self, text, line, begidx, endidx):
        completions = self.complete_delete_application(text, line, begidx, endidx)
        return completions

    def check_application_exist(self):
        """Check if there is any open application"""
        if (len(self.applications)==0):
            print("No open applications available")
            return False
        else:
            return True

# DATASET STUFF
    def do_dataset_delete(self, name):
        """Delete a dataset from the current application"""
        if (not self.check_application_exist()): return
        done=False
        for index, ds in enumerate(self.current_application.datasets):
            if (ds.name==name):
                if (self.current_application.current_dataset==ds):
                    if (index<len(self.current_application.datasets)-1):
                        self.current_application.current_dataset=self.current_application.datasets[index+1]
                    else:
                        self.current_application.current_dataset=self.current_application.datasets[0]
                self.current_application.datasets.remove(ds)
                done=True
        if (not done):
            print("Data Set \"%s\" not found"%name)            

    def complete_dataset_delete(self, text, line, begidx, endidx):
        """Complete delete dataset command"""
        if (not self.check_application_exist()): return [""]
        dataset_names=[]
        for ds in self.current_application.datasets:
            dataset_names.append(ds.name)
        if not text:
            completions = dataset_names[:]
        else:
            completions = [ f
                            for f in dataset_names
                            if f.startswith(text)
                            ]
        return completions

    def do_dataset_list(self, line):
        """List the datasets of the current application"""
        if (not self.check_application_exist()): return
        for ds in self.current_application.datasets:
            if (ds==self.current_application.current_dataset):
                print("*%s:\t%s"%(ds.name, ds.description))
                for i, f in enumerate(ds.files):
                    if (f==ds.current_file):
                        print("  *File%02d: %s"%(i+1,f.file_name_short))
                    else:
                        print("   File%02d: %s"%(i+1,f.file_name_short))
                for i, t in enumerate(ds.theories):
                    if (t==ds.current_theory):
                        print("  *%s: %s\t %s"%(t.name, t.thname, t.description))
                    else:
                        print("   %s: %s\t %s"%(t.name, t.thname, t.description))

            else:
                print("%s:\t%s"%(ds.name, ds.description))

    def do_dataset_new(self, line):
        """If there is an active application, create a new empty dataset in it.
        Arguments: [NAME [, Description]]
                NAME: of the new dataset (optional)
                DESCRIPTION: of the dataset (optional)"""
        if (not self.check_application_exist()): return
        if (line==""):
            num_ds=self.current_application.num_datasets+1
            self.current_application.new_dataset("DataSet%02d"%num_ds, "")
        else:
            items=line.split(',')
            if (len(items)>1):
                self.current_application.new_dataset(items[0],items[1])
            else:
                self.current_application.new_dataset(items[0],"")
            
    def do_dataset_switch(self, name):
        """ Switch the current dataset"""
        if (not self.check_application_exist()): return
        if (not self.check_datasets_exist()): return
        for ds in self.current_application.datasets:
            if (ds.name==name):
                self.current_application.current_dataset=ds    
                done=True
        if (not done):
            print("Dataset \"%s\" not found"%line)                        

    def complete_dataset_switch(self, text, line, begidx, endidx):
        """ Complete the switch dataset command"""
        if (not self.check_application_exist()): return [""]
        if (not self.check_datasets_exist()): return [""]
        ds_names=[]
        for ds in self.current_application.datasets:
            ds_names.append(ds.name)
        if not text:
            completions = ds_names[:]
        else:
            completions = [ f
                            for f in ds_names
                            if f.startswith(text)
                            ]
        return completions

    def check_datasets_exist(self):
        """Check if there is any open dataset"""
        if (len(self.current_application.datasets)==0):
            print("No open datasets available")
            return False
        else:
            return True

# FILE STUFF
    def do_file_delete(self, line):
        """Delete file from the current data set"""
        if (not self.check_application_exist()): return
        if (not self.check_datasets_exist()): return
        done=False
        for index, f in enumerate(self.current_application.current_dataset.files):
            if (f.file_name_short==line):
                if (self.current_application.current_dataset.current_file==f):
                    if (index<len(self.current_application.current_dataset.files)-1):
                        self.current_application.current_dataset.current_file=self.current_application.current_dataset.files[index+1]
                    else:
                        self.current_application.current_dataset.current_file=self.current_application.current_dataset.files[0]
                self.current_application.current_dataset.files.remove(f)
                done=True
        if (not done):
            print("File \"%s\" not found"%line)

    def complete_file_delete(self, text, line, begidx, endidx):
        if (not self.check_application_exist()): return [""]
        if (not self.check_datasets_exist()): return [""]
        f_names=[]
        for fl in self.current_application.current_dataset.files:
            f_names.append(fl.file_name_short)
        if not text:
            completions = f_names[:]
        else:
            completions = [ f
                            for f in f_names
                            if f.startswith(text)
                            ]
        return completions
    
    def do_file_list(self, line):
        """List the files in the current dataset"""
        if (not self.check_application_exist()): return
        if (not self.check_datasets_exist()): return
        ds=self.current_application.current_dataset
        for f in ds.files:
            if (f==ds.current_file):
                print("*%s"%f.file_name_short)
            else:
                print("%s"%f.file_name_short)

    def do_file_new(self, line):
        """Add an empty file of the given type to the current Data Set
        Arguments: TYPE [, NAME]
                TYPE: extension of file
                NAME: Name (optional)
        TODO: if no app and no data set are open, create the right ones!
        """
        if (not self.check_application_exist()): return
        if (not self.check_datasets_exist()): return
        if (line==""): 
            print("Missing file type")
            return
        ftypes=list(self.current_application.filetypes.values())
        items=line.split(',')
        if (items[0] in self.current_application.filetypes):  
            if (len(items)>1):
                self.current_application.current_dataset.new_file(self.current_application.filetypes[items[0]],items[1])
            else:
                self.current_application.current_dataset.new_file(self.current_application.filetypes[line])
        else:
            print("File type \"%s\" does not exists"%line)
    
    def complete_file_new(self, text, line, begidx, endidx):
        """Complete new file command"""
        if (not self.check_application_exist()): return [""]
        if (not self.check_datasets_exist()): return [""]
        file_types=list(self.current_application.filetypes.keys())
        if not text:
            completions = file_types[:]
        else:
            completions = [ f
                            for f in file_types
                            if f.startswith(text)
                            ]
        return completions

    def do_file_open(self, line):
        """Open a file from the current folder"""
        pass

    def do_file_switch(self, line):
        """Change active file in the current dataset"""
        if (not self.check_application_exist()): return
        if (not self.check_datasets_exist()): return
        for f in self.current_application.current_dataset.files:
            if (f.file_name_short==line):
                self.current_application.current_dataset.current_file=f    
                done=True
        if (not done):
            print("File \"%s\" not found"%line)                        

    def complete_file_switch(self, text, line, begidx, endidx):
        """Select names among the files in the current dataset"""
        completions=self.complete_file_delete(text, line, begidx, endidx)
        return completions

# FILE TYPE STUFF
    def do_filetype_available(self, line):
        """List available file types in the current application"""
        if (not self.check_application_exist()): return
        ftypes=list(self.current_application.filetypes.values())
        for ftype in ftypes:
            print("%s:\t%s\t*.%s"%(ftype.name,ftype.description,ftype.extension))

# THEORY STUFF
    def do_theory_available(self, line):
        """List available theories in the current application"""
        if (not self.check_application_exist()): return
        for t in list(self.current_application.theories.values()):
            print("%s:\t%s"%(t.thname,t.description))
 
    def do_theory_delete(self, name):
        """Delete a theory from the current dataset"""
        if (not self.check_application_exist()): return
        if (not self.check_datasets_exist()): return
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
        if (not self.check_application_exist()): return [""]
        if (not self.check_datasets_exist()): return [""]
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
        if (not self.check_application_exist()): return
        if (not self.check_datasets_exist()): return
        for t in self.current_application.current_dataset.theories:
            if (t==self.current_application.current_dataset.current_theory):
                print("  *%s: %s\t %s"%(t.name, t.thname, t.description))
            else:
                print("   %s: %s\t %s"%(t.name, t.thname, t.description))

    def do_theory_new(self, line):
        """Add a new theory of the type specified to the current Data Set"""
        if (not self.check_application_exist()): return
        if (not self.check_datasets_exist()): return
        thtypes=list(self.current_application.theories.keys())
        if (line in thtypes):
            num_th=self.current_application.current_dataset.num_theories+1
            self.current_application.current_dataset.new_theory(self.current_application.theories[line]("Theory%02d"%num_th))
        else:
            print("Theory \"%s\" does not exists"%line)
    
    def complete_theory_new(self, text, line, begidx, endidx):
        """Complete new theory command"""
        if (not self.check_application_exist()): return [""]
        if (not self.check_datasets_exist()): return [""]
        
        theory_names=list(self.current_application.theories.keys())
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

# VIEW STUFF
    def do_view_available(self, line):
        """List available views in the current application"""
        if (not self.check_application_exist()): return
        for view in self.current_application.views:
            if (view==self.current_application.current_view):
                print("*%s:\t%s"%(view.name,view.description))
            else:
                print("%s:\t%s"%(view.name,view.description))

    def do_view_switch(self, name):
        """Change to another view from open application"""
        done=False
        if (not self.check_application_exist()): return
        for view in self.current_application.views:
            if (view.name==name):
                self.current_application.current_view=view
                done=True
        if (not done):
            print("View \"%s\" not found"%name)                        

    def complete_view_switch(self, text, line, begidx, endidx):
        """Complete switch view command"""
        if (not self.check_application_exist()): return [""]
        view_names=[]
        for view in self.current_application.views:
            view_names.append(view.name)
        if not text:
            completions = view_names[:]
        else:
            completions = [ f
                            for f in view_names
                            if f.startswith(text)
                            ]
        return completions
    
# OTHER STUFF
    def do_shell(self, line):
        """Run a shell command"""
        print("running shell command:", line)
        output = os.popen(line).read()
        print(output)
        self.last_output = output

    def do_cd(self, line):
        """Change folder"""
        if os.path.isdir(line):
            os.chdir(line)
        else:
            print("Folder %s does not exist"%line)

    def complete_cd(self, text, line, begidx, endidx):
        """Complete cd command"""
        test_directory=''
        dirs=[]
        for child in os.listdir():
            test_path = os.path.join(test_directory, child)
            if os.path.isdir(test_path): 
                dirs.append(test_path)
        if not text:
            completions = dirs[:]
        else:
            completions = [ f
                            for f in dirs
                            if f.startswith(text)
                            ]
        return completions

    def do_ls(self, line):
        """List contents of current folder"""
        dirs=os.listdir()
        for d in dirs:
            print("%s"%d)

    def do_dir(self, line):
        """List contents of current folder"""
        self.do_ls(line)

    def do_info(self, line):
        """Show info about the current RepTate session"""
        print("##AVAILABLE APPLICATIONS:")
        self.do_application_available(line)

        print("\n##OPEN APPLICATIONS (*=current):")
        self.do_application_list(line)

        print("\n##CURRENT APPLICATION:")
        print("-->FILE TYPES AVAILABLE:")
        self.do_filetype_available(line)

        print("-->VIEWS AVAILABLE (*=current):")
        self.do_view_available(line)

        print("-->THEORIES AVAILABLE:")
        self.do_theory_available(line)

        print("\n##DATA SETS IN CURRENT APPLICATION:")
        self.do_dataset_list(line)
        
    def do_quit(self, line):
        self.do_EOF(line)

    def do_EOF(self, line):
        """Exit RepTate"""
        self.reptatelogger.debug("Exiting RepTate...")
        readline.write_history_file()
        return True
