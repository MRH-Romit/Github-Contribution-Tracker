import pystray
from PIL import Image, ImageDraw
import time
import threading
import json
import os
from github_api import GitHubAPI
from notifier import Notifier

class SystemTrayIcon:
    def __init__(self, main_app=None):
        self.main_app = main_app
        self.last_check_time = None
        self.check_interval = 6 * 60 * 60  # 6 hours in seconds
        self.icon = None
        self.running = False
        self.github_api = GitHubAPI()
        self.create_icon()
        
    def create_icon(self):
        # Create a simple icon
        width = 64
        height = 64
        color1 = 'black'
        color2 = '#39d353'  # GitHub green
        
        # Generate an image for the icon
        image = Image.new('RGB', (width, height), color1)
        dc = ImageDraw.Draw(image)
        dc.rectangle((width // 4, height // 4, 3 * width // 4, 3 * height // 4), fill=color2)
        
        # Create a menu and icon
        menu = (
            pystray.MenuItem('Check Contributions Now', self.check_contribution),
            pystray.MenuItem('Open App', self.open_app),
            pystray.MenuItem('Exit', self.exit_app)
        )
        
        self.icon = pystray.Icon("GitHub Tracker", image, "GitHub Contribution Tracker", menu)
    
    def run(self):
        self.running = True
        # Start background thread for periodic checks
        self.check_thread = threading.Thread(target=self.background_check, daemon=True)
        self.check_thread.start()
        
        # Run the system tray icon
        self.icon.run()
    
    def background_check(self):
        while self.running:
            self.check_contribution()
            # Sleep for the check interval
            time.sleep(self.check_interval)
    
    def check_contribution(self):
        # Save the current time as last check time
        self.last_check_time = time.time()
        
        # Update the config
        self.update_last_check()
        
        # Check if user has contributed today
        has_contributed = self.github_api.get_today_contributions()
        
        if has_contributed is False:
            # Notify if no contribution today
            Notifier.notify_no_contribution()
        elif has_contributed is True:
            # Optionally notify of successful contribution
            Notifier.notify_contribution_success()
    
    def update_last_check(self):
        config_file = 'config.json'
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                config = json.load(f)
            
            config['last_check'] = time.strftime('%Y-%m-%d %H:%M:%S')
            
            with open(config_file, 'w') as f:
                json.dump(config, f)
    
    def open_app(self):
        if self.main_app:
            # If we have a reference to the main app, bring it to front
            self.main_app.deiconify()
            self.main_app.lift()
            self.main_app.focus_force()
        else:
            # Otherwise, we might need to start the app
            import subprocess
            import sys
            subprocess.Popen([sys.executable, 'main.py'])
    
    def exit_app(self):
        self.running = False
        self.icon.stop()
        if self.main_app:
            self.main_app.quit()
