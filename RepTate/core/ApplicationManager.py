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
        done=False
        """Delete an open application"""
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

    def do_list_available_views(self, line):
        """List available views in the current application"""
        if (len(self.applications)==0):
            print("No open applications available")
            return
        for view in self.current_application.views:
            if (view==self.current_application.current_view):
                print("*%s:\t%s"%(view.name,view.description))
            else:
                print("%s:\t%s"%(view.name,view.description))

    def do_switch_view(self, name):
        """Change to another view from open application"""
        done=False
        if (len(self.applications)==0):
            print("No open applications available")
            return
        for view in self.current_application.views:
            if (view.name==name):
                self.current_application.current_view=view
                done=True
        if (not done):
            print("View \"%s\" not found"%name)                        

    def complete_switch_view(self, text, line, begidx, endidx):
        """Complete switch view command"""
        if (len(self.applications)==0):
            return ["No open applications available"]
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
        if (len(self.applications)==0):
            print("No open applications available")
            return
        ftypes=list(self.current_application.filetypes.values())
        for ftype in ftypes:
            print("%s:\t%s\t*.%s"%(ftype.name,ftype.description,ftype.extension))

    def do_shell(self, line):
        "Run a shell command"
        print("running shell command:", line)
        output = os.popen(line).read()
        print(output)
        self.last_output = output

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
        