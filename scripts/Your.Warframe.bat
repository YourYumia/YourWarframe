@echo off
setlocal

cd /d "%~dp0.."

py -m pip install -r src\requirements.txt --upgrade

cls && py src\app.py