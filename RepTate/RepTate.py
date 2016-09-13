import sys
import getopt
sys.path.append('core')
sys.path.append('gui')
sys.path.append('console')
sys.path.append('applications')
sys.path.append('theories')
sys.path.append('visual')
from ApplicationManager import *
from QApplicationManager import *

def start_RepTate(argv):
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
        ex = QApplicationManager()
        ex.showMaximized()
        sys.exit(app.exec_())
    else:
        app = ApplicationManager()
        sys.exit(app.cmdloop())

if __name__ == '__main__':
    start_RepTate(sys.argv[1:])
