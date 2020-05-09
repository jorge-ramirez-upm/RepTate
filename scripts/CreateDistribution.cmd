echo off
rem ################################################
rem RECOMMENDED: Install WinPython64-3.7.4.1Zero.exe
rem Either install from scratch or create an empty environment
rem REPTATE REQUIRED PACKAGES: pip install numpy pyreadline PyQt5 matplotlib scipy openpyxl xlrd psutil colorama
rem INSTALL PACKAGING "pip install packaging"
rem INSTALL PYINSTALLER "pip install pyinstaller"
rmdir /s /q build\RepTate
rmdir /s /q dist\RepTate
rem ADAPT THE FOLLOWING LINE TO MATCH YOUR PYTHON DISTRIBUTION
rem set PATH=%PATH%;c:\Users\Jorge\Downloads\WPy64-3741\\python-3.7.4.amd64\Lib\site-packages\scipy\.libs\;
rem TO DEBUG THE CREATION OF THE INSTALLER ADD FLAGS: -d all
rem ########################
rem CREATE GUI Version First
pyinstaller -w -i RepTate\gui\Images\Reptate64.ico --hidden-import=packaging --hidden-import=packaging.version --hidden-import=packaging.specifiers --hidden-import=packaging.requirements --hidden-import=scipy._lib.messagestream --hidden-import=pandas._libs.tslibs.timedeltas --name=RepTate RepTate\__main__.py 
REM -p RepTate\applications;core;theories;tools;gui 
mkdir dist\RepTate\RepTate\gui
copy RepTate\gui\theorytab.ui dist\RepTate\RepTate\gui
copy RepTate\gui\tooltab.ui dist\RepTate\RepTate\gui
copy RepTate\gui\DataSet.ui dist\RepTate\RepTate\gui
copy RepTate\gui\Theory_rc.py dist\RepTate\RepTate\gui
copy RepTate\gui\RepTate_rc.py dist\RepTate\RepTate\gui
copy RepTate\gui\QApplicationWindow.ui dist\RepTate\RepTate\gui
copy RepTate\gui\AboutDialog.ui dist\RepTate\RepTate\gui
copy RepTate\gui\About_rc.py dist\RepTate\RepTate\gui
copy RepTate\gui\Tool_rc.py dist\RepTate\RepTate\gui
copy RepTate\gui\ReptateMainWindow.ui dist\RepTate\RepTate\gui
copy RepTate\gui\MainWindow_rc.py dist\RepTate\RepTate\gui
copy RepTate\gui\annotationedit.ui dist\RepTate\RepTate\gui
copy RepTate\gui\dummyfilesDialog.ui dist\RepTate\RepTate\gui
copy RepTate\gui\import_excel_dialog.ui dist\RepTate\RepTate\gui
copy RepTate\dist\RepTate\Qt5Core.dll dist\RepTate\PyQt5\Qt\bin\Qt5Core.dll 
copy Reptate_license.txt dist\RepTate
copy Reptate_license.rtf dist\RepTate

mkdir dist\RepTate\RepTate\tools
copy RepTate\tools\materials_database.npy dist\RepTate\RepTate\tools
copy RepTate\tools\user_database.npy dist\RepTate\RepTate\tools
copy RepTate\tools\polymer_data.py dist\RepTate\RepTate\tools
rem copy c:\Miniconda3\Library\bin\mkl_def.dll dist\RepTate
mkdir dist\RepTate\data
xcopy data dist\RepTate\data /E
mkdir dist\RepTate\RepTate\theories
copy RepTate\theories\linlin.npz dist\RepTate\RepTate\theories
REM copy RepTate\theories\linlin.npz dist\RepTate
copy RepTate\theories\*win32.so dist\RepTate\RepTate\theories
mkdir dist\RepTate\RepTate\gui\Images
copy RepTate\gui\Images\logo_with_uni_logo.png dist\RepTate\RepTate\gui\Images
copy RepTate\gui\Images\RepTate_logo_100.png dist\RepTate\RepTate\gui\Images
copy RepTate\gui\Images\Reptate64.ico dist\RepTate\RepTate\gui\Images
copy RepTate\gui\Images\new_icons\*.ico dist\RepTate\RepTate\gui\Images

mkdir dist\RepTate\platforms
copy dist\RepTate\PyQt5\Qt\plugins\platforms\* dist\RepTate\platforms 
mkdir dist\RepTate\tests\output
copy tests\*.* dist\RepTate\tests

mkdir dist\RepTate\docs\build\html
xcopy docs\build\html dist\RepTate\docs\build\html /E

rem ########################
rem Then CREATE CL Version
rmdir /s /q build\RepTateCL
rmdir /s /q dist\RepTateCL
rem TO DEBUG THE CREATION OF THE INSTALLER ADD FLAGS: -d all
pyinstaller -i RepTate\gui\Images\Reptate64.ico --hidden-import=packaging --hidden-import=packaging.version --hidden-import=packaging.specifiers --hidden-import=packaging.requirements --hidden-import=scipy._lib.messagestream --hidden-import=pandas._libs.tslibs.timedeltas --name=RepTateCL RepTate\CL.py
REM -p applications;core;theories;tools;gui 
copy dist\RepTateCL\RepTateCL.exe dist\RepTate

rem Clean up build folders
rmdir /s /q build\RepTate
rmdir /s /q build\RepTateCL
rmdir /s /q dist\RepTateCL

rem Create ZIP (portable package)
for /f %%i in ('python RepTate\core\Version.py') do set version=%%i
cd dist
c:\Progra~1\7-zip\7z.exe a RepTate%version%.zip RepTate
cd ..

rem Run NSIS to create installation package
C:\Progra~2\NSIS\makensis.exe dist\RepTate.nsi

