@echo off
setlocal

cd /d "%~dp0.."

python -m pip install --upgrade pyinstaller
if errorlevel 1 (
    echo.
    echo Failed to install or upgrade PyInstaller.
    pause
    exit /b 1
)

python -m PyInstaller --onefile ^
  --icon=src\warframe.ico ^
  --add-data "src\warframe.ico;." ^
  --collect-all plyer ^
  --hidden-import=plyer.platforms.win.notification ^
  --hidden-import=plyer.platforms.win ^
  --name YourWarframe ^
  src\app.py

if errorlevel 1 (
    echo.
    echo Build failed - check the output above.
    echo If it reports Access is denied, close all running YourWarframe.exe instances and retry.
    pause
    exit /b 1
)

if exist dist\YourWarframe.exe (
    echo.
    echo Build complete: dist\YourWarframe.exe
) else (
    echo.
    echo Build failed - check the output above.
    pause
    exit /b 1
)

pause
cls