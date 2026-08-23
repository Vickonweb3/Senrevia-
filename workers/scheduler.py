# Background task scheduler
# Manages scheduled tasks and background jobs

from apscheduler.schedulers.background import BackgroundScheduler

class TaskScheduler:
    """Background task scheduler."""
    
    def __init__(self):
        self.scheduler = BackgroundScheduler()
    
    def start(self):
        """Start the scheduler."""
        self.scheduler.start()
