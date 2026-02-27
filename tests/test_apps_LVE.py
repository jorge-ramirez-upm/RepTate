
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
    assert logG00 == pytest.approx(-9.98121345866038, rel=1e-4)
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


if __name__ == "__main__":
    test_LVE_Likhtman_McLeish()
    test_LVE_Maxwell_Modes()
    test_LVE_DTD_Stars()
    test_LVE_ReSpect()