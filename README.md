# GitHub Contribution Tracker

A simple desktop app to track your daily GitHub contributions, get notified if you haven't contributed today, and visualize your recent activity.

## Features
- Check if you have contributed today
- System notification if no activity
- Simple Tkinter GUI
- Stores your GitHub username and token locally
- (Planned) Graph of last 7/30 days' contributions

## Setup
1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Run the app:
   ```
   python main.py
   ```
3. Enter your GitHub username and Personal Access Token (PAT) with `read:user` and `repo` scopes.

## Packaging
- Use PyInstaller to build a standalone executable:
  ```
  pyinstaller --onefile --windowed main.py
  ```

## Roadmap
See `Roadmap.txt` for planned features and phases.

## License
MIT
