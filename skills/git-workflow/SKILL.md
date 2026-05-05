---
name: git-workflow
description: Guide git workflows including writing commit messages, structuring branches, writing PR descriptions, resolving merge conflicts, squashing commits, rebasing, tagging releases, and undoing mistakes. Use this skill whenever the user wants help with a commit message, pull request, branching strategy, git history, rebasing, undoing a commit, stashing, or anything git-related. Trigger on phrases like "write a commit message", "help me PR this", "how should I branch", "clean up my commits", "git conflict", "undo", "revert", "stash", or any git command question.
---

# Git Workflow

Help the user work effectively with git — from individual commits to full branching strategies and pull request descriptions.

---

## Commit messages — Conventional Commits

### Format
```
<type>(<scope>): <short summary>

<optional body — explain WHY, not what>

<optional footer>
```

### Types
| Type | When to use |
|---|---|
| `feat` | New user-facing feature |
| `fix` | Bug fix |
| `refactor` | Code restructuring, no behaviour change |
| `perf` | Performance improvement |
| `test` | Adding or fixing tests |
| `docs` | Documentation only |
| `chore` | Build, deps, tooling |
| `ci` | CI/CD pipeline |
| `revert` | Reverting a previous commit |

### Rules
- Summary: max 50 chars, imperative mood ("add" not "added"), no trailing period
- Blank line between summary and body
- Body: explain *why* — the diff shows *what*
- Wrap body at 72 characters
- Reference issues in footer: `Closes #42`

---

## Branching strategy

### GitHub Flow (default — simple projects, CI/CD)
- `main` is always deployable
- Branch for every feature or fix
- PR → review → merge to `main`

**Branch naming:** `feature/jwt-refresh`, `fix/profile-update-race`, `chore/upgrade-dependencies`

### Git Flow (versioned releases, larger teams)
- `main`: production, always tagged
- `develop`: integration branch
- `feature/*`: from develop, back to develop
- `release/*`: from develop when prepping a release
- `hotfix/*`: from main for urgent fixes, merge back to both main and develop

---

## When the user provides context

If they share a diff or describe changes — **write the commit message directly**, don't just explain the format.

If they show a messy branch history — recommend the exact rebase commands with the real commit count.

If they describe a PR — write the full PR description using the template.

---

## Additional resources

- For command examples (squash, rebase, undo, stash, tagging, conflict resolution), see [examples.md](examples.md)
- For commit message and PR description templates, see [template/](template/)
