@echo off
setlocal

rem Conservative typed-test validation for RepTate.

set "PYTHON=C:\WPy64-31131\python-3.11.3.amd64\python.exe"

"%PYTHON%" -m pyright tests

exit /b %ERRORLEVEL%
