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
from polymer_data import polymer

read_dictionary = np.load('materials_database.npy').item()
for k in read_dictionary.keys():
    print(k, ': ', read_dictionary[k].data, '\n')
