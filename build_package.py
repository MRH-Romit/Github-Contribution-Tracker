import PyInstaller.__main__
import os
import shutil
import sys

# Check if PyInstaller is installed
try:
    import PyInstaller
except ImportError:
    print("PyInstaller is not installed. Installing...")
    import subprocess
    subprocess.call([sys.executable, "-m", "pip", "install", "pyinstaller"])

# Path to the icon file
icon_path = os.path.join('assets', 'icon.ico')
if not os.path.exists(icon_path):
    # Try to convert png to ico if needed
    try:
        from PIL import Image
        png_path = os.path.join('assets', 'icon.png')
        if os.path.exists(png_path):
            print("Converting PNG icon to ICO format...")
            img = Image.open(png_path)
            ico_path = os.path.join('assets', 'icon.ico')
            img.save(ico_path)
            icon_path = ico_path
    except Exception as e:
        print(f"Could not convert icon: {e}")
        # Use default icon (empty string)
        icon_path = ""

# Create dist directory if it doesn't exist
if not os.path.exists('dist'):
    os.makedirs('dist')

# Copy the config file to dist directory
config_path = 'config.json'
if os.path.exists(config_path):
    # Create an empty config file to avoid including personal data
    empty_config = {"username": "", "token": "", "minimize_to_tray": True, "last_check": ""}
    import json
    with open('dist/config.json', 'w') as f:
        json.dump(empty_config, f)

# Create the assets directory in dist if it doesn't exist
assets_dir = os.path.join('dist', 'assets')
if not os.path.exists(assets_dir):
    os.makedirs(assets_dir)

# Copy the icon to the assets directory in dist
if os.path.exists(os.path.join('assets', 'icon.png')):
    shutil.copy(os.path.join('assets', 'icon.png'), os.path.join(assets_dir, 'icon.png'))

# PyInstaller options
pyinstaller_args = [
    'enhanced_main.py',  # Use the enhanced version of main.py
    '--name=GitHubContributionTracker',
    '--onefile',         # Create a single executable
    f'--icon={icon_path}' if icon_path else "",  # Set the icon
    '--noconsole',       # No console window
    '--add-data=assets/icon.png;assets',  # Include the icon in the executable
    '--hidden-import=pystray',  # Make sure pystray is included
    '--hidden-import=PIL',      # Include PIL
    '--hidden-import=tkinter',  # Include tkinter
]

# Filter out empty arguments
pyinstaller_args = [arg for arg in pyinstaller_args if arg]

print("Building executable with PyInstaller...")
PyInstaller.__main__.run(pyinstaller_args)

print("Done! Executable created in the dist directory.")
print("You can distribute GitHubContributionTracker.exe to your users.")
