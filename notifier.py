from plyer import notification

class Notifier:
    @staticmethod
    def notify_no_contribution():
        notification.notify(
            title='GitHub Contribution Tracker',
            message='No GitHub contribution detected today! Make a commit to keep your streak.',
            timeout=10
        )
    
    @staticmethod
    def notify_contribution_success():
        notification.notify(
            title='GitHub Contribution Tracker',
            message='Success! You have made contributions today.',
            timeout=10
        )
        
    @staticmethod
    def notify_background_start():
        notification.notify(
            title='GitHub Contribution Tracker',
            message='Running in the background. Will check periodically.',
            timeout=5
        )
