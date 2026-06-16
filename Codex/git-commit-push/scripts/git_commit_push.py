from __future__ import annotations

import argparse
import subprocess
import sys


ACTION_LABELS = {
    "A": "Add",
    "M": "Update",
    "D": "Remove",
    "R": "Rename",
    "C": "Copy",
    "T": "Update",
    "U": "Update",
    "?": "Add",
}


def run_git(args: list[str], *, capture: bool = False) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        check=False,
        text=True,
        capture_output=capture,
    )


def git_output(args: list[str]) -> str:
    result = run_git(args, capture=True)
    if result.returncode != 0:
        stderr = (result.stderr or "").strip()
        stdout = (result.stdout or "").strip()
        detail = stderr or stdout or f"git {' '.join(args)} failed"
        raise RuntimeError(detail)
    return (result.stdout or "").strip()


def ensure_git_repository() -> None:
    result = run_git(["rev-parse", "--is-inside-work-tree"], capture=True)
    if result.returncode != 0 or (result.stdout or "").strip() != "true":
        raise RuntimeError("Current directory is not inside a git work tree.")


def status_lines() -> list[str]:
    result = run_git(["status", "--porcelain"], capture=True)
    if result.returncode != 0:
        stderr = (result.stderr or "").strip()
        stdout = (result.stdout or "").strip()
        detail = stderr or stdout or "git status --porcelain failed"
        raise RuntimeError(detail)
    output = result.stdout or ""
    return [line for line in output.splitlines() if line.strip()]


def has_staged_changes() -> bool:
    result = run_git(["diff", "--cached", "--quiet"])
    return result.returncode == 1


def parse_name_status_line(line: str) -> tuple[str, str]:
    parts = line.split("\t")
    if len(parts) < 2:
        raise RuntimeError(f"Unexpected git name-status line: {line}")
    status = parts[0].strip()[:1] or "M"
    path = parts[-1].strip()
    return status, path


def staged_name_status() -> list[tuple[str, str]]:
    output = git_output(["diff", "--cached", "--name-status", "--find-renames"])
    return [parse_name_status_line(line) for line in output.splitlines() if line.strip()]


def pending_name_status() -> list[tuple[str, str]]:
    changes: list[tuple[str, str]] = []
    for line in status_lines():
        if len(line) < 4:
            continue
        index_status = line[0]
        worktree_status = line[1]
        path = line[3:].strip()
        if index_status != " ":
            changes.append((index_status, path))
        elif worktree_status != " ":
            changes.append((worktree_status, path))
    return changes


def humanize_path(path: str) -> str:
    name = path.rsplit("/", 1)[-1].rsplit("\\", 1)[-1]
    stem = name.rsplit(".", 1)[0] if "." in name else name
    text = stem.replace("-", " ").replace("_", " ").strip()
    return text or path


def choose_action(changes: list[tuple[str, str]]) -> str:
    actions = {status for status, _ in changes}
    if len(actions) == 1:
        return ACTION_LABELS.get(next(iter(actions)), "Update")
    return "Update"


def build_commit_message(changes: list[tuple[str, str]]) -> str:
    if not changes:
        raise RuntimeError("Unable to generate a commit message without file changes.")

    action = choose_action(changes)
    unique_paths: list[str] = []
    seen: set[str] = set()
    for _, path in changes:
        if path not in seen:
            unique_paths.append(path)
            seen.add(path)

    subject = humanize_path(unique_paths[0])
    if len(unique_paths) == 1:
        return f"{action} {subject}"
    return f"{action} {subject} and {len(unique_paths) - 1} other files"


def current_branch() -> str:
    branch = git_output(["rev-parse", "--abbrev-ref", "HEAD"])
    if branch == "HEAD":
        raise RuntimeError("Detached HEAD detected. Specify --branch before pushing.")
    return branch


def tracked_upstream() -> tuple[str, str] | None:
    result = run_git(
        ["rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"],
        capture=True,
    )
    if result.returncode != 0:
        return None

    upstream = (result.stdout or "").strip()
    if "/" not in upstream:
        return None
    remote, branch = upstream.split("/", 1)
    return remote, branch


def require_success(result: subprocess.CompletedProcess[str], action: str) -> None:
    if result.returncode == 0:
        return
    stderr = (result.stderr or "").strip()
    stdout = (result.stdout or "").strip()
    detail = stderr or stdout or f"{action} failed."
    raise RuntimeError(f"{action} failed: {detail}")


def print_command(args: list[str]) -> None:
    print("$ " + " ".join(args))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Stage, commit, and push repository changes with basic guardrails."
    )
    parser.add_argument("--message", help="Commit message to use.")
    parser.add_argument(
        "--auto-message",
        action="store_true",
        help="Generate the commit message from the staged or pending diff.",
    )
    parser.add_argument(
        "--stage-all",
        action="store_true",
        help="Run `git add -A` before committing.",
    )
    parser.add_argument("--remote", help="Override push remote.")
    parser.add_argument("--branch", help="Override push branch.")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the git commands that would run without mutating git state.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if not args.message and not args.auto_message:
        print("Provide --message or --auto-message.", file=sys.stderr)
        return 2

    if args.message is not None and not args.message.strip():
        print("Commit message must not be empty.", file=sys.stderr)
        return 2

    try:
        ensure_git_repository()

        pending = status_lines()
        if not pending:
            raise RuntimeError("Working tree is clean. Nothing to commit.")

        branch_name = args.branch or current_branch()

        if args.stage_all:
            add_cmd = ["git", "add", "-A"]
            if args.dry_run:
                print_command(add_cmd)
            else:
                require_success(run_git(["add", "-A"], capture=True), "git add -A")

        staged_ready = has_staged_changes() or (args.dry_run and args.stage_all)
        if not staged_ready:
            raise RuntimeError(
                "No staged changes found. Use --stage-all or stage files manually first."
            )

        if args.message:
            commit_message = args.message.strip()
        elif args.dry_run and args.stage_all:
            commit_message = build_commit_message(pending_name_status())
        else:
            commit_message = build_commit_message(staged_name_status())

        commit_cmd = ["git", "commit", "-m", commit_message]
        if args.dry_run:
            print_command(commit_cmd)
        else:
            require_success(
                run_git(["commit", "-m", commit_message], capture=True),
                "git commit",
            )

        upstream = tracked_upstream()
        remote_name = args.remote
        push_args: list[str]

        if remote_name and args.branch:
            push_args = ["push", remote_name, args.branch]
        elif remote_name:
            push_args = ["push", "-u", remote_name, branch_name]
        elif upstream:
            upstream_remote, upstream_branch = upstream
            push_args = ["push", upstream_remote, f"HEAD:{upstream_branch}"]
        else:
            push_args = ["push", "-u", "origin", branch_name]

        if args.dry_run:
            print_command(["git", *push_args])
        else:
            require_success(run_git(push_args, capture=True), "git push")

        if args.dry_run:
            print("Dry run complete.")
        else:
            target = f"{push_args[-2]} {push_args[-1]}" if len(push_args) >= 3 else "upstream"
            print(f"Committed and pushed successfully to {target}.")
        return 0
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
