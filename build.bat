@echo off
echo =========================
echo   Building Cysra Anome
echo =========================

python -m pip install --upgrade pip
python -m pip install pyinstaller pyqt5 pyqtwebengine

python -m PyInstaller CysraAnome.spec --clean --noconfirm

echo =========================
echo Build completed!
echo =========================
pause
