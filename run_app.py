#!/usr/bin/env python3
"""
GitHub Contribution Tracker - Main entry point
"""

import os
import sys
import argparse
import json

def check_dependencies():
    """Check if all required dependencies are installed"""
    try:
        import requests
        import tkinter
        import plyer
        import pystray
        from PIL import Image, ImageDraw
        return True
    except ImportError as e:
        print(f"Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def ensure_config_exists():
    """Create config file if it doesn't exist"""
    config_file = 'config.json'
    if not os.path.exists(config_file):
        default_config = {
            "username": "",
            "token": "",
            "minimize_to_tray": True,
            "last_check": ""
        }
        with open(config_file, 'w') as f:
            json.dump(default_config, f)
        print(f"Created default config file: {config_file}")

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="GitHub Contribution Tracker")
    parser.add_argument('--tray', action='store_true', help='Start minimized to system tray')
    parser.add_argument('--interval', type=int, default=6,
                      help='Check interval in hours (default: 6)')
    return parser.parse_args()

def main():
    """Main function to start the application"""
    # Check dependencies first
    if not check_dependencies():
        return 1
        
    # Ensure config file exists
    ensure_config_exists()
    
    # Parse command line arguments
    args = parse_arguments()
    
    # Define application options from arguments
    options = {
        'start_minimized': args.tray,
        'check_interval': args.interval * 60 * 60  # Convert hours to seconds
    }
    
    try:
        # Try to import and run the enhanced version
        from enhanced_main import GithubContributionTracker
        app = GithubContributionTracker()
        
        # Apply any command line options
        if options['start_minimized'] and hasattr(app, 'minimize_to_tray'):
            # Schedule minimize_to_tray to run after the app starts
            app.root.after(100, app.minimize_to_tray)
            
        # Run the application
        app.run()
        
    except ImportError:
        # Fallback to basic version
        print("Enhanced version not found. Falling back to basic version.")
        import main
        # The basic version will handle its own mainloop
        
    return 0

if __name__ == "__main__":
    sys.exit(main())
