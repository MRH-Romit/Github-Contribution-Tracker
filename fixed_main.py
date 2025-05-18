import tkinter as tk
from tkinter import messagebox
import json
from github_api import GitHubAPI
from notifier import Notifier
try:
    from contribution_calendar import ContributionCalendar
except ImportError:
    # Fix the import if the module name conflicts
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from contribution_calendar import ContributionCalendar

CONFIG_FILE = 'config.json'

def save_config(username, token):
    with open(CONFIG_FILE, 'r') as f:
        config = json.load(f)
    config['username'] = username
    config['token'] = token
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)

def check_contribution():
    api = GitHubAPI()
    result = api.get_today_contributions()
    stats = api.get_profile_stats()
    contrib = api.get_contribution_stats()
    if result is None:
        messagebox.showerror('Error', 'Failed to fetch contribution data. Check your token and username.')
    elif result:
        status_label.config(text='You have contributed today! 🎉', fg='green')
    else:
        status_label.config(text='No contribution today.', fg='red')
        Notifier.notify_no_contribution()
    show_stats_window(stats, contrib)

def show_stats_window(stats, contrib):
    stats_win = tk.Toplevel(root)
    stats_win.title('GitHub Stats')
    stats_win.geometry('600x550')  # Make window slightly taller
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
        except Exception:
            pass
            
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
    
    # --- Show Contribution Calendar using our simplified implementation ---
    try:
        from simple_calendar import SimpleContributionCalendar
        # Create and display the calendar directly
        calendar = SimpleContributionCalendar(stats_win)
        calendar.display()
    except Exception as e:
        tk.Label(stats_win, text=f'Could not load contribution calendar: {str(e)}', bg='#1c1c1c', fg='white').place(x=150, y=180)

def on_save():
    username = username_entry.get()
    token = token_entry.get()
    save_config(username, token)
    check_contribution()

root = tk.Tk()
root.title('GitHub Contribution Tracker')
root.geometry('400x200')

# Username
username_label = tk.Label(root, text='GitHub Username:')
username_label.pack()
username_entry = tk.Entry(root)
username_entry.pack()

# Token
token_label = tk.Label(root, text='Personal Access Token:')
token_label.pack()
token_entry = tk.Entry(root, show='*')
token_entry.pack()

save_button = tk.Button(root, text='Save & Check', command=on_save)
save_button.pack(pady=10)

status_label = tk.Label(root, text='Status will appear here')
status_label.pack(pady=10)

# Try to load saved username/token if exists
try:
    with open(CONFIG_FILE, 'r') as f:
        config = json.load(f)
    username = config.get('username', '')
    if username:
        username_entry.insert(0, username)
except:
    pass

root.mainloop()
