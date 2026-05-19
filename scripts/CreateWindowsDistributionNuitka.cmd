REM python -m pip install --upgrade pip
REM python -m pip install -r requirements.txt
REM python -m pip install -r docs/requirements.txt
REM python scripts/build_ui.py
REM python -m pip install -e .
REM python -m sphinx -b html docs/source docs/build/html
REM python -m pip install Nuitka
python -m nuitka ^
  --assume-yes-for-downloads ^
  --mode=standalone ^
  --enable-plugin=pyside6 ^
  --windows-console-mode=disable ^
  --output-dir=dist ^
  --windows-icon-from-ico=RepTate\gui\Images\Reptate64.ico ^
  --noinclude-qt-translations ^
  --include-package=RepTate.tools ^
  --include-module=RepTate.gui.Reptate_rc ^
  --include-module=RepTate.gui.About_rc ^
  --include-module=RepTate.gui.Theory_rc ^
  --include-module=RepTate.gui.Tool_rc ^
  --include-module=RepTate.gui.MainWindow_rc ^
  --include-package=RepTate.tools ^
  --include-data-dir=data=data ^
  --include-data-dir=RepTate\gui\Images=RepTate\gui\Images ^
  --include-data-files=RepTate\tools\*.npy=RepTate\tools\ ^
  --include-data-files=RepTate\theories\*.npz=RepTate\theories\ ^
  --include-data-files=RepTate\theories\*_win32*.so=RepTate\theories\ ^
  --python-flag=-m ^
  RepTate
  