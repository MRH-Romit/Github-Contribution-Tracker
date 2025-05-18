@echo off
:: GitHub Contribution Tracker Startup Script
:: This script starts the application minimized to the system tray

echo Starting GitHub Contribution Tracker...

:: Get the directory where this script is located
set SCRIPT_DIR=%~dp0

:: Change to the application directory
cd /d "%SCRIPT_DIR%"

:: Start the application in tray mode
start /min pythonw run_app.py --tray

echo Application started in system tray.
timeout /t 3
exit
