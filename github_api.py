import requests
import json
from datetime import datetime

CONFIG_FILE = 'config.json'

class GitHubAPI:
    def __init__(self):
        self.load_config()

    def load_config(self):
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
        self.username = config.get('username', '')
        self.token = config.get('token', '')

    def get_today_contributions(self):
        if not self.username or not self.token:
            return None
        url = f'https://api.github.com/users/{self.username}/events'
        headers = {'Authorization': f'token {self.token}'}
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return None
        today = datetime.utcnow().date()
        events = response.json()
        for event in events:
            created_at = event.get('created_at', '')
            if created_at:
                event_date = datetime.strptime(created_at, '%Y-%m-%dT%H:%M:%SZ').date()
                if event_date == today:
                    return True
        return False
