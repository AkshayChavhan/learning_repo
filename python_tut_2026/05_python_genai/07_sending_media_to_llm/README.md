# 07 — Sending Media to an LLM

The smallest possible vision call: hand `gpt-4o-mini` an image URL, get a caption
back. One file, ~30 lines.

**Mental model:** a vision request is an ordinary chat request. The only change is
that `content` becomes a *list of parts* instead of a string — some parts `text`,
some `image_url`.

```python
"content": [
    {"type": "text",      "text": "Generate a caption..."},
    {"type": "image_url", "image_url": {"url": "https://..."}},
]
```

---

## Setup

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install openai python-dotenv
```

### Environment

| Variable | Where |
|---|---|
| `OPENAI_API_KEY` | `.env` in this folder |

```bash
# from the repo root
export OPENAI_API_KEY='sk-proj-...'
./scripts/setup_env.sh
```

`main.py:4` calls `load_dotenv()`, so the `.env` is picked up automatically —
no export needed at run time.

---

## Run

```bash
python3 main.py
```

Prints a ~50-word caption of the Google logo.

---

## Gotchas

| Gotcha | Detail |
|---|---|
| **`gpt-4-vision-preview` is dead** | Retired by OpenAI — returns `404 model_not_found`. Modern `gpt-4o` / `gpt-4o-mini` / `gpt-4.1` take images natively, no special model name |
| **URL must be publicly reachable** | OpenAI fetches it server-side. `localhost` and private URLs fail |
| **Local files need base64** | Send `{"url": "data:image/png;base64,<...>"}` instead of an http URL |
| **Images cost tokens** | Billed by resolution. A large image can outweigh the prompt — use `"detail": "low"` for thumbnails |

## Next

Swap the URL for a base64 data URI to caption a local file, or add a second
`image_url` part and ask the model to compare the two.
