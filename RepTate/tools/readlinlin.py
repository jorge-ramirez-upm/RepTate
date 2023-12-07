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
# Copyright (2017-2023): Jorge Ramirez, Victor Boudara, Universidad Politécnica de Madrid, University of Leeds
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
"""Module readlinlin

Reads the linlin data from the compact *.npz file

"""
import os
import numpy as np

dir_path = os.path.dirname(os.path.realpath(__file__))
f = np.load(os.path.join(dir_path, "..", "theories", "linlin.npz"), allow_pickle=True)
Z = f["Z"]
cnu = f["cnu"]
data = f["data"]

Z0 = 100
cnu0 = 1.0
indZ = (np.where(Z == Z0))[0][0]
indcnu = (np.where(cnu == cnu0))[0][0]

table = data[indZ]
ind1 = 1 + indcnu * 2
ind2 = ind1 + 1
for i in range(len(table)):
    print(table[i][0], table[i][ind1], table[i][ind2])
