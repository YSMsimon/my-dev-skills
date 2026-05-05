# Git Workflow — Examples

## Good commit messages

```
feat(memory): add background profile extraction after each turn

Profile updates were blocking the conversation response loop,
making the agent feel slow on every exchange. Running the
extractor in a daemon thread keeps it transparent to the user.

Closes #34
```

```
fix(db): index foreign key on llm_memory.user_id

PostgreSQL does not automatically index foreign keys. Sequential
scans on llm_memory were causing 800ms+ query times with >10k rows.
```

```
chore: upgrade psycopg2-binary to 2.9.9
```

**Bad:** `fixed stuff`, `updated code`, `wip`, `asdfasdf`

---

## Cleaning up history

### Squash WIP commits before merging
```bash
git rebase -i HEAD~4
# In the editor: change "pick" to "squash" on commits to fold in
```

### Amend the last commit
```bash
git add forgotten_file.py
git commit --amend --no-edit         # add staged changes
git commit --amend -m "better msg"   # rewrite the message
```
⚠️ Only amend commits that haven't been pushed.

### Rebase onto main
```bash
git fetch origin
git rebase origin/main
# On conflict: fix file → git add → git rebase --continue
# To abort: git rebase --abort
```

---

## Undoing mistakes

```bash
git reset --soft HEAD~1       # undo last commit, keep changes staged
git reset HEAD~1              # undo last commit, keep changes unstaged
git reset --hard HEAD~1       # undo last commit, DISCARD changes (⚠ destructive)
git revert abc1234            # revert a pushed commit (safe — creates new commit)
git restore --staged myfile   # unstage a file
git restore myfile            # discard unstaged changes (⚠ destructive)
git reflog                    # recover a deleted branch — find the commit hash
```

---

## Stashing

```bash
git stash                          # stash all uncommitted changes
git stash push -m "wip: auth"      # stash with a label
git stash list                     # list all stashes
git stash pop                      # apply last stash and remove it
git stash apply stash@{2}          # apply specific stash, keep it
git stash branch new-branch        # create branch from stash
```

---

## Release tagging

```bash
git tag -a v1.2.0 -m "Release v1.2.0: description"
git push origin v1.2.0
git tag -l "v1.*"                  # list tags
```

Semantic versioning: `MAJOR.MINOR.PATCH` — MAJOR=breaking, MINOR=new feature, PATCH=bug fix.

---

## Common issues

### "Rejected — non-fast-forward"
```bash
git pull --rebase origin main
# If you must overwrite your own feature branch:
git push --force-with-lease    # safer than --force
```

### Merge conflict
```bash
git status                     # shows conflicted files
# Edit each file, resolve between <<<< ==== >>>>
git add <resolved-file>
git merge --continue
```

### Detached HEAD
```bash
git checkout -b new-branch     # save your work on a branch
```

### Accidentally committed to main
```bash
git checkout -b fix/save-work
git checkout main
git reset --hard HEAD~1        # remove commit from main (⚠ if not pushed)
```

### Committed .env or secrets
```bash
git rm --cached .env
echo ".env" >> .gitignore
git commit -m "chore: remove .env from tracking"
# Rotate ALL secrets that were exposed — they're in GitHub's cache
```
