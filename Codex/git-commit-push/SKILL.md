---
name: git-commit-push
description: Create a git commit and push it to the correct remote branch with a consistent safety workflow. Use when Codex needs to turn the current repository changes into a real commit, stage unstaged edits, generate or confirm a commit message, and push to the tracked upstream or a specified remote/branch.
---

# Git Commit Push

Follow this workflow when the user wants the agent to handle the full git handoff instead of only editing files.

## Workflow

1. Inspect the repository state first with `git status --short --branch`.
2. Summarize the pending changes in 1-3 short points before choosing a commit message.
3. Prefer a concise imperative commit message that matches the actual diff.
4. If the user does not provide a commit message, use `--auto-message` to generate one from the staged or pending file changes.
5. If files are already staged, preserve that staging set unless the user asked to include everything.
6. If nothing is staged and the user asked for a normal commit of the current work, stage all tracked and untracked changes with the helper script's `--stage-all`.
7. Push to the branch's upstream when it exists. If upstream is missing, default to `origin <current-branch>` and set upstream during push.

## Commands

Use the bundled helper for the actual commit and push flow:

```powershell
python scripts/git_commit_push.py --message "Add search placeholder update" --stage-all
```

Auto-generate the commit message:

```powershell
python scripts/git_commit_push.py --auto-message --stage-all
```

Preview without changing git state:

```powershell
python scripts/git_commit_push.py --auto-message --stage-all --dry-run
```

Target a specific remote and branch:

```powershell
python scripts/git_commit_push.py --message "Release content update" --stage-all --remote origin --branch main
```

## Guardrails

- Refuse to run if there are no staged changes and `--stage-all` was not requested.
- Refuse to create an empty commit unless the user explicitly asks for one and the script is extended for it.
- Treat detached HEAD as a blocker unless the user specifies a branch.
- Do not rewrite history, force-push, or amend commits unless the user explicitly asks.
- If `git push` fails because of auth, branch protection, or non-fast-forward state, surface the exact git error and stop.

## Resource

Use [scripts/git_commit_push.py](scripts/git_commit_push.py) for deterministic execution. Read the script if you need to adjust staging or push-target behavior.
