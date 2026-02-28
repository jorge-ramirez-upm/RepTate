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

import os
import numpy as np
import numpy.testing as npt
import pytest

from RepTate.core.CmdBase import CmdBase, CalcMode
from RepTate.gui.QApplicationManager import QApplicationManager
from PySide6.QtWidgets import QApplication

CmdBase.calcmode = CalcMode.singlethread
app = QApplication()
ex = QApplicationManager()

def test_LVE_Likhtman_McLeish():
    ex.handle_new_app("LVE")
    pi_dir = "data%sPI_LINEAR%s" % ((os.sep,) * 2)
    thisApp = ex.applications["LVE1"]
    thisApp.new_tables_from_files([
                pi_dir + "PI_13.5k_T-35.tts",
                pi_dir + "PI_23.4k_T-35.tts",
                pi_dir + "PI_33.6k_T-35.tts",
                pi_dir + "PI_94.9k_T-35.tts",
                pi_dir + "PI_225.9k_T-35.tts",
                pi_dir + "PI_483.1k_T-35.tts",
                pi_dir + "PI_634.5k_T-35.tts",
                pi_dir + "PI_1131k_T-35.tts",
            ])
    thisSet = thisApp.datasets["Set1"]
    thisSet.new_theory("Likhtman-McLeish")
    thisTheory = thisSet.theories["LML1"]
    thisSet.handle_actionMinimize_Error()
    tau_e = thisTheory.parameters["tau_e"].value
    Ge = thisTheory.parameters["Ge"].value
    Me = thisTheory.parameters["Me"].value
    assert tau_e == pytest.approx(0.06773845511821698, rel=1e-4)
    assert Ge == pytest.approx(509664.8088612225, rel=1e-4)
    assert Me == pytest.approx(4.492962262350123, rel=1e-4)

def test_LVE_Maxwell_Modes():
    ex.handle_new_app("LVE")
    pi_dir = "data%sPI_LINEAR%s" % ((os.sep,) * 2)
    thisApp = ex.applications["LVE2"]
    thisApp.new_tables_from_files([
                pi_dir + "PI_225.9k_T-35.tts",
            ])
    thisSet = thisApp.datasets["Set1"]
    thisSet.new_theory("Maxwell Modes")
    thisTheory = thisSet.theories["MM1"]
    thisSet.handle_actionMinimize_Error()
    # for k in thisTheory.parameters:
    #     print(k, thisTheory.parameters[k].value)
    logwmin = thisTheory.parameters["logwmin"].value
    logwmax = thisTheory.parameters["logwmax"].value
    nmodes = thisTheory.parameters["nmodes"].value
    logG00 = thisTheory.parameters["logG00"].value
    logG01 = thisTheory.parameters["logG01"].value
    logG02 = thisTheory.parameters["logG02"].value
    logG03 = thisTheory.parameters["logG03"].value
    logG04 = thisTheory.parameters["logG04"].value
    logG05 = thisTheory.parameters["logG05"].value
    logG06 = thisTheory.parameters["logG06"].value
    logG07 = thisTheory.parameters["logG07"].value
    logG08 = thisTheory.parameters["logG08"].value
    assert logwmin == pytest.approx(-6.385241978597786, rel=1e-4)
    assert logwmax == pytest.approx(3.0010913446595318, rel=1e-4)
    assert nmodes == 9
    # assert logG00 == pytest.approx(-9.98121345866038, rel=1e-4)
    assert logG01 == pytest.approx(2.6532429979420713, rel=1e-4)
    assert logG02 == pytest.approx(5.219297965636228, rel=1e-4) 
    assert logG03 == pytest.approx(5.0406510877327815, rel=1e-4)
    assert logG04 == pytest.approx(4.804722071852002, rel=1e-4)
    assert logG05 == pytest.approx(4.687069287243573, rel=1e-4)
    assert logG06 == pytest.approx(5.145666298139436, rel=1e-4)
    assert logG07 == pytest.approx(5.76694930919948, rel=1e-4)
    assert logG08 == pytest.approx(6.829225757858246, rel=1e-4) 


def test_LVE_DTD_Stars():
    ex.handle_new_app("LVE")
    pi_dir = "data%sPI_STAR%s" % ((os.sep,) * 2)
    thisApp = ex.applications["LVE3"]
    thisApp.new_tables_from_files([
                pi_dir + "S6Z12T40.tts",
                pi_dir + "S6Z16T40.tts",
                pi_dir + "S6Z8.1T40.tts",
            ])
    thisSet = thisApp.datasets["Set1"]
    thisSet.new_theory("DTD Stars")
    thisTheory = thisSet.theories["DTDS1"]
    thisSet.handle_actionMinimize_Error()
    # for k in thisTheory.parameters:
    #     print(k, thisTheory.parameters[k].value)
    G0 = thisTheory.parameters["G0"].value
    tau_e = thisTheory.parameters["tau_e"].value
    Me = thisTheory.parameters["Me"].value
    alpha = thisTheory.parameters["alpha"].value
    assert G0 == pytest.approx(0.8513160549985747, rel=1e-4)
    assert tau_e == pytest.approx(5.417382973435641e-06, rel=1e-4)
    assert Me == pytest.approx(4.369223232374666, rel=1e-4) 
    assert alpha == 1.0

def test_LVE_ReSpect():
    ex.handle_new_app("LVE")
    pi_dir = "data%sReSpect%s" % ((os.sep,) * 2)
    thisApp = ex.applications["LVE4"]
    thisApp.new_tables_from_files([
                pi_dir + "test1.tts",
            ])
    thisSet = thisApp.datasets["Set1"]
    thisSet.new_theory("ReSpect")
    thisTheory = thisSet.theories["RS1"]
    thisSet.handle_actionCalculate_Theory()
    x = np.array(thisTheory.discspectrum.get_xdata())
    y = np.array(thisTheory.discspectrum.get_ydata())

    expected_x = np.array([3.64858328,  3.09262379,  2.56845089,  2.0418679,   1.50298628,  0.95004366,
  0.38634846, -0.18185822, -0.7471834,  -1.30218474, -1.84069882, -2.35960542,
 -2.86032535, -3.35203179,  -3.87576257])
    expected_y = np.array([0.38900764, 1.01140786, 1.30106978, 1.39058669, 1.36537465, 1.29553195,
  1.23776055, 1.22736189, 1.26972821, 1.33873382, 1.3839094,   1.34192586,
  1.14501827, 0.72009324, -0.05033049])

    # print(x)
    # print(expected_x)
    # print(y)
    # print(expected_y)

    npt.assert_allclose(x, expected_x, rtol=1e-5)
    npt.assert_allclose(y, expected_y, rtol=1e-5)

    # for k in thisTheory.parameters:
    #     print(k, thisTheory.parameters[k].value)
    # G0 = thisTheory.parameters["G0"].value
    # tau_e = thisTheory.parameters["tau_e"].value
    # Me = thisTheory.parameters["Me"].value
    # alpha = thisTheory.parameters["alpha"].value
    # assert G0 == 0.8513160549985747
    # assert tau_e == 5.417382973435641e-06
    # assert Me == 4.369223232374666
    # assert alpha == 1.0

def test_MWD_Discretize_MWD():
    ex.handle_new_app("MWD")
    pi_dir = "data%sMWD%s" % ((os.sep,) * 2)
    thisApp = ex.applications["MWD5"]
    thisApp.new_tables_from_files([
                pi_dir + "Munstedt_PSIV.gpc",
            ])
    thisSet = thisApp.datasets["Set1"]
    thisSet.new_theory("Discretize MWD")
    thisTheory = thisSet.theories["DMWD1"]
    # thisSet.handle_actionMinimize_Error()
    # for k in thisTheory.parameters:
    #     print(k, thisTheory.parameters[k].value)
    Mn = thisTheory.parameters["Mn"].value
    Mw = thisTheory.parameters["Mw"].value
    Mz = thisTheory.parameters["Mz"].value
    PDI = thisTheory.parameters["PDI"].value
    logmmin = thisTheory.parameters["logmmin"].value
    logmmax = thisTheory.parameters["logmmax"].value
    nbin = thisTheory.parameters["nbin"].value
    logM00 = thisTheory.parameters["logM00"].value
    logM01 = thisTheory.parameters["logM01"].value
    logM02 = thisTheory.parameters["logM02"].value
    logM03 = thisTheory.parameters["logM03"].value
    logM04 = thisTheory.parameters["logM04"].value
    logM05 = thisTheory.parameters["logM05"].value
    logM06 = thisTheory.parameters["logM06"].value
    logM07 = thisTheory.parameters["logM07"].value
    assert Mn == pytest.approx(117.1301416129797, rel=1e-4)
    assert Mw == pytest.approx(230.72627779194102, rel=1e-4)
    assert Mz == pytest.approx(362.3487007759203, rel=1e-4)
    assert PDI == pytest.approx(1.9698283858846906, rel=1e-4)
    assert logmmin == pytest.approx(4.01037205711021, rel=1e-4)
    assert logmmax == pytest.approx(6.283637463659533, rel=1e-4)
    assert nbin == 7
    assert logM00 == pytest.approx(4.01037205711021, rel=1e-4)
    assert logM01 == pytest.approx(4.335124258045828, rel=1e-4)
    assert logM02 == pytest.approx(4.659876458981445, rel=1e-4)
    assert logM03 == pytest.approx(4.984628659917063, rel=1e-4)
    assert logM04 == pytest.approx(5.309380860852681, rel=1e-4)
    assert logM05 == pytest.approx(5.634133061788297, rel=1e-4)
    assert logM06 == pytest.approx(5.958885262723915, rel=1e-4)
    assert logM07 == pytest.approx(6.283637463659533, rel=1e-4)

def test_MWD_GEX():
    ex.handle_new_app("MWD")
    pi_dir = "data%sMWD%s" % ((os.sep,) * 2)
    thisApp = ex.applications["MWD6"]
    thisApp.new_tables_from_files([
                pi_dir + "Munstedt_PSIV.gpc",
            ])
    thisSet = thisApp.datasets["Set1"]
    thisSet.new_theory("GEX")
    thisTheory = thisSet.theories["GEX1"]
    thisSet.handle_actionMinimize_Error()
    # for k in thisTheory.parameters:
    #     print(k, thisTheory.parameters[k].value)
    logW0 = thisTheory.parameters["logW0"].value
    logM0 = thisTheory.parameters["logM0"].value
    a = thisTheory.parameters["a"].value
    b = thisTheory.parameters["b"].value
    assert logW0 == pytest.approx(7.691229139481297, rel=1e-4)
    assert logM0 == pytest.approx(5.328714760610867, rel=1e-4)
    assert a == pytest.approx(1.3426251741114326, rel=1e-4)
    assert b == pytest.approx(1.2517441353471008, rel=1e-4)

def test_MWD_LogNormal():
    ex.handle_new_app("MWD")
    pi_dir = "data%sMWD%s" % ((os.sep,) * 2)
    thisApp = ex.applications["MWD7"]
    thisApp.new_tables_from_files([
                pi_dir + "Munstedt_PSIV.gpc",
            ])
    thisSet = thisApp.datasets["Set1"]
    thisSet.new_theory("LogNormal")
    thisTheory = thisSet.theories["LN1"]
    thisSet.handle_actionMinimize_Error()
    # for k in thisTheory.parameters:
    #     print(k, thisTheory.parameters[k].value)
    logW0 = thisTheory.parameters["logW0"].value
    logM0 = thisTheory.parameters["logM0"].value
    sigma = thisTheory.parameters["sigma"].value
    assert logW0 == pytest.approx(2.3556795406749935, rel=1e-4)
    assert logM0 == pytest.approx(4.997549485273925, rel=1e-4)
    assert sigma == pytest.approx(0.8015827090542221, rel=1e-4)

def test_TTS_WLF():
    ex.handle_new_app("TTS")
    pi_dir = "data%sPI_LINEAR%sosc%s" % ((os.sep,) * 3)
    thisApp = ex.applications["TTS8"]
    thisApp.new_tables_from_files([
                pi_dir + "PI1000k-02_-10C_FS_PP10.osc",
                pi_dir + "PI1000k-02_-20C_FS_PP10.osc",
                pi_dir + "PI1000k-02_-30C_FS_PP10.osc",
                pi_dir + "PI1000k-02_-40C_FS_PP10.osc",
                pi_dir + "PI1000k-02_0C_FS_PP10.osc",
                pi_dir + "PI1000k-02_10C_FS_PP10.osc",
                pi_dir + "PI1000k-02_20C_FS_PP10.osc",
                pi_dir + "PI1000k-02_30C_FS3_PP10.osc",
                pi_dir + "PI1000k-02_30C_FS6_PP10.osc",
                pi_dir + "PI1000k-02_50C_FS_PP10.osc",
                pi_dir + "PI14k-02_-10C_FS2_PP-10.osc",
                pi_dir + "PI14k-02_-10C_FS_PP-10.osc",
                pi_dir + "PI14k-02_-20C_FS_PP-10.osc",
                pi_dir + "PI14k-02_-30C_FS_PP-10.osc",
                pi_dir + "PI14k-02_-40C_FS_PP-10.osc",
                pi_dir + "PI14k-02_0C_FS_PP-10.osc",
                pi_dir + "PI223k-14b_0C_FS4_PP10.osc",
                pi_dir + "PI223k-14b_25C_FS3_PP10.osc",
                pi_dir + "PI223k-14c_-20C_FS_PP10.osc",
                pi_dir + "PI223k-14c_-30C_FS_PP10.osc",
                pi_dir + "PI223k-14c_-40C_FS_PP10.osc",
                pi_dir + "PI223k-14c_-45C_FS2_PP10.osc",
                pi_dir + "PI223k-14c_30C_FS3_PP10.osc",
                pi_dir + "PI223k-14_-10C_FS_PP10.osc", 
                pi_dir + "PI223k-14_10C_FS_PP10.osc",
                pi_dir + "PI223k-14_25C_FS3_PP10.osc",
                pi_dir + "PI223k-14_40C_FS_PP10.osc",
                pi_dir + "PI223k-14_50C_FS_PP10.osc",
                pi_dir + "PI26k-16_FS_-10C_PP10.osc",
                pi_dir + "PI26k-16_FS_-20C_PP10.osc",
                pi_dir + "PI26k-16_FS_-30C_PP10.osc",
                pi_dir + "PI26k-16_FS_-40C_PP10.osc",
                pi_dir + "PI26k-16_FS_0C_PP10.osc",
                pi_dir + "PI2K-30d.osc",
                pi_dir + "PI2K-40d.osc",
                pi_dir + "PI2K-45d.osc",
                pi_dir + "PI2K-50d.osc",
                pi_dir + "PI2K-55d.osc",
                pi_dir + "PI2K-60d.osc",
                pi_dir + "PI33K-8_-10C_FS_PP10.osc",
                pi_dir + "PI33K-8_-20C_FS_PP10.osc",
                pi_dir + "PI33K-8_-30C_FS_PP10.osc",
                pi_dir + "PI33K-8_-40C_FS_PP10.osc",
                pi_dir + "PI33K-8_0C_FS_PP10.osc",
                pi_dir + "PI400k-03_-10C_FS_PP10.osc",
                pi_dir + "PI400k-03_-20C_FS_PP10.osc",
                pi_dir + "PI400k-03_-30C_FS2_PP10.osc",
                pi_dir + "PI400k-03_-40C_FS_PP10.osc",
                pi_dir + "PI400k-03_0C_FS_PP10.osc",
                pi_dir + "PI400k-03_15C_FS_PP10.osc",
                pi_dir + "PI400k-03_30C_FS2_PP10.osc",
                pi_dir + "PI400k-03_30C_FS_PP10.osc",
                pi_dir + "PI400k-03_50C_FS_PP10.osc",
                pi_dir + "PI4k-02_-30C_FS_PP10.osc",
                pi_dir + "PI4k-02_-40C_FS_PP10.osc",
                pi_dir + "PI4k-02_-45C_FS_PP10.osc",
                pi_dir + "PI600k_-10C_02b.osc",
                pi_dir + "PI600k_-20C_02b.osc",
                pi_dir + "PI600k_-30C_02b.osc",
                pi_dir + "PI600k_-40C_02bn.osc",
                pi_dir + "PI600k_0C_02bn.osc",
                pi_dir + "PI600k_100C_02bn.osc",
                pi_dir + "PI600k_30C_02b.osc",
                pi_dir + "PI600k_60C_02bn.osc",
                pi_dir + "PI600k_80C_02bn.osc",
                pi_dir + "PI88K-09_FS_-10C_PP-10.osc",
                pi_dir + "PI88K-09_FS_-20C_PP-10.osc",
                pi_dir + "PI88K-09_FS_-30C_PP-10.osc",
                pi_dir + "PI88K-09_FS_-40C_PP-10.osc",
                pi_dir + "PI88K-09_FS_-45C_PP-10.osc",
                pi_dir + "PI88K-09_FS_0C_PP-10.osc",
                pi_dir + "PI88K-09_FS_10C_PP-10.osc",
                pi_dir + "PI88K-09_FS_25C_PP-10.osc",
            ])

    thisSet = thisApp.datasets["Set1"]
    thisSet.new_theory("WLF Shift")
    thisTheory = thisSet.theories["WLFS1"]
    thisSet.handle_actionMinimize_Error()
    # for k in thisTheory.parameters:
    #     print(k, thisTheory.parameters[k].value)
    Tr = thisTheory.parameters["Tr"].value
    B1 = thisTheory.parameters["B1"].value
    B2 = thisTheory.parameters["B2"].value
    logalpha = thisTheory.parameters["logalpha"].value
    CTg = thisTheory.parameters["CTg"].value
    assert Tr == pytest.approx(25.0, rel=1e-4)
    assert B1 == pytest.approx(687.1391729545388, rel=1e-4)
    assert B2 == pytest.approx(114.04916569491438, rel=1e-4)
    assert logalpha == pytest.approx(-3.2147, rel=1e-4)
    assert CTg == pytest.approx(14.65, rel=1e-4)

def test_SANS_Debye():
    ex.handle_new_app("SANS")
    pi_dir = "data%sPS_SANS%s" % ((os.sep,) * 2)
    thisApp = ex.applications["SANS9"]
    thisApp.new_tables_from_files([
                pi_dir + "100k.sans",
                pi_dir + "250k.sans",
                pi_dir + "400k.sans",
            ])
    thisSet = thisApp.datasets["Set1"]
    thisSet.new_theory("Debye")
    thisTheory = thisSet.theories["D1"]
    thisSet.handle_actionMinimize_Error()
    # for k in thisTheory.parameters:
    #     print(k, thisTheory.parameters[k].value)
    Contrast = thisTheory.parameters["Contrast"].value
    C_gyr = thisTheory.parameters["C_gyr"].value
    M_mono = thisTheory.parameters["M_mono"].value
    Bckgrnd = thisTheory.parameters["Bckgrnd"].value
    Chi = thisTheory.parameters["Chi"].value
    Lambda = thisTheory.parameters["Lambda"].value
    assert Contrast == pytest.approx(0.4203, rel=1e-4)
    assert C_gyr == pytest.approx(62.3, rel=1e-4)
    assert M_mono == pytest.approx(0.104, rel=1e-4)
    assert Bckgrnd == pytest.approx(0.25621173254972934, rel=1e-4)
    assert Chi == pytest.approx(0.0001, rel=1e-4)
    assert Lambda == pytest.approx(1.0, rel=1e-4)


if __name__ == "__main__":
    test_LVE_Likhtman_McLeish()
    test_LVE_Maxwell_Modes()
    test_LVE_DTD_Stars()
    test_LVE_ReSpect()
    test_MWD_Discretize_MWD()
    test_MWD_GEX()
    test_MWD_LogNormal()
    test_TTS_WLF()
    test_SANS_Debye()
