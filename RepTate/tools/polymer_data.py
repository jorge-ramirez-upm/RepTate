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
            # Basic info
            'name'       : '',      # Short name
            'long'        : '',     # Full name
            'author'      : '',     # Who added/Modified the parameters
            'date'        : '',     # Date of parameter modification
            'source'      : '',     # Source/paper from where the data was obtained
            'comment'     : '',     # Additional comments about the parameters            
            'chem'        : '',     # Short hand Chemistry
            # WLF Parameters
            'B1'          : 0,      # Material parameter B1 for WLF Shift
            'B2'          : 0,      # Material parameter B2 for WLF Shift
            'logalpha'    : 0,      # Log_10 of the thermal expansion coefficient at 0 °C
            'CTg'         : 0,      # Molecular weight dependence of Tg
            # Likhtman-McLeish parameters
            'tau_e'       : 0,      # Rouse time of one entanglement
            'Ge'          : 0,      # Entanglement modulus
            'Me'          : 0,      # Entanglemnet molecular while
            'c_nu'        : 0,      # Constraint release parameter
            'rho0'        : 0,      # Density of polymer at 0 °C
            'Te'          : 0,      # Temperature at which the tube parameters have been determined
            'M0'          : 0,      # Molecular weight of repeating unit
        }

        self.data.update(kwargs)

    # def __init__ (self, oldpolymer):
    #     self.data={}
    #     for k in oldpolymer.data.keys():
    #         self.data[k] = oldpolymer.data[k]
