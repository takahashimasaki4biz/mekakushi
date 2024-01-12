# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['mekakushi.py'],
    pathex=['.venv/Lib/site-packages'], # [] -> ['.venv/Lib/site-packages']
    binaries=[],
    datas=[('assets/*','assets')], # [] -> [('assets/*','assets')]
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    # a.binaries,
    # a.datas,
    [],
    exclude_binaries=True, # add
    name='mekakushi',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    # upx_exclude=[],
    # runtime_tmpdir=None,
    console=False, # True -> False
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='mekakushi',
)
