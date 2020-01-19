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
