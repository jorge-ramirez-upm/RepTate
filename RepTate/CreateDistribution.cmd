echo off
rem CREATE GUI Version First
rem INSTALL PACKAGING "pip install packaging"
rmdir /s /q build\RepTate
rmdir /s /q dist\RepTate
rem ADAPT THE FOLLOWING LINE TO MATCH YOUR PYTHON DISTRIBUTION
set PATH=%PATH%;c:\WPy64-3741\python-3.7.4.amd64\Lib\site-packages\scipy\.libs\;
pyinstaller -w -i gui\Images\Reptate64.ico --hidden-import=packaging --hidden-import=packaging.version --hidden-import=packaging.specifiers --hidden-import=packaging.requirements --hidden-import=scipy._lib.messagestream --hidden-import=pandas._libs.tslibs.timedeltas -p applications;core;theories;tools;gui RepTate.py
mkdir dist\RepTate\gui
copy gui\theorytab.ui dist\RepTate
copy gui\tooltab.ui dist\RepTate
copy gui\DataSet.ui dist\RepTate
copy gui\Theory_rc.py dist\RepTate\gui
copy gui\QApplicationWindow.ui dist\RepTate
copy gui\AboutDialog.ui dist\RepTate
copy gui\About_rc.py dist\RepTate
copy gui\Tool_rc.py dist\RepTate
copy gui\ReptateMainWindow.ui dist\RepTate
copy gui\MainWindow_rc.py dist\RepTate
copy gui\annotationedit.ui dist\RepTate
copy gui\dummyfilesDialog.ui dist\RepTate
copy gui\import_excel_dialog.ui dist\RepTate
copy ..\Reptate_license.txt dist\RepTate

copy tools\materials_database.npy dist\RepTate
copy tools\user_database.npy dist\RepTate
copy tools\polymer_data.py dist\RepTate
rem copy c:\Miniconda3\Library\bin\mkl_def.dll dist\RepTate
mkdir dist\RepTate\data
xcopy data dist\RepTate\data /E
mkdir dist\RepTate\theories
copy theories\linlin.npz dist\RepTate\theories
copy theories\linlin.npz dist\RepTate
copy theories\*win32.so dist\RepTate
mkdir dist\RepTate\gui\Images
copy gui\Images\logo.jpg dist\RepTate\gui\Images
mkdir dist\RepTate\platforms
copy dist\RepTate\PyQt5\Qt\plugins\platforms\* dist\RepTate\platforms 
mkdir dist\RepTate\tests
xcopy tests dist\RepTate\tests /E

rem Then CREATE CL Version
rmdir /s /q build\RepTateCL
rmdir /s /q dist\RepTateCL
pyinstaller -i gui\Images\Reptate64.ico --hidden-import=packaging --hidden-import=packaging.version --hidden-import=packaging.specifiers --hidden-import=packaging.requirements --hidden-import=scipy._lib.messagestream --hidden-import=pandas._libs.tslibs.timedeltas -p applications;core;theories;tools;gui RepTateCL.py
copy dist\RepTateCL\RepTateCL.exe dist\RepTate

rem Clean up build folders
rmdir /s /q build\RepTate
rmdir /s /q build\RepTateCL
rmdir /s /q dist\RepTateCL

for /f %%i in ('python tools\getreptateversion.py') do set version=%%i
cd dist
c:\Progra~1\7-zip\7z.exe a RepTate%version%.zip RepTate
cd ..
