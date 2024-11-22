import datetime
import os
from .observer import Observer

class LoggingObserver(Observer):
    _instance = None 

    def __new__(cls, *args, **kwargs):
        """Ensure only one instance of LoggingObserver is created."""
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        """Initialize the log file, but only the first time the instance is created."""
        if not hasattr(self, 'log_file_initialized'):  # Check if already initialized
            self.log_file = "trade_log.txt"
            # Initialize the log file only if it doesn't exist
            if not os.path.exists(self.log_file):
                with open(self.log_file, "w") as f:
                    f.write("Timestamp, Trade Details\n")
                    f.write("----------------------------\n")
            self.log_file_initialized = True  # Mark as initialized

    def update(self, message):
        """Update the log file with a new message."""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_file, "a") as f:
            if message == "Simulation complete":
                f.write(f"[{timestamp}], Simulation complete\n")
                f.write("\n")
            else:
                f.write(f"[{timestamp}] {message}\n")
                f.write("\n")
