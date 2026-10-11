# git add, commit & log — Working Directory → Staging → Repo

A file goes through **three zones** before Git remembers it: the **working directory**
(you edit), the **staging area** (you pick what to save), and the **repo** (saved
checkpoint). `git add` moves a file forward one zone, `git commit` moves it the last one,
and `git log` shows the checkpoints you made.

---

## Topic at a glance

```text
        git status                        git commit
            \                                 /
  run it everywhere ──\      needs -m "msg" ──/
                       \                     /
  tracked / untracked ──\   atomic, imperative
                          ►   ADD → COMMIT → LOG
  name files, avoid `.` ─/        full vs short id ──\
                       /                              \
  stage = pre-save ───/           --oneline ───────────\
            /                                            \
        git add                                      git log
```

---

## 🟢 Beginner — the three zones

```text
  WORKING DIRECTORY   ──git add──►   STAGING AREA   ──git commit──►   REPO (.git)
  (files you edit)                   (pre-save screen)               (saved checkpoint)
       ▲                                                                   │
       └──────────────── git status reports on all three ──────────────────┘
```

| Zone | What it means | Game analogy |
|---|---|---|
| **Working directory** | files exist, Git may not track them | playing the level |
| **Staging area** | files picked to go in the next save | *"Save game? Yes / No"* screen |
| **Repo** | a commit, a permanent checkpoint | saved game |

### The walkthrough

```bash
git status                 # ALWAYS run first in any folder
touch test1.txt test2.txt  # create two files
git status                 # -> Untracked files: test1.txt test2.txt
git add test1.txt          # stage ONLY test1
git status                 # -> Changes to be committed: test1.txt
                           #    Untracked files: test2.txt
git commit -m "add file one"
git status                 # -> only test2.txt still untracked
```

```text
$ git commit -m "add file one"
[master (root-commit) 4c8a...] add file one
 1 file changed, 0 insertions(+), 0 deletions(-)
```

> **Key idea:** `git status` is the magic command. Run it after **every** step to see
> which zone each file is in.

---

## 🟡 Intermediate — add, commit and their gotchas

### `git add`: what it really does

| Command | Effect |
|---|---|
| `git add file1` | stage one file |
| `git add file1 file2` | stage several (space-separated) |
| `git add .` | stage **everything**, sensitive files included |
| `git rm --cached file1` | unstage / stop tracking (rarely used) |

**Prefer naming files.** `git add .` is fine when intentional, but most people type it
by habit and stage files they never meant to (secrets, scratch files, `.venv`).

### `git commit`: the message is not optional

| Command | What happens |
|---|---|
| `git commit -m "add file one"` | ✅ commit with an inline message. **Use this.** |
| `git commit` | opens an editor for the message. Default editor is **Vim** |

**Stuck in Vim?**

| Keys | Meaning |
|---|---|
| `Esc` then `:q` | quit |
| `Esc` then `:q!` | force quit, discard message |

The instructor's `git commit` opened VS Code instead of Vim because of a **config**
setting (next lecture).

### `git status` vocabulary

| Message | Zone | Meaning |
|---|---|---|
| `Untracked files` | working dir | Git sees the file but ignores changes to it |
| `Changes to be committed` | staging | will go into the next commit |
| `nothing to commit, working tree clean` | repo | everything saved, nothing changed since |
| `On branch master` | always | you're always on **some** branch (master, main, feature…) |

---

## 🔴 Expert — logs, ids and how to write messages

### `git log`

```bash
git log            # full details per commit
git log --oneline  # one line per commit: short id + message
```

```text
$ git log
commit 4c8a9f1e2b3d4c5a6b7e8f9a0b1c2d3e4f5a6b7c (HEAD -> master)
Author: Hitesh <hitesh@example.com>
Date:   Thu Oct 9 13:40:00 2026 +0530

    add second file to code base

$ git log --oneline
4c8a9f1 (HEAD -> master) add second file to code base
1a2b3c4 add file one
```

| Field | Where from |
|---|---|
| **commit id** (SHA) | hash of the commit. Full is 40 chars, first **6–8** are unique enough |
| **Author / email** | the **git config** file (next lecture). Missing config = the "please tell me who you are" error |
| **Date** | when you committed |
| **message** | what you typed after `-m` |
| **HEAD -> master** | where you are now (covered later) |

**GitLens** (VS Code plugin) shows the same history as a graph. Nice to have, not required.

### Atomic commits: one commit, one job

| ✅ Do | ❌ Don't |
|---|---|
| one feature / one component / one fix per commit | 10 bug fixes in one commit |
| commit often, small steps | one giant "did stuff" commit at the end |
| 10 bugs → 10 commits | mix a feature with unrelated cleanup |

### Message style: imperative, present tense

The official recommendation: **give an order to the codebase**.

| ✅ Imperative (official) | ❌ Past tense |
|---|---|
| `add file one` | `added file one` |
| `add function to connect to database` | `adding db function` |
| `fix login redirect` | `fixed the login thing` |

Test: the message should complete *"If applied, this commit will ___"*.

---

## Gotchas & best practices

- **`git status` first, always.** Before and after every command.
- **Name the files** you stage. `git add .` only when you mean "everything".
- **`-m` every time.** Avoid the editor until you've set one you like.
- **One job per commit.** Small atomic commits are easy to read, revert and review.
- **Imperative messages.** `add`, `fix`, `remove`, not `added`, `fixed`, `removed`.
- **Repeat the flow** 2–3 times with new files until add → commit → log feels automatic.

> **Interview angle:** *"What's the difference between the working directory, staging area
> and repository?"* Working dir is where you edit. Staging is the set of changes you've
> picked for the next commit (`git add`). The repo holds committed snapshots (`git commit`),
> each with a unique SHA shown by `git log`.

---

## Quick recap

| Term | One-line definition |
|---|---|
| **Working directory** | your files on disk, edited freely |
| **Untracked** | Git sees the file but isn't watching changes |
| **Staging area** | pre-commit zone; what `git add` fills |
| **Commit** | a saved snapshot with id, author, date, message |
| **`git commit -m`** | commit with an inline message, skip the editor |
| **`git log` / `--oneline`** | history, full or one line per commit |
| **Atomic commit** | one commit does one job |
| **Imperative message** | "add X", an order to the codebase |
