import sys
from distutils.core import setup
import py2exe

sys.path.append('core')
sys.path.append('gui')
sys.path.append('console')
sys.path.append('applications')
sys.path.append('theories')
sys.path.append('visual')


setup(
    name="RepTate",
    version="0.5",
    description="Rheology of Entangled Polymers: Toolkit for the Analysis of Theory and Experiment",
    author="Jorge Ramirez",
    author_email="jorge.ramirez@upm.es",
    console=[{'script': 'RepTate.py'}],
)