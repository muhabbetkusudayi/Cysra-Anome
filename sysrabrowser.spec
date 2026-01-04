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
        full_path = os.path.join(root, file)
        rel_path = os.path.relpath(root, project_dir)
        datas.append((full_path, rel_path))

datas += collect_data_files("PyQt5", include_py_files=False)
datas += collect_data_files("PyQt5.QtWebEngineCore")

a = Analysis(
    ["sysrabrowser.py"],
    pathex=[project_dir],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="SysraBrowser",
    debug=False,
    strip=False,
    upx=True,
    console=False
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    name="SysraBrowser"
)
