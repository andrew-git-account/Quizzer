"""Results page UI for displaying quiz completion summary."""

import tkinter as tk
from typing import Callable
from models import QuizResult


class ResultsPage(tk.Frame):
    """Final page showing quiz results and score."""

    def __init__(self, parent, result: QuizResult,
                 close_callback: Callable[[], None]):
        """
        Initialize results page.

        Args:
            parent: Parent tkinter widget
            result: QuizResult object with score data
            close_callback: Function to call when Close button clicked
        """
        super().__init__(parent)
        self.result = result
        self.close_callback = close_callback

        self._create_widgets()

    def _create_widgets(self):
        """Create and layout all widgets."""
        # Main container with padding
        container = tk.Frame(self, padx=50, pady=50)
        container.pack(expand=True, fill=tk.BOTH)

        # Title
        title_label = tk.Label(
            container,
            text="Quiz Complete!",
            font=('Arial', 24, 'bold'),
            fg='#2196F3'
        )
        title_label.pack(pady=(0, 40))

        # Results frame
        results_frame = tk.Frame(container)
        results_frame.pack(pady=20)

        # Score
        score_text = (
            f"You answered {self.result.correct_answers} out of "
            f"{self.result.total_questions} questions correctly"
        )
        score_label = tk.Label(
            results_frame,
            text=score_text,
            font=('Arial', 16),
            wraplength=500
        )
        score_label.pack(pady=10)

        # Percentage
        percentage_label = tk.Label(
            results_frame,
            text=f"{self.result.score_percentage:.1f}%",
            font=('Arial', 36, 'bold'),
            fg=self._get_score_color()
        )
        percentage_label.pack(pady=20)

        # Time
        minutes = int(self.result.time_used_seconds // 60)
        seconds = int(self.result.time_used_seconds % 60)
        time_text = f"Time: {minutes:02d}:{seconds:02d}"
        time_label = tk.Label(
            results_frame,
            text=time_text,
            font=('Arial', 14),
            fg='gray'
        )
        time_label.pack(pady=10)

        # Performance message
        message = self._get_performance_message()
        message_label = tk.Label(
            results_frame,
            text=message,
            font=('Arial', 12, 'italic'),
            fg='gray'
        )
        message_label.pack(pady=20)

        # Close button
        close_button = tk.Button(
            container,
            text="Close",
            command=self.close_callback,
            font=('Arial', 14, 'bold'),
            bg='#4CAF50',
            fg='white',
            padx=40,
            pady=10,
            cursor='hand2'
        )
        close_button.pack(pady=30)

    def _get_score_color(self) -> str:
        """Get color based on score percentage."""
        percentage = self.result.score_percentage
        if percentage >= 90:
            return '#4CAF50'  # Green
        elif percentage >= 70:
            return '#FFC107'  # Yellow/Orange
        else:
            return '#F44336'  # Red

    def _get_performance_message(self) -> str:
        """Get encouraging message based on performance."""
        percentage = self.result.score_percentage

        if percentage == 100:
            return "Perfect score! Outstanding! 🌟"
        elif percentage >= 90:
            return "Excellent work! You've mastered this topic!"
        elif percentage >= 80:
            return "Great job! You have a strong understanding."
        elif percentage >= 70:
            return "Good effort! Keep practicing to improve."
        elif percentage >= 60:
            return "Not bad! Review the material and try again."
        else:
            return "Keep studying! You'll do better next time."
