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
    a.binaries, # add
    a.datas, # add
    [],
    # exclude_binaries=True,
    name='mekakushi',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[], # add
    runtime_tmpdir=None, # add
    console=False, # True -> False
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
