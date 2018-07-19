# -*- mode: python -*-
# Create RepTate distribution with
# pyinstaller RepTate.spec

block_cipher = None


a = Analysis(['RepTate.py'],
             pathex=['applications', 'core', 'theories', 'tools', 'gui', '/Users/mmvahb/Documents/vahb/Repate/RepTate/RepTate'],
             binaries=[('theories/kww_lib_darwin.so', '.'), ('theories/rouse_lib_darwin.so', '.'), ('theories/bob2p5_lib_darwin.so', '.'), ('theories/rp_blend_lib_darwin.so', '.'), ('theories/dtd_lib_darwin.so', '.'), ('theories/schwarzl_lib_darwin.so', '.'), ('theories/react_lib_darwin.so', '.')],
             datas=[('tools/polymer_data.py', '.'), ('tools/user_database.npy', '.'), ('tools/materials_database.npy', '.'), ('gui/annotationedit.ui', '.'), ('gui/MaterialsDatabase.ui', '.'), ('gui/tooltab.ui', '.'), ('gui/Tool_rc.py', '.'), ('gui/dummyfilesDialog.ui', '.'), ('gui/theorytab.ui', '.'), ('gui/DataSet.ui', '.'), ('gui/Theory_rc.py', 'gui/'), ('gui/QApplicationWindow.ui', '.'), ('gui/AboutDialog.ui', '.'), ('gui/About_rc.py', '.'), ('gui/ReptateMainWindow.ui', '.'), ('gui/MainWindow_rc.py', '.'), ('data/', 'data/'), ('theories/linlin.npz', '.'), ('gui/Images/logo.png', 'gui/Images/')],
             hiddenimports=['packaging', 'packaging.version', 'packaging.specifiers', 'packaging.requirements', 'scipy', 'scipy._lib.messagestream', 'pandas', 'pandas._libs.tslibs.timedeltas'],
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
          console=False , icon='gui/Images/RepTate_logo_new.icns')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='RepTate')
app = BUNDLE(coll,
             name='RepTate.app',
             icon='gui/Images/RepTate_logo_new.icns',
             bundle_identifier=None,
             info_plist={
             'NSHighResolutionCapable': 'True'
             })
