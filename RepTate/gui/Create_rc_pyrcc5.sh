#!/bin/bash
pyrcc5 Reptate.qrc -o Reptate_rc.py
pyrcc5 About.qrc -o About_rc.py
pyrcc5 Theory.qrc -o Theory_rc.py
pyrcc5 Tool.qrc -o Tool_rc.py
pyrcc5 MainWindow.qrc -o MainWindow_rc.py
pyuic5 markerSettings.ui -o markerSettings.py
pyuic5 fittingoptions.ui -o fittingoptions.py
pyuic5 errorcalculationoptions.ui -o errorcalculationoptions.py
