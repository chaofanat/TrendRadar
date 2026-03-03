@echo off
REM ========================================
REM TrendRadar - Create Desktop Shortcut
REM ========================================

set "SCRIPT_DIR=%~dp0"
set "SHORTCUT_NAME=TrendRadar Monitor.lnk"
set "DESKTOP=%USERPROFILE%\Desktop"

echo ========================================
echo Creating TrendRadar Desktop Shortcut
echo ========================================
echo.

REM Create VBScript to generate shortcut
set "VBS_FILE=%TEMP%\create_shortcut.vbs"

echo Set WshShell = WScript.CreateObject("WScript.Shell") > "%VBS_FILE%"
echo Set Shortcut = WshShell.CreateShortcut("%DESKTOP%\%SHORTCUT_NAME%") >> "%VBS_FILE%"
echo Shortcut.TargetPath = "powershell.exe" >> "%VBS_FILE%"
echo Shortcut.Arguments = "-ExecutionPolicy Bypass -WindowStyle Hidden -File ""%SCRIPT_DIR%run-monitor.ps1""" >> "%VBS_FILE%"
echo Shortcut.WorkingDirectory = "%SCRIPT_DIR%" >> "%VBS_FILE%"
echo Shortcut.Description = "TrendRadar Force Majeure Event Monitor" >> "%VBS_FILE%"
echo Shortcut.Save >> "%VBS_FILE%"

REM Execute VBScript
cscript //nologo "%VBS_FILE%"

REM Cleanup
del "%VBS_FILE%" >nul 2>&1

echo.
echo ========================================
echo [SUCCESS] Shortcut created!
echo ========================================
echo.
echo Location: %DESKTOP%\%SHORTCUT_NAME%
echo.
echo Usage:
echo   - Double-click to start monitoring
echo   - Runs in background (no window)
echo   - Single instance (won't duplicate)
echo.
pause
