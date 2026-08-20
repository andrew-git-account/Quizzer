"""Deployment script for quiz-run skill and quiz-agent."""

import sys
import json
import shutil
import argparse
from pathlib import Path


def get_claude_dir():
    """Get the .claude directory (3 levels up from this script)."""
    # Script is at: .claude/skills/deploy-quiz/scripts/deployer.py
    # Go up: scripts -> deploy-quiz -> skills -> .claude
    return Path(__file__).resolve().parent.parent.parent.parent


def get_home_claude_dir():
    """Get the ~/.claude directory path."""
    return Path.home() / '.claude'


def ignore_pycache(dir, files):
    """Ignore function for shutil.copytree to skip __pycache__ and .pyc files."""
    return [f for f in files if f == '__pycache__' or f.endswith('.pyc')]


def copy_quiz_run_skill():
    """Copy all quiz-run files to ~/.claude/skills/quiz-run/"""
    source = get_claude_dir() / 'skills' / 'quiz-run'
    target = get_home_claude_dir() / 'skills' / 'quiz-run'

    if not source.exists():
        raise FileNotFoundError(f"Source directory not found: {source}")

    print(f"Copying quiz-run skill...")
    print(f"  From: {source}")
    print(f"  To:   {target}")

    # Copy with overwrite, skip __pycache__
    shutil.copytree(source, target, dirs_exist_ok=True, ignore=ignore_pycache)

    # Count files copied (excluding __pycache__)
    file_count = sum(1 for _ in target.rglob('*') if _.is_file() and '__pycache__' not in str(_))
    print(f"  [OK] Copied {file_count} files")


def copy_quiz_agent():
    """Copy quiz-agent.md to ~/.claude/agents/"""
    source = get_claude_dir() / 'agents' / 'quiz-agent.md'
    target_dir = get_home_claude_dir() / 'agents'
    target = target_dir / 'quiz-agent.md'

    if not source.exists():
        raise FileNotFoundError(f"Source file not found: {source}")

    print(f"Copying quiz-agent...")
    print(f"  From: {source}")
    print(f"  To:   {target}")

    # Create agents directory if it doesn't exist
    target_dir.mkdir(parents=True, exist_ok=True)

    # Copy file (preserves metadata)
    shutil.copy2(source, target)
    print(f"  [OK] Copied quiz-agent.md")


def validate_file_existence():
    """Validate that all required files exist."""
    print("\nValidating file existence...")

    home_claude = get_home_claude_dir()

    required_files = [
        'skills/quiz-run/SKILL.md',
        'skills/quiz-run/scripts/quiz_runner.py',
        'skills/quiz-run/scripts/models.py',
        'skills/quiz-run/scripts/quiz_app.py',
        'skills/quiz-run/scripts/utils.py',
        'skills/quiz-run/scripts/ui/__init__.py',
        'skills/quiz-run/scripts/ui/start_page.py',
        'skills/quiz-run/scripts/ui/question_page.py',
        'skills/quiz-run/scripts/ui/results_page.py',
        'skills/quiz-run/scripts/debug_run.py',
        'skills/quiz-run/scripts/test_quiz.py',
        'skills/quiz-run/scripts/test_ui_load.py',
        'agents/quiz-agent.md'
    ]

    missing_files = []
    for rel_path in required_files:
        full_path = home_claude / rel_path
        if not full_path.exists():
            missing_files.append(rel_path)

    if missing_files:
        print("  [FAIL] Missing files:")
        for file in missing_files:
            print(f"    - {file}")
        return False

    print(f"  [OK] All {len(required_files)} files present")
    return True


def validate_imports():
    """Validate that Python imports work from global location."""
    print("\nValidating Python imports...")

    home_claude = get_home_claude_dir()
    scripts_path = str(home_claude / 'skills' / 'quiz-run' / 'scripts')

    # Add to path temporarily
    if scripts_path not in sys.path:
        sys.path.insert(0, scripts_path)

    try:
        # Test core model imports
        from models import Quiz, Question, QuizOption, QuizResult
        print("  [OK] models.py imports")

        # Test app imports
        from quiz_app import QuizApp
        print("  [OK] quiz_app.py imports")

        # Test utilities
        from utils import QuizTimer
        print("  [OK] utils.py imports")

        # Test UI imports
        from ui import StartPage, QuestionPage, ResultsPage
        print("  [OK] UI module imports")

        return True

    except ImportError as e:
        print(f"  [FAIL] Import error: {e}")
        return False
    finally:
        # Clean up path
        if scripts_path in sys.path:
            sys.path.remove(scripts_path)


def validate_quiz_execution():
    """Validate that a sample quiz can be loaded and validated."""
    print("\nValidating quiz execution...")

    home_claude = get_home_claude_dir()
    scripts_path = str(home_claude / 'skills' / 'quiz-run' / 'scripts')

    # Add to path temporarily
    if scripts_path not in sys.path:
        sys.path.insert(0, scripts_path)

    try:
        from models import Quiz

        # Create minimal test quiz
        test_quiz_data = {
            "title": "Validation Test",
            "questions": [
                {
                    "id": 1,
                    "domain": "Test",
                    "question": "Test question?",
                    "options": [
                        {"id": 1, "answer": "Option A"},
                        {"id": 2, "answer": "Option B"}
                    ],
                    "correctAnswerIds": [1]
                }
            ]
        }

        # Write to temp file
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(test_quiz_data, f)
            temp_path = Path(f.name)

        try:
            # Validate with Quiz.from_file()
            quiz = Quiz.from_file(temp_path)

            # Basic validation
            assert quiz.title == "Validation Test"
            assert len(quiz.questions) == 1
            assert quiz.questions[0].question == "Test question?"

            print("  [OK] Sample quiz validates successfully")
            return True

        finally:
            # Cleanup temp file
            temp_path.unlink()

    except Exception as e:
        print(f"  [FAIL] Quiz validation error: {e}")
        return False
    finally:
        # Clean up path
        if scripts_path in sys.path:
            sys.path.remove(scripts_path)


def validate_agent_format():
    """Validate that quiz-agent.md has valid frontmatter."""
    print("\nValidating agent format...")

    home_claude = get_home_claude_dir()
    agent_path = home_claude / 'agents' / 'quiz-agent.md'

    try:
        content = agent_path.read_text(encoding='utf-8')

        # Check frontmatter
        if not content.startswith('---'):
            print("  [FAIL] No frontmatter found")
            return False

        # Check required fields
        if 'name:' not in content:
            print("  [FAIL] Missing 'name' field in frontmatter")
            return False

        if 'description:' not in content:
            print("  [FAIL] Missing 'description' field in frontmatter")
            return False

        print("  [OK] Agent format valid")
        return True

    except Exception as e:
        print(f"  [FAIL] Agent validation error: {e}")
        return False


def validate_deployment():
    """Validate that deployment succeeded."""
    print("\n" + "="*60)
    print("VALIDATION")
    print("="*60)

    checks = [
        ("File existence", validate_file_existence),
        ("Python imports", validate_imports),
        ("Quiz execution", validate_quiz_execution),
        ("Agent format", validate_agent_format)
    ]

    all_passed = True
    for name, check_func in checks:
        if not check_func():
            all_passed = False

    return all_passed


def deploy():
    """Main deployment function."""
    print("="*60)
    print("DEPLOYING QUIZ COMPONENTS TO GLOBAL ~/.claude/")
    print("="*60)

    try:
        # Create base directories if they don't exist
        home_claude = get_home_claude_dir()
        (home_claude / 'skills').mkdir(parents=True, exist_ok=True)
        (home_claude / 'agents').mkdir(parents=True, exist_ok=True)

        # Copy files
        copy_quiz_run_skill()
        copy_quiz_agent()

        # Validate
        if validate_deployment():
            print("\n" + "="*60)
            print("SUCCESS!")
            print("="*60)
            print(f"\nQuiz components deployed to: {home_claude}")
            print("\nYou can now use these globally across all projects:")
            print("  /quiz-run <quiz-file>")
            print("  Invoke quiz-agent for quiz conversion")
            return 0
        else:
            print("\n" + "="*60)
            print("DEPLOYMENT FAILED - VALIDATION ERRORS")
            print("="*60)
            print("\nFiles were copied but validation failed.")
            print("Check the errors above for details.")
            return 1

    except Exception as e:
        print("\n" + "="*60)
        print("DEPLOYMENT FAILED")
        print("="*60)
        print(f"\nError: {e}")
        return 1


def uninstall():
    """Remove quiz components from global location."""
    print("="*60)
    print("UNINSTALLING QUIZ COMPONENTS FROM ~/.claude/")
    print("="*60)

    home_claude = get_home_claude_dir()

    removed = []
    errors = []

    # Remove quiz-run skill directory
    skill_path = home_claude / 'skills' / 'quiz-run'
    if skill_path.exists():
        try:
            shutil.rmtree(skill_path)
            removed.append(str(skill_path))
            print(f"[OK] Removed: {skill_path}")
        except Exception as e:
            errors.append(f"Failed to remove {skill_path}: {e}")
            print(f"[FAIL] {errors[-1]}")
    else:
        print(f"[SKIP] Not found: {skill_path}")

    # Remove quiz-agent file
    agent_path = home_claude / 'agents' / 'quiz-agent.md'
    if agent_path.exists():
        try:
            agent_path.unlink()
            removed.append(str(agent_path))
            print(f"[OK] Removed: {agent_path}")
        except Exception as e:
            errors.append(f"Failed to remove {agent_path}: {e}")
            print(f"[FAIL] {errors[-1]}")
    else:
        print(f"[SKIP] Not found: {agent_path}")

    print("\n" + "="*60)
    if not removed and not errors:
        print("NOTHING TO UNINSTALL")
        print("="*60)
        print("\nQuiz components were not found in global location.")
        return 0
    elif errors:
        print("UNINSTALL FAILED")
        print("="*60)
        print(f"\nRemoved {len(removed)} item(s), {len(errors)} error(s)")
        return 1
    else:
        print("UNINSTALL COMPLETE")
        print("="*60)
        print(f"\nRemoved {len(removed)} item(s) from {home_claude}")
        return 0


def main():
    """Entry point for deployment script."""
    parser = argparse.ArgumentParser(description='Deploy quiz components to global ~/.claude/')
    parser.add_argument('--uninstall', action='store_true',
                        help='Remove quiz components from global location')

    args = parser.parse_args()

    if args.uninstall:
        return uninstall()
    else:
        return deploy()


if __name__ == '__main__':
    sys.exit(main())
