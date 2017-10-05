*** Remove following line from c:\Miniconda3\Lib\site-packages\pyinstaller-3.2-py3.5.egg\PyInstaller\loader\rthooks.dat

'PyQt4': ['pyi_rth_qt4plugins.py'],

*** Compile using the following command:

pyinstaller --hidden-import=packaging --hidden-import=packaging.version --hidden-import=packaging.specifiers --hidden-import=packaging.requirements -p applications -p core -p theories -p tools -p gui RepTate.py

*** Copy files from gui folder into dist/Reptate folder
AboutDialog.ui
ReptateMainWindow.ui
About_rc.py
MainWindow_rc.py
(LOOK FOR ALTERNATIVE, LIKE COMPILING THE UI FILES AND IMPORTING THEM TO THE PROJECT)

*** Copy mkl_def.dll from miniconda distribution into dist/Reptate folder
(LOOK FOR ALTERNATIVE SOLUTION!)


OR JUST RUN:

pyinstaller Reptate.spec 

with Reptate.spec given by:

# -*- mode: python -*-

block_cipher = None


a = Analysis(['RepTate.py'],
             pathex=['applications', 'core', 'theories', 'tools', 'gui', 'c:\\Users\\Jorge\\OneDrive\\Codes\\Python\\RepTate\\RepTate'],
             binaries=['c:\\Miniconda3\\pkgs\\mkl-2017.0.3-0\\Library\\bin\\mkl_def.dll', 'gui\\AboutDialog.ui'', 'gui\\ReptateMainWindow.ui', 'gui\\About_rc.py', 'gui\\MainWindow_rc.py'],
             datas=None,
             hiddenimports=['packaging', 'packaging.version', 'packaging.specifiers', 'packaging.requirements'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='RepTate',
          debug=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='RepTate')
