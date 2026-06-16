---
name: restore-git-version
description: Safely restore a local Git working tree to the latest version from a remote repository. Use when the user asks to discard current local edits, reset to the repo's latest version, recover the local checkout from GitHub/origin, undo all uncommitted changes, clean generated/untracked files, or return a repository to the newest remote branch state.
---

# Restore Git Version

## Overview

Restore a Git repository by verifying the current branch and remote, fetching the newest remote refs, then resetting the local branch to the matching remote branch. Treat `git reset --hard` and `git clean -fd` as destructive operations because they discard local work.

## Workflow

1. Confirm the repository and branch.

```powershell
git status --short
git branch --show-current
git remote -v
```

2. If the user has not explicitly confirmed they want to discard local changes, stop and ask for confirmation before running destructive commands.

Use direct wording:

> This will delete uncommitted local changes. Should I reset this repo to the latest remote version?

3. Fetch the latest remote state.

```powershell
git fetch origin
```

4. Reset to the matching remote branch.

Prefer the current branch name discovered in step 1:

```powershell
git reset --hard origin/<branch>
```

Example for `main`:

```powershell
git reset --hard origin/main
```

5. Remove untracked files only when the user asked to fully clean the workspace or when generated/untracked files are part of what they want discarded.

Preview first when there is any doubt:

```powershell
git clean -fdn
```

Then clean after confirmation:

```powershell
git clean -fd
```

6. Verify the final state.

```powershell
git status --short
git status --branch
```

## Branch Selection

Use `origin/<current-branch>` by default. If the current branch has no matching remote branch, inspect remote branches:

```powershell
git branch -r
```

If the user explicitly asks for a branch such as `main`, `master`, or a feature branch, reset to that branch's remote ref.

## Safety Rules

- Never run `git reset --hard`, `git clean -fd`, or other destructive cleanup unless the user's request clearly asks to discard local work or the user confirms it.
- Do not delete ignored files with `git clean -fdx` unless the user explicitly asks to remove ignored files too.
- If the user might need a backup, offer a temporary branch or stash before resetting:

```powershell
git branch backup-before-reset
git stash push -u -m "backup before reset"
```

- If command execution requires elevated sandbox approval, request approval with a short explanation that the command will discard local changes or clean untracked files.
