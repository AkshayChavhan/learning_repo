# 01 — LLMs

The first component. A **chat model** takes messages in and returns a message
out. Everything else in LangChain sits on top of this.

---

## The files


| File                      | Shows                                                       |
| ------------------------- | ----------------------------------------------------------- |
| `openai_chat_model.py`    | the basic call — build a model, `.invoke()`, read the reply |
| `gemini_chat_model.py`    | the same code against Google                                |
| `anthropic_chat_model.py` | the same code against Anthropic                             |
| `local_models.py`         | a model running on your own machine via Ollama              |
| `model_parameters.py`     | the dials that change how generation behaves                |


---

## One interface, many providers

The first three files are **the same code**. They differ only in their print
labels — three lines each. The provider is not chosen by the filename; it comes
from `config.json` at the project root:

```json
{ "provider": "groq" }
```

```text
      config.json
           │
           ▼
   llm_client.get_llm()
           │
   ┌───────┼───────┬──────────┐
   ▼       ▼       ▼          ▼
 openai  gemini  anthropic  groq
   └───────┴───────┴──────────┘
           │
           ▼
   the same .invoke() call
```

> **So** `openai_chat_model.py` **does not necessarily call OpenAI.** With
> `provider` set to `groq`, every one of these files talks to Groq and prints
> its own label above the answer. Change the config, not the file you run.

That interchangeability is the whole point of the abstraction: swap the
provider and the code downstream never notices.

---



## Calling a model

```python
llm = get_llm()
response = llm.invoke("Explain LangChain in three bullet points.")
print(response.text)
```

`.invoke()` is the standard call. The reply is an `AIMessage` object, not a
string.

### Reading the reply


| Access                               | Gives you                                     |
| ------------------------------------ | --------------------------------------------- |
| `response.text`                      | the reply as a plain **string** — use this    |
| `response.content`                   | may be a list of content blocks, not a string |
| `response.type`                      | the role — `"ai"` for a model reply           |
| `response.usage_metadata`            | token counts, provider-neutral                |
| `response.model_dump_json(indent=2)` | the whole object, nested and readable         |


**Use** `.text`**, not** `.content`**.** `.content` returns content blocks on some
providers (Gemini does this), which breaks any string operation you try on it.
`.text` is a `langchain_core` property that returns a string everywhere.

---



## Model parameters

Applied with `llm.bind(**params)`, so one model object serves different
settings per call.


| Parameter           | Effect                                                          | Example                                    |
| ------------------- | --------------------------------------------------------------- | ------------------------------------------ |
| `temperature`       | randomness. `0` is near-deterministic, higher is more varied    | `llm.bind(temperature=0.1)` → same answer every run |
| `max_tokens`        | cap on the reply length                                         | `llm.bind(max_tokens=50)` → cut off mid-sentence |
| `top_p`             | nucleus sampling — an alternative to temperature, not a partner | `llm.bind(top_p=0.5)` → picks only from the likeliest half |
| `frequency_penalty` | discourages repeating the same words                            | `llm.bind(frequency_penalty=1.2)` → stops looping on one word |
| `presence_penalty`  | encourages introducing new topics                               | `llm.bind(presence_penalty=1.2)` → wanders to new ideas |
| `stop`              | cut generation when a given string appears                      | `llm.bind(stop=["4."])` → a numbered list ends at 3 |

Full call, for shape:

```python
response = llm.bind(temperature=0.1).invoke("Suggest three AI startup ideas.")
```


### Which parameter goes to which provider

Not every provider takes every parameter.

| Provider                     | Parameters it accepts                                                                            |
| ---------------------------- | ------------------------------------------------------------------------------------------------ |
| **ChatGPT** (`ChatOpenAI`)   | `temperature`, `max_tokens`, `top_p`, `frequency_penalty`, `presence_penalty`, `stop` — **all six** |
| **Claude** (`ChatAnthropic`) | `temperature`, `max_tokens`, `top_p`, `top_k`, `stop` — **no** `frequency_penalty` / `presence_penalty` |
| **Gemini** (`ChatGoogleGenerativeAI`) | `temperature`, `max_tokens`, `top_p`, `top_k`, `frequency_penalty`, `presence_penalty`, `stop` — all six, plus `top_k` |
| **Groq** (`ChatGroq`)        | `temperature`, `max_tokens`, `stop`, `reasoning_effort` — others only via `model_kwargs`            |

Two naming details LangChain hides for you:

- Gemini's real field is `max_output_tokens`, **aliased to** `max_tokens`.
- Claude's real field is `stop_sequences`, **aliased to** `stop`.

So you write the same name everywhere and LangChain maps it.

Two things that surprise people:

- `max_tokens` **covers thinking too.** On a reasoning model the budget is
shared between internal reasoning and the visible answer, so a tight cap can
return an empty `.text` with no error raised.
- **An unsupported parameter fails SILENTLY.** `.bind()` passes anything
through, so `llm.bind(frequency_penalty=1.2)` on Claude raises nothing — the
value is simply ignored and you wonder why the output never changed.

---



## Local models

`local_models.py` is the odd one out — it does **not** use `get_llm()` or
`config.json`. It builds `ChatOllama` directly:

```python
llm = ChatOllama(model="llama3.2", temperature=0.7)
```


|         | Hosted API         | Local (Ollama)                    |
| ------- | ------------------ | --------------------------------- |
| API key | required           | none                              |
| Cost    | per token          | free                              |
| Data    | leaves the machine | stays local                       |
| Needs   | network            | `ollama serve` + the model pulled |


The Runnable interface is identical, so a local model drops into any chain
unchanged.

---



## Guide — bring up your own local LLM

Nothing here needs an API key or a network call once the model is pulled.
Six steps, roughly ten minutes plus the download.


| # | Step                  | Command                                | Notes                                                       |
| - | --------------------- | -------------------------------------- | ----------------------------------------------------------- |
| 1 | **Install Ollama**    | `brew install ollama`                  | or the installer from `ollama.com/download`                 |
| 2 | **Start the server**  | `ollama serve`                         | serves `localhost:11434`; the macOS app starts it for you   |
| 3 | **Pull a model**      | `ollama pull llama3.2`                 | ~2 GB, once. Lands in `~/.ollama/models`                    |
| 4 | **Smoke-test it**     | `ollama run llama3.2 "say hi"`         | proves the model works before Python is involved            |
| 5 | **Install the glue**  | `pip install langchain-ollama`         | already in this project's `requirements.txt`                |
| 6 | **Call it**           | `python src/01_llms/local_models.py`   | `ChatOllama(model="llama3.2")`                              |


### What actually happens on `.invoke()`

```text
  local_models.py
        │  ChatOllama(model="llama3.2").invoke(prompt)
        ▼
   langchain_ollama          ← the Runnable interface, same as any provider
        │  HTTP POST /api/chat
        ▼
   ollama serve  ·  localhost:11434
        │  loads weights into RAM (first call is the slow one)
        ▼
   ~/.ollama/models/llama3.2   ← the weights, on your disk
```

The only thing that changed versus a hosted provider is the last two boxes.
No key, no bill, no packet leaving the machine.

### Picking a model for your machine

Rule of thumb: **the model must fit in free RAM**, or the OS swaps and
everything crawls.


| Tag                | Size    | Comfortable on | Good for                        |
| ------------------ | ------- | -------------- | ------------------------------- |
| `llama3.2:1b`      | ~1.3 GB | 8 GB           | fast smoke tests, cheap loops   |
| `llama3.2`  (3b)   | ~2 GB   | 8 GB           | the default in this repo        |
| `llama3.1:8b`      | ~4.7 GB | 16 GB          | noticeably better answers       |
| `qwen2.5:14b`      | ~9 GB   | 32 GB          | near-hosted quality, slower     |
| `nomic-embed-text` | ~275 MB | anything       | **embeddings** for the RAG work |


---

### Making your own model — `ollama create`

You are not stuck with the published models. A **Modelfile** wraps an existing
model with a baked-in system prompt and default parameters, and the result is a
new model name you can call like any other.

```text
FROM llama3.2

PARAMETER temperature 0.2
PARAMETER num_ctx 4096

SYSTEM """
You are a terse Python tutor. Answer in at most three bullet points.
Always show a runnable example. Never apologise.
"""
```

```bash
ollama create py-tutor -f Modelfile   # build it
ollama list                           # py-tutor now appears
ollama run py-tutor "what is a decorator?"
```

Then in Python it is just another model name — no other code changes:

```python
llm = ChatOllama(model="py-tutor")
print(llm.invoke("what is a decorator?").text)
```

```text
• A decorator wraps a function to add behaviour without editing it.
• Applied with @name above the def.
• Example: @functools.cache def fib(n): ...
```


| Modelfile line | Does                                                        |
| -------------- | ----------------------------------------------------------- |
| `FROM`         | the base model to build on — required                       |
| `SYSTEM`       | system prompt baked in, so every caller gets it for free    |
| `PARAMETER`    | default `temperature`, `num_ctx`, `top_k`, `stop`, …        |
| `TEMPLATE`     | the chat template — rarely worth touching                   |


> **This is customisation, not training.** `ollama create` re-packages existing
> weights; it does not learn anything new. Teaching a model new facts means
> fine-tuning (LoRA, outside Ollama) — or, far more often, **RAG**, which is
> what the later modules cover.

### Local parameter names differ

The dials from the table above are OpenAI-shaped. Ollama's own names:


| Hosted        | Ollama          | Note                                    |
| ------------- | --------------- | --------------------------------------- |
| `max_tokens`  | `num_predict`   | `-1` means no cap                       |
| —             | `num_ctx`       | context window; bigger costs RAM        |
| `temperature` | `temperature`   | same                                    |
| `top_p`       | `top_p`         | same, plus `top_k`                      |
| penalties     | `repeat_penalty`| one dial instead of two                 |


```python
llm = ChatOllama(model="llama3.2", temperature=0.2, num_predict=120)
```

### When it goes wrong


| Symptom                                    | Cause and fix                                                       |
| ------------------------------------------ | ------------------------------------------------------------------- |
| `ConnectError` / connection refused        | server not running → `ollama serve`, or open the Ollama app         |
| `model "llama3.2" not found, try pulling`  | you skipped step 3 → `ollama pull llama3.2`                         |
| `ollama serve` says address already in use | it is **already** running (the app started it) — nothing to fix     |
| first call hangs ~30 s, later ones are fast| weights loading into RAM; it stays warm ~5 min, then unloads        |
| whole machine crawls                       | model larger than free RAM → drop to a smaller tag                  |
| answers are worse than the hosted ones     | expected — a 3B model is not GPT-class. Size up or keep prompts tight |
| model lives on another machine             | `ChatOllama(base_url="http://192.168.1.9:11434", ...)`              |


---

## Gotchas


| Gotcha                                                    | Detail                                                                           |
| --------------------------------------------------------- | -------------------------------------------------------------------------------- |
| **The filename does not pick the provider**               | `config.json` does. Check `"provider"` before trusting the label a script prints |
| `.content` **is not always a string**                     | Use `.text`                                                                      |
| `max_tokens` **too low returns** `''`                     | No error — the reply is just empty, especially on reasoning models               |
| **Each provider needs its own** `config.json` **section** | Selecting one whose section is missing raises `KeyError`                         |
| `local_models.py` **ignores config entirely**             | It will not switch providers, and fails unless Ollama is running                 |


