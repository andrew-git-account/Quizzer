---
name: quiz-run
description: Execute an interactive quiz with tkinter GUI. Features color-coded navigation, inline feedback, learning/exam modes, timers, multi-select questions.
argument-hint: <quiz-file-path> [--mode=learning|exam] [--time=<seconds>]
allowed-tools:
  - Bash(python *)
  - Bash(python3 *)
---

# quiz-run

Executes an interactive quiz session from a JSON configuration file.

## Usage

```
/quiz-run path/to/quiz.json
/quiz-run path/to/quiz.json --mode=exam --time=600
```

## Parameters

- **quiz-file-path** (required): Path to quiz JSON file
- **--mode** (optional): 'learning' (default) or 'exam'
  - Learning: Shows correct answers immediately, clickable question navigation bar, Previous button
  - Exam: No immediate feedback, no navigation bar, must answer to proceed, no Previous
- **--time** (optional): Time limit in seconds, 0 (default) = unlimited
  - Countdown timer displayed, auto-stops when expired

## UI Features

- **Question Navigation Bar** (learning mode): Clickable buttons [1][2][3]...
  - 🔵 Blue = current question
  - 🟢 Green = correctly answered
  - 🔴 Red = incorrectly answered
  - ⚪ Gray = unanswered
- **Inline Feedback**: Appears directly under selected answer with explanation
- **Auto-hide Confirm Button**: Disappears after answering
- **Multi-select Support**: Requires ALL correct answers to be selected

## Quiz File Format

JSON structure:
```json
{
  "title": "Quiz Title",
  "questions": [
    {
      "id": 1,
      "domain": "Topic Area",
      "question": "Question text?",
      "options": [
        {
          "id": 1,
          "answer": "Option A",
          "explanation": "Explanation for this option"
        }
      ],
      "correctAnswerIds": [1]
    }
  ]
}
```

See `/quizzes/sample_quiz.json` for a complete example.

## Output

JSON object printed to stdout:
```json
{
  "total_questions": 10,
  "correct_answers": 8,
  "time_used_seconds": 245.3
}
```

## Implementation

Launches Python tkinter application via `scripts/quiz_runner.py`.
