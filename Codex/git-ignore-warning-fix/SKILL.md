---
name: git-ignore-warning-fix
description: Diagnose and fix Git warnings in Codex when commands such as git status report unable to access C:\Users\user\.config\git\ignore or another default global ignore file because of permission denied. Use when Codex needs to explain or remove this warning by configuring a repository-local core.excludesFile that avoids the inaccessible global ignore path.
---

# Git Ignore Warning Fix

## Purpose

Use this skill to handle Git warnings like:

```text
warning: unable to access 'C:\Users\user/.config/git/ignore': Permission denied
```

The common Codex-specific cause is that Git for Windows tries to read the default XDG global ignore file, while the Codex execution sandbox cannot read that path. The repo can still be clean; the warning only means Git could not load that ignore file.

## Workflow

1. Check the repository status and capture the warning:

```powershell
git status --short --branch
```

2. Check whether the repo explicitly configures an excludes file:

```powershell
git config --show-origin --get core.excludesfile
```

If this returns nothing, Git may still try its default global ignore location, such as `C:\Users\user\.config\git\ignore` on Windows.

3. If useful, verify the file exists and whether Codex can read it:

```powershell
Test-Path -LiteralPath 'C:\Users\user\.config\git\ignore'
Get-Acl -LiteralPath 'C:\Users\user\.config\git\ignore' | Format-List Owner,Group,AccessToString
Get-Content -LiteralPath 'C:\Users\user\.config\git\ignore'
```

Interpretation:

- If ACL shows the user has access but `Get-Content` fails in Codex, treat it as an execution-environment restriction.
- If the same commands also fail in the user's own PowerShell, suggest fixing Windows permissions or recreating the global ignore file outside Codex.

4. To suppress the warning for the current repository only, configure Git to use the repo-local exclude file:

```powershell
git config core.excludesFile 'D:/path/to/repo/.git/info/exclude'
```

Use the actual absolute repository path. Prefer forward slashes in the config value on Windows.

5. Verify the warning is gone:

```powershell
git status --short --branch
```

## Guidance

Keep the fix local unless the user asks for a global change. Setting `core.excludesFile` without `--global` writes only to `.git/config` for the current repo and does not affect other repositories.

Do not modify, delete, or recreate `C:\Users\user\.config\git\ignore` unless the user explicitly asks to repair the global file. For Codex-only warnings, the local repo setting is safer and sufficient.

If the user wants to apply the same approach to another repo, repeat the local config command in that repo with that repo's `.git/info/exclude` path.
