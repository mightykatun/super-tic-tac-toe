# run the compiler in the main.py parent directory

import os
specpath = os.path.dirname(os.path.abspath(SPEC))

block_cipher = None

a = Analysis(["main.py"],
         pathex=[],
         binaries=[],
         datas=[],
         hiddenimports=[],
         hookspath=[],
         runtime_hooks=[],
         excludes=[],
         win_no_prefer_redirects=False,
         win_private_assemblies=False,
         cipher=block_cipher)

a.datas += [("pixelmix_micro.ttf","pixelmix_micro.ttf", "DATA")]
a.datas += [("icon.ico","icon.ico", "DATA")]

pyz = PYZ(a.pure, a.zipped_data,
         cipher=block_cipher)

exe = EXE(pyz,
      a.scripts,
      a.binaries,
      a.zipfiles,
      a.datas,
      name="Super Tic Tac Toe",
      icon=os.path.join(specpath, "icon.ico"),
      debug=False,
      strip=False,
      upx=True,
      console=False)