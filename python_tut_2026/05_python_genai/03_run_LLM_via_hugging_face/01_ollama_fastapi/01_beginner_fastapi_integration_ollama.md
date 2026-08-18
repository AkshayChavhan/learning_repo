# FastAPI + Ollama — Your Own LLM API

Open WebUI gave you a **chat UI**. FastAPI gives you an **API** — the thin layer where *your* rules
live (validation, prompt templates, auth, logging) so any app can call your local model.
**Mental model:** Ollama is already an HTTP server on `:11434`. You are building a *second* server
in front of it.

```text
                  ┌──────────────────────────┐
                  │    FastAPI + OLLAMA      │
                  │  your API in front of a  │
                  │  local model, no cloud   │
                  └──────────────────────────┘
                              │
    ┌──────────────┬──────────┴──────────┬──────────────────┐
    ▼              ▼                     ▼                  ▼
  DOCKER        FASTAPI               OLLAMA             FAILURES
  ollama on     @app.post             Client(host=)      404 no model
  :11434        Pydantic body         client.chat()      422 bad params
  must be       runs in a             ChatResponse       timeouts
  RUNNING       threadpool            .message.content   slow on CPU
```

Two-line summary:

- Your code is a **translator**: HTTP request in → `client.chat()` → text out as JSON.
- Nearly every beginner bug is one of two things: **the model isn't pulled**, or **the parameter
  isn't where you think it is**.

---

## Part 0 — Setup

Run these in the folder holding `server.py`. Use `python -m pip`, not bare `pip` — on this machine
Python came from the Microsoft Store *Python Install Manager*, which never puts `pip` on PATH.

```powershell
python -m pip install "fastapi[standard]"    # fastapi + uvicorn + fastapi CLI + extras
python -m pip install ollama                 # the Python client for Ollama
python -m pip freeze > requirements.txt      # snapshot your versions
```

`fastapi[standard]` — the `[standard]` part is an **extra**: an optional bundle. It pulls in
`uvicorn` (the server), `fastapi-cli` (the `fastapi dev` command), `httptools`, `watchfiles`
(auto-reload), `jinja2` and `email-validator`. Always quote it in PowerShell — `[ ]` are wildcard
characters there.

**Ollama must be running first.** It lives in a Docker container here, and containers stop when you
reboot:

```powershell
docker start ollama          # it will be "Exited" after a restart
docker exec ollama ollama list
```

```text
NAME           ID              SIZE      MODIFIED
llama3.2:3b    a80c4f17acd5    2.0 GB    14 hours ago
```

**Remember that list.** It decides whether your code works — see Part 3.

Then run the server:

```powershell
python -m fastapi dev server.py
```

Open `http://localhost:8000/docs` — FastAPI generates a clickable test UI for free. Port 8000 does
not clash with Open WebUI on 3000.

---

## Part 1 — The request flow

Two servers, two hops. Seeing this makes the bugs obvious.

```text
  you / curl / browser
        │  POST http://localhost:8000/chat
        ▼
  ┌───────────────────────────┐   hop 1: your rules live here
  │  FastAPI  (port 8000)     │   validation, prompt shaping, auth
  │  server.py                │
  └───────────────────────────┘
        │  client.chat(model=..., messages=[...])
        ▼
  ┌───────────────────────────┐   hop 2: the actual model
  │  Ollama   (port 11434)    │   in a Docker container
  │  llama3.2:3b              │   loads weights, generates tokens
  └───────────────────────────┘
        │  ChatResponse
        ▼
  {"answer": "..."}   ← what your endpoint returns
```

| If it breaks here | You see | Real cause |
|---|---|---|
| Before hop 1 | `422 Unprocessable Entity` | FastAPI didn't find your parameter |
| Between 1 and 2 | `ConnectError` | Ollama container isn't running |
| At hop 2 | `404 model not found` | model was never pulled |
| At hop 2, slowly | `ReadTimeout` | CPU inference is just slow |

---

## Part 2 — Reading `server.py`

```python
from fastapi import FastAPI
from ollama import Client

client = Client(host="http://localhost:11434")   # 1. connect to Ollama
app = FastAPI()                                   # 2. create the API

@app.get("/")
def read_root():
    return {"Hello": "World"}                     # 3. health check

def chat_with_ollama(prompt: str):                # 4. plain helper, not an endpoint
    response = client.chat(
        model="llama3.1:8b",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.message.content

@app.post("/chat")
def chat(prompt: str):                            # 5. the endpoint
    return chat_with_ollama(prompt)
```

| Line | What it really does |
|---|---|
| `Client(host=...)` | Made **once at import**, reused by every request — good, connections are pooled |
| `app = FastAPI()` | The object `fastapi dev` looks for by name |
| `@app.get("/")` | Decorator = "run this function for `GET /`" |
| `messages=[{...}]` | Chat format. `role` is `user`, `assistant` or `system` |
| `response.message.content` | Just the text. `response` is a whole `ChatResponse` object |
| `def` (not `async def`) | Correct choice — see Part 6 |

`client.chat()` returns a Pydantic object, not a dict. Dot access is the modern style:

```python
response.model_dump().keys()
```

```text
['model', 'created_at', 'done', 'done_reason', 'total_duration', 'load_duration',
 'prompt_eval_count', 'prompt_eval_duration', 'eval_count', 'eval_duration',
 'message', 'logprobs']
```

Useful ones: `eval_count` (tokens generated), `total_duration` (nanoseconds) — that's how you
measure tokens/second.

---

## Part 3 — Bug #1: the model was never pulled ★

`server.py` asks for `llama3.1:8b`. Your `ollama list` shows only `llama3.2:3b`. Result:

```text
ResponseError: model 'llama3.1:8b' not found (status code: 404)
```

The comment `# default model for ollama` is **wrong** — Ollama has **no default model**. Every model
must be downloaded explicitly before any code can use it.

Two fixes:

| Fix | Command / change | Cost |
|---|---|---|
| **Use what you have** (recommended) | `model="llama3.2:3b"` | free, instant |
| Pull the bigger one | `docker exec -it ollama ollama pull llama3.1:8b` | ~4.9 GB download |

`llama3.1:8b` means **8 billion parameters** vs `3b`'s 3 billion — smarter, but roughly 2–3× slower
and needs ~3× the RAM. On CPU, stay on `3b` while learning.

> **Habit:** `docker exec ollama ollama list` before you blame your Python.

---

## Part 4 — Bug #2: `prompt: str` is a *query* parameter ★

This is the one that confuses everybody. You wrote a **POST** endpoint, so you expect to send JSON.
You don't. Here is FastAPI's actual rule:

| Type hint in your function | FastAPI reads it from |
|---|---|
| `prompt: str`, `n: int`, `flag: bool` (bare scalars) | the **URL query string** |
| `body: SomeBaseModel` (a Pydantic model) | the **JSON body** |
| name matches a `{placeholder}` in the path | the **path** |
| `prompt: str = Body(...)` | forces it into the body |

So `def chat(prompt: str)` produces this schema — note `"in": "query"` and **no** request body:

```text
/chat POST parameters:  [{"name":"prompt","in":"query","required":true,"schema":{"type":"string"}}]
/chat POST requestBody: NONE
```

Sending JSON therefore fails:

```powershell
curl -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d "{\"prompt\":\"hi\"}"
```

```text
422 {"detail":[{"type":"missing","loc":["query","prompt"],"msg":"Field required","input":null}]}
```

**Read `loc` in any 422** — it tells you exactly where FastAPI looked. `["query","prompt"]` means
"I wanted `prompt` in the URL." The working call puts it in the URL instead:

```powershell
curl -X POST "http://localhost:8000/chat?prompt=hello"
```

Why that's still bad: prompts are long and multiline, URLs have length limits, and URLs get written
to access logs. **Use a Pydantic model** — that's Part 5.

---

## Part 5 — The corrected `server.py`

Every line below was run against your live Ollama.

```python
from fastapi import FastAPI, HTTPException
from ollama import Client, ResponseError
from pydantic import BaseModel

client = Client(host="http://localhost:11434", timeout=300)   # generous timeout
app = FastAPI()

MODEL = "llama3.2:3b"        # one place to change the model


class ChatRequest(BaseModel):     # <- makes it a JSON BODY
    prompt: str


@app.get("/")
def read_root():
    return {"status": "ok"}


@app.post("/chat")
def chat(body: ChatRequest):
    try:
        response = client.chat(
            model=MODEL,
            messages=[{"role": "user", "content": body.prompt}],
        )
    except ResponseError as e:                     # model missing, bad request...
        raise HTTPException(status_code=503, detail=f"Ollama error: {e.error}")
    return {"model": MODEL, "answer": response.message.content}
```

```powershell
curl -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d "{\"prompt\":\"Reply with exactly: pong\"}"
```

```text
{"model":"llama3.2:3b","answer":"pong"}
```

Four changes, four reasons:

| Change | Why |
|---|---|
| `class ChatRequest(BaseModel)` | moves `prompt` into the JSON body + validates it |
| `timeout=300` | `Client(host, **kwargs)` forwards extras to `httpx`; default would fire |
| `except ResponseError` → `HTTPException(503)` | a missing model is a *dependency* failure, not a 500 |
| `{"model":..., "answer":...}` | an object, not a bare string — you can add fields later |

Now a bad request names the right place:

```text
422 {"detail":[{"type":"missing","loc":["body","prompt"],...}]}
```

`loc` changed from `query` to `body`. That's your proof the model took effect.

---

## Part 6 — `def` vs `async def` (the real trap)

`client.chat()` **blocks** — it waits for the model. On CPU that is genuinely slow:

```text
llama3.2:3b, prompt "Say hi in 5 words"  ->  17.6 seconds
```

Plain `def` handles this correctly, and this surprises people:

| You write | FastAPI runs it | 17s blocking call means |
|---|---|---|
| `def chat(...)` | in an **external threadpool** (~40 workers) | ✅ other requests keep working |
| `async def` + blocking `Client` | **on the event loop** | ❌ the whole server freezes for 17s |
| `async def` + `AsyncClient` | on the event loop, but it *awaits* | ✅ best at high concurrency |

So `def` is **not a bug** — it's the right beginner choice. The anti-pattern is `async def` wrapped
around blocking code. The async version, when you need it:

```python
from ollama import AsyncClient

aclient = AsyncClient(host="http://localhost:11434", timeout=300)

@app.post("/chat")
async def chat(body: ChatRequest):
    response = await aclient.chat(model=MODEL,
                                  messages=[{"role": "user", "content": body.prompt}])
    return {"answer": response.message.content}
```

---

## Part 7 — Docker networking

`localhost` works **only because `server.py` runs on your host** while Ollama publishes port 11434.
The moment FastAPI itself goes into a container, `localhost` means *that container*:

```text
  server.py on host        ->  http://localhost:11434            ✅ (your situation)
  server.py in container   ->  http://host.docker.internal:11434 ✅
  both on one docker net   ->  http://ollama:11434               ✅ best
```

Rule: inside a container, `localhost` is always **the container itself**.

---

## Part 8 — Streaming (expert)

`stream=True` turns one long wait into tokens as they arrive — the difference between a frozen page
and a ChatGPT-style typing effect.

```python
from fastapi.responses import StreamingResponse

@app.post("/chat/stream")
def chat_stream(body: ChatRequest):
    def tokens():
        for chunk in client.chat(
            model=MODEL,
            messages=[{"role": "user", "content": body.prompt}],
            stream=True,
        ):
            yield chunk.message.content
    return StreamingResponse(tokens(), media_type="text/plain")
```

Other `client.chat()` options worth knowing: `format="json"` (force JSON output),
`options={"temperature": 0.2}` (creativity), `keep_alive` (how long the model stays in RAM),
`tools=[...]` (function calling), `think=` (reasoning models).

---

## Fishbone — where FastAPI + Ollama goes wrong

```text
                  DOCKER / OLLAMA               FASTAPI WIRING
                        \                             /
   container "Exited" ───\      bare `prompt: str` ──/
   model not pulled ──────\     returns bare string /
   port 11434 unmapped ────\                       /
                            \                     /
                             ►  BROKEN /chat  ◄
                            /                     \
   default timeout too low─/      async def + ─────\
   CPU inference ~17s ────/       blocking client   \
   no try/except ────────/        no response_model  \
                        /                             \
                  TIMEOUTS / ERRORS              CONCURRENCY
```

---

## Gotchas & best practices

| Gotcha | Do this |
|---|---|
| `pip` not recognised | use `python -m pip` — it always hits the right interpreter |
| `ConnectError` to 11434 | `docker start ollama` — containers don't survive reboot |
| `404 model not found` | `docker exec ollama ollama list` before blaming your code |
| `422` on a POST | read `loc` — `query` means you need a Pydantic model |
| Request hangs then dies | pass `timeout=300`; CPU inference is ~17s+ per reply |
| `pip freeze` writes UTF-16 | PowerShell `>` defaults to UTF-16LE. pip still reads it, but it's not portable — use `python -m pip freeze \| Out-File -Encoding ascii requirements.txt` |
| `pip freeze` dumps 71 packages | you're on the global interpreter — use a venv per project |
| `UnicodeEncodeError` on `fastapi dev` | only when output is piped/redirected; set `$env:PYTHONIOENCODING="utf-8"` |
| Model name hardcoded twice | keep one `MODEL = "..."` constant |
| Hidden extra container | you have a stray `goofy_raman` (ollama/ollama) — `docker rm goofy_raman` |

**Command reference**

| Command | Purpose |
|---|---|
| `python -m fastapi dev server.py` | dev server, auto-reload, port 8000 |
| `python -m fastapi run server.py` | production — no reload |
| `python -m uvicorn server:app --reload` | the same thing, one layer lower |
| `http://localhost:8000/docs` | Swagger UI — click to test |
| `http://localhost:8000/openapi.json` | the raw schema — proves query vs body |
| `docker exec ollama ollama list` | which models exist |
| `docker exec -it ollama ollama pull <model>` | download a model |

**Interview angle:** *"Why does a bare `str` become a query parameter in FastAPI?"* — because FastAPI
infers location from type. Scalars are assumed to be query params; anything structured (a Pydantic
model) is assumed to be the body. `Body()`, `Query()` and `Path()` override that inference.
