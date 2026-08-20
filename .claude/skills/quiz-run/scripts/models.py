"""Data models for quiz application."""

import json
from dataclasses import dataclass
from pathlib import Path
from typing import List


@dataclass
class QuizOption:
    """Represents a single answer option in a question."""
    id: int
    answer: str
    explanation: str

    @classmethod
    def from_dict(cls, data: dict) -> 'QuizOption':
        return cls(
            id=data['id'],
            answer=data['answer'],
            explanation=data['explanation']
        )


@dataclass
class Question:
    """Represents a single quiz question."""
    id: int
    domain: str
    question: str
    options: List[QuizOption]
    correct_answer_ids: List[int]

    @property
    def is_multi_select(self) -> bool:
        """Returns True if question has multiple correct answers."""
        return len(self.correct_answer_ids) > 1

    @classmethod
    def from_dict(cls, data: dict) -> 'Question':
        return cls(
            id=data['id'],
            domain=data['domain'],
            question=data['question'],
            options=[QuizOption.from_dict(opt) for opt in data['options']],
            correct_answer_ids=data['correctAnswerIds']
        )

    def is_correct(self, selected_ids: List[int]) -> bool:
        """Check if the selected answer IDs are correct."""
        return sorted(selected_ids) == sorted(self.correct_answer_ids)

    def get_option_by_id(self, option_id: int) -> QuizOption:
        """Get an option by its ID."""
        for option in self.options:
            if option.id == option_id:
                return option
        raise ValueError(f"Option ID {option_id} not found")


@dataclass
class Quiz:
    """Represents a complete quiz with metadata and questions."""
    title: str
    questions: List[Question]

    @classmethod
    def from_file(cls, path: Path) -> 'Quiz':
        """Load quiz from JSON file."""
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        return cls(
            title=data['title'],
            questions=[Question.from_dict(q) for q in data['questions']]
        )


@dataclass
class QuizResult:
    """Represents the result of a completed quiz."""
    total_questions: int
    correct_answers: int
    time_used_seconds: float

    def to_json(self) -> str:
        """Convert result to JSON string."""
        return json.dumps({
            'total_questions': self.total_questions,
            'correct_answers': self.correct_answers,
            'time_used_seconds': round(self.time_used_seconds, 1)
        }, indent=2)

    @property
    def score_percentage(self) -> float:
        """Calculate score as percentage."""
        if self.total_questions == 0:
            return 0.0
        return (self.correct_answers / self.total_questions) * 100
