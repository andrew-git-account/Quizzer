"""Debug runner to catch any startup errors."""

import sys
import traceback
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

try:
    from models import Quiz
    from quiz_app import QuizApp

    quiz_path = Path('../../../../quizzes/sample_quiz.json')
    quiz = Quiz.from_file(quiz_path)

    print("Starting quiz app...", flush=True)
    app = QuizApp(quiz, 'learning', 0)
    result = app.run()

    if result:
        print(result.to_json())
    else:
        print("No result - quiz not completed")

except Exception as e:
    print(f"EXCEPTION: {e}", file=sys.stderr, flush=True)
    traceback.print_exc(file=sys.stderr)
    sys.exit(1)
