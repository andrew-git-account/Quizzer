"""Question page UI for displaying and answering questions."""

import tkinter as tk
from tkinter import ttk
from typing import Callable, List, Optional
from models import Question


class QuestionPage(tk.Frame):
    """Page for displaying a quiz question and handling user interaction."""

    def __init__(self, parent, question: Question, question_num: int,
                 total_questions: int, mode: str, timer_remaining: int,
                 previous_answer: Optional[List[int]],
                 show_previous: bool, show_next: bool,
                 previous_callback: Optional[Callable[[], None]],
                 next_callback: Optional[Callable[[], None]],
                 confirm_callback: Callable[[List[int]], None],
                 answered_questions: Optional[List[int]] = None,
                 correctly_answered_questions: Optional[List[int]] = None,
                 incorrectly_answered_questions: Optional[List[int]] = None,
                 jump_to_question_callback: Optional[Callable[[int], None]] = None):
        """
        Initialize question page.

        Args:
            parent: Parent tkinter widget
            question: Question object to display
            question_num: Current question number (1-indexed)
            total_questions: Total number of questions in quiz
            mode: Quiz mode ('learning' or 'exam')
            timer_remaining: Seconds remaining (0 if no timer)
            previous_answer: Previously selected answer IDs (for read-only review)
            show_previous: Whether to show Previous button
            show_next: Whether to show Next button
            previous_callback: Function to call on Previous click
            next_callback: Function to call on Next click
            confirm_callback: Function to call on Confirm click with selected IDs
            answered_questions: List of question indices (0-based) that have been answered
            correctly_answered_questions: List of question indices that were answered correctly
            incorrectly_answered_questions: List of question indices that were answered incorrectly
            jump_to_question_callback: Function to jump to question by index (0-based)
        """
        super().__init__(parent)
        self.question = question
        self.question_num = question_num
        self.total_questions = total_questions
        self.mode = mode
        self.timer_remaining = timer_remaining
        self.previous_answer = previous_answer
        self.show_previous = show_previous
        self.show_next = show_next
        self.previous_callback = previous_callback
        self.next_callback = next_callback
        self.confirm_callback = confirm_callback
        self.answered_questions = answered_questions if answered_questions else []
        self.correctly_answered_questions = correctly_answered_questions if correctly_answered_questions else []
        self.incorrectly_answered_questions = incorrectly_answered_questions if incorrectly_answered_questions else []
        self.jump_to_question_callback = jump_to_question_callback

        # State
        self.is_review_mode = previous_answer is not None
        self.selected_options = previous_answer if previous_answer else []
        self.answered = False
        self.option_vars = {}  # {option_id: IntVar or BooleanVar}
        self.option_frames = {}  # {option_id: Frame} for inline feedback

        self._create_widgets()

    def _create_widgets(self):
        """Create and layout all widgets."""
        # Main container
        container = tk.Frame(self, padx=30, pady=20)
        container.pack(expand=True, fill=tk.BOTH)

        # Header with timer and progress
        header_frame = tk.Frame(container)
        header_frame.pack(fill=tk.X, pady=(0, 10))

        # Progress
        progress_label = tk.Label(
            header_frame,
            text=f"Question {self.question_num} of {self.total_questions}",
            font=('Arial', 11, 'bold')
        )
        progress_label.pack(side=tk.LEFT)

        # Timer (if enabled)
        if self.timer_remaining > 0:
            from utils import QuizTimer
            timer_text = QuizTimer.format_time(self.timer_remaining)
            timer_label = tk.Label(
                header_frame,
                text=f"Time: {timer_text}",
                font=('Arial', 11, 'bold'),
                fg='red' if self.timer_remaining < 60 else 'black'
            )
            timer_label.pack(side=tk.RIGHT)

        # Question navigation buttons (learning mode only)
        if self.mode == 'learning' and self.jump_to_question_callback:
            nav_buttons_frame = tk.Frame(container)
            nav_buttons_frame.pack(fill=tk.X, pady=(0, 15))

            for i in range(self.total_questions):
                # Determine button styling based on state
                is_current = (i == self.question_num - 1)
                is_correct = i in self.correctly_answered_questions
                is_incorrect = i in self.incorrectly_answered_questions

                if is_current:
                    bg_color = '#2196F3'  # Blue for current
                    fg_color = 'white'
                    relief = tk.SUNKEN
                elif is_correct:
                    bg_color = '#4CAF50'  # Green for correctly answered
                    fg_color = 'white'
                    relief = tk.RAISED
                elif is_incorrect:
                    bg_color = '#F44336'  # Red for incorrectly answered
                    fg_color = 'white'
                    relief = tk.RAISED
                else:
                    bg_color = '#E0E0E0'  # Gray for unanswered
                    fg_color = 'black'
                    relief = tk.RAISED

                btn = tk.Button(
                    nav_buttons_frame,
                    text=str(i + 1),
                    width=3,
                    bg=bg_color,
                    fg=fg_color,
                    relief=relief,
                    command=lambda idx=i: self.jump_to_question_callback(idx),
                    cursor='hand2'
                )
                btn.pack(side=tk.LEFT, padx=2)

        # Domain
        if self.question.domain:
            domain_label = tk.Label(
                container,
                text=f"Domain: {self.question.domain}",
                font=('Arial', 10),
                fg='gray'
            )
            domain_label.pack(anchor='w', pady=(0, 10))

        # Question text
        question_label = tk.Label(
            container,
            text=self.question.question,
            font=('Arial', 14, 'bold'),
            wraplength=650,
            justify=tk.LEFT
        )
        question_label.pack(anchor='w', pady=(0, 20))

        # Options frame - will contain options and inline feedback
        self.options_container = tk.Frame(container)
        self.options_container.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

        self._create_options(self.options_container)

        # Show feedback if in review mode
        if self.is_review_mode:
            self._show_feedback()

        # Navigation buttons
        nav_frame = tk.Frame(container)
        nav_frame.pack(pady=20)

        if self.show_previous and not self.is_review_mode:
            prev_button = tk.Button(
                nav_frame,
                text="Previous",
                command=self.previous_callback,
                font=('Arial', 12),
                padx=20,
                pady=5
            )
            prev_button.pack(side=tk.LEFT, padx=5)

        if not self.is_review_mode:
            self.confirm_button = tk.Button(
                nav_frame,
                text="Confirm Answer",
                command=self._on_confirm_clicked,
                font=('Arial', 12, 'bold'),
                bg='#2196F3',
                fg='white',
                padx=20,
                pady=5,
                cursor='hand2'
            )
            self.confirm_button.pack(side=tk.LEFT, padx=5)

        if self.show_next:
            next_button = tk.Button(
                nav_frame,
                text="Next",
                command=self.next_callback,
                font=('Arial', 12),
                padx=20,
                pady=5
            )
            next_button.pack(side=tk.LEFT, padx=5)

    def _create_options(self, parent):
        """Create option widgets (radio buttons or checkboxes) with frames for feedback."""
        if self.question.is_multi_select:
            # Checkboxes for multi-select
            for option in self.question.options:
                # Create frame for each option
                option_frame = tk.Frame(parent)
                option_frame.pack(anchor='w', fill=tk.X, pady=2)
                self.option_frames[option.id] = option_frame

                var = tk.BooleanVar(value=option.id in self.selected_options)
                self.option_vars[option.id] = var

                cb = tk.Checkbutton(
                    option_frame,
                    text=option.answer,
                    variable=var,
                    font=('Arial', 12),
                    wraplength=600,
                    justify=tk.LEFT,
                    state=tk.DISABLED if self.is_review_mode else tk.NORMAL
                )
                cb.pack(anchor='w')
        else:
            # Radio buttons for single-select
            selected_var = tk.IntVar(
                value=self.selected_options[0] if self.selected_options else -1
            )
            self.option_vars['selected'] = selected_var

            for option in self.question.options:
                # Create frame for each option
                option_frame = tk.Frame(parent)
                option_frame.pack(anchor='w', fill=tk.X, pady=2)
                self.option_frames[option.id] = option_frame

                rb = tk.Radiobutton(
                    option_frame,
                    text=option.answer,
                    variable=selected_var,
                    value=option.id,
                    font=('Arial', 12),
                    wraplength=600,
                    justify=tk.LEFT,
                    state=tk.DISABLED if self.is_review_mode else tk.NORMAL
                )
                rb.pack(anchor='w')

    def _get_selected_ids(self) -> List[int]:
        """Get currently selected option IDs."""
        if self.question.is_multi_select:
            return [opt_id for opt_id, var in self.option_vars.items() if var.get()]
        else:
            selected = self.option_vars['selected'].get()
            return [selected] if selected != -1 else []

    def _on_confirm_clicked(self):
        """Handle Confirm button click."""
        selected_ids = self._get_selected_ids()

        if not selected_ids:
            tk.messagebox.showwarning(
                "No Answer Selected",
                "Please select at least one answer before confirming."
            )
            return

        self.answered = True
        self.selected_options = selected_ids

        # Remove the Confirm button after answering
        self.confirm_button.pack_forget()

        # Show feedback in learning mode
        if self.mode == 'learning':
            self._show_feedback()

        # Call callback
        self.confirm_callback(selected_ids)

    def _show_feedback(self):
        """Display feedback inline after the selected answer(s)."""
        # Check if correct
        is_correct = self.question.is_correct(self.selected_options)

        # Show feedback under each selected option
        for selected_id in self.selected_options:
            if selected_id in self.option_frames:
                option_frame = self.option_frames[selected_id]
                option = self.question.get_option_by_id(selected_id)

                # Determine if this selected answer is correct
                is_correct_answer = selected_id in self.question.correct_answer_ids

                # Build feedback text
                if is_correct_answer:
                    feedback_text = "Correct! "
                    fg_color = 'green'
                else:
                    feedback_text = "Incorrect. "
                    fg_color = 'red'

                # Add explanation if available
                if option.explanation:
                    feedback_text += option.explanation

                # Create feedback label indented under the option
                feedback_label = tk.Label(
                    option_frame,
                    text=feedback_text,
                    font=('Arial', 11),
                    fg=fg_color,
                    wraplength=580,
                    justify=tk.LEFT
                )
                feedback_label.pack(anchor='w', padx=(30, 0), pady=(2, 8))
