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
  RepTate/core/CmdBase.py ^
  RepTate/core/typing.py ^
  RepTate/core/__init__.py ^
  RepTate/core/MultiView.py ^
  RepTate/core/DraggableArtists.py ^
  RepTate/tools/ToolResampleData.py ^
  RepTate/tools/polymer_data.py ^
  RepTate/tools/ToolGradient.py ^
  RepTate/tools/ToolIntegral.py ^
  RepTate/tools/ToolInterpolate.py ^
  RepTate/tools/ToolEvaluate.py ^
  RepTate/tools/__init__.py ^
  RepTate/tools/get_palettes.py ^
  RepTate/tools/readlinlin.py ^
  RepTate/tools/ToolTemplate.py ^
  RepTate/tools/ToolPowerLaw.py ^
  RepTate/tools/ToolSmooth.py ^
  RepTate/tools/ToolBounds.py ^
  RepTate/tools/linlin2npz.py ^
  RepTate/tools/ReadMaterialsDataBaseFile.py ^
  RepTate/tools/CreateMaterialsDatabaseFile.py ^
  RepTate/tools/standard_pyQt5_icons.py ^
  RepTate/tools/ToolFindPeaks.py ^
  RepTate/tools/ToolMaterialsDatabase.py ^
  RepTate/theories/theory_helpers.py ^
  RepTate/theories/GOpolySTRAND_initialGuess.py ^
  RepTate/theories/timeArraySplit.py ^
  RepTate/theories/__init__.py ^
  RepTate/theories/kww_ctypes_helper.py ^
  RepTate/theories/schwarzl_ctypes_helper.py ^
  RepTate/theories/dtd_ctypes_helper.py ^
  RepTate/theories/goLandscape_ctypes_helper.py ^
  RepTate/theories/rouse_ctypes_helper.py ^
  RepTate/theories/BobCtypesHelper.py ^
  RepTate/theories/react_ctypes_helper.py ^
  RepTate/theories/rp_blend_ctypes_helper.py ^
  RepTate/theories/sccr_ctypes_helper.py ^
  RepTate/theories/SchneiderRate.py ^
  RepTate/theories/QuiescentSmoothStrand.py ^
  RepTate/theories/SmoothPolySTRAND.py ^
  RepTate/theories/TheoryTemplate.py ^
  RepTate/theories/TheoryBasic.py ^
  RepTate/theories/TheoryArrhenius.py ^
  RepTate/theories/TheoryCarreauYasuda.py ^
  RepTate/theories/TheoryDebye.py ^
  RepTate/theories/TheoryGEX.py ^
  RepTate/theories/TheoryLogNormal.py ^
  RepTate/theories/TheoryUCM.py ^
  RepTate/theories/TheoryWLF.py ^
  RepTate/theories/TheoryDebyeModes.py ^
  RepTate/theories/TheoryMaxwellModes.py ^
  RepTate/theories/TheoryRetardationModes.py ^
  RepTate/theories/TheoryKWWModes.py ^
  RepTate/theories/TheoryShanbhagMaxwellModes.py ^
  RepTate/theories/TheoryTTS.py ^
  RepTate/theories/TheoryTTS_Automatic.py ^
  RepTate/theories/TheoryDiscrMWD.py ^
  RepTate/theories/TheoryPETS.py

exit /b %ERRORLEVEL%
