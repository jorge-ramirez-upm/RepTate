# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['RepTate.py'],
             pathex=['applications', 'core', 'theories', 'tools', 'gui', 'c:\\Users\\Jorge Ramirez\\OneDrive - Universidad Politécnica de Madrid\\Projects\\RepTate\\RepTate\\RepTate'],
             binaries=[],
             datas=[],
             hiddenimports=['packaging', 'packaging.version', 'packaging.specifiers', 'packaging.requirements', 'scipy._lib.messagestream', 'pandas._libs.tslibs.timedeltas'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='RepTate',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False , icon='gui\\Images\\Reptate64.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='RepTate')
