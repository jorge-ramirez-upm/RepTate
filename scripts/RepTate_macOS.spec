# -*- mode: python -*-
# Create RepTate distribution with
# pyinstaller RepTate.spec

block_cipher = None

import sys
sys.path.append('../')
# sys.path.append('core')
# sys.path.append('gui')
# sys.path.append('console')
# sys.path.append('applications')
# sys.path.append('theories')
# sys.path.append('tools')

a = Analysis(['../RepTate/__main__.py'],
             pathex=[
                 "RepTate/"
             ],
             binaries=[('../RepTate/theories/*darwin.so', '.'),
                    #    ('RepTate/theories/kww_lib_darwin.so', '.'),
                    #    ('RepTate/theories/rouse_lib_darwin.so', '.'),
                    #    ('RepTate/theories/bob2p5_lib_darwin.so', '.'),
                    #    ('RepTate/theories/rp_blend_lib_darwin.so', '.'),
                    #    ('RepTate/theories/dtd_lib_darwin.so', '.'),
                    #    ('RepTate/theories/schwarzl_lib_darwin.so', '.'),
                    #    ('RepTate/theories/react_lib_darwin.so', '.'),
                    #    ('RepTate/theories/sccr_lib_darwin.so', '.')
                       ],
             datas=[('../docs/build/', 'docs/build/'),
                    ('../RepTate/gui/*.ui', '.'),
                    ('../RepTate/gui/*_rc.py', '.'),
                    ('../RepTate/tools/polymer_data.py', '.'),
                    ('../RepTate/tools/user_database.npy', '.'),
                    ('../RepTate/tools/materials_database.npy', '.'),
                    # ('RepTate/gui/import_excel_dialog.ui', '.'),
                    # ('RepTate/gui/annotationedit.ui', '.'),
                    # ('RepTate/gui/MaterialsDatabase.ui', '.'),
                    # ('RepTate/gui/tooltab.ui', '.'),
                    # ('RepTate/gui/Tool_rc.py', '.'),
                    # ('RepTate/gui/dummyfilesDialog.ui', '.'),
                    # ('RepTate/gui/theorytab.ui', '.'),
                    # ('RepTate/gui/DataSet.ui', '.'),
                    ('../RepTate/gui/Theory_rc.py', '.'),
                    ('../RepTate/gui/MainWindow_rc.py', '.'), 
                    ('../data/', 'data/'),
                    ('../RepTate/theories/linlin.npz', '.'),
                    ('../RepTate/gui/Images/logo.png', 'gui/Images/')],
             hiddenimports=[
                 'packaging', 'packaging.version', 'packaging.specifiers',
                 'packaging.requirements', 'scipy', 'scipy._lib.messagestream',
                 'pandas', 'pandas._libs.tslibs.timedeltas', 'pkg_resources.py2_warn'
             ],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='RepTate',
          debug=False,
          strip=False,
          upx=True,
          console=False,
          icon='../RepTate/gui/Images/RepTate_logo_new.icns')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='RepTate')
app = BUNDLE(coll,
             name='RepTate.app',
             version="1.0.0",
             licence="GPL v3+",
             author="Jorge Ramirez, Victor Boudara",
             icon='../RepTate/gui/Images/RepTate_logo_new.icns',
             bundle_identifier=None,
             info_plist={'NSHighResolutionCapable': 'True'})
