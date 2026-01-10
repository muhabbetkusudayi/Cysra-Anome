@echo off
echo =========================
echo   Building SysraBrowser
echo =========================

python -m pip install --upgrade pip
python -m pip install pyinstaller pyqt5 pyqtwebengine

python -m PyInstaller SysraBrowser.spec --clean --noconfirm

echo =========================
echo Build completed!
echo =========================
pause
