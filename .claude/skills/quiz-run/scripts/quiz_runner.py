#!/usr/bin/env python3
"""Quiz runner entry point - CLI interface for quiz execution."""

import argparse
import sys
from pathlib import Path

# Add script directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from models import Quiz, QuizResult
from quiz_app import QuizApp


def main():
    """Main entry point for quiz runner."""
    parser = argparse.ArgumentParser(
        description='Execute an interactive quiz with tkinter GUI'
    )
    parser.add_argument(
        'quiz_file',
        type=Path,
        help='Path to quiz JSON file'
    )
    parser.add_argument(
        '--mode',
        choices=['learning', 'exam'],
        default='learning',
        help='Quiz mode: learning (immediate feedback) or exam (deferred feedback)'
    )
    parser.add_argument(
        '--time',
        type=int,
        default=0,
        help='Time limit in seconds (0 = unlimited)'
    )

    args = parser.parse_args()

    # Validate file exists
    if not args.quiz_file.exists():
        print(f"Error: Quiz file not found: {args.quiz_file}", file=sys.stderr)
        sys.exit(1)

    # Validate time limit
    if args.time < 0:
        print("Error: Time limit cannot be negative", file=sys.stderr)
        sys.exit(1)

    # Load quiz
    try:
        quiz = Quiz.from_file(args.quiz_file)
    except Exception as e:
        print(f"Error loading quiz file: {e}", file=sys.stderr)
        sys.exit(1)

    # Validate quiz has questions
    if not quiz.questions:
        print("Error: Quiz file contains no questions", file=sys.stderr)
        sys.exit(1)

    # Launch GUI application
    try:
        app = QuizApp(quiz, args.mode, args.time)
        result = app.run()

        # Output JSON result to stdout
        if result:
            print(result.to_json())
        else:
            # User closed window without completing
            print("Quiz was not completed", file=sys.stderr)
            sys.exit(1)

    except KeyboardInterrupt:
        print("\nQuiz interrupted by user", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"Error running quiz: {e}", file=sys.stderr)
        sys.exit(1)

    sys.exit(0)


if __name__ == '__main__':
    main()
