# GitHub Contribution Tracker

A desktop application that helps developers maintain their GitHub contribution streak by tracking daily contributions and providing notifications when they haven't contributed yet.

## Features

- **Daily Contribution Check:** Monitors your GitHub activity and alerts you if you haven't made any contributions today
- **System Tray Integration:** Runs quietly in the background with an accessible system tray icon
- **GitHub Statistics:** Displays your profile information, repository count, followers, and following
- **Contribution Calendar:** Visual representation of your contribution activity (similar to GitHub's contribution graph)
- **Automatic Background Checking:** Periodically checks for contributions (every 6 hours by default)
- **Dark Theme UI:** Designed with GitHub's dark theme colors for a familiar experience

## Screenshots

(Screenshots will be added here)

## Installation

### Windows

1. Download the latest `GitHubContributionTracker.exe` from the Releases page
2. Run the executable - no installation needed!

### From Source

```bash
# Clone the repository
git clone https://github.com/yourusername/github-contribution-tracker.git
cd github-contribution-tracker

# Install dependencies
pip install -r requirements.txt

# Run the application
python run_app.py

# Optional command line arguments:
# Start minimized to system tray:
python run_app.py --tray
# Set custom check interval (in hours):
python run_app.py --interval 4
```

## Setup

1. **GitHub Personal Access Token:**
   - Go to [GitHub Settings > Developer Settings > Personal Access Tokens](https://github.com/settings/tokens)
   - Click on "Generate New Token"
   - Give it a name (e.g., "Contribution Tracker")
   - Select scopes: `read:user` and `public_repo` (minimum required permissions)
   - Copy the generated token

2. **First Run:**
   - Launch the application
   - Enter your GitHub username and the personal access token
   - Click "Save & Check"
   - The app will verify your credentials and start monitoring

## Usage

### Main Interface

- **Save & Check:** Saves your credentials and immediately checks for today's contributions
- **Minimize to Tray:** Sends the application to the system tray while continuing to monitor in the background
- **Contribution Status:** Shows whether you've contributed today

### System Tray

Right-click the system tray icon to:
- **Check Contributions Now:** Manually trigger a check
- **Open App:** Bring the main window back to view
- **Exit:** Close the application completely

## Building from Source

To build a standalone executable:

```bash
# Install PyInstaller if not already installed
pip install pyinstaller

# Build using our script
python build_package.py
```

The built application will be available in the `dist` folder.

## Requirements

- Python 3.7+
- Required packages (see requirements.txt):
  - requests
  - plyer
  - matplotlib
  - pystray
  - pillow
  - numpy
  - pyinstaller (for building executable)

## Privacy and Security

- Your GitHub token is stored locally on your machine only
- No data is transmitted to any third-party servers
- The application only makes API calls to GitHub.com

## Roadmap
See `Roadmap.txt` for detailed planned features and development phases.

## License
MIT
