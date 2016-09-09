import os
import sys
import cmd
import readline

class CmdBase(cmd.Cmd):
    """Basic Cmd Console that is inherited by most Reptate objects"""

    prompt = '> '

    def __init__ (self, parent=None):
        """Constructor """
        super(CmdBase, self).__init__()

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
        """Complete cd command
           TODO: COMPLETE SUBFOLDERS TOO"""
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
        """List contents of current folder
           TODO: CONSIDER SUBFOLDERS TOO
        """
        dirs=os.listdir()
        for d in dirs:
            print("%s"%d)
    do_dir = do_ls

    def do_pwd(self, line):
        """Print the current folder"""
        print(os.getcwd())
    do_cwd = do_pwd

    def emptyline(self):
        pass

    def do_EOF(self, args):
        """Exit Console and Return to Parent or exit"""
        print("")
        return True
    
    def do_quit(self, args):
        """Exit from the application"""
        msg = 'Do you really want to exit RepTate?'
        shall = input("%s (y/N) " % msg).lower() == 'y'         
        if (shall):
            print ("Exiting RepTate...")
            readline.write_history_file()
            sys.exit()
            
    

