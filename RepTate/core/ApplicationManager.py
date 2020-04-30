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
# Copyright (2017-2020): Jorge Ramirez, Victor Boudara, Universidad Politécnica de Madrid, University of Leeds
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
import matplotlib.pyplot as plt
import readline
from urllib.request import urlopen
import json
import logging
import logging.handlers
from pathlib import Path
import os

from RepTate.core.CmdBase import CmdBase, CmdMode
from RepTate.applications.ApplicationTTS import ApplicationTTS
from RepTate.applications.ApplicationTTSFactors import ApplicationTTSFactors
from RepTate.applications.ApplicationLVE import ApplicationLVE
from RepTate.applications.ApplicationNLVE import ApplicationNLVE
from RepTate.applications.ApplicationCrystal import ApplicationCrystal
from RepTate.applications.ApplicationMWD import ApplicationMWD
from RepTate.applications.ApplicationGt import ApplicationGt
from RepTate.applications.ApplicationCreep import ApplicationCreep
from RepTate.applications.ApplicationSANS import ApplicationSANS
from RepTate.applications.ApplicationReact import ApplicationReact
from RepTate.applications.ApplicationDielectric import ApplicationDielectric
from RepTate.applications.ApplicationLAOS import ApplicationLAOS
# from ApplicationXY import ApplicationXY
#from ApplicationFRS_I import *
import RepTate.core.Version as Version
from collections import OrderedDict
from colorama import Fore
class ApplicationManager(CmdBase):
    """Main Reptate container of applications

    """

    version = Version.VERSION
    date = Version.DATE
    prompt = Fore.GREEN + 'RepTate> '
    intro = 'RepTate Version %s - %s command processor\nhelp [command] for instructions\nTAB for completions' % (
        version, date)

    def __init__(self, parent=None, loglevel=logging.INFO):
        """
        **Constructor**"""
        super().__init__()

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

        # LOGGING STUFF
        self.logger = logging.getLogger('RepTate')
        self.logger.setLevel(loglevel)
        home_path = str(Path.home())
        logfile = os.path.join(home_path, 'RepTate.log')
        fh = logging.handlers.RotatingFileHandler(logfile, maxBytes=20000, backupCount=2)
        fh.setLevel(loglevel)
        ch = logging.StreamHandler()
        ch.setLevel(logging.WARNING)
        # create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s: %(message)s',
                                      "%Y%m%d %H%M%S")
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        # add the handlers to the logger
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)
        self.logger.debug('New ApplicationManager')
        if (self.mode == CmdMode.batch):
            self.prompt += Fore.RESET

# APPLICATION STUFF

    def available(self):
        """Return list of available applications

        [description]

        Returns:
            - [type] -- [description]
        """
        L = []
        for app in list(self.available_applications.values()):
            L.append(Fore.RED + "%s:"%app.appname + Fore.RESET + (12-len(app.appname))*" "
                     + "%s"%app.description)
        return L

    def do_available(self, line):
        """List all the available applications in RepTate."""
        print("AVAILABLE APPLICATIONS")
        print("======================")

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
            self.applications[name].delete_multiplot()
            del self.applications[name]
        else:
            print("Application \"%s\" not found" % name)

    def do_delete(self, name):
        """Delete an open application. By hitting TAB, all the currently open applications are shown.

        Arguments:
            - name {str} -- Application to delete"""
        self.delete(name)
    do_del = do_delete

    def complete_delete(self, text, line, begidx, endidx):
        """Complete delete application command"""
        app_names = list(self.applications.keys())
        if not text:
            completions = app_names[:]
        else:
            completions = [f for f in app_names if f.startswith(text)]
        return completions
    complete_del = complete_delete

    def list(self):
        """List open applications"""
        L = []
        for app in list(self.applications.values()):
            L.append(Fore.RED + "%s:"%app.appname + Fore.RESET + (12-len(app.appname))*" "
                     + "%s"%app.description)
        return L

    def do_list(self, line):
        """List all the currently open applications."""
        print("CURRENTLY RUNNING APPLICATIONS")
        print("==============================")

        L = self.list()
        for app in L:
            print(app)

    def do_tree(self, line):
        """Show a tree structure of all open applications, tools, datasets and theories"""
        for app in self.applications.keys():
            print(Fore.RED + "%s"%self.applications[app].name + Fore.RESET)
            self.applications[app].do_tree(str(1))

    def new(self, appname):
        """Create a new application and open it.

Arguments:
    - name {str} -- Application to open (MWD, LVE, TTS, etc)"""
        if (appname in self.available_applications):
            self.application_counter += 1
            newapp = self.available_applications[appname](
                appname + str(self.application_counter), self)
            self.applications[newapp.name] = newapp
            if (self.mode == CmdMode.batch):
                newapp.prompt = ''
            else:
                newapp.prompt = self.prompt[:-2] + '/' + Fore.RED + newapp.name + '> '
            return newapp
        else:
            print("Application \"%s\" is not available" % appname)
            return None

    def do_new(self, appname):
        """Create a new application and open it.

Arguments:
    - name {str} -- Application to open (MWD, LVE, TTS, etc)"""
        newapp = self.new(appname)
        if (newapp != None):
            if CmdBase.mode != CmdMode.GUI:
                newapp.cmdqueue.append("new")
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

    def do_switch(self, line):
        """Set focus to an open application/set/theory/tool.
By hitting TAB, all the currently accessible elements are shown.
Arguments:
    - name {str} -- Name of the applicaton/set/theory/tool to switch the focus to."""
        items=line.split('.')
        if len(items)>1:
            name=items[0]
            if name in self.applications.keys():
                app = self.applications[name]
                app.cmdqueue.append('switch '+'.'.join(items[1:]))
                app.cmdloop()
            else:
                print("Application \"%s\" not found" % name)
        else:
            name=items[0]
            if name in self.applications.keys():
                app = self.applications[name]
                app.cmdloop()
            else:
                print("Application \"%s\" not found" % name)

    def complete_switch(self, text, line, begidx, endidx):
        """Complete switch command"""
        applist = list(self.applications.keys())
        setlist = []
        for app in applist:
            setnames = self.applications[app].get_tree()
            setlist += [app + '.' + s for s in setnames]
        switchlist = applist + setlist
        if not text:
            completions = switchlist[:]
        else:
            completions = [f for f in switchlist if f.startswith(text)]
        return completions

# MAXWELL MODES COPY

    def do_copy_modes(self, line):
        """Copy maxwell modes from one theory to another. Both theories may live inside different applications and/or datasets

Usage:
    copymodes App1.SetA.TheoryI App2.SetB.TheoryJ

Arguments:
    - line {str} -- Origin (App.Dataset.Theory) Destination (App.Dataset.Theory) """
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
        if source==target:
            print("Source and Target theories must be different")
            return

        get_dict, set_dict = self.list_theories_Maxwell()
        dict_keys = list(
            get_dict.keys())  #get_dict and set_dict have the same keys
        if ((source in dict_keys) and (target in dict_keys)):
            tau, G, success = get_dict[source]()
            if not success:
                self.logger.warning("Could not get modes successfully")
                return
            success = set_dict[target](tau, G)
            if not success:
                self.logger.warning("Could not set modes successfully")
                return
            print('Copied modes from %s to %s' % (source, target))
            return
        else:
            print("Source or Target not found\n"
                  "or theory does not have modes.\n"
                  "No copy has been made")
            return

    def complete_copy_modes(self, text, line, begidx, endidx):
        """Complete the command copy_modes"""
        L, S = self.list_theories_Maxwell()
        L = list(L.keys())
        if not text:
            completions = L[:]
        else:
            completions = [f for f in L if f.startswith(text)]
        return completions

    def list_theories_Maxwell(self, th_exclude=None):
        """List the theories in the current RepTate instance that provide and need
        Maxwell modes"""
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

    def do_list_theories_Maxwell(self, line=""):
        """List the theories in the current RepTate instance that provide Maxwell modes"""
        L, S = self.list_theories_Maxwell()
        if len(L)>0:
            print("The following open theories provide/require Maxwell Modes:")
            for k in L.keys():
                items = k.split('.')
                print(Fore.RED + items[0] + Fore.RESET + "." +
                      Fore.YELLOW + items[1] + Fore.RESET + "." +
                      Fore.MAGENTA + items[2])
        else:
            print("Currently there are no open theories that provide Maxwell modes.")

# OTHER STUFF

    def help_tutorial(self):
        """[summary]

        [description]
        """
        print('Visit the page:')
        print('https://reptate.readthedocs.io/manual/Applications/All_Tutorials/All_Tutorials.html')

    def do_about(self, line):
        """Show about info."""
        print(Fore.GREEN + "RepTate " + Fore.RESET +
              "(Rheology of Entangled Polymers: Toolkit for the Analysis of Theory and Experiment), " +
              "was originally created in Delphi by Jorge Ramírez and Alexei Likhtman at the University of Leeds " +
              "and the University of Reading, as part of the muPP2 project, funded by the EPSRC.")
        print("")
        print("This new version is a port (and enhancement) of the original RepTate code to python," +
              " using pyqt and matplotlib for the visuals, and numpy and scipy for the numerical calculations.")
        print("")
        print("It has been developed by Jorge Ramírez (Universidad Politécnica de Madrid, " + Fore.CYAN
            + "jorge.ramirez@upm.es" + Fore.RESET + ") and Victor Boudara (University of Leeds, "
            + Fore.CYAN + "v.a.boudara@leeds.ac.uk" + Fore.RESET +").")
        print("")
        print("The program and source code are released under the GPLv3 license.")
        print("")
        print("This project is dedicated to the memory of our great friend and collaborator Alexei.")
        print("")
        print("Project page: " + Fore.CYAN + "https://github.com/jorge-ramirez-upm/RepTate")
        print("Documentation: " + Fore.CYAN + "http://reptate.readthedocs.io/")

    def do_quit(self, args):
        """Exit from the application."""
        msg = 'Do you really want to exit RepTate?'
        shall = input("\n%s (y/N) " % msg).lower() == 'y'
        if (shall):
            print("Exiting RepTate...")
            readline.write_history_file()
            #sys.exit()
            return True

    do_EOF = do_quit
    do_up = do_quit

    def check_version(self):
        url='https://api.github.com/repos/jorge-ramirez-upm/RepTate/releases'
        releasedata = (urlopen(url).read()).decode('UTF-8')
        parsed_json = (json.loads(releasedata))
        release_dict=parsed_json[0] # Get the latest release
        tag=release_dict['tag_name']
        version_github=tag.split('v')[1]
        version_current=Version.VERSION
        newversion=version_github>version_current
        return newversion, version_github, version_current

    def do_check_version(self, line):
        """Check if there is a new version of RepTate on Github."""
        newversion, version_github, version_current = self.check_version()
        if CmdBase.mode != CmdMode.GUI:
            print("Current Version:   " + Fore.CYAN + "%s"%version_current + Fore.RESET)
            print("Version on Github: " + Fore.CYAN + "%s"%version_github + Fore.RESET)
            if newversion:
                print("The version of RepTate on Github (%s) is more recent than the one you are running (%s)"%(version_github, version_current))
            else:
                print("Your version is up to date.")
