import sys
import getopt
#import click
sys.path.append('core')
sys.path.append('gui')
sys.path.append('console')
sys.path.append('applications')
sys.path.append('theories')
sys.path.append('visual')
from ApplicationManager import *
from QApplicationManager import *

#@click.command()
#@click.option('--gui', default=0, help='Start RepTate using GUI')
#def start_RepTate(gui):
    #if (gui):
    #    click.echo('Not implemented yet!')
    #else:
        #ApplicationManager().cmdloop()

def start_RepTate(argv):
    GUI=False
    try:
        opts, args = getopt.getopt(argv,"hg")
    except getopt.GetoptError:
        print ('test.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h","--help"):
            print ('RepTate.py -i <inputfile> -o <outputfile>')
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
        #ApplicationManager().cmdloop()

if __name__ == '__main__':
    #sys.exit(start_RepTate())
    start_RepTate(sys.argv[1:])
