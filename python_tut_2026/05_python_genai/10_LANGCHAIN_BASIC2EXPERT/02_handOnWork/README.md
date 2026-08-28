# LangChain Tutorials

This repository contains all the source code used throughout the LangChain YouTube series.

## Setup

### 1. Create Virtual Environment

```bash
python -m venv .venv
```

### 2. Activate Virtual Environment

**Windows**

```bash
.venv\Scripts\activate
```

**Mac/Linux**

```bash
source .venv/bin/activate
```

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

> **`GOOGLE_API_KEY` here, `GEMINI_API_KEY` in project 01.** Same Google key, two
> different variable names. Set both if you use both projects.

`.env` is gitignored — and this repo is public, so keep it that way. See
[ENVIRONMENT.md](../../../../ENVIRONMENT.md) for the full picture.

### 5. Select Model

Edit `config.json` and choose the provider and model:

```json
{ "provider": "openai", "openai": { "model": "...", "temperature": 0, "max_token": 1000 } }
```

`provider` must be one of `openai`, `gemini`, `anthropic` — anything else raises
`Unsupported provider`. The file is tracked in git, so it is safe to edit and commit;
it holds no secrets.

Happy Learning 🚀

---

## Gotchas

| Gotcha | Detail |
|---|---|
| **`config.json` is read from the cwd** | `load_config()` defaults to the relative path `config.json`, so run scripts from this folder or the open fails |
| **The `anthropic` branch reads `config["gemini"]`** | `llm_client.py:34-37` — a copy-paste slip. Selecting `anthropic` picks up the Gemini model name and will fail until that block is fixed |
| **JSON key is `max_token`, kwarg is `max_tokens`** | The code passes `max_tokens=config[...]["max_token"]`. The singular spelling survives only as the config key — as a kwarg LangChain ignores it and warns *"Did you mean: 'max_tokens'?"* |
| **`response.content` is not a string on Gemini** | It returns content blocks — `[{'type':'text','text':'…','extras':{'signature':'…'}}]`. Use `response.text`, which is a `langchain_core` property and works for every provider |
| **`gemini-2.5-flash` is retired** | New accounts get `404 … no longer available to new users`. Use `gemini-3.6-flash` |
| **`gemini-3.6-flash` ignores `temperature`** | It uses fixed sampling defaults and warns as much. The `temperature` in `config.json` is a no-op on this model |
| **The `src/02_prompts/` scripts crash** | Pre-existing: the prompt literals are Python f-strings (`f"…{profession}…"`), so Python interpolates at import time and raises `NameError`. Drop the `f` prefix — those braces belong to LangChain, not Python |