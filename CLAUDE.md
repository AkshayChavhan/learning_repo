# CLAUDE.md — Learning Repo Workflow Rules

This is a personal **learning repository** (Python, JavaScript, …). The user (Akshay) is
learning topic-by-topic. These rules define exactly how Claude must teach, take notes, and commit.
**Follow them on every learning interaction. Do not skip steps.**

---

## 1. The Learning Loop (MOST IMPORTANT — never break this order)

For **every** topic, follow these phases strictly **in order**. Do not jump ahead.

```
TEACH  →  ANSWER QUESTIONS  →  CONFIRM UNDERSTANDING  →  WRITE NOTE  →  CONFIRM AGAIN  →  COMMIT  →  NEXT TOPIC
```

1. **TEACH** — Explain the current topic from **beginner → intermediate → expert** (see §2).
2. **ANSWER QUESTIONS** — The user will ask about anything they don't understand.
   Answer clearly, with small runnable examples. Stay on the **current topic only**.
3. **CONFIRM UNDERSTANDING** — Before writing any note, **explicitly ask the user**:
   *"Have you fully understood this topic?"* Do **NOT** assume.
   - Only proceed when the user clearly says yes / confirms.
   - If unsure or "partly", keep teaching — do not write the note yet.
4. **WRITE NOTE** — Only **after** confirmed understanding, create the topic README/note
   in the language's notes folder (see §3 and §4).
5. **CONFIRM AGAIN** — After writing the note, ask the user to review it and confirm
   *"Does this note cover everything correctly?"*
6. **COMMIT** — Only after the note is confirmed, commit (see §5). Commit only when the
   user asks, or after note confirmation if they've said to commit each topic.
7. **NEXT TOPIC** — Move to the next topic **only after** the user confirms they're done
   with the current one. Then mark the plan checkbox (see §6).

> **Golden rule:** Never write a note or move to the next topic until the user has
> **explicitly confirmed** complete understanding of the current topic. When in doubt, ask.

---

## 2. How to Teach a Topic (beginner → intermediate → expert)

Every topic is taught in three escalating layers. Don't dump everything at once —
build up, and check the user is following before going deeper.

- **🟢 Beginner** — What it is, the simplest mental model, the most common use, one tiny
  runnable example with its output. Plain language, no jargon (or jargon explained inline).
- **🟡 Intermediate** — Real-world usage, common methods/patterns, edge cases the user will
  actually hit, comparisons with related concepts, small gotchas.
- **🔴 Expert** — Under-the-hood behavior, performance, tricky edge cases, interview-style
  "why does this happen" details, best practices and anti-patterns.

Teaching style:
- Prefer **small, runnable examples** with the **expected output shown** (match the style of
  existing notes in `notes_python/`).
- Explain **why**, not just **what**.
- Pause and invite questions between layers. Let the user drive the depth.

---

## 3. Note / README Files (when & where)

- Notes are written **only after the user confirms full understanding** (see §1, step 3).
- **Before writing**, always check: *is this the topic currently being learned, and has the
  user confirmed they understand it?* If not, don't write.
- One note file **per topic**.
- Location per language:
  - JavaScript → `javascript_tut_2026/notes_javascript/`
  - Python → `python_tut_2026/notes_python/`
- **File naming:** `tutNN_<topic_snake_case>.md`
  - `NN` = two-digit tutorial number matching the topic's position in `plan.md`.
  - Examples: `tut01_variables.md`, `tut18_closures.md`, `tut35_polyfills.md`
- Keep numbering consistent with the existing `notes_python/` convention.

### Note content format (match existing notes_python style)
- Start with an `# H1 Title` (the topic).
- Short intro: what it is + the mental model, in 1–3 sentences.
- Sections with `##` / `###` headings going beginner → intermediate → expert.
- **Code blocks** with the right language fence (` ```js ` / ` ```python `).
- Show **output** in a ` ```text ` block right after examples.
- Use bullet lists for key facts, tables for comparisons/method references.
- End with gotchas / best practices, and (for JS) an interview-angle note where relevant.

### Note style rules (IMPORTANT — keep notes short & visual)
- **Keep it SHORT but COMPLETE.** Cover every important point, but no filler. If it can be
  a table or diagram instead of a paragraph, make it a table or diagram. Aim for "scannable
  in a few minutes, re-readable before an interview."
- **Prefer visuals over prose/code.** Most of the time a **table** or **diagram** explains a
  concept better than paragraphs or long code. Reach for them first, fall back to prose only
  when a visual won't fit.
- **Tables** — use for: comparisons (`var` vs `let` vs `const`), method references, when-to-use,
  pros/cons, type/coercion results, time complexity. One table often replaces a whole section.
- **Fishbone (Ishikawa) diagram** — use to break a topic into its main branches and sub-points
  at a glance (e.g. "Closures" → causes/uses/pitfalls/internals). Draw it as ASCII inside a
  ` ```text ` block. Use whenever a topic has several independent dimensions worth seeing together.
  Skeleton to follow:
  ```text
                    Cause A            Cause C
                      \                  /
            sub ───────\        sub ────/
                        \              /
   sub ─────────────────►   TOPIC / EFFECT
                        /              \
            sub ───────/        sub ────\
                      /                  \
                    Cause B            Cause D
  ```
- **Other diagrams when they help:** flow/sequence (event loop, async order), tree (prototype
  chain, DOM), box/timeline (call stack, microtask vs macrotask). ASCII in a ` ```text ` block.
- **Code examples:** small and only when they add something a table/diagram can't. Always show
  output. Don't paste long code dumps.
- **Readability:** short sentences, bold the key term, generous headings, white space. Optimize
  for "easy to understand and easy to re-read", not exhaustive prose.

---

## 4. Plan / Progress Tracking

- Each language has a `plan.md` (e.g. `javascript_tut_2026/plan.md`) — the master topic list.
- Topics use checkboxes: `- [ ]` = pending, `- [x]` = done.
- **Mark a topic `- [x]` only after**: the user confirmed understanding **and** the note file
  was written **and** confirmed.
- When a whole numbered section's sub-items are all done, the section is effectively complete.
- Never silently re-check or uncheck items — only update the checkbox for the topic just finished.

---

## 5. Git Commit Rules

### When to commit
- **Commit ONLY when the user explicitly says "commit".** Do not auto-commit.
  After a note is written & confirmed, prepare everything but **wait** for the user's
  go-ahead before running `git commit`.
- Never commit unfinished, unconfirmed, or note-less work.
- **Branch per language:**
  - JavaScript work → **`javascript`** branch. Create/switch to it before committing JS work.
  - Python work → **`python`** branch.
  - Never commit learning work directly to `main`.

### Commit message format (match this repo's existing history)

**Title (one line):**
```
tutNN: <Language> <topic> — <short, comma-separated list of subtopics>
```
- Use the em dash `—` (not `-`) between topic and subtopics, matching existing commits.
- Keep it concise; lowercase subtopics; comma-separated.
- For multiple tutorials in one commit: `tutNN + tutMM: <Language> <topics…>`

**Real examples from this repo (follow this exact style):**
```
tut17: Python functions — def, return, *args/**kwargs, /, *, scope, lambda, pitfalls
tut16: Python for loop — range, enumerate, zip, break/continue, else, comprehensions
tut18 + tut19: Python decorators, recursion & generators
```

**JavaScript examples (apply the same pattern):**
```
tut01: JavaScript variables — var/let/const, hoisting, scope, naming conventions
tut18: JavaScript async — promises, async/await, event loop, microtasks/macrotasks
tut35: JavaScript polyfills — bind, debounce, Promise.all, deep clone, curry
```

### Commit body (optional)
- Only add a body when it adds real value (what was covered / why). Keep it brief.
- Do **not** add a body for trivial single-topic commits — the title is enough.

### Commit hygiene
- Only stage files relevant to the topic (the note + plan.md checkbox update).
- Do not commit secrets, scratch files, or unrelated changes.
- Run a quick `git status` / `git diff --staged` review before committing.
- Do **not** add Claude as co-author or any "Generated with" footer to these learning commits
  unless the user explicitly asks (keep history clean and personal).

---

## 6. Quick Checklist (run this mentally every topic)

- [ ] Taught the topic beginner → intermediate → expert?
- [ ] Answered all the user's questions on this topic?
- [ ] **Asked** the user if they fully understood — and they confirmed?
- [ ] Verified this is the current topic before writing the note?
- [ ] Wrote `tutNN_<topic>.md` in the correct `notes_<lang>/` folder, in the house style?
- [ ] Note is **short but complete**, and uses **tables/diagrams (incl. fishbone)** instead of
      long prose/code wherever they explain better?
- [ ] User confirmed the note is correct/complete?
- [ ] Updated the `plan.md` checkbox to `- [x]`?
- [ ] On the right branch (`javascript` for JS, `python` for Python)?
- [ ] **Waited for the user to say "commit"** — then committed with the
      `tutNN: <Language> <topic> — <subtopics>` format?
- [ ] Got user's OK before moving to the next topic?

---

## 7. Repo Conventions (reference)

- Languages live in `<lang>_tut_2026/` (e.g. `python_tut_2026/`, `javascript_tut_2026/`).
- Code examples: `<lang>_tut_2026/<lang>_basics/` (Python uses `python_basics/`).
- Notes: `<lang>_tut_2026/notes_<lang>/`.
- Master plan: `<lang>_tut_2026/plan.md`.
- One topic = one note file = (usually) one commit.
