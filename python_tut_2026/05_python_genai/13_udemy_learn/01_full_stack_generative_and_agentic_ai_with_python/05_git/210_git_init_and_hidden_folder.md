# git init — Making a Folder Trackable

Installing Git doesn't make it track anything. A folder only becomes a
**repo** once you explicitly tell Git to track it - that's what `git init` does.

---

## 🟢 Beginner — install, and the one thing to unlearn

Download Git from **git-scm.com** - the install itself is trivial
(next, next, agree). But installing the software and *using* it on a
folder are two separate things:

| | |
|---|---|
| Creating a plain folder | Git knows **nothing** about it |
| A **repo** (repository) | a folder Git has been explicitly told to track |

Making three ordinary folders (`git1`, `git2`, `git3`) does **not** make
Git aware of any of them. Git has to be told, per folder, to start tracking.

---

## 🟡 Intermediate — the three first commands

```bash
git version          # or: git -v / git --version
git status            # what's the current state of this folder?
git init              # start tracking THIS folder
```

**Before `git init`:**

```text
$ git status
fatal: not a git repository
```

**After `git init`:**

```text
$ git init
Using 'master' as the initial branch name...

$ git status
On branch master
No commits yet
nothing to commit
```

That change in `git status`'s output is the proof the folder is now tracked.

| Command | Run how often |
|---|---|
| `git version` | once, just to confirm it's installed - version doesn't matter much, Git rarely ships breaking changes |
| `git status` | **often** - a good habit, check it constantly |
| `git init` | **exactly once per project** - never re-run it on a folder already tracked |

---

## 🔴 Expert — what `git init` actually creates, and the full workflow

### The hidden `.git` folder

`git init` creates a hidden folder named `.git` (dot-prefixed, so it
won't show in a plain `ls` - needs `ls -la`). Inside it: `HEAD`, `hooks`,
`refs` (with `heads` and `tags` subfolders), `config`, `info`,
`description`, `objects`. This is where every checkpoint actually lives.

> **Never manually edit anything inside `.git`.** The risk of corrupting
> the whole repo is entirely on you if you do.

### The workflow, start to finish

```text
  Working Directory ──git add──► Staging Area ──git commit──► Repo (checkpoint)
                                                                      │
                                                            git push (not yet covered)
                                                                      │
                                                                      ▼
                                                        remote / cloud (GitHub, Bitbucket, ...)
```

| Step | Command | What it means |
|---|---|---|
| 1 | *(just files in the folder)* | the working directory - nothing tracked yet |
| 2 | `git add <file>` (or `git add .` for everything) | moves changes into the **staging area** - "I'm ready to commit this" |
| 3 | `git commit` | creates the actual **checkpoint** |
| 4 | `git push` *(deferred - next videos)* | sends the repo + its checkpoints to a cloud provider like GitHub |

**A commit is just a checkpoint** - same save-game idea from the intro:
if something breaks later, you can go back to a commit where it worked.

---

## Gotchas

- **The official Git reference manual is a jungle.** It's a reference,
  not a tutorial - useful once you know what you're looking for, nearly
  unreadable for learning from scratch.
- **`git init` is one-time per project.** Running it again on an
  already-tracked folder isn't how you "add more tracking" - you just
  keep using `git add`/`git commit` as normal.
- **Tracking is per-folder, not global.** `git1` and `git2` can be
  tracked while `git3` is left completely alone - Git never touches a
  folder you haven't initialized.
- **Learn fundamentals first, then use git daily and solve problems as
  they come** - memorizing every command up front isn't the goal.

---

## Quick recap

| Term | One-line definition |
|---|---|
| **Repo** | a folder Git has been explicitly told to track |
| **`git init`** | turns a plain folder into a repo - run once per project |
| **`.git` folder** | the hidden folder holding everything Git tracks - never edit by hand |
| **Staging area** | where `git add` puts changes before they're committed |
| **Commit** | a checkpoint - the thing you can roll back to |
