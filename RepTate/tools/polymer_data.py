# RepTate: Rheology of Entangled Polymers: Toolkit for the Analysis of Theory and Experiments
# http://blogs.upm.es/compsoftmatter/software/reptate/
# https://github.com/jorge-ramirez-upm/RepTate
# http://reptate.readthedocs.io
# Jorge Ramirez, jorge.ramirez@upm.es
# Victor Boudara, mmvahb@leeds.ac.uk
# Copyright (2017) Universidad Politécnica de Madrid, University of Leeds
# This software is distributed under the GNU General Public License. 
"""Module polymer_data

Module to define the basic information about a polymer for the materials database.

""" 
class polymer:
    """[summary]
    
    [description]
    """
    def __init__ (self, **kwargs):
        """[summary]
        
        [description]
        
        Arguments:
            **kwargs {[type]} -- [description]
        """
        self.data = {
            'short'       : '',     # Short name
            'long'        : '',     # Full name
            'chem'        : '',     # Short hand Chemistry
            'M0'          : 0,      # Monomer molecular weight
            'description' : '',     # Description of parameters
            'author'      : '',     # Who added/Modified the parameters
            'date'        : '',     # Date of parameter modification
            # Likhtman-McLeish parameters
            'tau_e'       : 0,      # Rouse time of one entanglement
            'Ge'          : 0,      # Entanglement modulus
            'Me'          : 0,      # Entanglemnet molecular while
            'c_nu'        : 0,      # Constraint release parameter
            # WLF Parameters
            'C1'          : 0,      # Material parameter C1 for WLF Shift
            'C2'          : 0,      # Material parameter C2 for WLF Shift
            'Rho0'        : 0,      # Density of polymer at 0 °C
            'C3'          : 0,      # Density parameter TODO: Meaning of this?
            'T0'          : 0,      # Reference temperature?
            'CTg'         : 0,      # Molecular weight dependence of Tg
        }

        self.data.update(kwargs)
