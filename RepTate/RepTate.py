import sys
import click
sys.path.append('core')
sys.path.append('gui')
sys.path.append('console')
sys.path.append('applications')
sys.path.append('theories')
sys.path.append('visual')
from ApplicationManager import *

@click.command()
@click.option('--gui', default=0, help='Start RepTate using GUI')
def start_RepTate(gui):
    if (gui):
        click.echo('Not implemented yet!')
    else:
        ApplicationManager().cmdloop()

if __name__ == '__main__':
    #sys.exit(start_RepTate())
    start_RepTate()
