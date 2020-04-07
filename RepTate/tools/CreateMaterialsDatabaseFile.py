# RepTate: Rheology of Entangled Polymers: Toolkit for the Analysis of Theory and Experiments
# --------------------------------------------------------------------------------------------------------
#
# Authors:
#     Jorge Ramirez, jorge.ramirez@upm.es
#     Victor Boudara, victor.boudara@gmail.com
#
# Useful links:
#     http://blogs.upm.es/compsoftmatter/software/reptate/
#     https://github.com/jorge-ramirez-upm/RepTate
#     http://reptate.readthedocs.io
#
# --------------------------------------------------------------------------------------------------------
#
# Copyright (2017-2020): Jorge Ramirez, Victor Boudara, Universidad Politécnica de Madrid, University of Leeds
#
# This file is part of RepTate.
#
# RepTate is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# RepTate is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with RepTate.  If not, see <http://www.gnu.org/licenses/>.
#
# --------------------------------------------------------------------------------------------------------
"""Module CreateMaterialsDatabaseFile

Module that creates the basic Materials database data.

""" 
import numpy as np
import os
from polymer_data import polymer

polymerdict={}        
polymerdict['PEP'] = polymer(name='PEP',long='Polyethylene-propylene', author='Alexei Likhtman', date='17/03/2006', source='', comment='Recommended', B1=917.338632, B2=125.96, logalpha=-2.5897, CTg=0, tau_e=3.9636E-6, Ge=1.5503E6, Me=1.4306, c_nu=0.1, rho0=0.95, chem='', Te=25, M0=0, MK=0)
polymerdict['PS'] = polymer(name='PS',long='Polystyrene', author='Alexei Likhtman', date='17/03/2006', source='', comment='Recommended',B1=651.8653, B2=-52.237, logalpha=-3.161, CTg=0, tau_e=0.0010423, Ge=3.0555E5, Me=16.518, c_nu=0.1, rho0=0.95, chem='C8H8', Te=170, M0=104, MK=727)
polymerdict['PI'] = polymer(name='PI',long='Polyisoprene', author='Alexei Likhtman', date='17/03/2006', source='', comment='Recommended',B1=691.6245, B2=114.3, logalpha=-3.2147, CTg=14.65,tau_e=1.3213E-5, Ge=5.9535E5, Me=4.8158, c_nu=0.1, rho0=0.928, chem='C5H8', Te=25, M0=68, MK=140.5)
polymerdict['PBd'] = polymer(name='PBd',long='Polybutadiene', author='Alexei Likhtman', date='17/03/2006', source='', comment='Recommended',B1=606.626, B2=142.11, logalpha=-3.161, CTg=13.0,tau_e=3.3965E-7, Ge=1.6154E6, Me=1.8136, c_nu=0.1, rho0=0.95, chem='CH2CH=CHCH2', Te=25, M0=54, MK=103.9)
polymerdict['hPBd'] = polymer(name='hPBd',long='Hydrogenated Polybutadiene', author='Richard Graham', date='21/06/2006', source='', comment='Parameters for linear hydrogentated polybutadiene',B1=432, B2=70, logalpha=-3.161, CTg=0.01, tau_e=1.1885E-8, Ge=2.81E6, Me=1.26, c_nu=1, rho0=0.95, chem='CH2CH2-CH2CH2', Te=170, M0=56, MK=0)

polymeruserdict={}        

dir_path = os.path.dirname(os.path.realpath(__file__))
np.save(os.path.join(dir_path, 'materials_database.npy'), polymerdict) 
np.save(os.path.join(dir_path,'user_database.npy'), polymeruserdict) 


