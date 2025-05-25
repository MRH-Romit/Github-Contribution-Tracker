@echo off
:: GitHub Contribution Tracker Installation Script
echo Installing GitHub Contribution Tracker...
echo.

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH.
    echo Please install Python 3.7 or higher from https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

:: Install dependencies
echo Installing required packages...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Failed to install dependencies.
    pause
    exit /b 1
)

:: Create config file from template if it doesn't exist
if not exist config.json (
    echo Creating config file from template...
    copy config.json.template config.json
    echo Please edit the config.json file with your GitHub username and token.
)

:: Create github_api.py from template if it doesn't exist
if not exist github_api.py (
    echo Creating API file from template...
    copy github_api.py.template github_api.py
)

:: Create shortcuts
echo Creating shortcuts...
powershell -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('GitHub Contribution Tracker.lnk'); $Shortcut.TargetPath = 'pythonw.exe'; $Shortcut.Arguments = 'app.py'; $Shortcut.WorkingDirectory = '%~dp0'; $Shortcut.IconLocation = 'assets\icon.png,0'; $Shortcut.Save()"

:: Offer to create startup shortcut
echo.
echo Do you want the app to start automatically when Windows starts? (Y/N)
choice /c YN /n
if %errorlevel% equ 1 (
    echo Creating startup shortcut...
    powershell -Command "$WshShell = New-Object -ComObject WScript.Shell; $Startup = $WshShell.SpecialFolders('Startup'); $Shortcut = $WshShell.CreateShortcut(\"$Startup\GitHub Contribution Tracker.lnk\"); $Shortcut.TargetPath = 'pythonw.exe'; $Shortcut.Arguments = 'app.py --tray'; $Shortcut.WorkingDirectory = '%~dp0'; $Shortcut.IconLocation = 'assets\icon.png,0'; $Shortcut.Save()"
    echo Startup shortcut created.
) else (
    echo Startup shortcut not created.
)

echo.
echo Installation complete!
echo You can now run the app by double-clicking the shortcut or running "python app.py"
echo.
pause
