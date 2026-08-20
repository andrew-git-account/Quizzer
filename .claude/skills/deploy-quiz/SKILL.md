---
name: deploy-quiz
description: |
  Deploys quiz-run skill and quiz-agent to global ~/.claude/ directory for use across all projects.
  
  Use when:
  - User wants to make quiz components available globally
  - User updates quiz components and needs to redeploy
  - User wants to uninstall global quiz components
  
  <example>
  user: "Deploy quiz globally"
  assistant: [runs deployment script, validates, reports success]
  </example>
  
  <example>
  user: "Remove quiz from global location"
  assistant: [runs uninstall with --uninstall flag]
  </example>

argument-hint: "[--uninstall]"
allowed-tools:
  - Bash
---

Deploys quiz-run skill and quiz-agent globally to ~/.claude/ directory.

## Usage

Deploy to global:
```
/deploy-quiz
```

Uninstall from global:
```
/deploy-quiz --uninstall
```

## What Gets Deployed

**quiz-run skill** → `~/.claude/skills/quiz-run/` (13 files)
- SKILL.md
- scripts/quiz_runner.py
- scripts/models.py
- scripts/quiz_app.py
- scripts/utils.py
- scripts/ui/__init__.py
- scripts/ui/start_page.py
- scripts/ui/question_page.py
- scripts/ui/results_page.py
- scripts/debug_run.py
- scripts/test_quiz.py
- scripts/test_ui_load.py

**quiz-agent** → `~/.claude/agents/quiz-agent.md`

## Validation

After deployment, validates:
1. **File existence** - All 13 files present
2. **Python imports** - models, quiz_app, utils, UI modules
3. **Quiz execution** - Sample quiz validates successfully
4. **Agent format** - Frontmatter and structure valid

Deployment fails if any validation step fails.

## Behavior

- **Always overwrites** existing files (local is source of truth)
- **No backups** created before overwriting
- **Full validation** after deployment
- **Reports** success or specific failure reason

## Requirements

- Python 3.7+ with tkinter
- Write permissions to ~/.claude/ directory
- No external dependencies
