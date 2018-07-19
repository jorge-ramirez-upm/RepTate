# RepTate: Rheology of Entangled Polymers: Toolkit for the Analysis of Theory and Experiments
# http://blogs.upm.es/compsoftmatter/software/reptate/
# https://github.com/jorge-ramirez-upm/RepTate
# http://reptate.readthedocs.io
# Jorge Ramirez, jorge.ramirez@upm.es
# Victor Boudara, mmvahb@leeds.ac.uk
# Copyright (2017) Universidad Politécnica de Madrid, University of Leeds
# This software is distributed under the GNU General Public License. 
"""Module readlinlin

Reads the linlin data from the compact *.npz file

""" 
import os
import numpy as np

dir_path = os.path.dirname(os.path.realpath(__file__))
f=np.load(os.path.join(dir_path, "..", "theories", "linlin.npz"))
Z=f['Z']
cnu=f['cnu']
data=f['data']

Z0=100
cnu0=1.0
indZ = (np.where(Z==Z0))[0][0]
indcnu = (np.where(cnu==cnu0))[0][0]

table=data[indZ]
ind1=1+indcnu*2
ind2=ind1+1
for i in range(len(table)):
    print(table[i][0], table[i][ind1], table[i][ind2])
