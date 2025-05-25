# GitHub Contribution Tracker - Version Comparison

The GitHub Contribution Tracker has two main versions:

## Enhanced Version (`enhanced_main.py`)

The enhanced version provides a full-featured experience including:

- **System Tray Integration**: Run the app in the background with a system tray icon
- **Background Monitoring**: Automatically check for contributions at regular intervals
- **Minimization Options**: Minimize to tray instead of closing
- **Dark UI Theme**: Complete dark themed interface
- **User Preferences**: Remember settings like minimize-to-tray preference
- **Notifications**: System notifications for contribution status

This version is best for users who want to keep the app running all day to monitor their contributions.

## Basic Version (`fixed_main.py`)

The basic version provides core functionality:

- **Contribution Checking**: Check your GitHub contributions
- **Profile Stats**: View your profile information
- **Simple Calendar**: View your contribution calendar
- **Notifications**: Basic system notifications
- **Lightweight**: Uses fewer resources

This version is best for users who just want to check their contributions manually without background features.

## Choosing a Version

By default, when you run `app.py`, it will try to use the enhanced version. If you prefer to use the basic version, you can:

```bash
python app.py --basic
```

## System Requirements

- Enhanced version requires additional libraries like `pystray` and `pillow`
- Basic version has fewer dependencies

All necessary packages are included in `requirements.txt` and will be installed with the setup script.
