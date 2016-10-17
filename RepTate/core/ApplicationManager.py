import sys
import logging
import logging.handlers
import matplotlib.pyplot as plt

from CmdBase import *
from ApplicationMWD import *
from ApplicationLVE import *
from ApplicationNLVE import *
from ApplicationGt import *

class ApplicationManager(CmdBase):
    """Main Reptate container of applications"""

    version = '0.5'
    prompt = 'reptate> '
    intro = 'Reptate Version %s command processor\nhelp [command] for instructions\nTAB for completions'%version
    
    def __init__ (self, parent=None):
        """Constructor """
        super(ApplicationManager, self).__init__() 

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
        self.applications={}
        self.available_applications={}
        self.available_applications[ApplicationMWD.name]=ApplicationMWD
        self.available_applications[ApplicationLVE.name]=ApplicationLVE
        self.available_applications[ApplicationNLVE.name]=ApplicationNLVE
        self.available_applications[ApplicationGt.name]=ApplicationGt

# APPLICATION STUFF
    def do_available(self, line):
        """List available applications"""
        for app in list(self.available_applications.values()):
            print("%s: %s"%(app.name,app.description))

    def do_delete(self, name):
        """Delete an open application"""
        if name in self.applications.keys():
            del self.applications[name]
        else:
            print("Application \"%s\" not found"%name)            

    def complete_delete(self, text, line, begidx, endidx):
        """Complete delete application command"""
        app_names=list(self.applications.keys())
        if not text:
            completions = app_names[:]
        else:
            completions = [ f
                            for f in app_names
                            if f.startswith(text)
                            ]
        return completions

    def do_list(self, line):
        """List open applications"""
        for app in self.applications.values():
            print("%s: %s"%(app.name,app.description))

    def do_new(self, name):
        """ Create new application"""
        if (name in self.available_applications):
            self.application_counter+=1
            newapp=self.available_applications[name](name+str(self.application_counter), self)
            self.applications[newapp.name]=newapp
            if (self.mode==CmdMode.batch):
                newapp.prompt = ''
            else:
                newapp.prompt = self.prompt[:-2]+'/'+newapp.name+'> '
            newapp.cmdloop()

        else:
            print("Application \"%s\" is not available"%name)            
    
    def complete_new(self, text, line, begidx, endidx):
        """Complete new application command"""
        app_names=list(self.available_applications.keys())
        if not text:
            completions = app_names[:]
        else:
            completions = [ f
                            for f in app_names
                            if f.startswith(text)
                            ]
        return completions

    def do_switch(self, name):
        """Set focus to an open application"""
        if name in self.applications.keys():
            app=self.applications[name]               
            app.cmdloop()
        else:
            print("Application \"%s\" not found"%name)                        

    def complete_switch(self, text, line, begidx, endidx):
        completions = self.complete_delete(text, line, begidx, endidx)
        return completions        
    
# MAXWELL MODES COPY
    def do_copymodes(self, line):
        """Copy maxwell modes from one theory to another.
           Both theories may live inside different applications and/or datasets
           copymodes App1.Dataseta.Theoryi App2.Datasetb.Theoryj"""
        apps=line.split()
        if len(apps)<2:
            print("Not enough parameters passed")
            return                        
        appA=apps[0].split('.')
        app1=appA[0]
        if app1 in self.applications.keys():
            app1=self.applications[app1]
        else:
            print("Application %s not found"%app1)
            return
        dataset1=appA[1]
        if dataset1 in app1.datasets.keys():
            dataset1=app1.datasets[dataset1]
        else:
            print("Dataset %s not found"%dataset1)
            return
        theory1=appA[2]
        if theory1 in dataset1.theories.keys():
            theory1 = dataset1.theories[theory1]
        else:
            print("Theory %s not found"%theory1)
            return
        if not theory1.has_modes:
            print("Theory %s does not have modes"%theory1.name)
            return
        appB=apps[1].split('.')
        app2=appB[0]
        if app2 in self.applications.keys():
            app2=self.applications[app2]
        else:
            print("Application %s not found"%app2)
            return
        dataset2=appB[1]
        if dataset2 in app2.datasets.keys():
            dataset2=app2.datasets[dataset2]
        else:
            print("Dataset %s not found"%dataset2)
            return
        theory2=appB[2]
        if theory2 in dataset2.theories.keys():
            theory2 = dataset2.theories[theory2]
        else:
            print("Theory %s not found"%theory2)
            return
        if not theory2.has_modes:
            print("Theory %s does not have modes"%theory2.name)
            return
        tau, G = theory1.get_modes()
        theory2.set_modes(tau, G)

# OTHER STUFF
    def help_tutorial(self):
        print ('introduction')
        print ('a good place for a tutorial')

    def do_about(self, line):
        """Show about info"""
        pass

    def do_info(self, line):
        """Show info about the current RepTate session"""
        print("##AVAILABLE APPLICATIONS:")
        self.do_available(line)

        print("\n##OPEN APPLICATIONS")
        self.do_list(line)

        #print("\n##CURRENT APPLICATION:")
        #print("-->FILE TYPES AVAILABLE:")
        #self.do_filetype_available(line)

        #print("-->VIEWS AVAILABLE (*=current):")
        #self.do_view_available(line)

        #print("-->THEORIES AVAILABLE:")
        #self.do_theory_available(line)

        #print("\n##DATA SETS IN CURRENT APPLICATION:")
        #self.do_dataset_list(line)

    def do_quit(self, args):
        """Exit from the application"""
        msg = 'Do you really want to exit RepTate?'
        shall = input("\n%s (y/N) " % msg).lower() == 'y'         
        if (shall):
            print ("Exiting RepTate...")
            readline.write_history_file()
            sys.exit()
    do_EOF = do_quit
    do_up = do_quit
