import tkinter as tk
from datetime import datetime, timedelta
import os
import sys
from github_api import GitHubAPI

class SimpleContributionCalendar:
    def __init__(self, window, x=50, y=180):
        self.window = window
        self.x = x
        self.y = y
        self.api = GitHubAPI()
        
    def display(self):
        # Create a frame for the calendar
        frame = tk.Frame(self.window, bg='#1c1c1c', width=500, height=150)
        frame.place(x=self.x, y=self.y)
        
        # Add title
        title = tk.Label(self.window, text="GitHub Contribution Calendar", fg="white", bg="#1c1c1c")
        title.place(x=self.x+150, y=self.y-20)
        
        # Create a simple 7x52 grid for the calendar (7 days per week, 52 weeks)
        cell_size = 8
        padding = 2
        days = ["Mon", "Wed", "Fri", ""]
        
        # Create day labels
        for i, day in enumerate(days):
            if day:  # Skip empty labels
                day_label = tk.Label(self.window, text=day, fg="white", bg="#1c1c1c", font=("Arial", 8))
                day_label.place(x=self.x - 25, y=self.y + i*2*(cell_size + padding))
        
        # Create month labels
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        for i, month in enumerate(months):
            month_label = tk.Label(self.window, text=month, fg="white", bg="#1c1c1c", font=("Arial", 8))
            month_label.place(x=self.x + i*4*(cell_size + padding), y=self.y - 15)
        
        # Get contribution data - either real data from API or mock data
        try:
            contribution_data = self.api.get_yearly_contributions()
            # Convert to dictionary for easy lookup
            contribution_dict = {item['date']: item['count'] for item in contribution_data}
        except Exception:
            contribution_dict = {}  # Empty dict will trigger the fallback
            
        # Map dates to weeks and days
        today = datetime.now().date()
        cells = []
        
        # Create calendar cells
        for week in range(52):
            for day in range(7):
                # Calculate the date for this cell (going backwards from today)
                date = today - timedelta(days=(52-week-1)*7 + (6-day))
                date_str = date.strftime('%Y-%m-%d')
                
                # Get contribution count for this date
                count = contribution_dict.get(date_str, 0)
                
                # Determine activity level and color
                if count == 0:
                    color = "#0d1117"  # Dark gray/black
                elif count == 1:
                    color = "#006d32"  # Light green
                elif count <= 3:
                    color = "#26a641"  # Medium green
                else:
                    color = "#39d353"  # Bright green
                
                # Create cell with tooltip showing date and count
                cell = tk.Frame(self.window, bg=color, width=cell_size, height=cell_size)
                cell.place(x=self.x + week*(cell_size + padding), y=self.y + day*(cell_size + padding))
                
                # Add hover tooltip (using a label that appears on mouse hover)
                tooltip_text = f"{date_str}: {count} contributions"
                self.add_tooltip(cell, tooltip_text)
                
                # Store cell reference
                cells.append(cell)
                
        # Add a reference to prevent garbage collection
        self.frame = frame
        self.cells = cells
        return frame, title
    
    def add_tooltip(self, widget, text):
        """Add tooltip to any widget on hover"""
        tooltip = None
        
        def enter(event):
            nonlocal tooltip
            x, y = event.x_root + 15, event.y_root
            tooltip = tk.Toplevel(self.window)
            tooltip.wm_overrideredirect(True)  # Remove window decorations
            tooltip.wm_geometry(f"+{x}+{y}")
            label = tk.Label(tooltip, text=text, bg="#2d333b", fg="white", 
                           relief="solid", borderwidth=1, padx=2, pady=2, font=("Arial", 8))
            label.pack()
            
        def leave(event):
            nonlocal tooltip
            if tooltip:
                tooltip.destroy()
                tooltip = None
                
        widget.bind("<Enter>", enter)
        widget.bind("<Leave>", leave)
