import cmd
from ApplicationTest import *

class ApplicationManager(cmd.Cmd):
    """Main Reptate container of applications"""

    prompt = 'reptate> '
    intro = 'RepTate command processor'
    
    def __init__ (self, parent=None):
        cmd.Cmd.__init__(self)
        self.application_counter=0
        self.applications=[]
        self.available_applications=[]
        self.available_applications.append(ApplicationTest)

    def do_list_available_applications(self, line):
        """List available applications"""
        for app in self.available_applications:
            print("%s: %s"%(app.name,app.description))

    def do_list_applications(self, line):
        """List open applications"""
        for app in self.applications:
            print("%s: %s"%(app.name,app.description))

    def do_delete_application(self, line):
        """Delete an open application"""
        for app in self.applications:
            if (app.name==line):
                self.applications.remove(app)

    def do_EOF(self, line):
        """Exit RepTate"""
        return True

    def do_new_application(self, name):
        """ Create new application"""
        if (name==ApplicationTest.name):
            self.application_counter+=1
            newapp=ApplicationTest()
            newapp.name=newapp.name+str(self.application_counter)
            self.applications.append(newapp)
        else:
            print("Application %s is not available"%name)            


