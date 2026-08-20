"""Main quiz application with tkinter GUI."""

import tkinter as tk
from tkinter import messagebox
import random
from typing import List, Optional
from models import Quiz, QuizResult, Question
from utils import QuizTimer
from ui import StartPage, QuestionPage, ResultsPage


class QuizApp:
    """Main application orchestrating the quiz flow."""

    def __init__(self, quiz: Quiz, mode: str, time_limit: int):
        """
        Initialize quiz application.

        Args:
            quiz: Quiz object with questions
            mode: Quiz mode ('learning' or 'exam')
            time_limit: Time limit in seconds (0 = unlimited)
        """
        self.quiz = quiz
        self.mode = mode
        self.time_limit = time_limit

        # State
        self.selected_questions: List[Question] = []
        self.current_question_idx = 0
        self.user_answers = {}  # {question_id: [selected_option_ids]}
        self.answer_correctness = {}  # {question_id: bool} - True if correct, False if incorrect
        self.timer: Optional[QuizTimer] = None
        self.result: Optional[QuizResult] = None
        self.quiz_started = False

        # UI
        self.root = tk.Tk()
        self.root.title("Quiz Application")
        self.root.geometry("800x600")
        self.root.resizable(True, True)

        # Current page container
        self.current_page = None

    def run(self) -> QuizResult:
        """
        Start the application and show start page.

        Returns:
            QuizResult after quiz completion
        """
        self._show_start_page()
        self.root.mainloop()
        return self.result

    def _show_start_page(self):
        """Display the start configuration page."""
        self._clear_current_page()

        self.current_page = StartPage(
            self.root,
            quiz_title=self.quiz.title,
            total_questions=len(self.quiz.questions),
            initial_mode=self.mode,
            initial_time=self.time_limit,
            start_callback=self._on_quiz_start
        )
        self.current_page.pack(expand=True, fill=tk.BOTH)

    def _on_quiz_start(self, num_questions: int, mode: str, time_limit: int):
        """
        Handle quiz start from start page.

        Args:
            num_questions: Number of questions to include
            mode: Quiz mode selected
            time_limit: Time limit selected
        """
        # Update settings
        self.mode = mode
        self.time_limit = time_limit

        # Select questions randomly if needed
        if num_questions < len(self.quiz.questions):
            self.selected_questions = random.sample(
                self.quiz.questions,
                num_questions
            )
        else:
            self.selected_questions = self.quiz.questions.copy()

        # Start timer if needed
        if self.time_limit > 0:
            self.timer = QuizTimer(self.time_limit, self._on_time_expired)
            self.timer.start()

        self.quiz_started = True
        self.current_question_idx = 0

        # Show first question
        self._show_question(0)

    def _show_question(self, idx: int):
        """
        Display question at given index.

        Args:
            idx: Index in selected_questions list
        """
        if idx < 0 or idx >= len(self.selected_questions):
            return

        self.current_question_idx = idx
        question = self.selected_questions[idx]

        # Get previous answer if viewing in learning mode
        previous_answer = None
        if question.id in self.user_answers and self.mode == 'learning':
            previous_answer = self.user_answers[question.id]

        # Determine button visibility
        show_previous = (
            self.mode == 'learning' and
            idx > 0
        )

        show_next = (
            self.mode == 'learning' or
            question.id in self.user_answers
        )

        # Get timer remaining
        timer_remaining = 0
        if self.timer:
            timer_remaining = self.timer.get_remaining()

        # Get list of answered question indices and their correctness
        answered_indices = []
        correctly_answered_indices = []
        incorrectly_answered_indices = []

        for i, q in enumerate(self.selected_questions):
            if q.id in self.user_answers:
                answered_indices.append(i)
                if self.answer_correctness.get(q.id, False):
                    correctly_answered_indices.append(i)
                else:
                    incorrectly_answered_indices.append(i)

        self._clear_current_page()

        self.current_page = QuestionPage(
            self.root,
            question=question,
            question_num=idx + 1,
            total_questions=len(self.selected_questions),
            mode=self.mode,
            timer_remaining=timer_remaining,
            previous_answer=previous_answer,
            show_previous=show_previous,
            show_next=show_next,
            previous_callback=lambda: self._on_previous_clicked(),
            next_callback=lambda: self._on_next_clicked(),
            confirm_callback=lambda selected_ids: self._on_answer_confirmed(
                question.id, selected_ids
            ),
            answered_questions=answered_indices,
            correctly_answered_questions=correctly_answered_indices,
            incorrectly_answered_questions=incorrectly_answered_indices,
            jump_to_question_callback=lambda idx: self._show_question(idx)
        )
        self.current_page.pack(expand=True, fill=tk.BOTH)

    def _on_previous_clicked(self):
        """Handle Previous button click."""
        if self.current_question_idx > 0:
            self._show_question(self.current_question_idx - 1)

    def _on_next_clicked(self):
        """Handle Next button click."""
        if self.current_question_idx < len(self.selected_questions) - 1:
            self._show_question(self.current_question_idx + 1)
        else:
            # Last question, finish quiz
            self._finish_quiz()

    def _on_answer_confirmed(self, question_id: int, selected_ids: List[int]):
        """
        Handle answer confirmation.

        Args:
            question_id: ID of the question answered
            selected_ids: List of selected option IDs
        """
        # Store answer
        self.user_answers[question_id] = selected_ids

        # Check if answer is correct and store correctness
        question = next(q for q in self.selected_questions if q.id == question_id)
        self.answer_correctness[question_id] = question.is_correct(selected_ids)

        # In exam mode, auto-advance to next question
        if self.mode == 'exam':
            if self.current_question_idx < len(self.selected_questions) - 1:
                # Schedule next question after short delay
                self.root.after(300, lambda: self._on_next_clicked())
            else:
                # Last question in exam mode
                self.root.after(300, self._finish_quiz)

    def _on_time_expired(self):
        """Handle timer expiration."""
        # Use thread-safe method to show message and finish
        self.root.after(0, self._handle_timeout)

    def _handle_timeout(self):
        """Handle timeout in main thread."""
        messagebox.showinfo(
            "Time's Up!",
            "The time limit has been reached. The quiz will now end."
        )
        self._finish_quiz()

    def _finish_quiz(self):
        """Calculate results and show results page."""
        # Stop timer
        time_used = 0
        if self.timer:
            time_used = self.timer.stop()
        else:
            # No timer, calculate time from first question shown
            time_used = 0  # Could track start time separately if needed

        # Calculate score
        correct_count = 0
        for question in self.selected_questions:
            if question.id in self.user_answers:
                if question.is_correct(self.user_answers[question.id]):
                    correct_count += 1

        # Create result
        self.result = QuizResult(
            total_questions=len(self.selected_questions),
            correct_answers=correct_count,
            time_used_seconds=time_used
        )

        # Show results page
        self._show_results_page()

    def _show_results_page(self):
        """Display the results page."""
        self._clear_current_page()

        self.current_page = ResultsPage(
            self.root,
            result=self.result,
            close_callback=self._on_close
        )
        self.current_page.pack(expand=True, fill=tk.BOTH)

    def _on_close(self):
        """Handle application close."""
        self.root.quit()
        self.root.destroy()

    def _clear_current_page(self):
        """Remove current page from display."""
        if self.current_page:
            self.current_page.destroy()
            self.current_page = None
