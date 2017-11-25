import sys
import getopt
sys.path.append('core')
sys.path.append('gui')
sys.path.append('console')
sys.path.append('applications')
sys.path.append('theories')
from ApplicationManager import * 
from time import time, sleep

def start_RepTate(argv):
    """
    Main RepTate application. 
    
    :param list argv: Command line parameters passed to Reptate
    """
    GUI = False
    app = ApplicationManager()
    sys.exit(app.cmdloop())

if __name__ == '__main__':
    start_RepTate(sys.argv[1:])
