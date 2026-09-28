# LangChain Tutorials

This repository contains all the source code used throughout the LangChain YouTube series.

## Setup

### 1. Create Virtual Environment

This project's venv is called **`myenv`**, not `.venv`. Keep the name — the
VS Code interpreter path in `.vscode/settings.json` points at it.

```bash
python3 -m venv myenv
```

> Using `uv` instead? Pass `--seed`, or the venv ships **without `pip`**:
> `uv venv --seed myenv`. The existing `myenv` was built without it, which is
> why extra packages there have to go in via `uv pip install`.

### 2. Activate Virtual Environment

**Windows**

```bash
myenv\Scripts\activate
```

**Mac/Linux**

```bash
source myenv/bin/activate
```

Or skip activation entirely and call the interpreter directly —
`./myenv/bin/python src/01_llms/gemini_chat_model.py`.

> **`ModuleNotFoundError: No module named 'langchain_google_genai'`** (or
> `langgraph`, `langchain_groq`, …) means the file ran under system Python
> rather than this venv. The package is fine; the interpreter is wrong. Check
> with `which python` — it must print a path inside `myenv/`.

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Add API Keys

Create a `.env` file next to `llm_client.py`:

```env
OPENAI_API_KEY=your_openai_api_key
GOOGLE_API_KEY=your_gemini_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
```

Or generate it — plus every other `.env` in this repo — from the repo root:

```bash
export OPENAI_API_KEY='sk-proj-...'
export GOOGLE_API_KEY='AIza... or AQ....'
export ANTHROPIC_API_KEY='sk-ant-...'
./scripts/setup_env.sh
```

You only need the key for the provider you actually select in step 5. `llm_client.py`
reads all three (lines 24, 31, 38), but only the selected branch runs.

| Variable | Provider | Get it |
|---|---|---|
| `OPENAI_API_KEY` | `openai` | [platform.openai.com/api-keys](https://platform.openai.com/api-keys) |
| `GOOGLE_API_KEY` | `gemini` | [aistudio.google.com/apikey](https://aistudio.google.com/apikey) |
| `ANTHROPIC_API_KEY` | `anthropic` | [console.anthropic.com](https://console.anthropic.com/settings/keys) |
| `GROQ_API_KEY` | `groq` | [console.groq.com/keys](https://console.groq.com/keys) — free tier, starts `gsk_` |

> **`GOOGLE_API_KEY` here, `GEMINI_API_KEY` in project 01.** Same Google key, two
> different variable names. Set both if you use both projects.

`.env` is gitignored — and this repo is public, so keep it that way. See
[ENVIRONMENT.md](../../../../ENVIRONMENT.md) for the full picture.

### 5. Select Model

Edit `config.json` and choose the provider and model:

```json
{ "provider": "openai", "openai": { "model": "...", "temperature": 0, "max_token": 1000 } }
```

`provider` must be one of `openai`, `gemini`, `anthropic`, `groq` — anything else
raises `Unsupported provider`. The file is tracked in git, so it is safe to edit and
commit; it holds no secrets.

### When Gemini's free daily quota runs out

Switch one line to fall back to Groq (also a free tier, different daily budget):

```json
"provider":"groq"
```

| Provider | Default model | Notes |
|---|---|---|
| `gemini` | `gemini-3.6-flash` | free daily quota; ignores `temperature` |
| `groq` | `openai/gpt-oss-120b` | free tier, 131k context, very fast |
| `openai` | `gpt-4.1-mini` | paid — needs a funded account |
| `anthropic` | `claude-sonnet-4-5` | paid |

Groq is OpenAI-API-compatible, so only the class, key and model id change —
everything downstream (`response.text`, prompts, chains) is identical.

### Reasoning models eat your token budget

`gemini-3.6-flash` and `gpt-oss-120b` both *think* before answering, and
`max_token` caps **reasoning + answer together**. Measured on a 3-token prompt:

| Setting | in | out | *of which thinking* | total |
|---|---|---|---|---|
| gemini, default | 4 | 60 | 57 | **64** |
| groq, default | 74 | 62 | 52 | **136** |
| groq, `reasoning_effort: "low"` | 74 | 24 | 14 | **98** |

Two consequences:

- **Never set `max_token` below ~50.** There is nothing left after thinking, so
  `response.text` comes back as `''` — an empty string, with no error raised.
- `reasoning_effort` is set to `"low"` for Groq in `config.json`, worth roughly
  25% per call. Raise it to `"medium"`/`"high"` for work that needs the thinking.

Gemini has no equivalent escape: `thinking_budget=0` is rejected with
`400 INVALID_ARGUMENT` on `3.6-flash`, so its ~64-token floor is fixed. Even so
Gemini is the cheaper of the two per call, because Groq's `gpt-oss` prepends a
~74-token system prompt of its own before your text.

Your Groq account's model list is not fixed. Check what you can actually call:

```bash
curl -s -H "Authorization: Bearer $GROQ_API_KEY" \
  https://api.groq.com/openai/v1/models | python3 -m json.tool | grep '"id"'
```

Happy Learning 🚀

---

## Gotchas

| Gotcha | Detail |
|---|---|
| **`config.json` is read from the cwd** | `load_config()` defaults to the relative path `config.json`, so run scripts from this folder or the open fails |
| **Every provider needs its own `config.json` section** | The `anthropic` branch used to read `config["gemini"]` (a copy-paste slip) while no `"anthropic"` section existed at all — so selecting it raised `KeyError`. Both are fixed; keep the section name and the branch lookup in step |
| **JSON key is `max_token`, kwarg is `max_tokens`** | The code passes `max_tokens=config[...]["max_token"]`. The singular spelling survives only as the config key — as a kwarg LangChain ignores it and warns *"Did you mean: 'max_tokens'?"* |
| **`response.content` is not a string on Gemini** | It returns content blocks — `[{'type':'text','text':'…','extras':{'signature':'…'}}]`. Use `response.text`, which is a `langchain_core` property and works for every provider |
| **`gemini-2.5-flash` is retired** | New accounts get `404 … no longer available to new users`. Use `gemini-3.6-flash` |
| **`gemini-3.6-flash` ignores `temperature`** | It uses fixed sampling defaults and warns as much. The `temperature` in `config.json` is a no-op on this model |
| **The `src/02_prompts/` scripts crash** | Pre-existing: the prompt literals are Python f-strings (`f"…{profession}…"`), so Python interpolates at import time and raises `NameError`. Drop the `f` prefix — those braces belong to LangChain, not Python |