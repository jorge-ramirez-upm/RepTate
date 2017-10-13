import sys
import logging
import logging.handlers
import matplotlib.pyplot as plt

from CmdBase import *
from ApplicationMWD import *
from ApplicationLVE import *
from ApplicationNLVE import *
from ApplicationGt import *
#from ApplicationFRS_I import *

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
        try:
            readline.read_history_file()
        except Exception as e:
            print (e.__class__, ":", e)
            print ("History file not found. Creating a new one")
            

        # SETUP APPLICATIONS
        self.application_counter=0
        self.applications={}
        self.available_applications={}
        self.available_applications[ApplicationMWD.name]=ApplicationMWD
        self.available_applications[ApplicationLVE.name]=ApplicationLVE
        self.available_applications[ApplicationNLVE.name]=ApplicationNLVE
        self.available_applications[ApplicationGt.name]=ApplicationGt
        #self.available_applications[ApplicationFRS_I.name]=ApplicationFRS_I

# APPLICATION STUFF
    def available(self):
        """Return list of available applications"""
        L= ["%s: %s"%(app.name,app.description) for app in list(self.available_applications.values())]
        return L
        
    def do_available(self, line):
        """List available applications"""
        L=self.available()
        for app in L: 
            print(app)

    def delete(self, name):
        """Delete an open application"""
        if name in self.applications.keys():
            del self.applications[name]
        else:
            print("Application \"%s\" not found"%name)                   
            
    def do_delete(self, name):
        """Delete an open application"""
        self.delete(name)
        
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

    def list(self):
        """List open applications"""
        L= ["%s: %s"%(app.name,app.description) for app in self.applications.values()]
        return L        
        
    def do_list(self, line):
        """List open applications"""
        L=self.list()
        for app in L: 
            print(app)

    def new(self, name):
        """Create new application"""
        if (name in self.available_applications):
            self.application_counter+=1
            newapp=self.available_applications[name](name+str(self.application_counter), self)
            self.applications[newapp.name]=newapp
            return newapp
        else:
            print("Application \"%s\" is not available"%name)
            return None   
               
    def do_new(self, name):
        """Create new application"""
        newapp=self.new(name)
        if (newapp!=None):
            if (self.mode==CmdMode.batch):
                newapp.prompt = ''
            else:
                newapp.prompt = self.prompt[:-2]+'/'+newapp.name+'> '
            newapp.cmdloop()
                    
    
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
        apps = line.split()
        if len(apps)<2:
            print('Not enough parameters passed\n'
            "Use 'copymodes App1.Dataset1.Theory1 App2.Dataset2.Theory2'\n"
            "See 'list_theories_Maxwell' for a list of availiable theories")
            return                        
        
        source = str(apps[0])
        target = str(apps[1])
        if (not len(source.split('.'))==3):
            print("Source format should be: 'App1.Dataset1.Theory1'\n"
                "See 'list_theories_Maxwell' for a list of availiable theories")
            return
        if (not len(target.split('.'))==3):
            print("Target format should be: 'App2.Dataset2.Theory2'\n"
                "See 'list_theories_Maxwell' for a list of availiable theories")
            return

        get_dict, set_dict = self.list_theories_Maxwell()
        dict_keys = list(get_dict.keys()) #get_dict and set_dict have the same keys
        if ((source in dict_keys) and (target in dict_keys)):
            tau, G = get_dict[source]()
            set_dict[target](tau, G)
            print('Copied modes from %s to %s'%(source, target))
            return
        else:
            print("Source or Target not found\n"
                "or theory does not have modes.\n"
                "No copy has been made")
            return


    def list_theories_Maxwell(self):
        """List the theories in the current RepTate instance that provide
        Maxwell modes"""
        get_dict={}
        set_dict={}
        for appname in self.applications.keys():
            app=self.applications[appname]
            for dsname in app.datasets.keys():
                ds=app.datasets[dsname]
                #print ("%s %s"%(app.name, ds.name))
                for thname in ds.theories.keys():
                    th=ds.theories[thname]
                    if th.has_modes:
                        get_dict["%s.%s.%s"%(app.name, ds.name, th.name)] = th.get_modes
                        set_dict["%s.%s.%s"%(app.name, ds.name, th.name)] = th.set_modes
        return get_dict, set_dict
                        
    def do_list_theories_Maxwell(self, line):
        """List the theories in the current RepTate instance that provide
        Maxwell modes"""
        L, S =self.list_theories_Maxwell()
        print(list(L.keys()))
                        

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
