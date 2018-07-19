# RepTate: Rheology of Entangled Polymers: Toolkit for the Analysis of Theory and Experiments
# http://blogs.upm.es/compsoftmatter/software/reptate/
# https://github.com/jorge-ramirez-upm/RepTate
# http://reptate.readthedocs.io
# Jorge Ramirez, jorge.ramirez@upm.es
# Victor Boudara, mmvahb@leeds.ac.uk
# Copyright (2017) Universidad Politécnica de Madrid, University of Leeds
# This software is distributed under the GNU General Public License. 
"""Module CreateMaterialsDatabaseFile

Module that creates the basic Materials database data.

""" 
import numpy as np
import os
from polymer_data import polymer

polymerdict={}        
polymerdict['PEP'] = polymer(name='PEP',long='Polyethylene-propylene', author='Alexei Likhtman', date='17/03/2006', source='', comment='Recommended', B1=917.338632, B2=125.96, logalpha=-2.5897, CTg=0, tau_e=3.9636E-6, Ge=1.5503E6, Me=1.4306, c_nu=0.1, rho0=0.95, chem='', Te=25, M0=0)
polymerdict['PS'] = polymer(name='PS',long='Polystyrene', author='Alexei Likhtman', date='17/03/2006', source='', comment='Recommended',B1=651.8653, B2=-52.237, logalpha=-3.161, CTg=0, tau_e=0.0010423, Ge=3.0555E5, Me=16.518, c_nu=0.1, rho0=0.95, chem='C8H8', Te=170, M0=104)
polymerdict['PI'] = polymer(name='PI',long='Polyisoprene', author='Alexei Likhtman', date='17/03/2006', source='', comment='Recommended',B1=691.6245, B2=114.3, logalpha=-3.2147, CTg=14.65,tau_e=1.3213E-5, Ge=5.9535E5, Me=4.8158, c_nu=0.1, rho0=0.928, chem='C5H8', Te=25, M0=68)
polymerdict['PBd'] = polymer(name='PBd',long='Polybutadiene', author='Alexei Likhtman', date='17/03/2006', source='', comment='Recommended',B1=606.626, B2=142.11, logalpha=-3.161, CTg=13.0,tau_e=3.3965E-7, Ge=1.6154E6, Me=1.8136, c_nu=0.1, rho0=0.95, chem='CH2CH=CHCH2', Te=25, M0=54)
polymerdict['hPBd'] = polymer(name='hPBd',long='Hydrogenated Polybutadiene', author='Richard Graham', date='21/06/2006', source='', comment='Parameters for linear hydrogentated polybutadiene',B1=432, B2=70, logalpha=-3.161, CTg=0.01, tau_e=1.1885E-8, Ge=2.81E6, Me=1.26, c_nu=1, rho0=0.95, chem='CH2CH2-CH2CH2', Te=170, M0=56)

polymeruserdict={}        

dir_path = os.path.dirname(os.path.realpath(__file__))
np.save(os.path.join(dir_path, 'materials_database.npy'), polymerdict) 
np.save(os.path.join(dir_path,'user_database.npy'), polymeruserdict) 


