import requests
import json
from datetime import datetime, timedelta

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

    def get_profile_stats(self):
        if not self.username or not self.token:
            return None
        url = f'https://api.github.com/users/{self.username}'
        headers = {'Authorization': f'token {self.token}'}
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return None
        data = response.json()
        return {
            'name': data.get('name', self.username),
            'public_repos': data.get('public_repos', 0),
            'followers': data.get('followers', 0),
            'following': data.get('following', 0),
            'created_at': data.get('created_at', ''),
            'avatar_url': data.get('avatar_url', ''),
            'bio': data.get('bio', ''),
        }

    def get_contribution_stats(self):
        # This endpoint is not public, so we use events as a proxy for contributions
        if not self.username or not self.token:
            return None
        url = f'https://api.github.com/users/{self.username}/events'
        headers = {'Authorization': f'token {self.token}'}
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return None
        today = datetime.utcnow().date()
        events = response.json()
        total = 0
        for event in events:
            created_at = event.get('created_at', '')
            if created_at:
                event_date = datetime.strptime(created_at, '%Y-%m-%dT%H:%M:%SZ').date()
                if event_date == today:
                    total += 1
        return {'today': total, 'events': len(events)}
    
    def get_yearly_contributions(self):
        """
        Get a simplified mock of yearly contributions for the calendar view
        Returns a list of dicts with date and count
        """
        # This is a simplified version that uses recent events as a proxy
        # A more accurate version would require scraping GitHub's contribution graph
        if not self.username or not self.token:
            return []
            
        # Get events from GitHub API
        url = f'https://api.github.com/users/{self.username}/events'
        headers = {'Authorization': f'token {self.token}'}
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return []
            
        # Process events into daily counts
        contributions = {}
        today = datetime.utcnow().date()
        
        # Initialize the past 365 days with zero contributions
        for i in range(365):
            date = today - timedelta(days=i)
            date_str = date.strftime('%Y-%m-%d')
            contributions[date_str] = 0
            
        # Add contribution counts from events
        events = response.json()
        for event in events:
            created_at = event.get('created_at', '')
            if created_at:
                event_date = datetime.strptime(created_at, '%Y-%m-%dT%H:%M:%SZ').date()
                date_str = event_date.strftime('%Y-%m-%d')
                if date_str in contributions:
                    contributions[date_str] += 1
                    
        # Format for the calendar
        return [{'date': date, 'count': count} for date, count in contributions.items()]
