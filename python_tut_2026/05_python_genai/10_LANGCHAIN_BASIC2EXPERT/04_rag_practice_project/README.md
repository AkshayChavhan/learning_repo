# RAG Practice Project

Blank scaffold, ready for code. Nothing is implemented yet — `app.py` and
`requirements.txt` are deliberately empty.

---

## Structure

```text
04_rag_practice_project/
├── myenv/            ← virtual environment (Python 3.11.5, gitignored)
├── .env              ← real keys, chmod 600, GITIGNORED
├── .env.example      ← placeholder template, COMMITTED
├── .gitignore        ← project-scoped ignores
├── app.py            ← empty, your entry point
├── README.md         ← this file
└── requirements.txt  ← empty, add packages as you need them
```

---

## How it was built

```bash
cd python_tut_2026/05_python_genai/10_LANGCHAIN_BASIC2EXPERT/04_rag_practice_project

# 1. Virtual environment. Note the ABSOLUTE interpreter path - see Gotcha 1.
/opt/homebrew/bin/python3.11 -m venv myenv

# 2. Confirm which interpreter you actually got
./myenv/bin/python -V                                   # Python 3.11.5
./myenv/bin/python -c "import sys; print(sys.prefix)"   # ...04_rag.../myenv

# 3. Upgrade pip (venv ships an older one)
./myenv/bin/python -m pip install --upgrade pip

# 4. Empty files for your code
touch app.py requirements.txt

# 5. Config files
#    .env.example and .gitignore were written by hand - see this repo's
#    03_short_project_ticket_analyser for the same pattern.

# 6. Secrets - cp, never cat, so nothing prints to the terminal
cp ../03_short_project_ticket_analyser/.env .env
printf 'EMBEDDING_MODEL=models/gemini-embedding-001\n' >> .env
chmod 600 .env

# 7. Prove git will never see the secrets
git check-ignore -v .env      # must print a matching rule
git check-ignore -v myenv     # must print a matching rule
```

**No packages were installed** — only `pip` and `setuptools` that a venv ships
with. Add what you need as you go.

---

## What's in `.env`

| Variable | Value | Secret? |
|---|---|---|
| `LLM_PROVIDER` | `groq` | no |
| `OPENAI_MODEL` | `gpt-4.1-mini` | no |
| `GROQ_MODEL` | `openai/gpt-oss-120b` | no |
| `EMBEDDING_MODEL` | `models/gemini-embedding-001` | no |
| `OPENAI_API_KEY` | set — **but the account has no credit** | **yes** |
| `GROQ_API_KEY` | set, free tier | **yes** |
| `GOOGLE_API_KEY` | set, free tier | **yes** |
| `ANTHROPIC_API_KEY` | empty | **yes** |

Copied from `03_short_project_ticket_analyser`. Wipe it and start from
`.env.example` if you would rather set your own.

---

## Getting started

```bash
# Install whatever you add to requirements.txt
./myenv/bin/python -m pip install -r requirements.txt

# Run
./myenv/bin/python app.py
```

Or activate first, so plain `python` works:

```bash
source myenv/bin/activate     # prompt becomes (myenv)
python app.py
deactivate
```

A likely starting set for RAG work in this repo:

```text
langchain           langchain-core          langchain-community
langchain-groq      langchain-google-genai  langchain-text-splitters
faiss-cpu==1.10.0   python-dotenv           pydantic
```

---

## Gotchas

| # | Gotcha | Why it bites |
|---|---|---|
| 1 | **`python3` on this machine is NOT a base interpreter** | It resolves to the repo-root `.venv`. `python3 -m venv myenv` would build a venv *from inside another venv*. Always use the absolute `/opt/homebrew/bin/python3.11`. |
| 2 | **`/usr/bin/python3` is 3.9.6 — too old** | LangChain 1.x requires `>=3.10`. The Apple system Python cannot run it. |
| 3 | **`python app.py` may use the wrong venv** | If another venv is active, you get `ModuleNotFoundError` for packages you know are installed. Check with `which python`. Both sibling projects solve this with a `_bootstrap.py` that re-execs under `myenv/` — worth copying once you have code. |
| 4 | **`faiss-cpu` needs an exact pin** | `>=1.11` ships no arm64 wheel for Python 3.11 and builds from source (needs swig/cmake). Use `faiss-cpu==1.10.0`. |
| 5 | **`text-embedding-004` is 404 on this Google account** | Only `gemini-embedding-001` / `-2` / `-2-preview` are served. Check with:<br>`curl "https://generativelanguage.googleapis.com/v1beta/models?key=$GOOGLE_API_KEY"` |
| 6 | **OpenAI returns 429 `credit_balance_exhausted`** | The key is valid, the balance is not. `LLM_PROVIDER=groq` is why the default works. |
| 7 | **Embedding dimensions differ** | Gemini 3072 vs OpenAI 1536. Vectors from different models are not comparable — switching models means **rebuilding** the index, not reusing it. |
| 8 | **`python-dotenv`, not `dotenv`** | `pip install dotenv` is a deprecated stub. Both import as `from dotenv import load_dotenv`, so the mistake is invisible. |
| 9 | **Never paste a real key into `.env.example`** | It is the one file here that reaches GitHub, and this repo is public. |

---

## Rebuilding from scratch

```bash
rm -rf myenv
/opt/homebrew/bin/python3.11 -m venv myenv
./myenv/bin/python -m pip install --upgrade pip
./myenv/bin/python -m pip install -r requirements.txt
```

`.env` survives — it lives outside `myenv/`.
