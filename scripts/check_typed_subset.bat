@echo off
setlocal

rem Conservative typed-subset validation for RepTate.
rem This is not a full-project strict type check.

set "PYTHON=C:\WPy64-31131\python-3.11.3.amd64\python.exe"

"%PYTHON%" -m pyright ^
  RepTate/gui/DataSetWidget.py ^
  RepTate/gui/DataSetWidgetItem.py ^
  RepTate/gui/SpreadsheetWidget.py ^
  RepTate/gui/ImportExcelWindow.py ^
  RepTate/gui/ImportFromPastedWindow.py ^
  RepTate/gui/QTool.py ^
  RepTate/gui/QTheory.py ^
  RepTate/gui/QApplicationWindow.py ^
  RepTate/gui/QDataSet.py ^
  RepTate/gui/QApplicationManager.py ^
  RepTate/gui/SplashScreen.py ^
  RepTate/gui/error_handling.py ^
  RepTate/gui/QAboutReptate.py ^
  RepTate/core/units.py ^
  RepTate/core/Parameter.py ^
  RepTate/core/File.py ^
  RepTate/core/FileType.py ^
  RepTate/core/View.py ^
  RepTate/core/DataTable.py ^
  RepTate/core/expression_parser.py ^
  RepTate/core/axis_labels.py ^
  RepTate/tools/ToolResampleData.py ^
  RepTate/tools/polymer_data.py ^
  RepTate/tools/ToolGradient.py ^
  RepTate/tools/ToolIntegral.py ^
  RepTate/tools/ToolInterpolate.py ^
  RepTate/tools/ToolEvaluate.py ^
  RepTate/theories/theory_helpers.py ^
  RepTate/theories/GOpolySTRAND_initialGuess.py

exit /b %ERRORLEVEL%
