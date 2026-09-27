@echo off
setlocal

cd /d "%~dp0.."

python -m pip install --upgrade pyinstaller

pyinstaller --onefile ^
  --icon=src\warframe.ico ^
  --add-data "src\warframe.ico;." ^
  --collect-all plyer ^
  --hidden-import=plyer.platforms.win.notification ^
  --hidden-import=plyer.platforms.win ^
  --name YourWarframe ^
  src\app.py

if exist dist\YourWarframe.exe (
    echo.
    echo Build complete: dist\YourWarframe.exe
) else (
    echo.
    echo Build failed - check the output above.
    exit /b 1
)

pause

cls