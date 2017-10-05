import sys
import getopt
sys.path.append('core')
sys.path.append('gui')
sys.path.append('console')
sys.path.append('applications')
sys.path.append('theories')
sys.path.append('visual')
from QApplicationManager import *
from ApplicationManager import * #moved that one lines down solved the issue with the matplot window not opening on Mac
from PyQt5.QtWidgets import QApplication
from SplashScreen import *
from time import time, sleep

def start_RepTate(argv):
    """
    Main RepTate application. 
    
    :param list argv: Command line parameters passed to Reptate
    """
    GUI=False
    try:
        opts, args = getopt.getopt(argv,"hg")
    except getopt.GetoptError:
        print ('test.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h","--help"):
            print ('RepTate.py [-g] \n\t-g\tRun the Graphic User Interface')
            sys.exit()
        elif opt == '-g':
            GUI=True

    if GUI:
        app = QApplication(sys.argv)
        start = time() 
        splash = SplashScreen()
        splash.show()
        while time() - start < 2:
            sleep(0.001)
            if (time()-start < 1):
                splash.showMessage("Loading Reptate...")
            else:
                splash.showMessage("Final touches...")
            app.processEvents()

        ex = QApplicationManager()
        splash.finish(ex)
        ex.showMaximized()
        sys.exit(app.exec_())
    else:
        app = ApplicationManager()
        sys.exit(app.cmdloop())

if __name__ == '__main__':
    start_RepTate(sys.argv[1:])
