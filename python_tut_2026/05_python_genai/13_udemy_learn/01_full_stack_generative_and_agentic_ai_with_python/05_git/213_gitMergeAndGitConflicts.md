# Branches, HEAD, Merge & Conflicts

A **branch** is an alternative timeline of the same codebase. Everyone works on their own
timeline, then **merges** back. **HEAD** is the needle that says which timeline you're on.
A **conflict** is just Git refusing to guess when two timelines changed the same lines.

---

## Topic at a glance

```text
        Branches                           Merge
            \                                 /
  alternative timeline ──\   fast-forward ──/
                          \                /
  git branch / checkout ──\   3-way merge ─/
                            ►   BRANCHING & MERGING
  cassette needle ─────────/     <<< === >>> markers ──\
                          /                             \
  .git/HEAD → refs/heads ─/    you decide, Git doesn't ──\
            /                                              \
         HEAD                                         Conflicts
```

---

## 🟢 Beginner — branches are timelines

```text
  master:  C1 ──► C2 ──► C3
                   \
  navbar:           └──► C4        ◄── another coder, own timeline
```

| Command | What it does |
|---|---|
| `git branch` | list branches. `*` marks the one you're on |
| `git branch navbar` | create a branch (you stay where you are) |
| `git checkout navbar` / `git switch navbar` | move to it |
| `git checkout -b footer` / `git switch -c footer` | **create + move** in one go |
| `git branch -d navbar` | delete a branch (history stays, the label goes) |

### What switching actually does

| On branch | Files you see |
|---|---|
| `master` | `index.html`, `hero_section.html` |
| `navbar` | `index.html`, `navbar.html` |

Switch to master and `navbar.html` **vanishes**. Switch back and it's there again. Files
aren't deleted. You're just looking at a different timeline.

> **Key idea:** creating a branch changes **nothing** until you commit on it. A fresh
> branch points to the exact same commit as the branch it came from.

**Default name:** Git creates `master`. GitHub and most teams rename it `main`. Call it
`master`, `main`, `superman`. It's only a name.

---

## 🟡 Intermediate — HEAD, and the two kinds of merge

### HEAD = the cassette needle

```text
  .git/HEAD            →  ref: refs/heads/master
  .git/refs/heads/master  →  31ae...   (latest commit on master)
  .git/refs/heads/navbar  →  9f02...   (latest commit on navbar)
```

| Fact | Detail |
|---|---|
| HEAD points to a **branch**, the branch points to a **commit** | `git log --oneline` shows `(HEAD -> master)` |
| `git checkout navbar` rewrites `.git/HEAD` | now `ref: refs/heads/navbar` |
| Usually HEAD is at the **tip** of the branch | but it can point to an older commit (restore a checkpoint). Later lecture |

### Merging: be on the branch that **receives**

```bash
git checkout master     # I am master, I'm bringing navbar INTO me
git merge navbar
```

| Type | When | What Git does |
|---|---|---|
| **Fast-forward** | receiving branch had **no new commits** | just moves the pointer forward. No merge commit |
| **3-way (not fast-forward)** | **both** branches moved on | creates a **merge commit** with two parents. Asks for a message: `Merge branch 'navbar'` |

```text
  FAST-FORWARD                          NOT FAST-FORWARD

  master: C1 ─ C2                       master: C1 ─ C2 ─ C5 (hero) ─ M (merge)
                 \                                      \              /
  footer:         └─ C6 (footer)        navbar:          └─ C4 (navbar)

  after merge: master → C6              M has two parents: C5 and C4
```

Both merges in the lecture were **clean** because each branch touched **different files**.

### Clean-up after merge

```bash
git branch -d navbar    # branch served its purpose
```

GitLens still shows the navbar commits. You deleted the **label**, not the history.

---

## 🔴 Expert — merge conflicts

### How a conflict happens

| Branch | Change to `index.html` |
|---|---|
| `master` | added line `footer added` |
| `footer` | added line `footer was added successfully` on the **same spot** |

```bash
git checkout master
git merge footer
```

```text
Auto-merging index.html
CONFLICT (content): Merge conflict in index.html
Automatic merge failed; fix conflicts and then commit the result.
```

Git is not an AI. It will not pick which line is right. You do.

### Reading the markers

```text
<<<<<<< HEAD
footer added                        ← what's on YOUR branch (master, where HEAD is)
=======
footer was added successfully       ← what's coming IN (footer)
>>>>>>> footer
```

| Section | From |
|---|---|
| above `=======` | the branch you're on (HEAD) |
| below `=======` | the incoming branch |

### Resolving: 3 steps, no shortcuts

1. **Pick** what to keep: current, incoming, or both. Talk to the other coder if unsure.
2. **Delete the markers** `<<<<<<<`, `=======`, `>>>>>>>` and the lines you rejected.
3. **Save, add, commit** to finish the merge:

```bash
git add index.html
git commit -m "merge footer branch"
```

VS Code adds buttons above the block (**Accept Current / Incoming / Both**) and a
**Resolve in Merge Editor** view. Same three steps, less typing.

### Result

```text
  master: C1 ─ C2 ─ C5 ─ C7 (footer in index) ─ M (merge footer, conflict resolved)
                      \                        /
  footer:              └─ C6 ─ C8 (index edit) ┘
```

---

## Gotchas & best practices

- **Commit before switching branches.** Uncommitted changes follow you around and get messy.
- **Merge from the receiver.** `git merge X` means *"bring X into the branch I'm on"*.
- **`git branch` before `git merge`.** Confirm where you are first.
- **Conflicts are normal.** Only the markers look scary. Keep what you want, delete the rest.
- **Delete merged branches.** Keeps `git branch` readable. History is untouched.
- **Peek at `.git/HEAD`** while learning. It makes HEAD concrete.

> **Interview angle:** *"Fast-forward vs 3-way merge?"* Fast-forward happens when the
> receiving branch has no new commits, so Git just moves the pointer. A 3-way merge happens
> when both diverged, producing a merge commit with two parents. A **conflict** is a 3-way
> merge where both sides changed the same lines, so Git stops and asks you to choose.

---

## Quick recap

| Term | One-line definition |
|---|---|
| **Branch** | an alternative timeline; a pointer to a commit |
| **`git branch X`** | create X; `-d X` deletes it |
| **`git checkout X` / `git switch X`** | move HEAD to branch X |
| **`-b` / `-c`** | create and switch in one command |
| **HEAD** | the needle: which branch (and commit) you're on, stored in `.git/HEAD` |
| **Fast-forward merge** | receiver didn't move; pointer slides forward |
| **3-way merge** | both moved; new merge commit with two parents |
| **Conflict** | same lines changed on both sides; fix markers, add, commit |
