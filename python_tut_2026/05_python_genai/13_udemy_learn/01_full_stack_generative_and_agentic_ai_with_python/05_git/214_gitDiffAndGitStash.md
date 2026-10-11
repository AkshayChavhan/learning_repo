# git diff, git stash, and Time-Travel with git checkout

Three tools for three different needs: comparing a file across time,
temporarily shelving unfinished work, and jumping back to an earlier
commit without losing your place.

---

## 🟢 Beginner — the one thing everyone gets wrong about `git diff`

**`git diff` never compares two different files.** It compares the
**same file at two different points in time** - before staging vs after
staging, commit X vs commit Y, branch A's version vs branch B's version.

```bash
git status              # see what's changed, nothing staged yet
git add index.html       # stage it
git diff --staged        # compare: unstaged version vs staged version
```

**The `+`/`-` symbols do NOT mean "added"/"removed" code.** They just
label which side of the comparison is "file A" (`---`, shown first) and
which is "file B" (`+++`, shown second). Swap the order you compare in,
and the *same* line flips from `+` to `-`:

```text
git diff commit1 commit2   →  "nice footer" shows as  +
git diff commit2 commit1   →  "nice footer" shows as  -
```

Same content, same change - only the comparison direction changed.

---

## 🟡 Intermediate — comparing commits and branches, and the pager gotcha

```bash
git diff --staged                 # staged changes vs the last commit
git diff <commit1> <commit2>      # or with two dots:
git diff <commit1>..<commit2>     # same result - .. is the safer, more compatible form
git diff <branch1>..<branch2>     # works identically for branches
```

A short commit hash prefix works fine - you almost never need the full hash.

**The gotcha:** `git diff` (and `git log`, `git show`) often open in a
pager that looks like **vim**. You are not stuck - press **`q`** to exit.
It only shows glimpses (diff hunks), never the whole file - GUI tools
like GitKraken show more context if needed.

---

## 🔴 Expert — git stash: shelving work to switch branches

**The scenario:** you have uncommitted changes on a branch, and need to
switch to another branch. Git refuses:

```text
error: Your local changes to the following files would be overwritten by checkout...
Please commit your changes or stash them before you switch branches.
Aborting
```

**The fix:**

```bash
git stash              # shelve the uncommitted work
git switch footer       # now the switch works - the working tree is clean
# ...do work on the other branch...
git switch bug-fix      # back to where you were
git stash pop           # bring the shelved work back
```

| Command | Does |
|---|---|
| `git stash` | shelves all uncommitted changes, restores a clean working tree |
| `git stash pop` | re-applies the most recent stash **and removes it** from the stash list |
| `git stash apply stash@{N}` | re-applies a specific stash **without removing it** - safer when juggling several |
| `git stash list` | shows every stashed entry - check this before popping when more than one exists |

**A genuinely surprising, verified-live fact:** a stash isn't locked to
the branch it was made on - popping it on a *different* branch works
fine. Convenient, but exactly why `git stash list` matters before
popping on a team project - it's easy to apply the wrong stash onto the
wrong branch.

> **Stash is for short-term, temporary shelving only** - not long-term
> storage, and extra caution is warranted on any branch others are
> actively working on too.

---

## Expert, part 2 — checkout as time travel, and finding your way back

```bash
git log --oneline                 # find a commit to jump to
git checkout <commit-hash>        # HEAD moves there - a detached, read-only view
git checkout HEAD~2               # or relative to HEAD - "2 commits back"
```

Checking out a commit directly moves `HEAD` away from any branch tip -
you're looking at history, not standing on a branch.

**Getting back - the one real gotcha:**

```bash
git checkout head      # does NOT return you to the branch - this is a trap
git checkout master    # THIS returns you to the branch tip
```

If you've lost track of where you came from, `git reflog` shows where
`HEAD` has pointed recently - rarely needed, but it's the safety net.

**`git restore`** can bring a file back too, but only to the **last
commit** - unlike `checkout`, it can't reach further back in history.

---

## Quick recap

| Term | One-line definition |
|---|---|
| **`git diff`** | compares the same file across two points in time - never two different files |
| **`+`/`-` in a diff** | just labels for "first side" / "second side" of the comparison - not add/remove |
| **`git stash`** | temporarily shelves uncommitted work so you can switch branches |
| **`git stash pop` vs `apply`** | `pop` removes the stash after applying; `apply` keeps it in the list |
| **Detached HEAD** (via `checkout <commit>`) | viewing an old commit directly, off any branch - return with `checkout <branch-name>` |
| **`git reflog`** | a log of where HEAD has been - the way back if you lose track |
