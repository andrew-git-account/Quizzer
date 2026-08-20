"""Test script to validate quiz components without GUI."""

from pathlib import Path
from models import Quiz, QuizResult
from utils import QuizTimer
import time


def test_quiz_loading():
    """Test quiz file loading."""
    print("Testing quiz loading...")
    quiz_path = Path('../../../../quizzes/sample_quiz.json')
    quiz = Quiz.from_file(quiz_path)

    assert quiz.title == "Python Programming Basics Quiz"
    assert len(quiz.questions) == 10
    assert quiz.questions[0].id == 1
    assert quiz.questions[0].domain == "Data Types"
    assert quiz.questions[0].is_multi_select == False
    assert quiz.questions[2].is_multi_select == True

    print("[OK] Quiz loading works correctly")


def test_answer_checking():
    """Test answer validation."""
    print("\nTesting answer validation...")
    quiz_path = Path('../../../../quizzes/sample_quiz.json')
    quiz = Quiz.from_file(quiz_path)

    # Test single-select question (question 1, correct answer is 2)
    q1 = quiz.questions[0]
    assert q1.is_correct([2]) == True
    assert q1.is_correct([1]) == False
    assert q1.is_correct([1, 2]) == False

    # Test multi-select question (question 3, correct answers are 1 and 3)
    q3 = quiz.questions[2]
    assert q3.is_correct([1, 3]) == True
    assert q3.is_correct([3, 1]) == True  # Order doesn't matter
    assert q3.is_correct([1]) == False
    assert q3.is_correct([1, 2, 3]) == False

    print("[OK] Answer validation works correctly")


def test_quiz_result():
    """Test result formatting."""
    print("\nTesting result formatting...")
    result = QuizResult(
        total_questions=10,
        correct_answers=8,
        time_used_seconds=245.6
    )

    assert result.score_percentage == 80.0

    json_output = result.to_json()
    assert '"total_questions": 10' in json_output
    assert '"correct_answers": 8' in json_output
    assert '"time_used_seconds": 245.6' in json_output

    print("[OK] Result formatting works correctly")


def test_timer():
    """Test timer functionality."""
    print("\nTesting timer...")

    # Test timer without time limit
    timer1 = QuizTimer(0, lambda: None)
    timer1.start()
    time.sleep(0.1)
    elapsed = timer1.stop()
    assert elapsed >= 0.1
    print(f"  Timer without limit tracked {elapsed:.2f}s")

    # Test time formatting
    assert QuizTimer.format_time(0) == "00:00"
    assert QuizTimer.format_time(65) == "01:05"
    assert QuizTimer.format_time(3661) == "61:01"

    print("[OK] Timer works correctly")


def test_option_retrieval():
    """Test getting options by ID."""
    print("\nTesting option retrieval...")
    quiz_path = Path('../../../../quizzes/sample_quiz.json')
    quiz = Quiz.from_file(quiz_path)

    q1 = quiz.questions[0]
    option2 = q1.get_option_by_id(2)
    assert option2.answer == "Tuple"
    assert "immutable" in option2.explanation.lower()

    print("[OK] Option retrieval works correctly")


if __name__ == '__main__':
    print("="*60)
    print("Quiz Application Component Tests")
    print("="*60)

    test_quiz_loading()
    test_answer_checking()
    test_quiz_result()
    test_timer()
    test_option_retrieval()

    print("\n" + "="*60)
    print("All tests passed! [OK]")
    print("="*60)
    print("\nTo test the full GUI application, run:")
    print("  python quiz_runner.py ../../../../quizzes/sample_quiz.json")
    print("\nOr use the skill:")
    print("  /quiz-run quizzes/sample_quiz.json")
