import matplotlib.pyplot as plt
from datetime import datetime, timedelta

class Graph:
    @staticmethod
    def plot_contributions(dates, counts):
        plt.figure(figsize=(8, 3))
        plt.bar(dates, counts, color=['green' if c > 0 else 'red' for c in counts])
        plt.title('GitHub Contributions (Last 7 Days)')
        plt.xlabel('Date')
        plt.ylabel('Contributions')
        plt.tight_layout()
        plt.savefig('assets/contributions.png')
        plt.close()
