@echo off
setlocal enabledelayedexpansion

:: NOTE: Prompt for the commit message
set /p "msg=Commit message: "

:: Validate message input
if "%msg%"=="" (
    echo [ERROR] Message cannot be empty.
    pause
    exit /b 1
)

cd /d "%~dp0.."

echo attempting to stage changes...
git add .
echo attempting to commit changes with message...
git commit -m "%msg%"
echo attempting to push to origin main...
git push origin main
echo attempting to push to gitea main...
git push gitea main

pause
cls
