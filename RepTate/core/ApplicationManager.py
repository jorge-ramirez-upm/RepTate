import sys
import logging
import logging.handlers
import matplotlib.pyplot as plt

from CmdBase import *
from ApplicationTest import *
from ApplicationReact import *
from ApplicationMWD import *
from ApplicationTTS import *
from ApplicationLVE import *
from ApplicationNLVE import *
from ApplicationGt import *

class ApplicationManager(CmdBase):
    """Main Reptate container of applications"""

    version = '0.4'
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
        self.applications=[]
        self.available_applications={}
        self.available_applications[ApplicationTest.name]=ApplicationTest
        self.available_applications[ApplicationReact.name]=ApplicationReact
        self.available_applications[ApplicationMWD.name]=ApplicationMWD
        self.available_applications[ApplicationTTS.name]=ApplicationTTS
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
        done=False
        for index, app in enumerate(self.applications):
            if (app.name==name):
                self.applications.remove(app)
                done=True
        if (not done):
            print("Application \"%s\" not found"%name)            

    def complete_delete(self, text, line, begidx, endidx):
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

    def do_list(self, line):
        """List open applications"""
        for app in self.applications:
            print("%s: %s"%(app.name,app.description))

    def do_new(self, name):
        """ Create new application"""
        if (name in self.available_applications):
            self.application_counter+=1
            newapp=self.available_applications[name](name+str(self.application_counter), self)
            self.applications.append(newapp)
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
        done=False
        for app in self.applications:
            if (app.name==name):
                app.cmdloop()
                done=True
        if (not done):
            print("Application \"%s\" not found"%name)                        

    def complete_switch(self, text, line, begidx, endidx):
        completions = self.complete_delete(text, line, begidx, endidx)
        return completions        
    
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
