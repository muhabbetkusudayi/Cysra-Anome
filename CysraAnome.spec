from PyInstaller.utils.hooks import collect_submodules, collect_data_files
import os

block_cipher = None
project_dir = os.getcwd()

hiddenimports = (
    collect_submodules("PyQt5") +
    collect_submodules("PyQt5.QtWebEngineWidgets") +
    collect_submodules("PyQt5.QtWebEngineCore") +
    collect_submodules("PyQt5.QtWebChannel")
)

datas = []
for root, dirs, files in os.walk(project_dir):
    for file in files:
        if "venv" in root or "__pycache__" in root or ".git" in root:
            continue
        full_path = os.path.join(root, file)
        rel_path = os.path.relpath(root, project_dir)
        datas.append((full_path, rel_path))

datas += collect_data_files("PyQt5", include_py_files=False)
datas += collect_data_files("PyQt5.QtWebEngineCore")

a = Analysis(
    ["cysrabrowser.py"],
    pathex=[project_dir],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
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
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name="CysraAnome",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico'
)