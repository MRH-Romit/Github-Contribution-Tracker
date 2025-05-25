# Getting Started with GitHub Contribution Tracker

Thank you for using GitHub Contribution Tracker! This guide will help you get up and running quickly.

## Installation

### Option 1: Run the executable (Windows)
1. Download the latest `GitHubContributionTracker.exe` from the Releases page
2. Run the executable - no installation required!

### Option 2: Automated setup (Windows)
1. Make sure you have Python 3.7+ installed
2. Run the `install.bat` script
3. Follow the on-screen instructions

### Option 3: Manual installation
1. Make sure you have Python 3.7+ installed
2. Install dependencies with: `pip install -r requirements.txt`
3. Copy `config.json.template` to `config.json`
4. Copy `github_api.py.template` to `github_api.py`
5. Run the application with: `python app.py`

## Setting up your GitHub token

1. Visit [GitHub Settings > Developer Settings > Personal Access Tokens](https://github.com/settings/tokens)
2. Click "Generate new token"
3. Give the token a name (e.g., "GitHub Contribution Tracker")
4. Select the following scopes:
   - `read:user` (to access your profile information)
   - `public_repo` (to check your public contributions)
5. Click "Generate token" at the bottom of the page
6. **Copy the token immediately** - GitHub will only show it once!

## First-time setup

1. Launch the application
2. Enter your GitHub username
3. Paste your personal access token
4. Check the "Minimize to system tray" option if you want the app to run in the background
5. Click "Save & Check"
6. The app will verify your credentials and show your GitHub stats

## Running in the background

To have the application run in the background and check your contributions periodically:

1. Use the "Minimize to Tray" button
2. The application will continue running in your system tray
3. It will check for contributions every 6 hours by default
4. You'll get a notification if you haven't contributed today

## Auto-start with Windows

To have the application start automatically when you log in to Windows:

1. Create a shortcut to `startup.bat` or `GitHubContributionTracker.exe`
2. Press `Win+R` to open the Run dialog
3. Type `shell:startup` and press Enter
4. Copy your shortcut into this folder

## Need help?

If you encounter any issues or have questions, please:
- Check the README.md file for additional information
- Visit our GitHub repository to report issues
- Make sure your GitHub token has the correct permissions
