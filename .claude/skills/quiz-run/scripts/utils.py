"""Utility classes and functions for quiz application."""

import threading
import time
from typing import Callable


class QuizTimer:
    """Thread-based countdown timer for quiz sessions."""

    def __init__(self, time_limit: int, callback: Callable[[], None]):
        """
        Initialize timer.

        Args:
            time_limit: Total time in seconds (0 = unlimited)
            callback: Function to call when timer expires
        """
        self.time_limit = time_limit
        self.callback = callback
        self.running = False
        self.thread = None
        self.start_time = None
        self.elapsed = 0

    def start(self):
        """Start the countdown timer in a background thread."""
        if self.time_limit == 0:
            # No time limit, just track elapsed time
            self.start_time = time.time()
            return

        self.running = True
        self.start_time = time.time()
        self.thread = threading.Thread(target=self._countdown, daemon=True)
        self.thread.start()

    def _countdown(self):
        """Internal countdown loop running in thread."""
        while self.running and self.elapsed < self.time_limit:
            time.sleep(0.1)
            self.elapsed = time.time() - self.start_time

        if self.running:  # Timer expired (not manually stopped)
            self.running = False
            self.callback()

    def stop(self) -> float:
        """
        Stop the timer and return elapsed time.

        Returns:
            Elapsed time in seconds
        """
        self.running = False
        if self.start_time:
            self.elapsed = time.time() - self.start_time
        return self.elapsed

    def get_remaining(self) -> int:
        """
        Get remaining time in seconds.

        Returns:
            Seconds remaining (0 if no time limit or expired)
        """
        if self.time_limit == 0:
            return 0

        if not self.start_time:
            return self.time_limit

        remaining = self.time_limit - (time.time() - self.start_time)
        return max(0, int(remaining))

    def get_elapsed(self) -> float:
        """
        Get elapsed time in seconds.

        Returns:
            Seconds elapsed since start
        """
        if not self.start_time:
            return 0
        return time.time() - self.start_time

    @staticmethod
    def format_time(seconds: int) -> str:
        """
        Format seconds as MM:SS string.

        Args:
            seconds: Time in seconds

        Returns:
            Formatted string like "05:30"
        """
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes:02d}:{secs:02d}"
