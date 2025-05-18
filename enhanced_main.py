import tkinter as tk
from tkinter import messagebox, ttk
import json
import threading
import time
import os
from github_api import GitHubAPI
from notifier import Notifier
from system_tray import SystemTrayIcon

# Fix the import if the module name conflicts with Python's calendar
try:
    from simple_calendar import SimpleContributionCalendar
except ImportError:
    import sys
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from simple_calendar import SimpleContributionCalendar

CONFIG_FILE = 'config.json'

class GithubContributionTracker:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('GitHub Contribution Tracker')
        self.root.geometry('400x250')  # Slightly taller for the new checkbox
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
        # Set icon for the window
        try:
            icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'icon.png')
            if os.path.exists(icon_path):
                from PIL import Image, ImageTk
                icon = ImageTk.PhotoImage(Image.open(icon_path))
                self.root.iconphoto(True, icon)
        except Exception:
            pass
            
        self.api = GitHubAPI()
        self.create_widgets()
        self.load_config()
        
        # Initialize system tray
        self.system_tray = SystemTrayIcon(self.root)
        self.system_tray_thread = None
        
    def create_widgets(self):
        # Add a dark theme by setting background colors
        bg_color = "#1c1c1c"
        fg_color = "white"
        
        main_frame = tk.Frame(self.root, bg=bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Username
        username_label = tk.Label(main_frame, text='GitHub Username:', bg=bg_color, fg=fg_color)
        username_label.pack(anchor='w')
        self.username_entry = tk.Entry(main_frame, width=30)
        self.username_entry.pack(fill='x', pady=(0, 10))
        
        # Token
        token_label = tk.Label(main_frame, text='Personal Access Token:', bg=bg_color, fg=fg_color)
        token_label.pack(anchor='w')
        self.token_entry = tk.Entry(main_frame, show='*', width=30)
        self.token_entry.pack(fill='x', pady=(0, 10))
        
        # Option to run in background
        self.tray_var = tk.BooleanVar()
        self.tray_var.set(True)  # Default to running in background
        tray_check = tk.Checkbutton(main_frame, text='Minimize to system tray', 
                                variable=self.tray_var, bg=bg_color, fg=fg_color,
                                selectcolor=bg_color, activebackground=bg_color, 
                                activeforeground=fg_color)
        tray_check.pack(anchor='w', pady=(0, 10))
        
        # Buttons
        button_frame = tk.Frame(main_frame, bg=bg_color)
        button_frame.pack(fill='x', pady=5)
        
        self.save_button = tk.Button(button_frame, text='Save & Check', command=self.on_save)
        self.save_button.pack(side='left', padx=5)
        
        self.minimize_button = tk.Button(button_frame, text='Minimize to Tray', command=self.minimize_to_tray)
        self.minimize_button.pack(side='right', padx=5)
        
        # Status label
        self.status_label = tk.Label(main_frame, text='Status will appear here', bg=bg_color, fg=fg_color)
        self.status_label.pack(pady=10)
        
    def load_config(self):
        """Load saved configuration"""
        try:
            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, 'r') as f:
                    config = json.load(f)
                username = config.get('username', '')
                if username:
                    self.username_entry.insert(0, username)
                # Load the minimize to tray preference if it exists
                minimize_to_tray = config.get('minimize_to_tray', True)  # Default is True
                self.tray_var.set(minimize_to_tray)
        except Exception as e:
            print(f"Error loading config: {e}")
    
    def save_config(self):
        """Save configuration to file"""
        username = self.username_entry.get()
        token = self.token_entry.get()
        minimize_to_tray = self.tray_var.get()
        
        config = {'username': username, 'token': token, 'minimize_to_tray': minimize_to_tray, 'last_check': ''}
        
        # Create file if it doesn't exist
        if not os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'w') as f:
                json.dump({}, f)
                
        # Update the config
        try:
            with open(CONFIG_FILE, 'r') as f:
                existing_config = json.load(f)
            
            # Merge the configs to preserve any other fields like last_check
            existing_config.update(config)
            
            with open(CONFIG_FILE, 'w') as f:
                json.dump(existing_config, f)
        except Exception as e:
            print(f"Error saving config: {e}")
            messagebox.showerror("Error", f"Could not save configuration: {e}")
            
    def check_contribution(self):
        """Check GitHub contributions"""
        self.api.load_config()  # Reload config in case it changed
        result = self.api.get_today_contributions()
        stats = self.api.get_profile_stats()
        contrib = self.api.get_contribution_stats()
        
        if result is None:
            messagebox.showerror('Error', 'Failed to fetch contribution data. Check your token and username.')
        elif result:
            self.status_label.config(text='You have contributed today! 🎉', fg='green')
        else:
            self.status_label.config(text='No contribution today.', fg='red')
            Notifier.notify_no_contribution()
            
        self.show_stats_window(stats, contrib)
    
    def show_stats_window(self, stats, contrib):
        """Show window with GitHub stats"""
        stats_win = tk.Toplevel(self.root)
        stats_win.title('GitHub Stats')
        stats_win.geometry('600x550')
        stats_win.configure(bg='#1c1c1c')  # Dark background like GitHub
        
        y = 10
        if stats:
            name = stats.get('name', '')
            bio = stats.get('bio', '')
            repos = stats.get('public_repos', 0)
            followers = stats.get('followers', 0)
            following = stats.get('following', 0)
            created = stats.get('created_at', '')
            avatar_url = stats.get('avatar_url', '')
            
            try:
                import requests
                from PIL import Image, ImageTk
                from io import BytesIO
                if avatar_url:
                    response = requests.get(avatar_url)
                    img = Image.open(BytesIO(response.content)).resize((64, 64))
                    photo = ImageTk.PhotoImage(img)
                    avatar_label = tk.Label(stats_win, image=photo, bg='#1c1c1c')
                    avatar_label.image = photo
                    avatar_label.place(x=20, y=y)
            except Exception as e:
                print(f"Error loading avatar: {e}")
                
            tk.Label(stats_win, text=f'Name: {name}', bg='#1c1c1c', fg='white').place(x=100, y=y)
            tk.Label(stats_win, text=f'Bio: {bio}', bg='#1c1c1c', fg='white').place(x=100, y=y+20)
            tk.Label(stats_win, text=f'Repos: {repos}', bg='#1c1c1c', fg='white').place(x=100, y=y+40)
            tk.Label(stats_win, text=f'Followers: {followers}', bg='#1c1c1c', fg='white').place(x=200, y=y+40)
            tk.Label(stats_win, text=f'Following: {following}', bg='#1c1c1c', fg='white').place(x=300, y=y+40)
            tk.Label(stats_win, text=f'Joined: {created[:10]}', bg='#1c1c1c', fg='white').place(x=100, y=y+60)
        
        if contrib:
            today = contrib.get('today', 0)
            events = contrib.get('events', 0)
            tk.Label(stats_win, text=f"Today's Contributions: {today}", bg='#1c1c1c', fg='white').place(x=100, y=y+80)
            tk.Label(stats_win, text=f"Recent Events: {events}", bg='#1c1c1c', fg='white').place(x=250, y=y+80)
        
        # Show Contribution Calendar
        try:
            calendar = SimpleContributionCalendar(stats_win)
            calendar.display()
        except Exception as e:
            tk.Label(stats_win, text=f'Could not load contribution calendar: {str(e)}', 
                    bg='#1c1c1c', fg='white').place(x=150, y=180)
    
    def on_save(self):
        """Save config and check contributions"""
        username = self.username_entry.get()
        token = self.token_entry.get()
        
        if not username or not token:
            messagebox.showwarning("Missing Information", "Please enter both GitHub username and token.")
            return
            
        self.save_config()
        self.check_contribution()
    
    def minimize_to_tray(self):
        """Minimize the app to system tray"""
        if self.tray_var.get():
            # Start the system tray icon if it's not already running
            if not self.system_tray_thread or not self.system_tray_thread.is_alive():
                # Save current config in case it wasn't saved
                self.save_config()
                # Start system tray in a new thread
                self.system_tray_thread = threading.Thread(target=self.system_tray.run, daemon=True)
                self.system_tray_thread.start()
                # Hide the main window
                self.root.withdraw()
                # Notify user
                Notifier.notify_background_start()
            else:
                # Just hide the window if tray is already running
                self.root.withdraw()
        else:
            # If the minimize to tray option is off, show a message
            messagebox.showinfo("Option Disabled", 
                                "The minimize to tray option is disabled. Enable it in the settings to use this feature.")
    
    def on_close(self):
        """Handle window close event"""
        if self.tray_var.get():
            # Minimize to tray instead of closing
            self.minimize_to_tray()
        else:
            # Confirm exit
            if messagebox.askyesno("Confirm Exit", "Are you sure you want to exit?"):
                # Stop the system tray if it's running
                if hasattr(self, 'system_tray') and self.system_tray:
                    self.system_tray.running = False
                    if hasattr(self.system_tray, 'icon'):
                        self.system_tray.icon.stop()
                # Close the application
                self.root.destroy()
    
    def run(self):
        """Run the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = GithubContributionTracker()
    app.run()
