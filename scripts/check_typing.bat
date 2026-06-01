@echo off
setlocal

call scripts\check_typed_subset.bat
if errorlevel 1 exit /b %ERRORLEVEL%

call scripts\check_typed_tests.bat
if errorlevel 1 exit /b %ERRORLEVEL%

exit /b 0
