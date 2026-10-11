# git rebase — Not That Scary

`git rebase` does what `git merge` does, bringing another branch's work into yours, but it
**rewrites history** to make it look like one straight line. No merge commits. The price:
old commits get **new ids**. Rule one: run it from the **side branch**, never from main.

---

## Topic at a glance

```text
        What it does                       The rule
            \                                 /
  replant branch on main ──\   side branch only ──/
                            \                    /
  no merge commits ─────────\   never shared commits
                              ►   GIT REBASE
  new commit ids ───────────/      add → --continue ──\
                            /                          \
  rewrites history ────────/        --abort to bail ────\
            /                                             \
      Why "scary"                                   Conflicts
```

---

## 🟢 Beginner — merge vs rebase, same goal, different shape

**The situation:** you're on `bug-fix`, `master` moved on, you want master's work in your
branch. Two ways:

```text
  MERGE  (git merge master, from bug-fix)        REBASE  (git rebase master, from bug-fix)

  master:  C1 ─ C2 ─ C5 ─ C6                     master:  C1 ─ C2 ─ C5 ─ C6
                 \            \                                            \
  bug-fix:        └─ C3 ─ C4 ─ M (merge commit)   bug-fix:                   └─ C3' ─ C4'
                                                                        (replanted, new ids)
```

| | `git merge` | `git rebase` |
|---|---|---|
| Result | two timelines joined by a **merge commit** | **one straight line** |
| Extra commits | yes: `Merge branch 'master' into bug-fix` | none |
| Commit ids | unchanged | **rewritten** (C3 → C3') |
| History | true to what happened | cleaned up |
| Safe on shared commits | ✅ | ❌ |

> **Key idea:** rebase = *"pick up my branch and replant it on the tip of master."*

### Why people avoid it

The instructor's hackathon story: a team ran rebase the wrong way in the last hour and
lost their project. Not because rebase is broken, but because rewriting history with
no idea what you're doing is irreversible in the moment.

---

## 🟡 Intermediate — the workflow

### The lecture's flow

```bash
git checkout master
git commit -am "update main website"      # -am = add tracked files + commit in one go
git checkout bug-fix
git commit -am "update navbar"            # work on the fix
git checkout master
git commit -am "images added"             # master keeps moving
git checkout bug-fix
git merge master                          # old way: creates "Merge branch 'master'" commit
git commit -am "about us fixed"
git checkout master
git commit -am "pricing card added"       # master moves again
```

Now `git log --oneline` on both branches is littered with `Merge branch ...` commits that
carry **no work**. That's what rebase removes.

### The rebase

```bash
git branch              # ALWAYS: confirm you're on bug-fix, not master
git rebase master       # "rebase MY branch onto master"
```

```text
Successfully rebased and updated refs/heads/bug-fix.
```

| Before | After |
|---|---|
| two colored lines in the git graph | one line: bug-fix sits on top of master's latest commit |
| `Merge branch` commits present | gone |
| bug-fix commits have ids X, Y | same work, **new** ids X', Y' |

Commit on bug-fix again and master again and the graph branches off as usual. Rebase
doesn't forbid future branching, it just flattens the past.

### `master` vs `main`

Git still creates `master` by default. GitHub renamed it to `main`. Same thing, just a
name. The lecture uses both interchangeably.

---

## 🔴 Expert — conflicts during rebase

Rebase replays your commits one by one on top of master. If a replayed commit touches the
same lines master changed, it **halts**:

```text
CONFLICT (content): Merge conflict in index.html
error: could not apply a1b2c3d... add card to index file
hint: Resolve all conflicts manually, mark them as resolved with
hint: "git add/rm <conflicted_files>", then run "git rebase --continue".
hint: You can instead skip this commit: run "git rebase --skip".
hint: To abort and get back to the state before "git rebase", run "git rebase --abort".
```

**Read that message.** It is the whole procedure.

| Step | Command | Note |
|---|---|---|
| 1. Resolve | edit the file, or VS Code **Accept Current / Incoming / Both** | same `<<< === >>>` markers as a merge conflict |
| 2. Stage | `git add index.html` (or `git add .`) | **add only, do not commit** |
| 3. Resume | `git rebase --continue` | Git reopens the editor with the original message, save and close |
| Bail out | `git rebase --abort` | back to exactly where you were before the rebase |
| Skip | `git rebase --skip` | drop this one commit (rare) |

| In a merge conflict | In a rebase conflict |
|---|---|
| resolve → `git add` → `git commit` | resolve → `git add` → `git rebase --continue` |
| one conflict for the whole merge | can halt once **per replayed commit** |

**"Current" vs "incoming" is flipped during rebase.** While replaying, HEAD is on
master's side, so *current* = master, *incoming* = your branch's commit. Read the labels,
don't assume.

### The golden rule

> **Never rebase commits you've shared.** Once a commit is pushed and someone else has it,
> rewriting its id creates two diverging histories and a mess for everyone. Rebase local,
> unpushed work only.

---

## Gotchas & best practices

- **`git branch` first, every time.** On master? Don't run rebase. On bug-fix? Go.
- **Direction:** `git rebase master` **from** the side branch. It means "put me on master".
- **Shared commits are off limits.** Pushed to GitHub = treat as frozen.
- **Conflict halts aren't failures.** Resolve, `git add`, `--continue`. Or `--abort`.
- **No commit during a halt.** Staging is enough; `--continue` makes the commit.
- **Team convention wins.** Some companies rebase always for clean history, some never.
  Follow the workflow you're given.

> **Interview angle:** *"Merge or rebase?"* Merge preserves true history and is safe on
> shared branches, at the cost of noisy merge commits. Rebase gives a linear, readable
> history by replaying your commits on top of the target, but rewrites commit ids, so it is
> only for local, unshared work. Never rebase main, and never rebase pushed commits.

---

## Quick recap

| Term | One-line definition |
|---|---|
| **`git rebase master`** | replant the current branch on master's tip; run from the side branch |
| **Rewriting history** | rebased commits get new ids; the old ones are discarded |
| **Linear history** | one timeline, no `Merge branch` commits |
| **`git commit -am`** | stage tracked files and commit in one command |
| **`git rebase --continue`** | resume after resolving a conflict (after `git add`) |
| **`git rebase --abort`** | cancel the rebase, restore the pre-rebase state |
| **Golden rule** | never rebase shared/pushed commits, never rebase on main |
