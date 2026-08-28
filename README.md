# learning_repo

Personal, topic-by-topic learning repo — Python (incl. GenAI/LLM work),
JavaScript, and reference PDFs for React, Next.js, Docker, HTML/CSS.

**Setting up on a new machine?** → [ENVIRONMENT.md](ENVIRONMENT.md) has every
API key, where each `.env` goes, and a one-command bootstrap.

---

## Layout

| Folder | Contents |
|---|---|
| [python_tut_2026/](python_tut_2026/) | Python basics → GenAI. The only folder with runnable projects |
| [javascript_tut_2026/](javascript_tut_2026/) | JS notes + [plan.md](javascript_tut_2026/plan.md) (9 notes so far) |
| [react_tut_2026/](react_tut_2026/) | 28 reference PDFs (hooks, router, performance) |
| [next_tut_2026/](next_tut_2026/) | 10 reference PDFs (routing, server actions, middleware) |
| [docker_tut_2026/](docker_tut_2026/) | 5 reference PDFs |
| [html_css_tut_2026/](html_css_tut_2026/) | 5 reference PDFs + cheatsheets |
| [scripts/](scripts/) | `setup_env.sh` — writes every `.env` from one key |

### Inside `python_tut_2026/`

| Folder | Contents |
|---|---|
| `01_python_basics/` | One folder per topic, variables → async → GIL |
| `02_python_basics/` | Scratch / practice |
| `03_notes_python/` | 31 written notes, `tutNN_<topic>.md` |
| `04_pdf_python_2026/` | Reference PDFs |
| `05_python_genai/` | **The runnable projects** — see below |

---

## GenAI projects

Each has its own README with setup, env vars, and run commands.

| # | Project | Needs | Services |
|---|---|---|---|
| 01 | [prompt_serialization](python_tut_2026/05_python_genai/01_prompt_serialization/) | OpenAI + Gemini keys | — |
| 02 | [local_LLM_Deployment](python_tut_2026/05_python_genai/02_local_LLM_Deployment/) | — | Ollama |
| 03 | [run_LLM_via_hugging_face](python_tut_2026/05_python_genai/03_run_LLM_via_hugging_face/) | — | Ollama / HF |
| 04 | [build_Ai_Agent_agentic_workflow](python_tut_2026/05_python_genai/04_build_Ai_Agent_agentic_workflow/) | — | Ollama |
| 05 | [building_chat_with_rag](python_tut_2026/05_python_genai/05_building_chat_with_rag/rag/) | OpenAI key | Qdrant |
| 06 | [scalable_rag_with_async_queue](python_tut_2026/05_python_genai/06_scalable_rag_with_async_queu_distributed_workers/02_rag_queue/) | OpenAI key | Qdrant + Valkey |
| 07 | [sending_media_to_llm](python_tut_2026/05_python_genai/07_sending_media_to_llm/) | OpenAI key | — |
| 08 | [lang_graph](python_tut_2026/05_python_genai/08_lang_graph/) | OpenAI key | — |
| 09 | [langgraph_checkpoints](python_tut_2026/05_python_genai/09_langgraph_checkpoints/) | OpenAI key | MongoDB |
| 10 | [LANGCHAIN_BASIC2EXPERT](python_tut_2026/05_python_genai/10_LANGCHAIN_BASIC2EXPERT/02_handOnWork/) | OpenAI + Google + Anthropic | — |
| 11 | [RAG_BASICS](python_tut_2026/05_python_genai/11_RAG_BASICS/02/) | none yet | — |

---

## Quickstart

```bash
git clone https://github.com/AkshayChavhan/learning_repo.git
cd learning_repo

export OPENAI_API_KEY='sk-proj-...'
./scripts/setup_env.sh                 # writes all 7 .env files

# then, per project:
cd python_tut_2026/05_python_genai/08_lang_graph
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python chat.py
```

Every project uses its **own** venv and `requirements.txt` — there is no
repo-wide environment. Activate the one next to the code you are running.

One exception to the `.env` flow: `01_prompt_serialization` reads the bare
environment rather than calling `load_dotenv()`, so run `set -a; source .env; set +a`
before that project. Details in [ENVIRONMENT.md](ENVIRONMENT.md).

---

## Conventions

- Notes are named `tutNN_<topic>.md`. They live in
  `javascript_tut_2026/notes_javascript/` and `python_tut_2026/03_notes_python/`
  (Python's folder carries the `03_` ordering prefix).
- Runnable code lives in `<lang>_tut_2026/<lang>_basics/` or, for GenAI, in
  its own numbered project folder.
- Master topic list: `javascript_tut_2026/plan.md`. Python has no `plan.md` yet.
- Branches: work happens on a dated working branch (currently `august`), which
  merges to `main` by PR. `javascript` and `python` are older per-language
  branches. Never commit directly to `main`.
- `README.md` files are *setup* docs; `note.md` / `tutNN_*.md` are *learning*
  notes. Different jobs — don't merge them.

See [CLAUDE.md](CLAUDE.md) for the full teaching/notes/commit workflow.

---

## Security

This repo is **public**. Secrets stay in gitignored `.env` files and never in
tracked source. Before pushing:

```bash
git ls-files -z | xargs -0 grep -InE -e 'sk-(proj|ant)-[A-Za-z0-9_-]{20,}' \
  -e 'AIza[A-Za-z0-9_-]{30,}' -e 'AQ\.[A-Za-z0-9_-]{30,}' \
  -e 'gsk_[A-Za-z0-9]{40,}' -e 'hf_[A-Za-z0-9]{30,}'
# must print nothing
```

Every pattern needs its own `-e`. Mixing one bare pattern with `-e` flags makes
grep read the bare one as a **filename**, and the scan silently checks the wrong
thing.

The patterns are deliberately entropy-gated — each requires 20+ key characters,
so the `sk-proj-...` placeholders in these docs do **not** trip them while a real
key does. `-z`/`-0` keeps it correct for the four tracked filenames containing
spaces, which a bare `$(git ls-files)` would silently skip.

Covered: OpenAI/Anthropic `sk-`, Google in **both** shapes (classic `AIza…` and
the newer `AQ.…`), Groq `gsk_`, HuggingFace `hf_`. A scan that only knows `AIza`
waves a real Google key straight through.

If a key ever lands in a commit, revoke it at the provider first — rewriting
history afterwards does not un-leak it.
