# git config, .gitignore & What's Inside .git

Git knows your name, email and editor because you told it once, in a **config file**. It
skips secrets because you listed them once, in **.gitignore**. And every commit it saves is
a **hash + parent pointer + info**, stored as plain files inside the `.git` folder.

---

## Topic at a glance

```text
        git config                          .gitignore
            \                                   /
  --global vs local ──\        .env, node_modules ──/
                       \                           /
  name, email, editor ──\      generators ────────/
                          ►   HOW GIT WORKS UNDER THE HOOD
  hash + parent + info ──/          HEAD, refs, objects ──\
                       /                                   \
  SHA-1, chain ───────/             hooks ──────────────────\
            /                                                 \
     Commit anatomy                                     .git folder
```

---

## 🟢 Beginner — tell Git who you are

```bash
git config --global user.name  "Your Name"          # quotes: names have spaces
git config --global user.email "you@example.com"
git config --global core.editor "code --wait"       # VS Code instead of Vim
```

| Scope | Flag | Applies to | Stored in |
|---|---|---|---|
| **Global** | `--global` | every repo on this machine | `~/.gitconfig` |
| **Local** | *(none)* | this repo only | `.git/config` |

Most people set name and email **globally** once and forget about it.

| Setting | Why |
|---|---|
| `user.name` / `user.email` | stamped on every commit. Missing = *"please tell me who you are"* error |
| `core.editor "code --wait"` | `git commit` without `-m` opens VS Code. `--wait` makes Git **pause** until you close the file |

**`code` not found?** In VS Code press `Cmd+Shift+P` (Windows `Ctrl+Shift+P`), type
*"Shell Command: Install 'code' command in PATH"*. Without it the editor setting fails.

### Where it lives

```bash
cd ~               # home directory
cat .gitconfig
```

```text
[user]
    name = Hitesh
    email = hitesh@example.com
[core]
    editor = code --wait
[commit]
    ...
```

It's a plain INI-style file with `[blocks]`. Forgot the command? Edit the file directly.

---

## 🟡 Intermediate — .gitignore

**The problem:** `.env` holds API keys, DB passwords, AWS keys. Leak them and someone runs
up your OpenAI or AWS bill. Without `.gitignore` you must dodge them on every `git add`,
and `git add .` becomes dangerous.

```bash
touch .gitignore          # exact name: lowercase, leading dot, no exceptions
```

```gitignore
.env              # a file
.vscode/          # a folder (trailing slash)
node_modules/     # the classic: thousands of files
```

| Before `.gitignore` | After |
|---|---|
| `git status` lists `.env`, `.vscode/` as untracked | they **disappear** from status |
| `git add .` would stage secrets | `git add .` is safe |
| must name files one by one | stage everything freely |

**Commit the `.gitignore` itself.** It is part of the project; everyone on the team needs it.

### Don't write it by hand

Google **"gitignore generator"** (gitignore.io, Toptal). Pick your stack (Node, Django,
Python…), copy, paste. VS Code plugins exist too. Copy-pasting this file is normal.

### The editor flow, now that it's configured

```bash
git add .
git commit            # no -m → VS Code opens .git/COMMIT_EDITMSG
```

Type the message on the first line, save, close. Lines starting with `#` are comments and
never enter the commit. Same imperative style: `add third and fourth file`.

### git log has many options, you use two

```bash
git log --oneline     # the one you'll use daily
git log               # full
```

The docs list dozens (`--graph`, `--pretty`, `--stat`, `-p`…). Nobody uses most of them.

---

## 🔴 Expert — commit anatomy and the .git folder

### Every commit = hash + parent + info

```text
  ┌─────────────┐      ┌─────────────┐      ┌─────────────┐
  │ COMMIT 1    │      │ COMMIT 2    │      │ COMMIT 3    │
  │ hash: a1f…  │◄─────│ hash: 7c2…  │◄─────│ hash: 9e4…  │◄── HEAD -> master
  │ parent: null│      │ parent: a1f…│      │ parent: 7c2…│
  │ info        │      │ info        │      │ info        │
  └─────────────┘      └─────────────┘      └─────────────┘
```

| Part | What it is |
|---|---|
| **hash** | unique id from **SHA-1**, computed from content, info **and the parent hash** |
| **parent** | pointer to the previous commit. First commit's parent is **null** |
| **info** | author, email, date, system, message |

Because each hash includes its parent's hash, the commits form a **chain**. That chain is
what lets you walk back to any checkpoint and restore it.

### Inside `.git`

```bash
ls -la            # shows the hidden .git/
cd .git && ls -l
```

| Entry | Type | What it holds |
|---|---|---|
| `COMMIT_EDITMSG` | file | the message file your editor opens on `git commit` |
| `config` | file | **local** config for this repo only |
| `HEAD` | file | which branch you're on: `ref: refs/heads/master` |
| `index` | file | the **staging area**. Don't hand-edit |
| `description` | file | unused ("unnamed repository") |
| `objects/` | dir | the actual commits, files and trees, by hash |
| `refs/` | dir | where branches point (`refs/heads/master` → a hash) |
| `logs/` | dir | history of where HEAD has been. Delete = history view gone |
| `hooks/` | dir | scripts run **before/after** Git events |
| `info/` | dir | rarely touched |

**See hidden files in VS Code:** `Cmd+,` → search *files: exclude* → remove `**/.git`.

### Hooks (preview)

Same idea as hooks in React: run your code at a lifecycle point.

| Hook | Runs | Typical use |
|---|---|---|
| `pre-commit` | before a commit is created | lint, run tests |
| `commit-msg` | after you write the message | enforce a format, require a ticket id |
| `pre-push` | before `git push` | run the full test suite |
| `pre-rebase` | before a rebase | block rebasing shared branches |

The folder ships with `*.sample` files. Rename one to activate it. Out of scope for the
course, but common in companies.

---

## Gotchas & best practices

- **Set name + email globally first.** Every commit is stamped with them.
- **`code --wait`, not `code`.** Without `--wait` Git thinks you wrote an empty message.
- **`.gitignore` before the first `git add .`.** Once a secret is committed it's in history.
- **Never hand-edit `index` or `objects/`.** Read, explore, don't touch.
- **Generate `.gitignore`, don't guess it.** The generators know your stack's junk files.
- **Next:** branches, and what `HEAD -> master` actually means.

> **Interview angle:** *"How does Git link commits together?"* Each commit stores its
> parent's hash and its own SHA-1 is computed partly from that parent. Changing any old
> commit changes every hash after it, which is why history is tamper-evident and why you
> can walk back checkpoint by checkpoint.

---

## Quick recap

| Term | One-line definition |
|---|---|
| **`git config --global`** | machine-wide settings, stored in `~/.gitconfig` |
| **`user.name` / `user.email`** | identity stamped on every commit |
| **`core.editor "code --wait"`** | editor for commit messages when `-m` is omitted |
| **`.gitignore`** | list of files/folders Git must never track (`.env`, `node_modules/`) |
| **Hash (SHA-1)** | unique commit id, derived from content + info + parent hash |
| **Parent pointer** | link to the previous commit; null for the first |
| **`.git/HEAD`** | file naming the branch you're on |
| **`.git/objects/`** | where commits and file contents actually live |
| **Hooks** | scripts that run before/after commit, push, rebase |
