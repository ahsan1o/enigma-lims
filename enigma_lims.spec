# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec for Enigma LIMS Windows EXE
# Run: pyinstaller enigma_lims.spec

block_cipher = None

a = Analysis(
    ['launcher.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('backend', 'backend'),
        ('docs', 'docs'),
    ],
    hiddenimports=[
        # Uvicorn internals
        'uvicorn',
        'uvicorn.logging',
        'uvicorn.loops',
        'uvicorn.loops.auto',
        'uvicorn.loops.asyncio',
        'uvicorn.protocols',
        'uvicorn.protocols.http',
        'uvicorn.protocols.http.auto',
        'uvicorn.protocols.http.h11_impl',
        'uvicorn.protocols.websockets',
        'uvicorn.protocols.websockets.auto',
        'uvicorn.lifespan',
        'uvicorn.lifespan.on',
        # FastAPI / Starlette
        'fastapi',
        'fastapi.staticfiles',
        'starlette',
        'starlette.staticfiles',
        'starlette.middleware',
        'starlette.middleware.cors',
        # Pydantic
        'pydantic',
        'pydantic.v1',
        'pydantic_settings',
        'email_validator',
        # SQLAlchemy
        'sqlalchemy',
        'sqlalchemy.dialects.sqlite',
        'sqlalchemy.ext.declarative',
        # Auth
        'jose',
        'jose.jwt',
        'jose.exceptions',
        'bcrypt',
        'cryptography',
        # File handling
        'python_multipart',
        'multipart',
        # Reporting
        'reportlab',
        'fpdf',
        'barcode',
        # LIMS app modules
        'database',
        'models',
        'api.auth',
        'api.patients',
        'api.doctors',
        'api.samples',
        'api.tests',
        'api.orders',
        'api.results',
        'api.instruments',
        'api.users',
        'api.dashboard',
        'api.reports',
        'services',
        'utils',
        'utils.auth',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tkinter', 'test', 'unittest'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='EnigmaLIMS',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,   # Show console so users can see server status
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
    onefile=True,   # Single .exe file
)
