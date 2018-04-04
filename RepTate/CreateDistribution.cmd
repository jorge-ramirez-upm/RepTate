echo off
rem CREATE CLEAN PYTHON ENVIRONMENT
rem NEED MODULES matplotlib pyreadline pint seaborn tabulate pyqt5 pyinstaller packaging certifi

rem CREATE GUI Version First
rmdir /s /q build\RepTate
rmdir /s /q dist\RepTate
rem ADD -w FLAG TO MAKE A WINDOWS APPLICATION WITH NO TERMINAL
rem pyinstaller -i gui\Images\Reptate64.ico --hidden-import=packaging --hidden-import=packaging.version --hidden-import=packaging.specifiers --hidden-import=packaging.requirements -p applications;core;theories;tools;gui RepTate.py
pyinstaller -w -i gui\Images\Reptate64.ico --hidden-import=packaging --hidden-import=packaging.version --hidden-import=packaging.specifiers --hidden-import=packaging.requirements -p applications;core;theories;tools;gui RepTate.py
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
rem exit /b


rem Then CREATE CL Version
rmdir /s /q build\RepTateCL
rmdir /s /q dist\RepTateCL
pyinstaller -i gui\Images\Reptate64.ico --hidden-import=packaging --hidden-import=packaging.version --hidden-import=packaging.specifiers --hidden-import=packaging.requirements -p applications;core;theories;tools;gui RepTateCL.py
copy dist\RepTateCL\RepTateCL.exe dist\RepTate
mkdir dist\RepTate\tests
xcopy tests dist\RepTate\tests /E

rem Clean up build folders
rmdir /s /q build\RepTate
rmdir /s /q build\RepTateCL
rmdir /s /q dist\RepTateCL

for /f %%i in ('python tools\getreptateversion.py') do set version=%%i
cd dist
c:\Progra~1\7-zip\7z.exe a RepTate%version%.zip RepTate
cd ..
