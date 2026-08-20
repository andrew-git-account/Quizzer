# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Quizzer is a Python-based quiz application with two core components:
- **quiz-run**: ✓ IMPLEMENTED - A skill that executes quizzes based on provided parameters
- **quiz-agent**: TODO - An agent that generates quiz content based on user input

## Current Status (as of 2026-08-20)

**Completed:**
- ✓ quiz-run skill fully implemented with tkinter GUI
- ✓ Start page with configurable settings (question count, mode, time limit)
- ✓ Learning mode (immediate feedback + Previous button)
- ✓ Exam mode (deferred feedback, no Previous button)
- ✓ Multi-select question support (auto-detected from correctAnswerIds)
- ✓ Countdown timer with auto-stop functionality
- ✓ Random question selection
- ✓ Results page with score percentage and time tracking
- ✓ JSON output to stdout
- ✓ Component test suite
- ✓ Sample quiz file with 10 Python questions
- ✓ Question navigation bar with clickable buttons (learning mode only)
- ✓ Color-coded question buttons (blue=current, green=correct, red=incorrect, gray=unanswered)
- ✓ Inline feedback display (appears directly after selected answer)
- ✓ Auto-removal of Confirm button after answering

**Completed (2026-08-20):**
- ✓ quiz-agent for converting and extracting quiz questions from various formats

## Architecture

### Component Structure

**quiz-run skill** ✓ IMPLEMENTED (`/.claude/skills/quiz-run/`)
- Executes quiz sessions via tkinter GUI
- Handles user interaction during quiz runtime
- Scores and reports results
- Takes quiz definition as input parameter
- **Files**: SKILL.md, quiz_runner.py (entry point), quiz_app.py (main app), models.py (data), utils.py (timer), ui/ (pages), test_quiz.py

**quiz-agent** ✓ IMPLEMENTED (`/.claude/agents/quiz-agent.md`)
- Converts incompatible JSON formats to quiz-run format
- Extracts quiz questions from images/screenshots using Claude vision
- Interactive prompts for missing fields (title, domain) with defaults
- Validates output using quiz-run models before saving
- Preserves explanations only if present in source
- Saves to `/quizzes/` directory for immediate use with quiz-run

### Quiz Data Format

Quiz definitions are JSON files with the following structure:

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
          "explanation": "Why this is/isn't correct"
        }
      ],
      "correctAnswerIds": [1]
    }
  ]
}
```

- **Single-select**: `correctAnswerIds` has one ID → renders as radio buttons
- **Multi-select**: `correctAnswerIds` has multiple IDs → renders as checkboxes
- All fields are required
- See `/quizzes/sample_quiz.json` for a complete example

## Development Commands

### Running a Quiz
```bash
# Via skill invocation in Claude Code
/quiz-run quizzes/sample_quiz.json
/quiz-run quizzes/sample_quiz.json --mode=exam --time=600

# Direct Python execution
cd .claude/skills/quiz-run/scripts
python quiz_runner.py ../../../../quizzes/sample_quiz.json

# Test components without GUI
cd .claude/skills/quiz-run/scripts
python test_quiz.py
```

**Parameters:**
- `--mode`: `learning` (default, immediate feedback) or `exam` (deferred feedback)
- `--time`: Time limit in seconds, 0 (default) = unlimited

### Generating a Quiz
```bash
# NOT YET IMPLEMENTED
# Future: Via agent invocation in Claude Code
# Prompt: "Generate a quiz about [topic] with [N] questions at [difficulty] level"
```

**Workaround**: Manually create JSON files in `/quizzes/` following the format in `sample_quiz.json`

### Testing
```bash
# Run component tests
cd .claude/skills/quiz-run/scripts
python test_quiz.py
```

## Implementation Details

### quiz-run Skill ✓ COMPLETE

**Technology Stack:**
- Python 3.7+ (uses dataclasses)
- tkinter for GUI (built-in, no external dependencies)
- Threading for timer functionality

**Architecture:**
```
quiz_runner.py          # CLI entry point, argument parsing
└── quiz_app.py         # Main orchestration (QuizApp class)
    ├── models.py       # Quiz, Question, QuizOption, QuizResult
    ├── utils.py        # QuizTimer (threading-based)
    └── ui/
        ├── start_page.py     # Configuration screen
        ├── question_page.py  # Question display + interaction
        └── results_page.py   # Final results
```

**Mode Behavior:**
- **Learning mode**: Shows correct answer immediately after confirming, allows Previous button to review
- **Exam mode**: No immediate feedback, must answer to proceed, no Previous button, results shown at end

**Features:**
- **Question Navigation Bar** (learning mode): Clickable numbered buttons [1][2][3]... for quick navigation
  - Blue = current question
  - Green = correctly answered (all correct options selected)
  - Red = incorrectly answered
  - Gray = not yet answered
- **Inline Feedback**: Correct/incorrect message appears directly under selected answer with explanation
- **Smart UI**: Confirm button automatically removes itself after answering
- **Random Question Selection**: When user reduces question count on start page
- **Countdown Timer**: Auto-stop when time expires
- **Multi-select Support**: Checkboxes for questions with multiple correct answers
- **Strict Correctness**: Multi-select questions require ALL correct answers to be marked as correct
- **Results Output**: JSON to stdout: `{total_questions, correct_answers, time_used_seconds}`
- **Read-only Previous**: In learning mode, shows feedback without allowing re-answering

**File Count:** ~800 lines of Python across 8 files + test suite

## Project Conventions

- Store quiz definitions in `/quizzes/` directory as JSON files
- Quiz runner launches tkinter window, blocks until completion
- Skills and agents reside in `/.claude/` hierarchy per Claude Code conventions
- No external Python dependencies required (all built-in modules)
