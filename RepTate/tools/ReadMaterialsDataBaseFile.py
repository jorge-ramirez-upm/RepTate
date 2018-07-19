# RepTate: Rheology of Entangled Polymers: Toolkit for the Analysis of Theory and Experiments
# http://blogs.upm.es/compsoftmatter/software/reptate/
# https://github.com/jorge-ramirez-upm/RepTate
# http://reptate.readthedocs.io
# Jorge Ramirez, jorge.ramirez@upm.es
# Victor Boudara, mmvahb@leeds.ac.uk
# Copyright (2017) Universidad Politécnica de Madrid, University of Leeds
# This software is distributed under the GNU General Public License. 
"""Module ReadMaterialsDataBaseFile

Module to read the contents of the materials database file.

""" 
import numpy as np
import os
from polymer_data import polymer

dir_path = os.path.dirname(os.path.realpath(__file__))
read_dictionary = np.load(os.path.join(dir_path, 'materials_database.npy')).item()
for k in read_dictionary.keys():
    print(k, ': ', read_dictionary[k].data, '\n')
