import tkinter as tk
from tkinter import messagebox
import json
from github_api import GitHubAPI
from notifier import Notifier
from PIL import Image, ImageTk
import requests
from io import BytesIO

CONFIG_FILE = 'config.json'

profile_labels = {}

def save_config(username, token):
    with open(CONFIG_FILE, 'r') as f:
        config = json.load(f)
    config['username'] = username
    config['token'] = token
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)

def show_profile_info(stats, contrib):
    for key, label in profile_labels.items():
        label.destroy()
    profile_labels.clear()
    y = 220
    if stats:
        name = stats.get('name', '')
        bio = stats.get('bio', '')
        repos = stats.get('public_repos', 0)
        followers = stats.get('followers', 0)
        following = stats.get('following', 0)
        created = stats.get('created_at', '')
        avatar_url = stats.get('avatar_url', '')
        if avatar_url:
            try:
                response = requests.get(avatar_url)
                img = Image.open(BytesIO(response.content)).resize((64, 64))
                photo = ImageTk.PhotoImage(img)
                avatar_label = tk.Label(root, image=photo)
                avatar_label.image = photo
                avatar_label.place(x=20, y=y)
                profile_labels['avatar'] = avatar_label
            except Exception:
                pass
        name_label = tk.Label(root, text=f'Name: {name}')
        name_label.place(x=100, y=y)
        profile_labels['name'] = name_label
        bio_label = tk.Label(root, text=f'Bio: {bio}')
        bio_label.place(x=100, y=y+20)
        profile_labels['bio'] = bio_label
        repo_label = tk.Label(root, text=f'Repos: {repos}')
        repo_label.place(x=100, y=y+40)
        profile_labels['repos'] = repo_label
        followers_label = tk.Label(root, text=f'Followers: {followers}')
        followers_label.place(x=200, y=y+40)
        profile_labels['followers'] = followers_label
        following_label = tk.Label(root, text=f'Following: {following}')
        following_label.place(x=300, y=y+40)
        profile_labels['following'] = following_label
        created_label = tk.Label(root, text=f'Joined: {created[:10]}')
        created_label.place(x=100, y=y+60)
        profile_labels['created'] = created_label
    if contrib:
        today = contrib.get('today', 0)
        events = contrib.get('events', 0)
        contrib_label = tk.Label(root, text=f"Today's Contributions: {today}")
        contrib_label.place(x=100, y=y+80)
        profile_labels['contrib'] = contrib_label
        events_label = tk.Label(root, text=f"Recent Events: {events}")
        events_label.place(x=250, y=y+80)
        profile_labels['events'] = events_label

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
    show_profile_info(stats, contrib)

def on_save():
    username = username_entry.get()
    token = token_entry.get()
    save_config(username, token)
    check_contribution()

root = tk.Tk()
root.title('GitHub Contribution Tracker')
root.geometry('500x350')

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

status_label = tk.Label(root, text='Status will appear here.')
status_label.pack(pady=10)

root.mainloop()
