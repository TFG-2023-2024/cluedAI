# main.spec

# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['cluedAI/main.py'],
    pathex=['cluedAI'],
    binaries=[        
        ('cluedAI/mongodb/bin/mongod.exe', 'mongodb/bin'),
        ('cluedAI/mongodb/bin/mongos.exe', 'mongodb/bin'),
        ('cluedAI/mongodb/bin/vc_redist.x64.exe', 'mongodb/bin')],
    datas=[
        ('cluedAI/db/', 'db'),
        ('cluedAI/mongodb/', 'mongodb'),
        ('cluedAI/characters/', 'characters'),
        ('cluedAI/initial_gui/', 'initial_gui'),
        ('cluedAI/users/', 'users'),
        ('build/', 'build'),
        ('.env', '.env'),
        ('cluedAI/README.md', 'README.md')
    ],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='cluedAI',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='cluedAI',
)
