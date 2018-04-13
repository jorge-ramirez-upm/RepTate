echo off
rem Then CREATE CL Version
rmdir /s /q build\RepTateCL
rmdir /s /q dist\RepTateCL
pyinstaller -d -i gui\Images\Reptate64.ico --hidden-import=packaging --hidden-import=packaging.version --hidden-import=packaging.specifiers --hidden-import=packaging.requirements --hidden-import=scipy._lib.messagestream --hidden-import=pandas._libs.tslibs.timedeltas -p applications;core;theories;tools;gui RepTateCL.py
copy gui\theorytab.ui dist\RepTate
copy gui\DataSet.ui dist\RepTate
copy gui\QApplicationWindow.ui dist\RepTate
copy theories\*win32.so dist\RepTate
mkdir dist\RepTate\data
xcopy data dist\RepTate\data /E
mkdir dist\RepTateCL\theories
copy theories\linlin.npz dist\RepTateCL\theories
mkdir dist\RepTateCL\tests
xcopy tests dist\RepTateCL\tests /E
mkdir dist\RepTateCL\platforms
copy dist\RepTateCL\PyQt5\Qt\plugins\platforms\* dist\RepTateCL\platforms 
