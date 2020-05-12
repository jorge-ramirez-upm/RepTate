echo off 
REM CREATE TEMPORARY FOLDER
set BUILDFOLDER=build
set OUTPUTFOLDER=dist\RepTate
if not exist %BUILDFOLDER% mkdir %BUILDFOLDER%

REM GET PYTHON INSTALLATION FOLDER
(python -c "import sys; print(sys.exec_prefix)") > tmp.txt
set /P WINPYDIR=<tmp.txt

REM GET PYTHON VERSION
(python -c "import sys; print('.'.join(map(str, sys.version_info[:3])))") > tmp.txt
set /P PYTHONVERSION=<tmp.txt

REM GET REPTATE VERSION AND DATE
(python -c "import RepTate; v=RepTate._version.get_versions(); print(v['version'].split('+')[0])") > tmp.txt
set /P REPTATEVERSION=<tmp.txt
(python -c "import RepTate; v=RepTate._version.get_versions(); print(v['date'].split('T')[0])") > tmp.txt
set /P REPTATEDATE=<tmp.txt
(python -c "import RepTate; v=RepTate._version.get_versions(); print(v['version'])") > tmp.txt
set /P REPTATEBUILD=<tmp.txt
del tmp.txt

echo #####################################################################
echo Creating installation package on Windows for Python %PYTHONVERSION%
echo Python running on folder %WINPYDIR%
echo RepTate Version %REPTATEVERSION% %REPTATEDATE% (Build %REPTATEBUILD%)
echo #####################################################################

REM GET PYTHON (SET VERSION EQUAL TO CURRENT VERSION ON YOUR SYSTEM, WHERE REPTATE IS WORKING)
REM AND TRY TO GET IT TO BE THE SAME VERSION AS IN THE GITHUB SERVER
set PYTHONFILENAME=python-%PYTHONVERSION%-embed-amd64.zip
curl -s -f -L -o %BUILDFOLDER%\%PYTHONFILENAME% https://www.python.org/ftp/python/%PYTHONVERSION%/%PYTHONFILENAME%

REM CREATE WHEEL CORRESPONDING TO OUR APPLICATIOn
del %BUILDFOLDER%\*.whl
python setup.py bdist_wheel --dist-dir %BUILDFOLDER%

REM PACK ALL NEEDED FOLDERS AND FILES FOR TCL/TK
if not exist %OUTPUTFOLDER% mkdir %OUTPUTFOLDER%
if not exist %OUTPUTFOLDER%\tcl mkdir %OUTPUTFOLDER%\tcl
if not exist %OUTPUTFOLDER%\tkinter mkdir %OUTPUTFOLDER%\tkinter
xcopy /S %WINPYDIR%\tcl %OUTPUTFOLDER%\tcl
xcopy /S %WINPYDIR%\Lib\tkinter %OUTPUTFOLDER%\tkinter
copy %WINPYDIR%\DLLs\_tkinter.pyd %OUTPUTFOLDER%
copy %WINPYDIR%\DLLs\tcl86t.dll %OUTPUTFOLDER%
copy %WINPYDIR%\DLLs\tk86t.dll %OUTPUTFOLDER%

REM COPY OTHER FOLDERS AND FILES NEEDED BY REPTATE
if not exist %OUTPUTFOLDER%\data mkdir %OUTPUTFOLDER%\data
xcopy /S data %OUTPUTFOLDER%\data
REM COPY DOCUMENTATION OR NOT?
REM if not exist %OUTPUTFOLDER%\docs\build\html mkdir %OUTPUTFOLDER%\docs\build\html
REM xcopy /S docs\build\html %OUTPUTFOLDER%\docs\build\html
if not exist %OUTPUTFOLDER%\tests mkdir %OUTPUTFOLDER%\tests
xcopy /S tests %OUTPUTFOLDER%\tests
copy Reptate_license.txt %OUTPUTFOLDER%
copy Reptate_license.rtf %OUTPUTFOLDER%
REM COPY ICONS
if not exist %OUTPUTFOLDER%\icons mkdir %OUTPUTFOLDER%\icons
copy RepTate\gui\Images\Reptate64.ico %OUTPUTFOLDER%\icons
copy RepTate\gui\Images\new_icons\OSC.ico %OUTPUTFOLDER%\icons
copy RepTate\gui\Images\new_icons\LVE.ico %OUTPUTFOLDER%\icons
copy RepTate\gui\Images\new_icons\NLVE.ico %OUTPUTFOLDER%\icons
copy RepTate\gui\Images\new_icons\React.ico %OUTPUTFOLDER%\icons
copy RepTate\gui\Images\new_icons\MWD.ico %OUTPUTFOLDER%\icons
copy RepTate\gui\Images\new_icons\Gt.ico %OUTPUTFOLDER%\icons
copy RepTate\gui\Images\new_icons\SANS.ico %OUTPUTFOLDER%\icons
copy RepTate\gui\Images\new_icons\Dielectric.ico %OUTPUTFOLDER%\icons
copy RepTate\gui\Images\new_icons\Creep.ico %OUTPUTFOLDER%\icons
copy RepTate\gui\Images\new_icons\LAOS.ico %OUTPUTFOLDER%\icons
copy RepTate\gui\Images\Crystal.ico %OUTPUTFOLDER%\icons

REM UNPACK PYTHON IN THE INSTALLATION FOLDER
"C:\Program Files\7-Zip\7z.exe" x -aos -o"%OUTPUTFOLDER%" "%BUILDFOLDER%\%PYTHONFILENAME%"
copy %BUILDFOLDER%\*.whl %OUTPUTFOLDER%

cd %OUTPUTFOLDER%
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
echo. >> python37._pth
echo Lib/site-packages>> python37._pth
echo. >> python37._pth
python get-pip.py
del get-pip.py
python -m pip install -r ..\..\requirements.txt
for /f "delims=" %%a in ('dir /b *.whl') do python -m pip install %%a
del *.whl

REM ALTERNATIVE 1: BYTE COMPILE ALL AND LEAVE ORIGINAL FILES UNTOUCHED
REM python -c "import compileall; compileall.compile_dir('./', force=True)"

REM ALTERNATIVE 2: BYTE COMPILE EACH FILE AND SUBSTITUTE py BY pyc (about 50 Mb less)
cd Lib\site-packages
python ..\..\..\..\scripts\traverse.py
cd ..\..


REM INVOKE makensis
cd ..
makensis -DREPTATEVERSION=%REPTATEVERSION% -DREPTATEDATE=%REPTATEDATE% -DREPTATEBUILD=%REPTATEBUILD% RepTate.nsi 
cd ..