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
"""Module CmdBase

Module that defines the basic command line interaction with the user.

""" 
import os
import sys
import cmd
import readline
import enum
#from pint import UnitRegistry
from colorama import Fore
from numpy import *
import logging

class CmdMode(enum.Enum):
    """[summary]
    
    [description]
    """
    cmdline = 0
    batch = 1
    GUI = 2
    modes=["Command Line Interpreter", "Batch processing", "Graphical User Interface"]

    def __str__(self):
        """[summary]
        
        [description]
        """
        return Fore.CYAN + "cmdline: " + Fore.RESET + "%s\n"%(self.modes.value[0]) + Fore.CYAN + "batch:   " + Fore.RESET + "%s\n"%self.modes.value[1] + Fore.CYAN + "GUI:     " + Fore.RESET + "%s"%self.modes.value[2]

class CalcMode(enum.Enum):
    """[summary]

    [decription]
    """
    singlethread = 0
    multithread = 1
    modes=["Calc and Min in the same thread as GUI", "Calc and Min in separate threads to GUI"]

    def __str__(self):
        """[summary]

        [description]
        """
        return "Single thread: %d\nMulti-thread: %d"%(self.modes.value[0], self.modes.value[1])

class CmdBase(cmd.Cmd):
    """Basic Cmd Console that is inherited by most Reptate objects
    
    [description]
    """

    prompt = '> '
    mode = CmdMode.cmdline
    calcmode = CalcMode.multithread
    #ureg = UnitRegistry()

    def __init__ (self, parent=None):
        """Constructor"""
        super().__init__()

        delims = readline.get_completer_delims()
        delims = delims.replace(os.sep, '')
        readline.set_completer_delims(delims)

        # list of safe methods for eval
        self.safe_globals = ['arccos', 'arcsin', 'arctan', 'arctan2', 'ceil', 'cos', 
                        'cosh', 'degrees', 'e', 'exp', 'fabs', 'floor', 
                        'fmod', 'frexp', 'hypot', 'ldexp', 'log', 'log10', 
                        'modf', 'pi', 'pow', 'radians', 'sin', 'sinh', 'sqrt', 
                        'tan', 'tanh'] 
        self.safe_locals = ['self']
            
        # creating a dictionary of safe methods 
        self.safe_dict = {}
        for k in self.safe_globals:
            self.safe_dict[k] = globals().get(k, None)
        for k in self.safe_locals:
            self.safe_dict[k] = locals().get(k, None)
        self.safe_dict['print'] = print
        self.safe_dict['list'] = list
        self.safe_dict['type'] = type

        self.logger=None
        
    def do_shell(self, line):
        """Run a shell command
        
Arguments:
    - line {str} -- Command to run"""
        print("running shell command:", line)
        output = os.popen(line).read()
        print(output)
        self.last_output = output

    #def do_cd(self, line):
    #    """Change folder
    #            
    #    Arguments:
    #        - line {[str} -- Folder to change to (.. means upper folder)
    #    """
    #    if os.path.isdir(line):
    #        os.chdir(line)
    #    else:
    #        print("Folder %s does not exist"%line)

    def __listdir(self, root):
        """List directory 'root' appending the path separator to subdirs.
        
        [description]
        
        Arguments:
            - root {[type]} -- [description]
        
        Returns:
            - [type] -- [description]
        """
        res = []
        for name in os.listdir(root):
            path = os.path.join(root, name)
            if os.path.isdir(path):
                name += os.sep
                #name += '/'
            res.append(name)
        return res


    def __complete_path(self, path=None):
        """Perform completion of filesystem path."""
        if not path:
            return self.__listdir('.')
        
        dirname, rest = os.path.split(path)
        tmp = dirname if dirname else '.'
        res = [os.path.join(dirname, p)
                for p in self.__listdir(tmp) if p.startswith(rest)]
                
        # more than one match, or single match which does not exist (typo)
        if len(res) > 1 or not os.path.exists(path):
            return res
        # resolved to a single directory, so return list of files below it
        if os.path.isdir(path):
            return [os.path.join(path, p) for p in self.__listdir(path)]
        # exact file match terminates this completion
        return [path + ' ']
        
    def complete_cd(self, text, line, begidx, endidx):
        """Completions for the cd command.
        
        [description]
        
        Arguments:
            - text {[type]} -- [description]
            - line {[type]} -- [description]
            - begidx {[type]} -- [description]
            - endidx {[type]} -- [description]
        
        Returns:
            - [type] -- [description]
        """
        test=line.split()
        if (len(test)>1):
            result=self.__complete_path(test[1])
        else:
            result=self.__complete_path()
        
        return result

    def do_ls(self, line):
        """List contents of current folder."""
        dirs=os.listdir()
        for d in dirs:
            print("%s"%d)
    do_dir = do_ls

    def do_pwd(self, line):
        """Print the current folder"""
        print(os.getcwd())
    do_cwd = do_pwd

    def emptyline(self):
        """Called when an empty line is introduced in the prompt.
        """
        pass

    def do_EOF(self, args):
        """Exit Console and Return to Parent or exit"""
        print("")
        return True
    do_up = do_EOF
    
    def do_quit(self, args):
        """Exit from the application."""
        if (CmdBase.mode==CmdMode.batch):
            print ("Exiting RepTate...")
            readline.write_history_file()
            sys.exit()
        msg = 'Do you really want to exit RepTate?'
        shall = input("%s (y/N) " % msg).lower() == 'y'         
        if (shall):
            print ("Exiting RepTate...")
            readline.write_history_file()
            sys.exit()
            
    
    def default(self, line):
        """Called on an input line when the command prefix is not recognized.
        In that case we execute the line as Python code.
        """
        try:
            eval(line, {"__builtins__":None}, self.safe_dict) #in self._locals, self._globals
        except NameError as e:
            print("Command " + Fore.RED + "%s"%line + Fore.RESET + " not found")
        except TypeError as e:
            print("Command " + Fore.RED + "%s"%line + Fore.RESET + " not found")
        except Exception as e:
            print (e.__class__, ":", e)

    def completedefault(self, text, line, begidx, endidx):
        items=line.replace(',',' ').replace('(',' ').replace(')', ' ').replace('.', ' ').split()
        lastitem=items[-1]
        if len(items)>1:
            onebeforelastitem=items[-2]
        else:
            onebeforelastitem=""
        L=list(self.safe_dict.keys())
        L2=list(vars(self))
        if not lastitem:
            completions = L
        elif onebeforelastitem=='self':
            completions = ['self.'+f for f in L2 if f.startswith(lastitem)]
        elif lastitem=='self':
            completions = L2
        elif lastitem in L and len(items)==1:
            completions=L
        else:
            completions = [f for f in L if f.startswith(lastitem)]
        return completions

    def do_log(self, line):
        """Info about the logger"""
        if self.logger!=None:
            nhandlers=len(logging.getLogger('RepTate').handlers)
            logfilename=""
            if nhandlers>0:
                print(Fore.RED + "%15s %10s"%("Log Handler", "Level"))
                print(26*"=" + Fore.RESET)
            print("%15s %10s"%("Main", logging.getLevelName(logging.getLogger('RepTate').level)))
            for i in range(nhandlers):
                h=logging.getLogger('RepTate').handlers[i]
                if isinstance(h, logging.handlers.RotatingFileHandler):
                    print("%15s %10s"%("File", logging.getLevelName(h.level)))
                    logfilename=h.baseFilename
                elif isinstance(h, logging.StreamHandler):
                    print("%15s %10s"%("Console", logging.getLevelName(h.level)))
            print("")
            print (Fore.RED+"Main Logger level:    " + Fore.RESET + "RepTate")
            print (Fore.RED+"Current Logger level: " + Fore.RESET + "%s"%self.logger.name)
            print (Fore.RED+"Log File: " + Fore.RESET + "%s"%logfilename)

    def do_loglevel(self, line):
        """Set log level"""
        if self.logger!=None:
            nhandlers=len(logging.getLogger('RepTate').handlers)
            for i in range(nhandlers):
                h=logging.getLogger('RepTate').handlers[i]
                if isinstance(h, logging.handlers.RotatingFileHandler):
                    fhandler=h
                elif isinstance(h, logging.StreamHandler):
                    chandler=h
            items=line.split()
            h=None
            l=None
            handlers=["Main", "File", "Console"]
            levels=["NOTSET", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
            if len(items)<2:
                print("Wrong number of parameters. Example of use: loglevel Console WARNING")
            else:
                if items[0]=="Main":
                    h=logging.getLogger('RepTate')
                elif items[0]=="File":
                    h=fhandler
                elif items[0]=="Console":
                    h=chandler
                else:
                    print("Wrong Log Handler. Valid values are:")
                    print(handlers)
                if items[1] not in levels:
                    print("Wrong Log level. Valid values are:")
                    print(levels)
                else:
                    l = items[1]

                if h is not None and l is not None:
                    h.setLevel(l)
    
    def complete_loglevel(self, text, line, begidx, endidx):
        handlers=["Main", "File", "Console"]
        levels=["NOTSET", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        items=line.split()
        nitems=len(items)
        if nitems<2:
            completions = [f for f in handlers if f.startswith(text)]
        elif nitems==2 and items[1] not in handlers:
            completions = [f for f in handlers if f.startswith(text)]
        else:
            completions = [f for f in levels if f.startswith(text)]
        return completions

    def do_console(self, line):
        """Print/Set current & available Console modes
        
    - console --> print current mode
    - console available --> print available modes
    - console [cmdline, batch, GUI] --> Set the console mode to [cmdline, batch, GUI]
        
Arguments:
    - [line] {str} -- available, cmdline, batch, GUI
        """
        if (line==""):
            print("Current console mode: %s"%CmdMode.modes.value[CmdBase.mode.value])
        elif (line=="available"):
            c = CmdMode(0)
            print(c)
        elif (line in dict(CmdMode.__members__.items())):
            CmdBase.mode=CmdMode[line]
        else:
            print ("Console mode %s not valid"%line)

        if (self.mode==CmdMode.batch):
            self.prompt = ''
            
    def complete_console(self, text, line, begidx, endidx):
        names = ["cmdline", "batch", "GUI", "available"]
        if not text:
            completions = names[:]
        else:
            completions = [f for f in names if f.startswith(text)]
        return completions

    def cmdloop(self, intro=""):
        #print(self.intro)
        while True:
            try:
                super(CmdBase, self).cmdloop(intro="")
                break
            except KeyboardInterrupt:
                print("^C")

