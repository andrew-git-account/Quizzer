"""Test UI loading without launching full app."""

import sys
from pathlib import Path

# Add script directory to path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from models import Quiz
    from quiz_app import QuizApp

    print("Loading quiz file...")
    quiz_path = Path('../../../../quizzes/sample_quiz.json')
    quiz = Quiz.from_file(quiz_path)
    print(f"✓ Quiz loaded: {quiz.title}")

    print("\nCreating QuizApp instance...")
    app = QuizApp(quiz, 'learning', 0)
    print("✓ QuizApp created successfully")

    print("\nAll imports and initialization successful!")
    print("If the GUI crashes, it's likely a tkinter rendering issue.")

except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
