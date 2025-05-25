#!/usr/bin/env python3
"""
GitHub Contribution Tracker - Main Application Entry Point

This is the main entry point for the application that helps you choose between:

1. Enhanced Version (enhanced_main.py):
   - Full-featured version with system tray integration
   - Background checking for contributions
   - Minimizable to tray
   - Dark theme UI

2. Basic Version (fixed_main.py):
   - Simpler version without system tray integration
   - Core functionality only
   - Lighter on resources

The app will use the enhanced version by default, unless you choose
the basic version with the --basic flag or an error occurs.
"""

import os
import sys
import json
import argparse

CONFIG_FILE = 'config.json'
CONFIG_TEMPLATE = 'config.json.template'
API_FILE = 'github_api.py'
API_TEMPLATE = 'github_api.py.template'

def check_setup():
    """Check if the application is properly set up"""
    if not os.path.exists(CONFIG_FILE):
        print(f"Config file not found. Creating from template...")
        if os.path.exists(CONFIG_TEMPLATE):
            import shutil
            shutil.copy2(CONFIG_TEMPLATE, CONFIG_FILE)
            print(f"Created {CONFIG_FILE} from template. Please edit it with your credentials.")
        else:
            print(f"Error: Config template not found. Please create {CONFIG_FILE} manually.")
            
    if not os.path.exists(API_FILE):
        print(f"API file not found. Creating from template...")
        if os.path.exists(API_TEMPLATE):
            import shutil
            shutil.copy2(API_TEMPLATE, API_FILE)
            print(f"Created {API_FILE} from template.")
        else:
            print(f"Error: API template not found. Please create {API_FILE} manually.")

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="GitHub Contribution Tracker")
    parser.add_argument('--tray', action='store_true', help='Start minimized to system tray')
    parser.add_argument('--interval', type=int, default=6,
                      help='Check interval in hours (default: 6)')
    parser.add_argument('--basic', action='store_true', 
                      help='Use basic version instead of enhanced version')
    return parser.parse_args()

def main():
    """Launch the GitHub Contribution Tracker application"""
    # Set working directory to script location
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Check if the application is set up
    check_setup()
    
    # Parse command line arguments
    args = parse_arguments()
    
    # Try to import required libraries
    try:
        import tkinter as tk
        import requests
    except ImportError as e:
        print(f"Error importing required libraries: {e}")
        print("Please install required packages with: pip install -r requirements.txt")
        return 1
          # Run the application
    if args.basic:
        # Use the basic version if requested
        print("Starting GitHub Contribution Tracker (Basic Version)")
        print("This version provides core functionality without system tray integration.")
        print("For the enhanced experience, run without the --basic flag.")
        print("-" * 60)
        import fixed_main
        return 0
    else:
        try:
            # Try to import and run the enhanced version first (best experience)
            print("Starting GitHub Contribution Tracker (Enhanced Version)")
            print("This version includes system tray integration and background monitoring.")
            print("-" * 60)
            
            from enhanced_main import GithubContributionTracker
            app = GithubContributionTracker()
            
            # Apply command line options
            if args.tray and hasattr(app, 'minimize_to_tray'):
                app.root.after(100, app.minimize_to_tray)
                
            app.run()
            return 0
        except ImportError as e:
            # Fall back to fixed version if enhanced isn't available
            print(f"Enhanced version not available: {e}")
            print("Falling back to basic version.")
            print("-" * 60)
            import fixed_main
            return 0
        except Exception as e:
            print(f"Error starting application: {e}")
            print(f"Error details: {str(e)}")
            print("Try running with --basic flag for the simpler version.")
            return 1

if __name__ == "__main__":
    sys.exit(main())
