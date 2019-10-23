# RepTate: Rheology of Entangled Polymers: Toolkit for the Analysis of Theory and Experiments
# --------------------------------------------------------------------------------------------------------
#
# Authors:
#     Jorge Ramirez, jorge.ramirez@upm.es
#     Victor Boudara, victor.boudara@gmail.com
#
# Useful links:
#     http://blogs.upm.es/compsoftmatter/software/reptate/
#     https://github.com/jorge-ramirez-upm/RepTate
#     http://reptate.readthedocs.io
#
# --------------------------------------------------------------------------------------------------------
#
# Copyright (2017): Jorge Ramirez, Victor Boudara, Universidad Politécnica de Madrid, University of Leeds
#
# This file is part of RepTate.
#
# RepTate is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# RepTate is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with RepTate.  If not, see <http://www.gnu.org/licenses/>.
#
# --------------------------------------------------------------------------------------------------------
"""Module ApplicationManager

Module for the Main interface that contains all applications. Command line version.

"""
import sys
#import logging
#import logging.handlers
import matplotlib.pyplot as plt
import readline

from CmdBase import CmdBase, CmdMode
from ApplicationTTS import ApplicationTTS
from ApplicationTTSFactors import ApplicationTTSFactors
from ApplicationLVE import ApplicationLVE
from ApplicationNLVE import ApplicationNLVE
from ApplicationCrystal import ApplicationCrystal
from ApplicationMWD import ApplicationMWD
from ApplicationGt import ApplicationGt
from ApplicationCreep import ApplicationCreep
from ApplicationSANS import ApplicationSANS
from ApplicationReact import ApplicationReact
from ApplicationDielectric import ApplicationDielectric
from ApplicationLAOS import ApplicationLAOS
# from ApplicationXY import ApplicationXY
#from ApplicationFRS_I import *
import Version
from collections import OrderedDict


class ApplicationManager(CmdBase):
    """Main Reptate container of applications

    """

    version = Version.VERSION
    date = Version.DATE
    prompt = 'RepTate> '
    intro = 'RepTate Version %s - %s command processor\nhelp [command] for instructions\nTAB for completions' % (
        version, date)

    def __init__(self, parent=None):
        """
        **Constructor**
        
        [description]
        
        Keyword Arguments:
            - parent {[type]} -- [description] (default: {None})
        """
        super().__init__()

        # SETUP LOG
        #self.reptatelogger = logging.getLogger('ReptateLogger')
        #self.reptatelogger.setLevel(logging.DEBUG)  # INFO, WARNING
        #logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
        #log_file_name = 'reptate.log'
        #handler = logging.handlers.RotatingFileHandler(
        #    log_file_name, maxBytes=20000, backupCount=2, mode='w')
        #MainWindow.reptatelogger.addHandler(handler)

        # SETUP READLINE, COMMAND HISTORY FILE, ETC
        try:
            readline.read_history_file()
        except Exception as e:
            print(e.__class__, ":", e)
            print("History file not found. Creating a new one")

        # SETUP APPLICATIONS
        self.application_counter = 0
        self.applications = OrderedDict()
        self.available_applications = OrderedDict()
        self.available_applications[ApplicationMWD.appname] = ApplicationMWD
        self.available_applications[ApplicationTTS.appname] = ApplicationTTS
        self.available_applications[ApplicationTTSFactors.appname] = ApplicationTTSFactors
        self.available_applications[ApplicationLVE.appname] = ApplicationLVE
        self.available_applications[ApplicationNLVE.appname] = ApplicationNLVE
        self.available_applications[ApplicationCrystal.appname] = ApplicationCrystal
        self.available_applications[ApplicationGt.appname] = ApplicationGt
        self.available_applications[ApplicationCreep.appname] = ApplicationCreep
        self.available_applications[ApplicationSANS.appname] = ApplicationSANS
        self.available_applications[ApplicationReact.appname] = ApplicationReact
        self.available_applications[ApplicationDielectric.appname] = ApplicationDielectric
        self.available_applications[ApplicationLAOS.appname] = ApplicationLAOS


# APPLICATION STUFF

    def available(self):
        """Return list of available applications
        
        [description]
        
        Returns:
            - [type] -- [description]
        """
        L = [
            "%s: %s" % (app.appname, app.description)
            for app in list(self.available_applications.values())
        ]
        return L

    def do_available(self, line):
        """List available applications
        
        [description]
        
        Arguments:
            - line {[type]} -- [description]
        """
        L = self.available()
        for app in L:
            print(app)

    def delete(self, name):
        """Delete an open application
        
        [description]
        
        Arguments:
            - name {[type]} -- [description]
        """
        if name in self.applications.keys():
            del self.applications[name]
        else:
            print("Application \"%s\" not found" % name)

    def do_delete(self, name):
        """Delete an open application
        
        [description]
        
        Arguments:
            - name {[type]} -- [description]
        """
        self.delete(name)

    def complete_delete(self, text, line, begidx, endidx):
        """Complete delete application command
        
        [description]
        
        Arguments:
            - text {[type]} -- [description]
            - line {[type]} -- [description]
            - begidx {[type]} -- [description]
            - endidx {[type]} -- [description]
        
        Returns:
            - [type] -- [description]
        """
        app_names = list(self.applications.keys())
        if not text:
            completions = app_names[:]
        else:
            completions = [f for f in app_names if f.startswith(text)]
        return completions

    def list(self):
        """List open applications
        
        [description]
        
        Returns:
            - [type] -- [description]
        """
        L = [
            "%s: %s" % (app.name, app.description)
            for app in self.applications.values()
        ]
        return L

    def do_list(self, line):
        """List open applications
        
        [description]
        
        Arguments:
            - line {[type]} -- [description]
        """
        L = self.list()
        for app in L:
            print(app)

    def new(self, appname):
        """Create new application
        
        [description]
        
        Arguments:
            - name {[type]} -- [description]
        
        Returns:
            - [type] -- [description]
        """
        if (appname in self.available_applications):
            self.application_counter += 1
            newapp = self.available_applications[appname](
                appname + str(self.application_counter), self)
            self.applications[newapp.name] = newapp
            #if CmdBase.mode != CmdMode.GUI:
            #    newapp.do_new("")
            return newapp
        else:
            print("Application \"%s\" is not available" % appname)
            return None

    def do_new(self, appname):
        """Create new application
        
        [description]
        
        Arguments:
            - appname {[type]} -- [description]
        """
        newapp = self.new(appname)
        if (newapp != None):
            if (self.mode == CmdMode.batch):
                newapp.prompt = ''
            else:
                newapp.prompt = self.prompt[:-2] + '/' + newapp.name + '> '
            if CmdBase.mode != CmdMode.GUI:
                newapp.do_new("")
            newapp.cmdloop()

    def complete_new(self, text, line, begidx, endidx):
        """Complete new application command
        
        [description]
        
        Arguments:
            - text {[type]} -- [description]
            - line {[type]} -- [description]
            - begidx {[type]} -- [description]
            - endidx {[type]} -- [description]
        
        Returns:
            - [type] -- [description]
        """
        app_names = list(self.available_applications.keys())
        if not text:
            completions = app_names[:]
        else:
            completions = [f for f in app_names if f.startswith(text)]
        return completions

    def do_switch(self, name):
        """Set focus to an open application
        
        [description]
        
        Arguments:
            - name {[type]} -- [description]
        """
        if name in self.applications.keys():
            app = self.applications[name]
            app.cmdloop()
        else:
            print("Application \"%s\" not found" % name)

    def complete_switch(self, text, line, begidx, endidx):
        """[summary]
        
        [description]
        
        Arguments:
            - text {[type]} -- [description]
            - line {[type]} -- [description]
            - begidx {[type]} -- [description]
            - endidx {[type]} -- [description]
        
        Returns:
            - [type] -- [description]
        """
        completions = self.complete_delete(text, line, begidx, endidx)
        return completions

# MAXWELL MODES COPY

    def do_copymodes(self, line):
        """Copy maxwell modes from one theory to another.
        
        Both theories may live inside different applications and/or datasets
        copymodes App1.Dataseta.Theoryi App2.Datasetb.Theoryj
        
        Arguments:
            - line {[type]} -- [description]
        """
        apps = line.split()
        if len(apps) < 2:
            print(
                'Not enough parameters passed\n'
                "Use 'copymodes App1.Dataset1.Theory1 App2.Dataset2.Theory2'\n"
                "See 'list_theories_Maxwell' for a list of availiable theories"
            )
            return

        source = str(apps[0])
        target = str(apps[1])
        if (not len(source.split('.')) == 3):
            print(
                "Source format should be: 'App1.Dataset1.Theory1'\n"
                "See 'list_theories_Maxwell' for a list of availiable theories"
            )
            return
        if (not len(target.split('.')) == 3):
            print(
                "Target format should be: 'App2.Dataset2.Theory2'\n"
                "See 'list_theories_Maxwell' for a list of availiable theories"
            )
            return

        get_dict, set_dict = self.list_theories_Maxwell()
        dict_keys = list(
            get_dict.keys())  #get_dict and set_dict have the same keys
        if ((source in dict_keys) and (target in dict_keys)):
            tau, G = get_dict[source]()
            set_dict[target](tau, G)
            print('Copied modes from %s to %s' % (source, target))
            return
        else:
            print("Source or Target not found\n"
                  "or theory does not have modes.\n"
                  "No copy has been made")
            return

    def list_theories_Maxwell(self, th_exclude=None):
        """List the theories in the current RepTate instance that provide and need
        Maxwell modes
        
        [description]
        
        Returns:
            - [type] -- [description]
        """
        get_dict = {}
        set_dict = {}
        for app in self.applications.values():
            for ds in app.datasets.values():
                for th in ds.theories.values():
                    if th.has_modes and th != th_exclude:
                        get_dict["%s.%s.%s" % (app.name, ds.name,
                                               th.name)] = th.get_modes
                        set_dict["%s.%s.%s" % (app.name, ds.name,
                                               th.name)] = th.set_modes
        return get_dict, set_dict

    def do_list_theories_Maxwell(self, line):
        """List the theories in the current RepTate instance that provide
        Maxwell modes
        
        [description]
        
        Arguments:
            - line {[type]} -- [description]
        """
        L, S = self.list_theories_Maxwell()
        print(list(L.keys()))


# OTHER STUFF

    def help_tutorial(self):
        """[summary]
        
        [description]
        """
        print('introduction')
        print('a good place for a tutorial')

    def do_about(self, line):
        """Show about info
        
        [description]
        
        Arguments:
            - line {[type]} -- [description]
        """
        pass

    def do_info(self, line):
        """Show info about the current RepTate session
        
        [description]
        
        Arguments:
            - line {[type]} -- [description]
        """
        print("##AVAILABLE APPLICATIONS:")
        self.do_available(line)

        print("\n##OPEN APPLICATIONS")
        self.do_list(line)

    def do_quit(self, args):
        """Exit from the application
        
        [description]
        
        Arguments:
            args {[type]} -- [description]
        """
        msg = 'Do you really want to exit RepTate?'
        shall = input("\n%s (y/N) " % msg).lower() == 'y'
        if (shall):
            print("Exiting RepTate...")
            readline.write_history_file()
            sys.exit()

    do_EOF = do_quit
    do_up = do_quit
