@echo off
REM TrendRadar Force Majeure Monitor
setlocal enabledelayedexpansion

REM Set paths
set "PROJECT_DIR=%~dp0"
set "VENV_DIR=C:\Users\CHAOFAN\Desktop\Workspace\Pyproject\News\.venv"

echo ========================================
echo TrendRadar Force Majeure Monitor
echo Polling: 10 minutes
echo Push Window: 08:00-21:00
echo ========================================
echo.

cd /d "%PROJECT_DIR%"

:LOOP
echo [%date% %time%] Starting monitor...
"%VENV_DIR%\Scripts\python.exe" -m trendradar
echo.
echo [%date% %time%] Monitor complete, waiting 10 minutes...
timeout /t 600 /nobreak > nul
goto LOOP
