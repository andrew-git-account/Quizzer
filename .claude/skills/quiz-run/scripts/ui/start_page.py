"""Start page UI for quiz configuration."""

import tkinter as tk
from tkinter import ttk
from typing import Callable


class StartPage(tk.Frame):
    """Initial configuration page shown before quiz starts."""

    def __init__(self, parent, quiz_title: str, total_questions: int,
                 initial_mode: str, initial_time: int,
                 start_callback: Callable[[int, str, int], None]):
        """
        Initialize start page.

        Args:
            parent: Parent tkinter widget
            quiz_title: Title of the quiz
            total_questions: Total number of questions available
            initial_mode: Initial quiz mode ('learning' or 'exam')
            initial_time: Initial time limit in seconds
            start_callback: Function to call when Start button clicked
                           with (num_questions, mode, time_limit)
        """
        super().__init__(parent)
        self.quiz_title = quiz_title
        self.total_questions = total_questions
        self.start_callback = start_callback

        # Variables
        self.num_questions_var = tk.IntVar(value=total_questions)
        self.mode_var = tk.StringVar(value=initial_mode)
        self.time_var = tk.IntVar(value=initial_time)

        self._create_widgets()

    def _create_widgets(self):
        """Create and layout all widgets."""
        # Main container with padding
        container = tk.Frame(self, padx=40, pady=40)
        container.pack(expand=True, fill=tk.BOTH)

        # Title
        title_label = tk.Label(
            container,
            text=self.quiz_title,
            font=('Arial', 20, 'bold'),
            wraplength=500
        )
        title_label.pack(pady=(0, 30))

        # Configuration frame
        config_frame = tk.Frame(container)
        config_frame.pack(pady=20)

        # Number of questions
        questions_frame = tk.Frame(config_frame)
        questions_frame.pack(pady=10, anchor='w')

        tk.Label(
            questions_frame,
            text="Number of questions:",
            font=('Arial', 12)
        ).pack(side=tk.LEFT, padx=(0, 10))

        questions_spinbox = tk.Spinbox(
            questions_frame,
            from_=1,
            to=self.total_questions,
            textvariable=self.num_questions_var,
            width=10,
            font=('Arial', 12)
        )
        questions_spinbox.pack(side=tk.LEFT)

        tk.Label(
            questions_frame,
            text=f"(available: {self.total_questions})",
            font=('Arial', 10),
            fg='gray'
        ).pack(side=tk.LEFT, padx=(10, 0))

        # Quiz mode
        mode_frame = tk.Frame(config_frame)
        mode_frame.pack(pady=10, anchor='w')

        tk.Label(
            mode_frame,
            text="Quiz mode:",
            font=('Arial', 12)
        ).pack(side=tk.LEFT, padx=(0, 10))

        learning_radio = tk.Radiobutton(
            mode_frame,
            text="Learning (immediate feedback)",
            variable=self.mode_var,
            value='learning',
            font=('Arial', 11)
        )
        learning_radio.pack(side=tk.LEFT, padx=(0, 20))

        exam_radio = tk.Radiobutton(
            mode_frame,
            text="Exam (feedback at end)",
            variable=self.mode_var,
            value='exam',
            font=('Arial', 11)
        )
        exam_radio.pack(side=tk.LEFT)

        # Time limit
        time_frame = tk.Frame(config_frame)
        time_frame.pack(pady=10, anchor='w')

        tk.Label(
            time_frame,
            text="Time limit (seconds):",
            font=('Arial', 12)
        ).pack(side=tk.LEFT, padx=(0, 10))

        time_spinbox = tk.Spinbox(
            time_frame,
            from_=0,
            to=7200,
            increment=60,
            textvariable=self.time_var,
            width=10,
            font=('Arial', 12)
        )
        time_spinbox.pack(side=tk.LEFT)

        tk.Label(
            time_frame,
            text="(0 = unlimited)",
            font=('Arial', 10),
            fg='gray'
        ).pack(side=tk.LEFT, padx=(10, 0))

        # Start button
        start_button = tk.Button(
            container,
            text="Start Quiz",
            command=self._on_start_clicked,
            font=('Arial', 14, 'bold'),
            bg='#4CAF50',
            fg='white',
            padx=30,
            pady=10,
            cursor='hand2'
        )
        start_button.pack(pady=30)

    def _on_start_clicked(self):
        """Handle Start button click."""
        num_questions = self.num_questions_var.get()
        mode = self.mode_var.get()
        time_limit = self.time_var.get()

        # Validate
        if num_questions < 1 or num_questions > self.total_questions:
            tk.messagebox.showerror(
                "Invalid Input",
                f"Number of questions must be between 1 and {self.total_questions}"
            )
            return

        if time_limit < 0:
            tk.messagebox.showerror(
                "Invalid Input",
                "Time limit cannot be negative"
            )
            return

        self.start_callback(num_questions, mode, time_limit)
