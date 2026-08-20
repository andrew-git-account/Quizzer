# Quizzer

A Python-based interactive quiz application with tkinter GUI.

## Features

- **Two Quiz Modes**:
  - **Learning Mode**: Immediate feedback after each answer, with Previous button for review
  - **Exam Mode**: All feedback deferred to end, no Previous button, must answer to proceed

- **Flexible Question Types**:
  - Single-select (radio buttons)
  - Multi-select (checkboxes) - auto-detected from quiz definition
  - Strict correctness checking: all correct answers must be selected for multi-select

- **Smart Navigation** (Learning Mode):
  - Clickable question buttons [1][2][3]... for quick navigation
  - Color-coded status: Blue (current), Green (correct), Red (incorrect), Gray (unanswered)

- **Inline Feedback**: Correct/incorrect messages appear directly under selected answers with explanations

- **Clean UI**: Confirm button automatically disappears after answering

- **Timer Support**: Optional countdown timer with auto-stop

- **Interactive Start Page**: Configure question count, mode, and time before starting

- **Result Tracking**: JSON output with score and time statistics

## Quick Start

### Running a Quiz

Using the Claude Code skill:
```bash
/quiz-run quizzes/sample_quiz.json
/quiz-run quizzes/sample_quiz.json --mode=exam --time=600
```

Direct Python execution:
```bash
cd .claude/skills/quiz-run/scripts
python quiz_runner.py ../../../../quizzes/sample_quiz.json
```

### Testing

Run component tests:
```bash
cd .claude/skills/quiz-run/scripts
python test_quiz.py
```

## Quiz File Format

Quiz definitions are JSON files:

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
          "answer": "Option text",
          "explanation": "Explanation text"
        }
      ],
      "correctAnswerIds": [1]
    }
  ]
}
```

- Single correct answer: `"correctAnswerIds": [1]` → radio buttons
- Multiple correct answers: `"correctAnswerIds": [1, 3]` → checkboxes

See `quizzes/sample_quiz.json` for a complete example.

## Project Structure

```
.claude/skills/quiz-run/
├── SKILL.md              # Skill definition
└── scripts/
    ├── quiz_runner.py    # CLI entry point
    ├── quiz_app.py       # Main application
    ├── models.py         # Data models
    ├── utils.py          # Timer utility
    ├── test_quiz.py      # Component tests
    └── ui/
        ├── start_page.py     # Start configuration
        ├── question_page.py  # Question display
        └── results_page.py   # Results summary

quizzes/
└── sample_quiz.json      # Example quiz

CLAUDE.md                 # Development guidance
```

## Requirements

- Python 3.7+ (uses dataclasses)
- tkinter (built-in with Python)
- No external dependencies required

## Command Line Options

```
python quiz_runner.py <quiz-file> [--mode MODE] [--time SECONDS]

Arguments:
  quiz-file              Path to quiz JSON file (required)
  --mode {learning,exam} Quiz mode (default: learning)
  --time SECONDS         Time limit in seconds, 0=unlimited (default: 0)
```

## Output

Quiz results are printed to stdout as JSON:

```json
{
  "total_questions": 10,
  "correct_answers": 8,
  "time_used_seconds": 245.6
}
```

## Quiz Creation

The **quiz-agent** helps convert various formats into quiz files:

### Convert Incompatible JSON
```bash
# In Claude Code conversation
"Convert quiz_data.json to quiz format"
```

The agent will:
1. Read and analyze the source file
2. Ask for missing fields (title, domain) with defaults
3. Convert to quiz-run compatible format
4. Validate using quiz-run models
5. Save to `quizzes/` directory

### Extract from Images
```bash
# In Claude Code conversation  
"Extract quiz from screenshot.png"
```

The agent will:
1. Use Claude vision to read quiz questions from images
2. Extract questions, answers, and correct answer indicators
3. Ask for confirmation of extracted content
4. Build and validate quiz JSON
5. Save for immediate use

### Agent Features
- Interactive prompts with sensible defaults
- Validates all output before saving
- Preserves explanations only if present in source
- Handles multi-select questions automatically
- No external dependencies (uses Claude vision)
