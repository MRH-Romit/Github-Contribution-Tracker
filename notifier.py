from plyer import notification

class Notifier:
    @staticmethod
    def notify_no_contribution():
        notification.notify(
            title='GitHub Contribution Tracker',
            message='No GitHub contribution detected today! Make a commit to keep your streak.',
            timeout=10
        )
