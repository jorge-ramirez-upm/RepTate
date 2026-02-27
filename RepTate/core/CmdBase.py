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
# Copyright (2017-2026): Jorge Ramirez, Victor Boudara, Universidad Politécnica de Madrid, University of Leeds
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
"""Module CmdBase

Module that defines the basic command line interaction with the user.

"""
import enum

from numpy import *


class CalcMode(enum.Enum):
    """Operation mode: Single or Multithread"""

    singlethread = 0
    multithread = 1
    modes = [
        "Calc and Min in the same thread as GUI",
        "Calc and Min in separate threads to GUI",
    ]

    def __str__(self):
        """String representation of the class"""
        return "Single thread: %d\nMulti-thread: %d" % (
            self.modes.value[0],
            self.modes.value[1],
        )


class CmdBase:
    """Basic Cmd Console that is inherited by most Reptate objects"""

    calcmode = CalcMode.multithread

    def __init__(self):
        """**Constructor**"""

        self.logger = None
