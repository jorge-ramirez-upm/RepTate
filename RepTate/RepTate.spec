# -*- mode: python -*-

block_cipher = None


a = Analysis(['RepTate.py'],
             pathex=['applications', 'core', 'theories', 'tools', 'gui', 'c:\\Users\\Jorge\\OneDrive\\Codes\\Python\\RepTate\\RepTate'],
             binaries=[('c:\\Miniconda3\\pkgs\\mkl-2017.0.3-0\\Library\\bin\\mkl_def.dll', 'BINARY')],
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
