import tkinter as tk
from tkinter import messagebox
import json
from github_api import GitHubAPI
from notifier import Notifier

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
    if result is None:
        messagebox.showerror('Error', 'Failed to fetch contribution data. Check your token and username.')
    elif result:
        status_label.config(text='You have contributed today! 🎉', fg='green')
    else:
        status_label.config(text='No contribution today.', fg='red')
        Notifier.notify_no_contribution()

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

status_label = tk.Label(root, text='Status will appear here.')
status_label.pack(pady=10)

root.mainloop()
