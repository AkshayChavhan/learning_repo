# 01 — Prompt Serialization

Two side-by-side API clients, OpenAI and Gemini, covering the same 8 concepts so
you can see where the SDKs differ. Plus 12 reference PDFs on prompt formats
(Alpaca, ChatML, `[INST]`).

**The point of the comparison:** OpenAI is a **stateless** API — *you* resend the
whole conversation every call. Gemini is **stateful** — the server keeps history.
That one difference drives most of the API design on both sides.

---

## Files

| File | What it shows |
|---|---|
| `llm_chatgpt.py` | OpenAI: text gen, chat history, system prompts, JSON mode, streaming, token counting, error handling |
| `llm_gemini.py` | Same 8 concepts against Gemini, plus retry handling for 503s |
| `Python_Topic22–33_*.pdf` | Prompt fundamentals → shot prompting → CoT → serialization formats |

---

## Setup

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install openai tiktoken google-genai python-dotenv
```

### Environment

Unlike the other projects here, these two scripts read the **bare environment** —
there is no `load_dotenv()` call. A `.env` file alone will not work; you must
export the values.

```bash
# .env is written by ../../../scripts/setup_env.sh, then:
set -a; source .env; set +a        # bash/zsh — exports everything in the file
python3 llm_chatgpt.py
```

```powershell
$env:OPENAI_API_KEY = "sk-proj-..."      # PowerShell
$env:GEMINI_API_KEY = "AIza..."
```

| Variable | Used by | Get it |
|---|---|---|
| `OPENAI_API_KEY` | `llm_chatgpt.py:35` | [platform.openai.com/api-keys](https://platform.openai.com/api-keys) — paid |
| `GEMINI_API_KEY` | `llm_gemini.py:77` | [aistudio.google.com/apikey](https://aistudio.google.com/apikey) — free tier |

Both scripts raise a clear `ValueError` naming the missing variable, so a
forgotten export fails loudly rather than as a confusing auth error.

---

## Run

```bash
python3 llm_chatgpt.py
python3 llm_gemini.py
```

---

## Gotchas

| Gotcha | Detail |
|---|---|
| **`.env` is not read here** | No `load_dotenv()` — use `set -a; source .env` or export by hand |
| **Two names, one Google key** | This project wants `GEMINI_API_KEY`; project 10 wants `GOOGLE_API_KEY`. Same value |
| **Cost asymmetry** | Gemini has a real free tier (100–1500 req/day); OpenAI needs a funded account |
| **The Avast SSL block** | `llm_gemini.py:40-63` patches `ssl.create_default_context` for Avast's HTTPS scanning. It only activates if `~/.certs/ca-bundle.pem` exists, so it is inert on Linux — delete it if you never used Avast |
| **Chatty SDK logs** | `llm_gemini.py` silences the `google_genai` "automatic function calling" notice; it is not an error |
