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
git stash
echo swapping to dev branch
git switch dev
echo attempting to commit changes with message...
git commit -m "%msg%"
echo attempting to push to origin dev...
git push -u origin dev
echo attempting to push to gitea dev...
git push -u gitea dev

echo swapping back to main branch
git switch main

pause
cls