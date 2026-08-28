# Environment Variables

Every secret this repo needs, where each file goes, and how to recreate them all
on a new machine.

> **This repository is PUBLIC.** No real key may ever be written into a tracked
> file. Every `.env` below is gitignored — keep it that way. Values shown here
> are placeholders.

---

## TL;DR — new machine, three commands

```bash
git clone https://github.com/AkshayChavhan/learning_repo.git
cd learning_repo
export OPENAI_API_KEY='sk-proj-...'      # paste once
./scripts/setup_env.sh                    # writes all 7 .env files
```

Add the optional keys before running the script if you want those projects too:

```bash
export GEMINI_API_KEY='AIza... or AQ....'          # 01_prompt_serialization
export GOOGLE_API_KEY='AIza... or AQ....'          # 02_handOnWork
export ANTHROPIC_API_KEY='sk-ant-...'    # 02_handOnWork
export GROQ_API_KEY='gsk_...'            # 02_handOnWork (Gemini quota fallback)
```

Useful flags: `--dry-run` (show, write nothing), `--force` (overwrite existing).

> **One exception.** `01_prompt_serialization` has no `load_dotenv()` — it reads
> the bare environment, so the `.env` the script writes there is *not* enough on
> its own. Before running that project:
>
> ```bash
> set -a; source .env; set +a        # export everything in the file
> ```
>
> Every other project reads its `.env` automatically.

---

## The variables

| Variable | Needed by | Where to get it |
|---|---|---|
| `OPENAI_API_KEY` | 7 projects — the only one most need | [platform.openai.com/api-keys](https://platform.openai.com/api-keys) (paid) |
| `GEMINI_API_KEY` | `01_prompt_serialization` | [aistudio.google.com/apikey](https://aistudio.google.com/apikey) (free tier) |
| `GOOGLE_API_KEY` | `02_handOnWork` (same key as above, different name) | as above |
| `ANTHROPIC_API_KEY` | `02_handOnWork` (only when `provider: anthropic`) | [console.anthropic.com](https://console.anthropic.com/settings/keys) |
| `GROQ_API_KEY` | `02_handOnWork` (only when `provider: groq`) | [console.groq.com/keys](https://console.groq.com/keys) — free tier, key starts `gsk_` |
| `MODEL` | `04_build_Ai_Agent...` — **optional** | defaults to `qwen2.5-coder:7b` |
| `OLLAMA_HOST` | `04_build_Ai_Agent...` — **optional** | defaults to `http://localhost:11434` |

## Where each `.env` lives

All paths are under `python_tut_2026/05_python_genai/`.

| Project | `.env` contents | Loads via |
|---|---|---|
| `01_prompt_serialization/` | `OPENAI_API_KEY`, `GEMINI_API_KEY` | bare env (no `load_dotenv`) |
| `05_building_chat_with_rag/rag/` | `OPENAI_API_KEY` | `load_dotenv()` |
| `06_scalable_rag_.../02_rag_queue/` | `OPENAI_API_KEY` | `load_dotenv()` |
| `07_sending_media_to_llm/` | `OPENAI_API_KEY` | `load_dotenv()` |
| `08_lang_graph/` | `OPENAI_API_KEY` | `load_dotenv()` |
| `09_langgraph_checkpoints/` | `OPENAI_API_KEY` | `load_dotenv()` |
| `10_LANGCHAIN_BASIC2EXPERT/02_handOnWork/` | `OPENAI_API_KEY`, `GOOGLE_API_KEY`, `ANTHROPIC_API_KEY`, `GROQ_API_KEY` | `load_dotenv()` |
| `04_build_Ai_Agent_agentic_workflow/` | *none* | defaults in code |
| `11_RAG_BASICS/02/` | *none yet* | local loaders only — needed once the notebook reaches embeddings |

Projects `02_local_LLM_Deployment` and `03_run_LLM_via_hugging_face` run fully
local (Ollama / HuggingFace) and need no key. `02_hf_transformer` needs
`huggingface-cli login` for gated models — an on-disk token, not an env var.

---

## Non-secret service config

Hardcoded in source; listed here so you know what must be running.

| Service | Address | Started by | Used by |
|---|---|---|---|
| Qdrant | `localhost:6333` | `docker compose -f docker-composer.yml up -d` | `05_building_chat_with_rag` |
| Qdrant + Valkey | `:6333`, `:6379` | `docker compose up -d` | `06_.../02_rag_queue` |
| MongoDB | `mongodb://admin:admin@localhost:27017/lg` | `docker compose up -d` | `09_langgraph_checkpoints` |
| Ollama | `localhost:11434` | `ollama serve` | `03_...`, `04_...` |

Mongo credentials are `admin`/`admin` from
`09_langgraph_checkpoints/docker-compose.yml`. Fine for localhost, never for
anything reachable.

---

## Moving real keys between machines

`setup_env.sh` handles the common case. To move the actual files instead —
no retyping, no transcription errors:

```bash
# on the old machine
find . -name .env -not -path '*/site-packages/*' | tar -czf ~/env-backup.tgz -T -

# copy ~/env-backup.tgz across by USB / scp / password manager, then:
tar -xzf ~/env-backup.tgz -C /path/to/learning_repo
```

Never email, paste into chat, or commit that tarball.

---

## Gotchas

| Gotcha | Why it bites |
|---|---|
| **No space after `=`** | `KEY= sk-...` — `python-dotenv` strips it, but `docker --env-file` and `set -a; source .env` keep the space and the key silently fails |
| **`python-dotenv`, not `dotenv`** | `pip install dotenv` installs a deprecated stub; both import as `from dotenv import load_dotenv`, so the mistake is invisible |
| **Exported vars beat `.env`** | `load_dotenv()` does not overwrite what is already in the environment — a stale `export` in your shell wins |
| **`GOOGLE_API_KEY` vs `GEMINI_API_KEY`** | Same Google key, two different names across two projects. Set both |
| **`pip freeze` outside the venv** | Captures every OS package (`apturl`, `python-apt`) and makes `pip install -r` fail elsewhere. Always freeze *inside* the venv |

---

## If a key leaks

Git history is currently clean — no key has ever been committed. If one does
get out: revoke it at the provider **first**, then rewrite history. Revoking is
what actually protects you; scrubbing history alone does not, since the commit
is already cloned and indexed.

OpenAI scans public GitHub and auto-revokes keys it finds, usually within
minutes — so a leak here breaks your projects rather than your wallet. Do not
rely on that as the safety net.
