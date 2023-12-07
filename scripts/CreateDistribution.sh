#!/bin/bash
# Need pyinstaller
# pip install pyinstaller
# CREATE CLEAN PYTHON ENVIRONMENT
# NEED MODULES pyqt pint (from unidata) matplotlib scipy tabulate (from conda-forge) seaborn 
# NEED MODULES packaging 
#line pint seaborn tabulate pyqt5 pyinstaller packaging certifi

# CREATE GUI Version First
rm -rf build/RepTate
rm -rf dist/RepTate
# ADD -w FLAG TO MAKE A WINDOWS APPLICATION WITH NO TERMINAL
pyinstaller -w -i gui\Images\Reptate64.ico --hidden-import=packaging --hidden-import=packaging.version --hidden-import=packaging.specifiers --hidden-import=packaging.requirements --hidden-import=scipy._lib.messagestream --hidden-import=pandas._libs.tslibs.timedeltas -p applications -p core -p theories -p tools -p gui RepTate.py
mkdir dist/RepTate/gui
cp gui/theorytab.ui dist/RepTate
cp gui/DataSet.ui dist/RepTate
cp gui/Theory_rc.py dist/RepTate/gui
cp gui/QApplicationWindow.ui dist/RepTate
cp gui/AboutDialog.ui dist/RepTate
cp gui/About_rc.py dist/RepTate
cp gui/ReptateMainWindow.ui dist/RepTate
cp gui/import_excel_dialog.ui dist/RepTate
cp gui/MainWindow_rc.py dist/RepTate
cp /home/jramirez/miniconda3/lib/libiomp5.so dist/RepTate
mkdir dist/RepTate/data
cp -r data/* dist/RepTate/data 
mkdir dist/RepTate/theories
cp theories/linlin.npz dist/RepTate/theories
cp theories/*so dist/RepTate
mkdir -p dist/RepTate/gui/Images
cp gui/Images/logo.jpg dist/RepTate/gui/Images


mkdir dist/RepTate/tests
cp -r tests/* dist/RepTate/tests 

# Clean up build folders
rm -rf build/RepTate

version=`python tools/getreptateversion.py`
cd dist
zip -r RepTate$version\_Linux.zip RepTate
cd ..

