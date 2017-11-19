import sys
import getopt
sys.path.append('core')
sys.path.append('gui')
sys.path.append('console')
sys.path.append('applications')
sys.path.append('theories')
sys.path.append('visual')
from QApplicationManager import *
from ApplicationManager import * #solved the issue with the matplot window not opening on Mac
from PyQt5.QtWidgets import QApplication
from SplashScreen import *
from time import time, sleep

def start_RepTate(argv):
    """
    Main RepTate application. 
    
    :param list argv: Command line parameters passed to Reptate
    """
    GUI = True
    try:
        opts, args = getopt.getopt(argv,"hc")
    except getopt.GetoptError:
        print ('test.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h","--help"):
            print ('RepTate.py [-g] \n\t-g\tRun the Graphic User Interface')
            sys.exit()
        elif opt == '-c':
            GUI=False

    if GUI:
        QApplication.setStyle("Fusion") #comment that line for a native look
        #for a list of available styles: "from PyQt5.QtWidgets import QStyleFactory; print(QStyleFactory.keys())"
        
        app = QApplication(sys.argv)
        start = time() 
        splash = SplashScreen()
        splash.show()
        while time() - start < 1:
            sleep(0.001)
            if (time()-start < 0.5):
                splash.showMessage("Loading Reptate...")
            else:
                splash.showMessage("Final touches...")
            app.processEvents()

        ex = QApplicationManager()
        ex.new_lve_window()
        splash.finish(ex)
        ex.showMaximized()
        sys.exit(app.exec_())
    else:
        app = ApplicationManager()
        sys.exit(app.cmdloop())

if __name__ == '__main__':
    start_RepTate(sys.argv[1:])
