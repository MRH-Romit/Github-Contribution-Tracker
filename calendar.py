import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
import os
import tkinter as tk
from PIL import Image, ImageTk

class ContributionCalendar:
    def __init__(self, contributions=None):
        """
        Create a GitHub-style contribution calendar
        
        contributions: List of dicts with date and count
        """
        self.contributions = contributions or []
    
    def generate_past_year_dates(self):
        """Generate dates for the past year in GitHub style calendar"""
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=365)
        return [start_date + timedelta(days=i) for i in range(366)]

    def create_calendar_image(self, save_path="assets/calendar.png"):
        """Create a GitHub-style contribution calendar as image"""
        # Create data structure
        all_dates = self.generate_past_year_dates()
        
        # Create data for the heatmap
        # For demo purpose, generate some random data if no contributions are provided
        if not self.contributions:
            # Generate random data for demonstration
            counts = np.zeros(len(all_dates))
            # Add some random contributions
            for i in range(len(all_dates)):
                if np.random.random() > 0.7:  # 30% of days have contributions
                    counts[i] = np.random.randint(1, 10)
        else:
            # Use actual contributions
            counts = np.zeros(len(all_dates))
            contrib_dict = {c['date']: c['count'] for c in self.contributions}
            for i, date in enumerate(all_dates):
                date_str = date.strftime('%Y-%m-%d')
                counts[i] = contrib_dict.get(date_str, 0)

        # Create a 7x52 grid for the heatmap (7 days a week, ~52 weeks a year)
        # Initialize with zeros
        heatmap_data = np.zeros((7, 53))  # Extra column for alignment
        
        # Fill in the heatmap data
        for i, date in enumerate(all_dates):
            day_of_week = date.weekday()
            week_of_year = date.isocalendar()[1] - all_dates[0].isocalendar()[1]
            if week_of_year < 0:  # Handle year boundary
                week_of_year += 52
            if week_of_year < 53:  # Ensure it fits in our grid
                heatmap_data[day_of_week, week_of_year] = counts[i]

        # Create the plot
        plt.figure(figsize=(12, 3))
        ax = plt.gca()
        
        # Create the heatmap
        cmap = plt.cm.Greens
        im = ax.imshow(heatmap_data, cmap=cmap, aspect='auto')
        
        # Remove axis ticks
        ax.set_xticks([])
        ax.set_yticks([0, 2, 4, 6])
        ax.set_yticklabels(['Mon', 'Wed', 'Fri', ''])
        
        # Add month labels
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        month_positions = []
        current_month = all_dates[0].month
        for i, date in enumerate(all_dates):
            if date.month != current_month:
                current_month = date.month
                week_pos = (date.isocalendar()[1] - all_dates[0].isocalendar()[1])
                if week_pos < 0:  # Handle year boundary
                    week_pos += 52
                month_positions.append((week_pos, months[date.month-1]))
        
        # Place month labels
        for pos, month in month_positions:
            if 0 <= pos < 53:  # Ensure within chart bounds
                ax.text(pos, -0.8, month, ha='center')
        
        # Remove spines
        for spine in ax.spines.values():
            spine.set_visible(False)
            
        plt.title("GitHub Contributions")
        plt.tight_layout()
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        # Save the image
        plt.savefig(save_path, dpi=100, bbox_inches='tight')
        plt.close()
        return save_path    def display_in_tk_window(self, window, x=50, y=180, width=500, height=150):
        """Display the calendar in a tkinter window"""
        try:
            # Generate and save calendar image
            img_path = self.create_calendar_image()
            
            # Load and display the image
            img = Image.open(img_path)
            img = img.resize((width, height))
            photo = ImageTk.PhotoImage(img)
            
            # Create label to display image
            label = tk.Label(window, image=photo)
            label.image = photo  # Keep a reference to prevent garbage collection
            label.place(x=x, y=y)
            
            # Add title label
            title = tk.Label(window, text='GitHub Contribution Calendar')
            title.place(x=x+150, y=y-20)
            
            return label, title
        except Exception as e:
            # If error occurs, just show a placeholder text
            error_label = tk.Label(window, text=f'Could not load contribution calendar: {str(e)}')
            error_label.place(x=x+50, y=y+50)
            return error_label, None
