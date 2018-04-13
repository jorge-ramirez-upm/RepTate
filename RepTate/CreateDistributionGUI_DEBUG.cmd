rmdir /s /q build\RepTate
rmdir /s /q dist\RepTate
pyinstaller -d -i gui\Images\Reptate64.ico --hidden-import=packaging --hidden-import=packaging.version --hidden-import=packaging.specifiers --hidden-import=packaging.requirements --hidden-import=scipy._lib.messagestream --hidden-import=pandas._libs.tslibs.timedeltas -p applications;core;theories;tools;gui RepTate.py
mkdir dist\RepTate\gui
copy gui\theorytab.ui dist\RepTate
copy gui\DataSet.ui dist\RepTate
copy gui\Theory_rc.py dist\RepTate\gui
copy gui\QApplicationWindow.ui dist\RepTate
copy gui\AboutDialog.ui dist\RepTate
copy gui\About_rc.py dist\RepTate
copy gui\ReptateMainWindow.ui dist\RepTate
copy gui\MainWindow_rc.py dist\RepTate
copy c:\Miniconda3\Library\bin\mkl_def.dll dist\RepTate
mkdir dist\RepTate\data
xcopy data dist\RepTate\data /E
mkdir dist\RepTate\theories
copy theories\linlin.npz dist\RepTate\theories
copy theories\*win32.so dist\RepTate
mkdir dist\RepTate\gui\Images
copy gui\Images\logo.jpg dist\RepTate\gui\Images
mkdir dist\RepTate\platforms
copy dist\RepTate\PyQt5\Qt\plugins\platforms\* dist\RepTate\platforms 
