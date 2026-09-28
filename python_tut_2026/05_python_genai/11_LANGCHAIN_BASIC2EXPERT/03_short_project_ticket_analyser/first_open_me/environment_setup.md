# Environment Setup — Ticket Analyser

How the Python environment for this project was built, and every command used.
**Environment only** — no application code was created by this setup.

---

## What exists now

```text
03_short_project_ticket_analyser/
├── myenv/          ← the virtual environment (Python 3.11.5, gitignored)
├── .env            ← real keys + model, chmod 600, GITIGNORED
├── .env.example    ← placeholder template, COMMITTED (no real key, ever)
├── prompts/        ← your prompt files
├── src/            ← your code
└── first_open_me/
    └── environment_setup.md   ← this file
```

---

## The commands, in order

```bash
cd python_tut_2026/05_python_genai/10_LANGCHAIN_BASIC2EXPERT/03_short_project_ticket_analyser

# 1. Create the venv — note the ABSOLUTE path to the interpreter (see Gotcha 1)
/opt/homebrew/bin/python3.11 -m venv myenv

# 2. Confirm which interpreter you actually got
./myenv/bin/python -V                                   # Python 3.11.5
./myenv/bin/python -c "import sys; print(sys.prefix)"   # ...03_short.../myenv

# 3. Upgrade pip (shipped 23.2.1 → 26.2.1)
./myenv/bin/python -m pip install --upgrade pip

# 4. Install the packages
./myenv/bin/python -m pip install \
    "langchain>=1.0.0,<2.0.0" \
    "langchain-openai>=1.0.0,<2.0.0" \
    "langchain-groq>=1.1.3,<2.0.0" \
    "langchain-google-genai>=4.2.7,<5.0.0" \
    "langchain-anthropic>=1.7.0,<2.0.0" \
    "pydantic>=2.11,<3.0" \
    "python-dotenv>=1.1,<2.0"

# 5. Bring in the API keys — cp, never cat, so nothing prints to the terminal
cp ../02_handOnWork/.env .env
chmod 600 .env

# 6. Prove git will never see it
git check-ignore -v .env        # must print a matching .gitignore rule

# 7. Add the model name. Appended with >> so the existing key VALUES are
#    never read, rewritten, or printed. The guard adds a trailing newline
#    first — without it, OPENAI_MODEL would glue onto the previous value.
[ -n "$(tail -c 1 .env)" ] && printf '\n' >> .env
printf 'OPENAI_MODEL=gpt-4.1-mini\n' >> .env
```

> Step 4 was actually run as `pip install -r requirements.txt`. That
> `requirements.txt` is no longer in the folder, so the direct command above is
> the equivalent. To regenerate one: `./myenv/bin/pip freeze > requirements.txt`.

---

## What got installed

7 packages requested, **61 installed** once dependencies resolved.

| Package | Version | Why it's here |
|---|---|---|
| `langchain` | 1.3.18 | chains, `RunnableBranch`, LCEL composition |
| `langchain-core` | 1.6.1 | prompt templates, runnables, message types |
| `langchain-openai` | 1.6.0 | `ChatOpenAI` — what the architecture diagram calls for |
| `langchain-groq` | 1.1.3 | free-tier fallback |
| `langchain-google-genai` | 4.4.0 | free-tier fallback |
| `langchain-anthropic` | 1.7.0 | fallback (key not filled in yet) |
| `pydantic` | 2.13.5 | structured-output schemas for triage / analysis / resolution |
| `python-dotenv` | 1.2.3 | loads `.env` |

`tiktoken`, `openai`, `groq`, `anthropic`, `langgraph` and friends arrived as
transitive dependencies — you did not ask for them directly.

---

## What's in `.env`

| Variable | State | Secret? |
|---|---|---|
| `OPENAI_MODEL` | `gpt-4.1-mini` | no — plain model name |
| `OPENAI_API_KEY` | set | **yes** |
| `GOOGLE_API_KEY` | set | **yes** |
| `GROQ_API_KEY` | set | **yes** |
| `ANTHROPIC_API_KEY` | **empty** — fill in if you switch to Claude | **yes** |

File is `-rw-------` (0600) and matched by the repo-root `.gitignore` (line 19).

### `.env.example`

A committed template holding the same variable names with **placeholder**
values. On a fresh clone:

```bash
cp .env.example .env
chmod 600 .env
# then paste your real keys into .env
```

`.env.example` is deliberately **not** gitignored — the root `.gitignore`
pattern `.env` matches only the exact filename, so the template tracks while
the real file stays out. Verify any time with:

```bash
git check-ignore -v .env          # prints a rule  → protected
git check-ignore -v .env.example  # prints nothing → committable
```

> Never paste a real key into `.env.example`. It is the one file here that
> **does** reach GitHub, and this repo is public.

---

## Daily use

Two equally valid ways — pick one:

```bash
# A. Activate, then plain `python`
source myenv/bin/activate
python src/workflow.py
deactivate

# B. Don't activate — call the interpreter directly (fewer surprises)
./myenv/bin/python src/workflow.py
```

Check you're in the right place at any time:

```bash
which python          # must contain /03_short_project_ticket_analyser/myenv/
```

---

## Gotchas

| # | Gotcha | Why it bites |
|---|---|---|
| 1 | **`python3` on your PATH is NOT a base interpreter** | It resolves to the repo-root `.venv/bin/python3`. Running `python3 -m venv myenv` would build a venv *from inside another venv*. Always use the absolute `/opt/homebrew/bin/python3.11` when creating one. |
| 2 | **`/usr/bin/python3` is 3.9.6 — too old** | `langchain`, `langchain-core` and `langchain-openai` all declare `requires-python >=3.10`. The Apple system Python cannot run this project. |
| 3 | **`python-dotenv`, not `dotenv`** | `pip install dotenv` installs a deprecated stub. Both import as `from dotenv import load_dotenv`, so the mistake is invisible until it fails. |
| 4 | **No space after `=` in `.env`** | `KEY= sk-...` — `python-dotenv` strips it, but `set -a; source .env` and `docker --env-file` keep the space and the key silently fails. |
| 5 | **Exported shell vars beat `.env`** | `load_dotenv()` will not overwrite something already in your environment. A stale `export` in your shell wins. |
| 6 | **`uv` is not installed on this machine** | The `02_handOnWork` README mentions it; here it's plain `venv` + `pip`. That's also why this `myenv` **has** pip, unlike 02's. |
| 7 | **`pip freeze` outside the venv** | Captures unrelated system packages. Always freeze via `./myenv/bin/pip`. |

---

## Rebuilding from scratch

```bash
rm -rf myenv
# then re-run steps 1–4 above
```

`.env` survives — it is not inside `myenv/`.
