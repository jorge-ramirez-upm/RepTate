import os
import cmd
import sys
import logging
import logging.handlers
from ApplicationTest import *

class ApplicationManager(cmd.Cmd):
    """Main Reptate container of applications"""

    version = '0.1'
    prompt = 'reptate> '
    intro = 'Reptate Version %s command processor'%version
    
    def __init__ (self, parent=None):
        """Constructor """
        cmd.Cmd.__init__(self)
        self.setup_applications()
        self.setup_log()
        
    def setup_log(self):
        self.reptatelogger = logging.getLogger('ReptateLogger')
        self.reptatelogger.setLevel(logging.DEBUG) # INFO, WARNING
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
        #log_file_name = 'reptate.log'
        #handler = logging.handlers.RotatingFileHandler(
        #    log_file_name, maxBytes=20000, backupCount=2, mode='w')
        #MainWindow.reptatelogger.addHandler(handler)

    def setup_applications(self):
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
            print("%s: %s"%(app.name,app.description))

    def do_switch_application(self, line):
        """Change to another open application"""
        for app in self.applications:
            if (app.name==line):
                self.current_application=app    

    def complete_switch_application(self, text, line, begidx, endidx):
        completions = complete_delete_application(text, line, begidx, endidx)
        return completions

    def do_delete_application(self, line):
        """Delete an open application"""
        for app in self.applications:
            if (app.name==line):
                self.applications.remove(app)

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

    def do_EOF(self, line):
        """Exit RepTate"""
        self.reptatelogger.debug("Exiting RepTate...")
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
            print("Application %s is not available"%name)            
    
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

    def do_shell(self, line):
        "Run a shell command"
        print("running shell command:", line)
        output = os.popen(line).read()
        print(output)
        self.last_output = output
