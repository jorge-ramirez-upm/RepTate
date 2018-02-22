# RepTate: Rheology of Entangled Polymers: Toolkit for the Analysis of Theory and Experiments
# http://blogs.upm.es/compsoftmatter/software/reptate/
# https://github.com/jorge-ramirez-upm/RepTate
# http://reptate.readthedocs.io
# Jorge Ramirez, jorge.ramirez@upm.es
# Victor Boudara, mmvahb@leeds.ac.uk
# Copyright (2017) Universidad Politécnica de Madrid, University of Leeds
# This software is distributed under the GNU General Public License. 
"""Module linlin2npz

Reads all the files of the precalculated linlin theory and saves them 
in a more compact *.npz format

""" 
import numpy as np
import glob

files=glob.glob("g*.dat")
flist={}
for file in glob.glob("g*.dat"):
    n = file.split('.')
    m = int(n[0][1:])
    flist[m]=file


p = list(flist.keys())
p.sort()
Z=np.asarray(p)
cnu=np.asarray([0, 0.01, 0.03, 0.1, 0.3, 1, 3, 10])

data=[]    
for k in p:
    data.append(np.loadtxt(flist[k]))

np.savez_compressed("linlin.npz",Z=Z, cnu=cnu, data=data)
