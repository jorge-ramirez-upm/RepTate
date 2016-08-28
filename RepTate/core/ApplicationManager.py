import os
import cmd
import sys
import logging
import logging.handlers
import readline
from ApplicationTest import *

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
        self.available_applications=[]
        self.available_applications.append(ApplicationTest)
        self.current_application=None

    def do_list_available_applications(self, line):
        """List available applications"""
        for app in self.available_applications:
            print("%s: %s"%(app.name,app.description))

    def do_list_applications(self, line):
        """List open applications"""
        for app in self.applications:
            if (app==self.current_application):
                print("*%s: %s"%(app.name,app.description))
            else:
                print("%s: %s"%(app.name,app.description))

    def do_switch_application(self, name):
        """Change to another open application"""
        done=False
        for app in self.applications:
            if (app.name==name):
                self.current_application=app    
                done=True
        if (not done):
            print("Application \"%s\" not found"%name)                        

    def complete_switch_application(self, text, line, begidx, endidx):
        completions = self.complete_delete_application(text, line, begidx, endidx)
        return completions

    def do_delete_application(self, name):
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

    def complete_delete_application(self, text, line, begidx, endidx):
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

    def do_quit(self, line):
        """Exit RepTate"""        
        self.do_EOF(line)

    def do_EOF(self, line):
        """Exit RepTate"""
        self.reptatelogger.debug("Exiting RepTate...")
        readline.write_history_file()
        return True

    def do_new_application(self, name):
        """ Create new application"""
        if (name==ApplicationTest.name):
            self.application_counter+=1
            newapp=ApplicationTest()
            newapp.name=newapp.name+str(self.application_counter)
            self.applications.append(newapp)
            self.current_application=newapp
        else:
            print("Application \"%s\" is not available"%name)            
    
    def complete_new_application(self, text, line, begidx, endidx):
        """Complete command"""
        app_names=[]
        for app in self.available_applications:
            app_names.append(app.name)
        if not text:
            completions = app_names[:]
        else:
            completions = [ f
                            for f in app_names
                            if f.startswith(text)
                            ]
        return completions

    def check_applications_exist(self):
        """Check if there is any open application"""
        if (len(self.applications)==0):
            print("No open applications available")
            return False
        else:
            return True

    def check_datasets_exist(self):
        """Check if there is any open dataset"""
        if (len(self.current_application.datasets)==0):
            print("No open datasets available")
            return False
        else:
            return True


    def do_list_available_views(self, line):
        """List available views in the current application"""
        if (not self.check_applications_exist()):
            return
        for view in self.current_application.views:
            if (view==self.current_application.current_view):
                print("*%s:\t%s"%(view.name,view.description))
            else:
                print("%s:\t%s"%(view.name,view.description))

    def do_switch_view(self, name):
        """Change to another view from open application"""
        done=False
        if (not self.check_applications_exist()):
            return
        for view in self.current_application.views:
            if (view.name==name):
                self.current_application.current_view=view
                done=True
        if (not done):
            print("View \"%s\" not found"%name)                        

    def complete_switch_view(self, text, line, begidx, endidx):
        """Complete switch view command"""
        if (not self.check_applications_exist()):
            return [""]
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

    def do_list_available_filetypes(self, line):
        """List available file types in the current application"""
        if (not self.check_applications_exist()):
            return
        ftypes=list(self.current_application.filetypes.values())
        for ftype in ftypes:
            print("%s:\t%s\t*.%s"%(ftype.name,ftype.description,ftype.extension))

    def do_add_empty_dataset(self, line):
        """If there is an active application, create a new empty dataset in it.
           The argument may contain the name, description (separated by a comma)"""
        if (not self.check_applications_exist()):
            return
        if (line==""):
            num_ds=self.current_application.num_datasets+1
            self.current_application.add_empty_dataset("DataSet%d"%num_ds, "")
        else:
            items=line.split(',')
            if (len(items)>1):
                self.current_application.add_empty_dataset(items[0],items[1])
            else:
                self.current_application.add_empty_dataset(items[0],"")

    def do_list_datasets(self, line):
        """List the datasets of the current application"""
        if (not self.check_applications_exist()):
            return
        for ds in self.current_application.datasets:
            if (ds==self.current_application.current_dataset):
                print("*%s:\t%s"%(ds.name, ds.description))
            else:
                print("%s:\t%s"%(ds.name, ds.description))
            for f in ds.files:
                if (f==ds.current_file):
                    print("\t*%s"%f.file_name_short)
                else:
                    print("\t%s"%f.file_name_short)

    def do_delete_dataset(self, name):
        """Delete a dataset from the current application"""
        if (not self.check_applications_exist()):
            return
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

    def complete_delete_dataset(self, text, line, begidx, endidx):
        """Complete delete dataset command"""
        if (not self.check_applications_exist()):
            return [""]
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

    def do_add_empty_file(self, line):
        """Add an empty file of the given type to the current Data Set"""
        if (not self.check_applications_exist()):
            return
        if (not self.check_datasets_exist()):
            return
        ftypes=list(self.current_application.filetypes.values())
        if (line==""):
            self.current_application.current_dataset.add_empty_file(ftypes[0])
        else:
            if (line in self.current_application.filetypes):  
                self.current_application.current_dataset.add_empty_file(self.current_application.filetypes[line])
            else:
                print("File type \"%s\" does not exists"%line)
    
    def do_list_files(self, line):
        """List the files in the current dataset"""
        if (not self.check_applications_exist()):
            return
        if (not self.check_datasets_exist()):
            return
        ds=self.current_application.current_dataset
        for f in ds.files:
            if (f==ds.current_file):
                print("*%s"%f.file_name_short)
            else:
                print("%s"%f.file_name_short)

    def do_open_file(self, line):
        """Open a file from the current folder"""
        pass

    def do_switch_file(self, line):
        """Change active file in the current dataset"""
        pass

    def complete_switch_file(self, line):
        """Select names among the files in the current dataset"""
        pass

    def delete_file(self, line):
        """Delete file from the current data set"""
        pass

    def complete_delete_file(self, line):
        self.complete_switch_file(line)
    


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
        print("AVAILABLE APPLICATIONS:")
        print("#######################")
        self.do_list_available_applications(line)

        print("\nOPEN APPLICATIONS (*=current):")
        print("##############################")
        self.do_list_applications(line)

        print("\nVIEWS IN CURRENT APPLICATION:")
        print("#############################")
        self.do_list_available_views(line)

        print("\nFILE TYPES IN CURRENT APPLICATION:")
        print("##################################")
        self.do_list_available_filetypes(line)

        print("\nDATA SETS IN CURRENT APPLICATION:")
        print("##################################")
        self.do_list_datasets(line)

        print("\nFILES IN CURRENT DATA SET:")
        print("##########################")
        self.do_list_files(line)
        