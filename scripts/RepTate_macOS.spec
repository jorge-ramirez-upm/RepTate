# -*- mode: python -*-
# Create RepTate distribution with
# pyinstaller RepTate.spec

block_cipher = None

# import sys
import os

# sys.path.append("../")
# sys.path.append('core')
# sys.path.append('gui')
# sys.path.append('console')
# sys.path.append('applications')
# sys.path.append('theories')
# sys.path.append('tools')

a = Analysis(
    ["../RepTate/__main__.py"],
    pathex=["RepTate/"],
    binaries=[("../RepTate/theories/*darwin.so", ".")],
    datas=[
        ("../docs/build/", "docs/build/"),
        ("../RepTate/gui/*.ui", "."),
        ("../RepTate/gui/*_rc.py", "."),
        ("../RepTate/tools/polymer_data.py", "."),
        ("../RepTate/tools/user_database.npy", "."),
        ("../RepTate/tools/materials_database.npy", "."),
        ("../RepTate/gui/Theory_rc.py", "."),
        ("../RepTate/gui/MainWindow_rc.py", "."),
        ("../data/", "data/"),
        ("../RepTate/theories/linlin.npz", "."),
        ("../RepTate/gui/Images/logo.png", "gui/Images/"),
        ("../RepTate/gui/Images/RepTate_logo_new.icns", "."),
    ],
    hiddenimports=[
        "packaging",
        "packaging.version",
        "packaging.specifiers",
        "packaging.requirements",
        "scipy",
        "scipy._lib.messagestream",
        "pkg_resources.py2_warn",
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(
    pyz,
    a.scripts,
    exclude_binaries=True,
    name="RepTate",
    debug=False,
    strip=False,
    upx=True,
    console=False,
    icon="../RepTate/gui/Images/RepTate_logo_new.icns",
)
coll = COLLECT(
    exe, a.binaries, a.zipfiles, a.datas, strip=False, upx=True, name="RepTate"
)
app = BUNDLE(
    coll,
    name="RepTate.app",
    version="1.1.0",
    licence="GPL v3+",
    author="Jorge Ramirez, Victor Boudara",
    icon="../RepTate/gui/Images/RepTate_logo_new.icns",
    bundle_identifier=None,
    # info_plist={"NSHighResolutionCapable": "True", "NSPrincipalClass": "NSApplication"},
    info_plist={
        "NSHighResolutionCapable": "True",
        "NSPrincipalClass": "NSApplication",
        "NSAppleScriptEnabled": False,
        "CFBundleDocumentTypes": [
            {
                "CFBundleTypeName": "RepTate",
                "CFBundleTypeIconFile": "../RepTate/gui/Images/RepTate_logo_new.icns",
                "LSItemContentTypes": [".rept"],
                "LSHandlerRank": "Owner",
            }
        ],
    },
)